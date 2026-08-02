import json, glob
REQ = ("appointment_required","inspection_required","action_required","report_required")
out = []
for f in sorted(glob.glob("before_clean/SNAP-*.json")):
    s = json.load(open(f, encoding="utf-8"))
    r = (s.get("response") or {}).get("partialResult") or {}
    pl = s.get("request_payload") or {}
    items = []
    for fld in REQ:
        for x in (r.get(fld) or []):
            if isinstance(x, dict):
                items.append({"cat": fld.replace("_required",""),
                              "law": (x.get("law_name") or "").strip(),
                              "ob": (x.get("obligation_summary") or "")[:140]})
    # 중복: 같은 (cat, law, ob) 다중 등장
    from collections import Counter
    key = Counter((i["cat"], i["law"], i["ob"]) for i in items)
    dups = [{"cat": k[0], "law": k[1], "ob": k[2][:80], "n": v} for k, v in key.items() if v > 1]
    # law+ob (cat 무시) 중복도 별도
    key2 = Counter((i["law"], i["ob"]) for i in items)
    dups_lawob = [{"law": k[0], "ob": k[1][:80], "n": v} for k, v in key2.items() if v > 1]
    out.append({"pid": s.get("profile_id"), "sector": s.get("sector"),
                "site_kind": pl.get("site_kind"), "scale": pl.get("scale"), "workers": pl.get("workers"),
                "applicable_count": r.get("applicable_count"), "full_count": len(items),
                "obligations": items,
                "dups_cat_law_ob": dups, "dups_law_ob": dups_lawob})
json.dump({"source": "before_clean(new)", "count": len(out), "profiles": out},
          open("revalidate_obs002.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote revalidate_obs002.json  profiles=", len(out))
