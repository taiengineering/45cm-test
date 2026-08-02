import json, glob
def ac(d, pid):
    fs = glob.glob(f"{d}/SNAP-{pid.split('-')[1]}-001.json")
    if not fs: return None
    s = json.load(open(fs[0], encoding="utf-8"))
    r = (s.get("response") or {}).get("partialResult") or {}
    req = sum(len(r.get(k) or []) for k in ("appointment_required","inspection_required","action_required","report_required"))
    return (r.get("applicable_count"), req)
allok = True
for pid in ["PF-0019","PF-0020","PF-0021","PF-0028","PF-0038","PF-0001"]:
    a = ac("wk_A", pid); b = ac("wk_B", pid)
    ok = a == b
    allok = allok and ok
    print(pid, "runA(ac,full)=", a, "runB=", b, "OK" if ok else "DIFF")
print("\n워커6 결정성:", "PASS" if allok else "FAIL (워커 낮춰야 함)")
