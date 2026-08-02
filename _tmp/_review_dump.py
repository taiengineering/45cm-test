import json, glob
def part(s):
    return (s.get("response") or {}).get("partialResult") or {}
out = []
for f in sorted(glob.glob("before_clean/SNAP-*.json")):
    s = json.load(open(f, encoding="utf-8"))
    p = part(s)
    pl = s.get("request_payload") or {}
    rules = p.get("rules_table") or p.get("rules") or []
    obs = []
    seen = {}
    for x in rules:
        law = (x.get("law_name") or "").strip()
        summ = (x.get("obligation_summary") or x.get("description") or "").strip()
        typ = (x.get("obligation_type") or x.get("rule_type") or x.get("category") or "").strip()
        key = (law, summ)
        seen[key] = seen.get(key, 0) + 1
        obs.append({"law": law, "ob": summ[:140], "type": typ})
    dups = [{"law": k[0], "ob": k[1][:80], "n": v} for k, v in seen.items() if v > 1]
    out.append({
        "pid": s.get("profile_id"),
        "sector": s.get("sector"),
        "site_kind": pl.get("site_kind"),
        "scale": pl.get("scale"),
        "workers": pl.get("workers"),
        "region": pl.get("region"),
        "applicable_count": p.get("applicable_count"),
        "rule_count": len(rules),
        "risk_level": p.get("risk_level"),
        "law_badges": sorted(set(p.get("law_badges") or [])),
        "summary": p.get("summary") or {},
        "obligations": obs,
        "duplicates": dups,
        "ok": s.get("ok"),
        "http": s.get("http_status"),
    })
json.dump({"source": "before_clean", "count": len(out), "profiles": out},
          open("review_dump.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote review_dump.json  profiles=", len(out))
