import json, glob
# 기존(preview) 집계 재현
def old_meta(r):
    rules = r.get("rules_table") or []
    return {"obligation_total": r.get("applicable_count") or (r.get("summary") or {}).get("total") or 0,
            "rule_count": len(rules),
            "evidence_count": sum(1 for x in rules if (x.get("obligation_summary") or "").strip() and (x.get("law_name") or "").strip())}
# 수정(full) 집계
REQ=("appointment_required","inspection_required","action_required","report_required")
def new_meta(r):
    full=[]
    for fld in REQ:
        for x in (r.get(fld) or []):
            if isinstance(x,dict):
                full.append(((x.get("law_name") or x.get("law") or "").strip(),
                             (x.get("obligation_summary") or x.get("title") or x.get("description") or x.get("name") or "").strip()))
    ev=sum(1 for law,ob in full if law and ob)
    return {"obligation_total": r.get("applicable_count") or (r.get("summary") or {}).get("total") or 0,
            "rule_count": len(full), "full_count": len(full), "evidence_count": ev}
rows=[]
for f in sorted(glob.glob("before_clean/SNAP-*.json")):
    s=json.load(open(f,encoding="utf-8")); r=(s.get("response") or {}).get("partialResult") or {}
    o=old_meta(r); n=new_meta(r)
    rows.append((s["profile_id"], o["rule_count"], n["rule_count"], n["full_count"], n["obligation_total"],
                 n["full_count"]==n["obligation_total"]))
# 판정
mism=[x for x in rows if not x[5]]
print(f"profiles={len(rows)}")
print(f"old rule_count(preview) 분포: {sorted(set(x[1] for x in rows))}")
print(f"new rule_count(full) == obligation_total(applicable_count): {sum(x[5] for x in rows)}/{len(rows)}")
print(f"full != applicable_count 인 profile: {len(mism)} {[x[0] for x in mism][:10]}")
print("샘플(pid, old_rc, new_rc, full, applicable_count):")
for x in rows[:5]: print("  ",x[:5])
json.dump({"rows":[{"pid":x[0],"old_preview":x[1],"new_full":x[2],"applicable_count":x[4],"match":x[5]} for x in rows]},
          open("regression_chg001_obs003.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
