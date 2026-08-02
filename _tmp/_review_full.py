import json, glob
FIELDS = ["appointment_required","inspection_required","action_required","report_required"]
def part(s): return (s.get("response") or {}).get("partialResult") or {}
def obl_items(p):
    items=[]
    for fld in FIELDS:
        for x in (p.get(fld) or []):
            if isinstance(x,dict):
                law=(x.get("law_name") or x.get("law") or "").strip()
                ob=(x.get("obligation_summary") or x.get("title") or x.get("description") or x.get("name") or "").strip()
                items.append({"cat":fld.replace("_required",""),"law":law,"ob":ob[:140]})
            else:
                items.append({"cat":fld.replace("_required",""),"law":"","ob":str(x)[:140]})
    return items
out=[]
for f in sorted(glob.glob("before_clean/SNAP-*.json")):
    s=json.load(open(f,encoding="utf-8")); p=part(s); pl=s.get("request_payload") or {}
    items=obl_items(p)
    from collections import Counter
    seen=Counter((i["law"],i["ob"]) for i in items)
    dups=[{"law":k[0],"ob":k[1][:70],"n":v} for k,v in seen.items() if v>1]
    out.append({
        "pid":s.get("profile_id"),"sector":s.get("sector"),
        "site_kind":pl.get("site_kind"),"scale":pl.get("scale"),"workers":pl.get("workers"),
        "applicable_count":p.get("applicable_count"),"full_count":len(items),
        "summary":p.get("summary") or {},"risk":p.get("risk_level"),
        "law_badges":sorted(set(p.get("law_badges") or [])),
        "obligations":items,"duplicates":dups,
    })
json.dump({"source":"before_clean_full","count":len(out),"profiles":out},
          open("review_full.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("wrote review_full.json profiles=",len(out),
      " sample full_count vs applicable_count:",
      [(o["pid"],o["full_count"],o["applicable_count"]) for o in out[:3]])
