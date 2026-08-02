import json, glob
f = sorted(glob.glob("before_clean/SNAP-0019-001.json"))[0]
s = json.load(open(f, encoding="utf-8"))
resp = s.get("response") or {}
print("== response keys ==", list(resp.keys()))
p = resp.get("partialResult") or {}
print("== partialResult keys ==", list(p.keys()))
for k, v in p.items():
    if isinstance(v, list):
        print(f"  {k}: list len={len(v)}")
    elif isinstance(v, dict):
        print(f"  {k}: dict keys={list(v.keys())}")
    else:
        print(f"  {k}: {type(v).__name__} = {str(v)[:60]}")
print("== hasFullResult / 기타 최상위 ==", {k: (v if not isinstance(v,(list,dict)) else type(v).__name__) for k,v in resp.items() if k!='partialResult'})
