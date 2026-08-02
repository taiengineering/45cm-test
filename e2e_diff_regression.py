#!/usr/bin/env python3
"""E2E Loop STEP 6-7 — Semantic Diff + Regression (test-universe)."""
from __future__ import annotations
import argparse, glob, json, os, sys
from typing import Any, Dict, List, Set, Tuple

CHG001_KEYWORDS = ("전기", "승강기")


def _load_snaps(d: str) -> Dict[str, dict]:
    out: Dict[str, dict] = {}
    files = glob.glob(os.path.join(d, "**", "SNAP-*.json"), recursive=True) \
        or glob.glob(os.path.join(d, "**", "*.json"), recursive=True)
    for f in files:
        try:
            s = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        pid = s.get("profile_id") or s.get("snapshot_id")
        if pid:
            out[str(pid)] = s
    return out


def _partial(snap: dict) -> dict:
    resp = snap.get("response") or snap.get("body") or {}
    if not isinstance(resp, dict):
        return {}
    data = resp.get("data") if isinstance(resp.get("data"), dict) else resp
    return data.get("partialResult") or data.get("partial_result") \
        or resp.get("partialResult") or resp.get("partial_result") or {}


def _obligations(snap: dict) -> List[dict]:
    p = _partial(snap)
    rows = p.get("rules_table") or p.get("rules") or []
    return rows if isinstance(rows, list) else []


def _sig(o: dict) -> Tuple[str, str, str]:
    law = str(o.get("law_name") or "").strip()
    summ = str(o.get("obligation_summary") or o.get("description") or o.get("remarks") or "").strip()
    kind = str(o.get("obligation_type") or o.get("rule_type") or o.get("category") or "").strip()
    return (law, summ, kind)


def _sig_set(snap: dict) -> Set[Tuple[str, str, str]]:
    return {_sig(o) for o in _obligations(snap)}


def _has_chg001(sigs: Set[Tuple[str, str, str]]) -> bool:
    for law, summ, _ in sigs:
        blob = f"{law} {summ}"
        if any(k in blob for k in CHG001_KEYWORDS):
            return True
    return False


def _metrics(snap: dict) -> Dict[str, Any]:
    p = _partial(snap)
    s = p.get("summary") or {}
    return {"applicable_count": p.get("applicable_count"), "risk_level": p.get("risk_level"),
            "law_badges": sorted(set(p.get("law_badges") or [])), "summary": s}


def _payload(snap: dict) -> dict:
    return snap.get("request_payload") or {}


def _is_building_large(snap: dict) -> bool:
    pl = _payload(snap)
    return str(pl.get("site_kind")) == "building" and str(pl.get("scale")) == "large"


def _is_building(snap: dict) -> bool:
    return str(_payload(snap).get("site_kind")) == "building"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--chg", default="CHG-001")
    ap.add_argument("--out-prefix", default="chg001_v1")
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()

    before = _load_snaps(a.before)
    after = _load_snaps(a.after)
    if not before or not after:
        print(f"[ERROR] load fail (before={len(before)} after={len(after)})", file=sys.stderr)
        return 2

    pids = sorted(set(before) | set(after))
    diff_records: List[dict] = []
    changed: List[str] = []
    unexpected: List[dict] = []
    small_building_loss: List[dict] = []
    improved_large: List[str] = []
    missing = [p for p in pids if p not in before or p not in after]

    for pid in pids:
        b, af = before.get(pid), after.get(pid)
        if not b or not af:
            continue
        bs, as_ = _sig_set(b), _sig_set(af)
        added = sorted(as_ - bs)
        removed = sorted(bs - as_)
        chg = bool(added or removed)
        bm, am = _metrics(b), _metrics(af)
        diff_records.append({
            "profile_id": pid, "sector": af.get("sector") or b.get("sector"),
            "payload": _payload(af) or _payload(b), "changed": chg,
            "obligations_added": [{"law": l, "obligation": s, "type": k} for (l, s, k) in added],
            "obligations_removed": [{"law": l, "obligation": s, "type": k} for (l, s, k) in removed],
            "applicable_count_before": bm["applicable_count"],
            "applicable_count_after": am["applicable_count"]})
        if not chg:
            continue
        changed.append(pid)
        b_has, a_has = _has_chg001(bs), _has_chg001(as_)
        if _is_building_large(af) and (not b_has) and a_has:
            improved_large.append(pid)
        if _is_building(af) and (not _is_building_large(af)) and b_has and (not a_has):
            small_building_loss.append({"profile_id": pid, "removed": [
                {"law": l, "obligation": s} for (l, s, k) in removed
                if any(kw in f"{l} {s}" for kw in CHG001_KEYWORDS)]})
        if not _is_building(af):
            unexpected.append({"profile_id": pid, "sector": af.get("sector"),
                               "added": [{"law": l, "obligation": s} for (l, s, k) in added],
                               "removed": [{"law": l, "obligation": s} for (l, s, k) in removed]})

    improved = len(improved_large) > 0
    regressions = len(unexpected) > 0 or len(small_building_loss) > 0
    verdict = "KEEP" if (improved and not regressions) else ("REVISE" if (improved and regressions) else "ROLLBACK")

    diff_out = {"chg": a.chg, "type": "semantic_diff", "before_count": len(before),
                "after_count": len(after), "changed_profiles": changed,
                "missing_profiles": missing, "records": diff_records}
    reg_out = {"chg": a.chg, "type": "regression", "total_profiles": len(pids),
               "changed": len(changed), "unchanged": len(pids) - len(changed) - len(missing),
               "improved_large_building": improved_large, "unexpected_changes": unexpected,
               "small_building_electric_elevator_loss": small_building_loss,
               "missing_profiles": missing, "verdict": verdict,
               "verdict_basis": {"improvement": improved_large,
                                 "unexpected_change_count": len(unexpected),
                                 "small_loss_count": len(small_building_loss)}}

    os.makedirs(a.out_dir, exist_ok=True)
    dp = os.path.join(a.out_dir, f"semantic_diff_{a.out_prefix}.json")
    rp = os.path.join(a.out_dir, f"regression_{a.out_prefix}.json")
    json.dump(diff_out, open(dp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    json.dump(reg_out, open(rp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"=== {a.chg} E2E STEP6-7 ===")
    print(f"profiles: {len(pids)}  changed: {len(changed)}  "
          f"unchanged: {len(pids)-len(changed)-len(missing)}  missing: {len(missing)}")
    print(f"large building 전기·승강기 획득(개선): {improved_large or '없음'}")
    print(f"예상 밖 변경(비건축물 회귀): {len(unexpected)}")
    print(f"소형 전기·승강기 상실(회귀): {len(small_building_loss)}")
    print(f"\n>>> 판정 권고: {verdict}  (운영자 확정)")
    print(f"산출: {dp} , {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
