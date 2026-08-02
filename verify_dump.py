import json, glob
REQ = ("appointment_required","inspection_required","action_required","report_required")
def dump(d):
    out = []
    for f in sorted(glob.glob(f"{d}/SNAP-*.json")):
        s = json.load(open(f, encoding="utf-8"))
        r = (s.get("response") or {}).get("partialResult") or {}
        pl = s.get("request_payload") or {}
        full = []
        for fld in REQ:
            for x in (r.get(fld) or []):
                if isinstance(x, dict):
                    full.append({"cat": fld.replace("_required",""),
                                 "law": (x.get("law_name") or "").strip(),
                                 "ob": (x.get("obligation_summary") or "")[:120]})
        out.append({"pid": s.get("profile_id"), "sector": s.get("sector"),
                    "site_kind": pl.get("site_kind"), "scale": pl.get("scale"), "workers": pl.get("workers"),
                    "applicable_count": r.get("applicable_count"),
                    "preview_count": len(r.get("rules_table") or []),
                    "full_count": len(full),
                    "summary": r.get("summary") or {},
                    "obligations": full})
    return out
b = dump("before_clean"); a = dump("after_obs003")
json.dump({"before": b, "after": a}, open("verify_obs003.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote verify_obs003.json  before=", len(b), " after=", len(a))
