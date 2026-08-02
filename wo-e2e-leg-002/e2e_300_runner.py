#!/usr/bin/env python3
"""WO-E2E-LEG-002 — 300 Profile /rtm/evaluate Runner (A/B/C).

운영자 맥 터미널 실행 (클라우드 세션은 Railway 도달 불가):
    cd ~/45cm-test/wo-e2e-leg-002 && python3 e2e_300_runner.py A
    python3 e2e_300_runner.py B
    python3 e2e_300_runner.py C     # 병렬(승인 조건)

입력: e2e_300_profile_universe.csv  (컬럼 input_payload = {"facility":{...}} JSON)
출력: e2e_300_run_<X>.json  (profile별 provenance/raw_response/trace/timing 보존)
      e2e_300_execution_log.csv

엔진/Rule/DB/프로필 무수정. 판정 없음(사실 수집만). Expected 비교는 STEP5에서.
"""
import json, csv, time, sys, os
from datetime import datetime, timezone
import urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

API = os.getenv("LEG_RTM_URL", "https://leg-runtime-production.up.railway.app/rtm/evaluate")
UNIVERSE = os.getenv("UNIVERSE_CSV", "e2e_300_profile_universe.csv")
EXPECT = {"release_version":"SEMREPO-RC1-2026.07.20",
          "freeze_signature":"15cd17e871b6885d34214c84a58adf47",
          "repository_size":337}

def call(payload, timeout=40):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API, data=data, method="POST",
                                 headers={"Content-Type":"application/json"})
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return {"ok":True,"http":resp.status,"body":body,"ms":round((time.perf_counter()-t0)*1000)}
    except urllib.error.HTTPError as e:
        return {"ok":False,"http":e.code,"body":e.read().decode("utf-8","replace")[:1000],
                "ms":round((time.perf_counter()-t0)*1000),"error":f"HTTP {e.code}"}
    except Exception as e:
        return {"ok":False,"http":None,"body":None,
                "ms":round((time.perf_counter()-t0)*1000),"error":f"{type(e).__name__}: {e}"}

def prov(body):
    if not isinstance(body, dict): return {}
    p = body.get("provenance") or body.get("partialResult",{}).get("provenance") or {}
    return {"release_version":p.get("release_version"),"freeze_signature":p.get("freeze_signature"),
            "repository_size":p.get("repository_size")}

def one(row, run_ts):
    payload = json.loads(row["input_payload"])
    res = call(payload)
    body = res["body"] if res["ok"] else None
    pv = prov(body)
    rec = {"profile_id":row["profile_id"],"anchor_or_new":row["anchor_or_new"],
           "request_payload":row["input_payload"],"input_checksum":row["input_checksum"],
           "response_status":("OK" if res["ok"] else "FAIL"),"http_status":res["http"],
           "trace_id":(body.get("trace_id") if isinstance(body,dict) else None),
           "provenance":pv,"duration_ms":res["ms"],"error":res.get("error"),
           "raw_response":body,"started_at":run_ts,
           "completed_at":datetime.now(timezone.utc).isoformat()}
    return rec

def main():
    run = (sys.argv[1] if len(sys.argv)>1 else "A").upper()
    rows = list(csv.DictReader(open(UNIVERSE, encoding="utf-8")))
    assert len(rows)==300, f"universe must be 300, got {len(rows)}"
    run_ts = datetime.now(timezone.utc).isoformat()
    parallel = (run=="C")
    if parallel:
        with ThreadPoolExecutor(max_workers=int(os.getenv("WORKERS","8"))) as ex:
            recs = list(ex.map(lambda r: one(r, run_ts), rows))
    else:
        recs = []
        for i,r in enumerate(rows,1):
            recs.append(one(r, run_ts))
            print(f"[{i}/300] {r['profile_id']} {recs[-1]['response_status']} {recs[-1]['http_status']} {recs[-1]['duration_ms']}ms", flush=True)
            time.sleep(float(os.getenv("PAUSE_S","0.3")))
    prov_set = {(x["provenance"].get("release_version"),x["provenance"].get("freeze_signature"),
                 x["provenance"].get("repository_size")) for x in recs if x["response_status"]=="OK"}
    out = {"wo":"WO-E2E-LEG-002","run":run,"run_at":run_ts,"endpoint":API,"expected_provenance":EXPECT,
           "total":len(recs),"ok":sum(x["response_status"]=="OK" for x in recs),
           "http_fail":sum(x["response_status"]!="OK" for x in recs),
           "distinct_provenance":[list(t) for t in prov_set],"parallel":parallel,
           "workers":(int(os.getenv("WORKERS","8")) if parallel else 1),"records":recs}
    json.dump(out, open(f"e2e_300_run_{run}.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
    newfile = not os.path.exists("e2e_300_execution_log.csv")
    with open("e2e_300_execution_log.csv","a",newline="",encoding="utf-8") as f:
        w=csv.writer(f)
        if newfile: w.writerow(["run","profile_id","status","http","trace_id","release","freeze","repo_size","duration_ms","error"])
        for x in recs:
            pv=x["provenance"]
            w.writerow([run,x["profile_id"],x["response_status"],x["http_status"],x["trace_id"],
                        pv.get("release_version"),pv.get("freeze_signature"),pv.get("repository_size"),
                        x["duration_ms"],x["error"]])
    print(f"\n=== RUN {run} DONE === ok={out['ok']}/300 fail={out['http_fail']} distinct_provenance={len(prov_set)}")
    if len(prov_set)>1: print("!! PROVENANCE MISMATCH — mixed run, STOP and review.")
    exp=(EXPECT['release_version'],EXPECT['freeze_signature'],EXPECT['repository_size'])
    if prov_set and prov_set!={exp}: print(f"!! provenance != expected RC1/337: {prov_set}")

if __name__=="__main__":
    main()
