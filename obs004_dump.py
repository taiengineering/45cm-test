import json, glob
REQ = ("appointment_required","inspection_required","action_required","report_required")
out = []
for f in sorted(glob.glob("after_obs002/SNAP-*.json")):
    s = json.load(open(f, encoding="utf-8"))
    r = (s.get("response") or {}).get("partialResult") or {}
    pl = s.get("request_payload") or {}
    items = []
    for fld in REQ:
        for x in (r.get(fld) or []):
            if isinstance(x, dict):
                items.append({
                    "cat": x.get("category"),
                    "law": (x.get("law_name") or "").strip(),
                    "art": (x.get("law_article") or "").strip(),
                    "ob": (x.get("obligation_summary") or "").strip(),
                })
    out.append({
        "pid": s.get("profile_id"),
        "sector": s.get("sector"),
        "site_kind": pl.get("site_kind"),
        "scale": pl.get("scale"),
        "workers": pl.get("workers"),
        "ac": r.get("applicable_count"),
        "items": items,
    })
json.dump({"source":"after_obs002","count":len(out),"profiles":out},
          open("obs004_review.json","w",encoding="utf-8"), ensure_ascii=False)
print("wrote obs004_review.json profiles=", len(out))
