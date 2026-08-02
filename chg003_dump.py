import json, glob
from collections import Counter
REQ = ("appointment_required","inspection_required","action_required","report_required")
def load(d):
    o = {}
    for f in glob.glob(f"{d}/SNAP-*.json"):
        s = json.load(open(f, encoding="utf-8"))
        r = (s.get("response") or {}).get("partialResult") or {}
        items = []
        for fld in REQ:
            for x in (r.get(fld) or []):
                if isinstance(x, dict):
                    items.append({
                        "cat": x.get("category"),
                        "law": (x.get("law_name") or "").strip(),
                        "art": (x.get("law_article") or "").strip(),
                        "ob": (x.get("obligation_summary") or "").strip(),
                        "cyc": x.get("inspection_cycle_value"),
                        "cond": x.get("condition_code"),
                        "merged": x.get("merged_count"),
                    })
        o[s["profile_id"]] = {"ac": r.get("applicable_count"), "items": items}
    return o
b = load("before_clean"); a = load("after_obs002")
out = {"before": b, "after": a}
json.dump(out, open("chg003_compare.json","w",encoding="utf-8"), ensure_ascii=False)
# 요약
print("profiles before/after:", len(b), len(a))
tot_b = sum(v["ac"] for v in b.values()); tot_a = sum(v["ac"] for v in a.values())
print("총 applicable_count  before:", tot_b, " after:", tot_a, " 감소:", tot_b-tot_a)
