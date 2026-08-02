import json, glob
def load(d):
    o = {}
    for f in glob.glob(f"{d}/SNAP-*.json"):
        s = json.load(open(f, encoding="utf-8"))
        r = (s.get("response") or {}).get("partialResult") or {}
        o[s["profile_id"]] = {"ac": r.get("applicable_count"), "ok": s.get("ok")}
    return o
a = load("after_obs003"); b = load("before_clean_v2_run2")
pids = sorted(set(a) | set(b))
changed = [p for p in pids if p in a and p in b and a[p]["ac"] != b[p]["ac"]]
missing = [p for p in pids if p not in a or p not in b]
aok = sum(1 for v in a.values() if v["ok"]); bok = sum(1 for v in b.values() if v["ok"])
print(f"run1(after_obs003): {len(a)} profiles ok={aok}")
print(f"run2: {len(b)} profiles ok={bok}")
print(f"changed(ac): {len(changed)} / {len(pids)}  missing: {len(missing)}")
if changed: print("  changed:", changed[:15])
gate = (len(a)==112 and len(b)==112 and aok==112 and bok==112 and len(changed)==0 and len(missing)==0)
print(">>> BASELINE GATE:", "PASS" if gate else "FAIL")
