#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""runtime_result/ 를 스캔해 runtime_summary.csv 와 runtime_manifest.json 을 재생성한다.
재실행·네트워크 불필요. 결과 파일은 읽기만 한다(수정 0).

사용:
    cd ~/45cm-test/wo-runtime-baseline-1000-001
    python3 rebuild_manifest.py

배경: 빈 --retry 실행이 전체 실행 manifest 를 덮어써 success/provenance 가 유실됨.
개별 결과 파일에는 provenance 가 온전히 남아 있으므로 스캔으로 복원한다.
"""
import csv, hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RESULT_DIR = os.environ.get("RUNTIME_RESULT_DIR") or os.path.join(HERE, "runtime_result")
INPUT = os.environ.get("RUNTIME_INPUT") or os.path.join(HERE, "runtime_input_1000.jsonl")

files = sorted(f for f in os.listdir(RESULT_DIR) if f.endswith(".json"))
if not files:
    sys.exit(f"결과 파일이 없습니다: {RESULT_DIR}")

rows, prov, started, finished, ok, fail = [], set(), [], [], 0, 0
for fn in files:
    d = json.load(open(os.path.join(RESULT_DIR, fn), encoding="utf-8"))
    raw = d.get("raw_response") or {}
    contract = raw.get("contract") or {}
    rows.append(dict(
        business_id=d["business_id"], status=d["status"], runtime_ms=d["runtime_ms"],
        rule_count="NOT_PROVIDED",                       # 응답 계약에 해당 키 없음
        obligation_count=raw.get("obligation_count"),
        runtime_status=raw.get("status"), trace_id=raw.get("trace_id"),
        accepted_count=contract.get("accepted_count"),
        active_fields=";".join(contract.get("active_fields") or []),
        unknown_fields=";".join(contract.get("unknown_fields") or []),
        missing_field_count=len(contract.get("missing_fields") or []),
        error=d.get("error") or "",
        started_at=d["started_at"], finished_at=d["finished_at"]))
    p = raw.get("provenance") or d.get("provenance") or {}
    if p:
        prov.add(json.dumps(p, sort_keys=True, ensure_ascii=False))
    started.append(d["started_at"]); finished.append(d["finished_at"])
    ok += (d["status"] == "OK"); fail += (d["status"] != "OK")

with open(os.path.join(HERE, "runtime_summary.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

p0 = json.loads(sorted(prov)[0]) if prov else {}
man = dict(
    wo="WO-RUNTIME-BASELINE-1000-001", rebuilt_from="runtime_result/ scan (재실행 없음)",
    universe_checksum="ccc275c4bbcc39adc49e8dd7…(GENERATOR_ASSET_UNIVERSE_1000 full_record)",
    input_file_sha256=(hashlib.sha256(open(INPUT, "rb").read()).hexdigest()
                       if os.path.exists(INPUT) else None),
    endpoint=os.environ.get("LEG_RTM_URL"),
    mode="FULL(reconstructed)",
    runtime_version=p0.get("release_version"), repository_version=p0.get("repository_version"),
    engine_version=p0.get("freeze_signature"), repository_size=p0.get("repository_size"),
    distinct_provenance=[json.loads(x) for x in sorted(prov)],
    railway_environment=os.environ.get("RAILWAY_ENVIRONMENT_NAME"),
    railway_service=os.environ.get("RAILWAY_SERVICE_NAME"),
    started_at=min(started), finished_at=max(finished),
    worker=4, targets=len(rows), success=ok, failed=fail, results_on_disk=len(rows))
with open(os.path.join(HERE, "runtime_manifest.json"), "w", encoding="utf-8") as f:
    json.dump(man, f, ensure_ascii=False, indent=1)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


cks = dict(
    summary=sha(os.path.join(HERE, "runtime_summary.csv")),
    manifest=sha(os.path.join(HERE, "runtime_manifest.json")),
    result_set=hashlib.sha256("".join(
        sha(os.path.join(RESULT_DIR, fn)) for fn in files).encode()).hexdigest(),
    retry=(sha(os.path.join(HERE, "retry_queue.json"))
           if os.path.exists(os.path.join(HERE, "retry_queue.json")) else None))
json.dump(cks, open(os.path.join(HERE, "baseline_checksums.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(json.dumps(dict(files=len(files), success=ok, failed=fail,
                      distinct_provenance=len(prov), checksums=cks), ensure_ascii=False, indent=1))
