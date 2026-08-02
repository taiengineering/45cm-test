#!/usr/bin/env python3
"""WO-E2E-FREEZE-001 STEP1 — 실패 2건 재실행 (누락분만).

Baseline에서 HTTP 502로 실패한 PF-0107·PF-0111만 동일 조건 재실행.
성공 시 snapshots_all/의 해당 파일을 성공본으로 교체(누락분 채움).
기존 성공 110건은 건드리지 않는다.

실행(사용자 PC / On-your-computer):
    cd ~/45cm-test && python3 refill_failed.py
"""
import json, time, os
from datetime import datetime, timezone
import urllib.request, urllib.error

API_BASE = os.getenv("TAI_API_BASE", "https://api.taieng.co.kr")
ENDPOINT = "/anonymous-diagnosis"
FAILED = ["PF-0107", "PF-0111"]   # Baseline HTTP 502 대상
SITE_KIND = {"MANUFACTURING":"manufacturing","BUILDING":"building",
             "CONSTRUCTION":"construction","SPECIAL_FACILITY":"other"}

def req_of(p):
    c = p["layers"]["company"]
    return {"site_kind":SITE_KIND[p["sector"]],"scale":c["scale"],
            "workers":int(c["worker_count"]),"region":c["region"]}

def call(payload, timeout=40):
    data=json.dumps(payload).encode()
    r=urllib.request.Request(API_BASE+ENDPOINT,data=data,method="POST",
                             headers={"Content-Type":"application/json"})
    t0=time.perf_counter()
    try:
        with urllib.request.urlopen(r,timeout=timeout) as resp:
            return {"ok":True,"http":resp.status,"body":json.loads(resp.read().decode()),
                    "ms":round((time.perf_counter()-t0)*1000)}
    except urllib.error.HTTPError as e:
        return {"ok":False,"http":e.code,"body":None,"ms":round((time.perf_counter()-t0)*1000),"error":f"HTTP {e.code}"}
    except Exception as e:
        return {"ok":False,"http":None,"body":None,"ms":round((time.perf_counter()-t0)*1000),"error":f"{type(e).__name__}: {e}"}

def meta(body):
    if not isinstance(body,dict): return {}
    r=body.get("partialResult") or {}; rules=r.get("rules_table") or []
    laws=set(r.get("law_badges") or [])
    ev=sum(1 for x in rules if (x.get("obligation_summary") or "").strip() and (x.get("law_name") or "").strip())
    s=r.get("summary") or {}
    return {"obligation_total":r.get("applicable_count") or s.get("total") or 0,
            "law_count":len(laws),"rule_count":len(rules),"evidence_count":ev,
            "risk_level":r.get("risk_level"),"engine_version":r.get("engine_version"),"summary":s}

d=json.load(open("profile_universe_v1.json"))
pmap={p["profile_id"]:p for p in d["profiles"]}
os.makedirs("snapshots_all",exist_ok=True)
ts=datetime.now(timezone.utc).isoformat()
out=[]
for pid in FAILED:
    p=pmap[pid]; payload=req_of(p); res=call(payload)
    num=pid.split("-")[1]; sid=f"SNAP-{num}-001"; m=meta(res["body"]) if res["ok"] else {}
    pub=res["body"].get("publicToken") if (res["ok"] and isinstance(res["body"],dict)) else None
    snap={"snapshot_id":sid,"profile_id":pid,"profile_version":"v1","sector":p["sector"],
          "boundary":p.get("boundary",False),"boundary_note":p.get("boundary_note",""),
          "engine_endpoint":API_BASE+ENDPOINT,"engine_version":m.get("engine_version"),
          "public_token":pub,"run_at":ts,"request_payload":payload,"http_status":res["http"],
          "execution_duration_ms":res["ms"],"ok":res["ok"],"error":res.get("error"),
          "response":res["body"],"note":"WO-E2E-FREEZE-001 refill (failed retry). No judgment."}
    if res["ok"] and res["http"]==200:
        json.dump(snap,open(f"snapshots_all/{sid}.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
        print(f"{pid} -> OK http=200 obl={m.get('obligation_total')} risk={m.get('risk_level')} (파일 교체)")
    else:
        print(f"{pid} -> 여전히 실패 http={res['http']} err={res.get('error')} (기존 파일 유지)")
    out.append({"profile_id":pid,"ok":res["ok"],"http":res["http"],"obligation_total":m.get("obligation_total")})
    time.sleep(0.5)
json.dump({"wo":"WO-E2E-FREEZE-001","step":"refill","run_at":ts,"results":out},
          open("refill_result.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("\n결과:", json.dumps(out,ensure_ascii=False))
