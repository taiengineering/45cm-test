#!/usr/bin/env python3
"""WO-E2E — Parallel Full Runner (112 Profile).

원본 e2e_runner_all.py와 동일한 스냅샷 스키마를 유지하되:
  - ThreadPool 동시성 (RUN_WORKERS, 기본 3 — 엔진 경합 방지용 보수값)
  - 요청 타임아웃 상향 (RUN_TIMEOUT_S, 기본 90)
  - 실패 자동 재시도 (RUN_RETRIES, 기본 2 — 타임아웃/429/5xx만 재시도, 지수 백오프)
  - 개별 스냅샷 snapshots_all/SNAP-XXXX-001.json + 집계 파일 생성

실행 (On-your-computer, Railway env 주입):
    RUN_WORKERS=3 railway run python3 e2e_runner_parallel.py
    # 특정 profile만:  ... python3 e2e_runner_parallel.py PF-0019 PF-0021 PF-0023
    # 실패건만 재실행: ... python3 e2e_runner_parallel.py --failed-only

튜닝: 타임아웃 대량 발생 시 RUN_WORKERS를 2~3으로 낮추세요.
      여유 있으면 5~8까지 올려 처리량↑ (엔진이 429/5xx면 자동 재시도).

산출:
    <OUT_SET>                          집계(기본 e2e_snapshot_set_v1.json)
    snapshots_all/SNAP-XXXX-001.json   각 스냅샷 전문
"""
import json, os, sys, time, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import urllib.request, urllib.error

API_BASE   = os.getenv("TAI_API_BASE", "https://api.taieng.co.kr")
ENDPOINT   = "/anonymous-diagnosis"
WORKERS    = int(os.getenv("RUN_WORKERS", "3"))
TIMEOUT_S  = float(os.getenv("RUN_TIMEOUT_S", "90"))
RETRIES    = int(os.getenv("RUN_RETRIES", "2"))
PAUSE_S    = float(os.getenv("RUN_PAUSE_S", "0"))     # 워커 내 요청 간 간격(기본 0)
OUT_SET    = os.getenv("OUT_SET", "e2e_snapshot_set_v1.json")
OUT_DIR    = os.getenv("OUT_DIR", "snapshots_all")

SITE_KIND = {"MANUFACTURING": "manufacturing", "BUILDING": "building",
             "CONSTRUCTION": "construction", "SPECIAL_FACILITY": "other"}

_print_lock = threading.Lock()
_done = 0


def profile_to_request(p):
    c = p["layers"]["company"]
    return {"site_kind": SITE_KIND[p["sector"]], "scale": c["scale"],
            "workers": int(c["worker_count"]), "region": c["region"]}


def _post(payload, timeout):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API_BASE + ENDPOINT, data=data, method="POST",
                                 headers={"Content-Type": "application/json"})
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return {"ok": True, "http": resp.status, "body": body,
                    "ms": round((time.perf_counter() - t0) * 1000), "retryable": False}
    except urllib.error.HTTPError as e:
        return {"ok": False, "http": e.code, "body": None,
                "ms": round((time.perf_counter() - t0) * 1000),
                "error": f"HTTP {e.code}", "retryable": e.code == 429 or 500 <= e.code < 600}
    except Exception as e:
        return {"ok": False, "http": None, "body": None,
                "ms": round((time.perf_counter() - t0) * 1000),
                "error": f"{type(e).__name__}: {e}", "retryable": True}   # timeout/conn = 재시도


def call_engine(payload):
    """재시도 포함 호출. 재시도 대상: 타임아웃/연결오류/429/5xx."""
    last = None
    for attempt in range(RETRIES + 1):
        res = _post(payload, TIMEOUT_S)
        if res["ok"] or not res.get("retryable"):
            res["attempts"] = attempt + 1
            return res
        last = res
        time.sleep(min(2 ** attempt, 8))   # 1,2,4,8...s 백오프
    last["attempts"] = RETRIES + 1
    return last


def extract_meta(body):
    if not isinstance(body, dict):
        return {}
    r = body.get("partialResult") or {}
    REQ = ("appointment_required","inspection_required","action_required","report_required")
    full=[]
    for fld in REQ:
        for x in (r.get(fld) or []):
            if isinstance(x, dict):
                full.append({"cat":fld.replace("_required",""),
                             "law_name":(x.get("law_name") or x.get("law") or "").strip(),
                             "obligation_summary":(x.get("obligation_summary") or x.get("title") or x.get("description") or x.get("name") or "").strip()})
    laws=set(r.get("law_badges") or [])
    evidence=sum(1 for x in full if x["obligation_summary"] and x["law_name"])
    return {
        "obligation_total": r.get("applicable_count") or (r.get("summary") or {}).get("total") or 0,
        "law_count": len(laws), "rule_count": len(full), "full_count": len(full),
        "evidence_count": evidence, "preview_count": len(r.get("rules_table") or []),
        "risk_level": r.get("risk_level"), "engine_version": r.get("engine_version"),
        "summary": r.get("summary") or {},
    }


def run_one(p, run_ts, total):
    global _done
    pid = p["profile_id"]
    payload = profile_to_request(p)
    res = call_engine(payload)
    num = pid.split("-")[1]
    snap_id = f"SNAP-{num}-001"
    meta = extract_meta(res["body"]) if res["ok"] else {}
    pub = res["body"].get("publicToken") if (res["ok"] and isinstance(res["body"], dict)) else None
    snap = {
        "snapshot_id": snap_id, "profile_id": pid, "profile_version": "v1",
        "sector": p["sector"], "boundary": p.get("boundary", False),
        "boundary_note": p.get("boundary_note", ""),
        "engine_endpoint": API_BASE + ENDPOINT, "engine_version": meta.get("engine_version"),
        "public_token": pub, "run_at": run_ts, "request_payload": payload,
        "http_status": res["http"], "execution_duration_ms": res["ms"],
        "attempts": res.get("attempts", 1), "ok": res["ok"], "error": res.get("error"),
        "response": res["body"],
        "note": "parallel runner fact collection. No judgment. No Golden.",
    }
    with open(f"{OUT_DIR}/{snap_id}.json", "w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=2)
    rec = {"snapshot_id": snap_id, "profile_id": pid, "sector": p["sector"],
           "boundary": p.get("boundary", False), "http_status": res["http"], "ok": res["ok"],
           "error": res.get("error"), "attempts": res.get("attempts", 1),
           "execution_duration_ms": res["ms"], "obligation_total": meta.get("obligation_total"),
           "law_count": meta.get("law_count"), "rule_count": meta.get("rule_count"),
           "evidence_count": meta.get("evidence_count"), "risk_level": meta.get("risk_level"),
           "engine_version": meta.get("engine_version"), "public_token": pub,
           "request_payload": payload}
    with _print_lock:
        _done += 1
        tag = "" if res["ok"] else f"  FAIL:{res.get('error')}"
        print(f"[{_done}/{total}] {pid} {p['sector']:16} http={res['http']} "
              f"obl={meta.get('obligation_total')} risk={meta.get('risk_level')} "
              f"{res['ms']}ms x{res.get('attempts',1)}{tag}", flush=True)
    if PAUSE_S:
        time.sleep(PAUSE_S)
    return rec


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    failed_only = "--failed-only" in sys.argv
    d = json.load(open("profile_universe_v1.json"))
    profiles = d["profiles"]
    pmap = {p["profile_id"]: p for p in profiles}

    if failed_only and os.path.exists(OUT_SET):
        prev = json.load(open(OUT_SET))
        targets = [f["profile_id"] for f in prev.get("failures", [])]
        print(f"[--failed-only] 이전 실패 {len(targets)}건만 재실행")
    else:
        targets = args or [p["profile_id"] for p in profiles]

    tp = [pmap[t] for t in targets if t in pmap]
    missing = [t for t in targets if t not in pmap]
    os.makedirs(OUT_DIR, exist_ok=True)
    run_ts = datetime.now(timezone.utc).isoformat()
    total = len(tp)
    print(f"=== PARALLEL RUN === targets={total} workers={WORKERS} "
          f"timeout={TIMEOUT_S}s retries={RETRIES}", flush=True)

    records = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(run_one, p, run_ts, total): p for p in tp}
        for fu in as_completed(futs):
            try:
                records.append(fu.result())
            except Exception as e:
                p = futs[fu]
                records.append({"profile_id": p["profile_id"], "sector": p["sector"],
                                "ok": False, "error": f"worker crash: {e}"})

    records.sort(key=lambda r: r["profile_id"])
    failures = [{"profile_id": r["profile_id"], "http": r.get("http_status"),
                 "error": r.get("error")} for r in records if not r["ok"]]
    for m in missing:
        failures.append({"profile_id": m, "error": "not found in profile set"})
    out = {
        "wo": "WO-E2E-CHG001-LOOP-001", "version": 1, "run_at": run_ts,
        "engine_expected": "v3.0-compiler-core-anonymous",
        "workers": WORKERS, "timeout_s": TIMEOUT_S, "retries": RETRIES,
        "total_targets": total, "executed": len(records),
        "success": sum(1 for r in records if r["ok"]), "failures": failures,
        "records": records,
    }
    json.dump(out, open(OUT_SET, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n=== DONE === success={out['success']}/{total} failures={len(failures)}")
    print(f"output: {OUT_SET} + {OUT_DIR}/*.json")
    if failures:
        print("실패 목록:", ", ".join(f["profile_id"] for f in failures[:20]),
              "..." if len(failures) > 20 else "")
        print("→ 실패건만 재실행:  RUN_WORKERS=2 railway run python3 e2e_runner_parallel.py --failed-only")


if __name__ == "__main__":
    main()
