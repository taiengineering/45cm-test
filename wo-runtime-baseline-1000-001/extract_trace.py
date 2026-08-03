#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RUNTIME_BASELINE_1000 결과 1,000건에서 분석용 최소 필드를 무손실 추출한다.

목적: WO-ROOTCAUSE-RUNTIME-1000-001 은 추정을 금지하므로, 분석 측이 실제 Runtime
      응답을 직접 읽어야 한다. 1,000개 JSON 원본 대신 필요한 필드만 1개 JSONL 로 모은다.
원칙: 결과 파일은 읽기만 한다(수정 0). 값 가공·추정 없음. 없는 값은 null 그대로.

사용:
    cd ~/45cm-test/wo-runtime-baseline-1000-001
    python3 extract_trace.py
    # 산출: runtime_extract_1000.jsonl  (+ extract_checksum.json)
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RESULT_DIR = os.environ.get("RUNTIME_RESULT_DIR") or os.path.join(HERE, "runtime_result")
OUT = os.path.join(HERE, "runtime_extract_1000.jsonl")

files = sorted(f for f in os.listdir(RESULT_DIR) if f.endswith(".json"))
if not files:
    sys.exit(f"결과 파일이 없습니다: {RESULT_DIR}")

n = 0
with open(OUT, "w", encoding="utf-8") as w:
    for fn in files:
        d = json.load(open(os.path.join(RESULT_DIR, fn), encoding="utf-8"))
        raw = d.get("raw_response") or {}
        ct = raw.get("contract") or {}
        pv = raw.get("provenance") or {}
        obls = raw.get("obligations") or []
        rec = dict(
            business_id=d.get("business_id"),
            sector=d.get("sector"),
            request_payload=d.get("request_payload"),
            input_checksum=d.get("input_checksum"),
            status=d.get("status"),
            http_status=d.get("http_status"),
            runtime_ms=d.get("runtime_ms"),
            error=d.get("error"),
            runtime_status=raw.get("status"),
            trace_id=raw.get("trace_id"),
            error_code=raw.get("error_code"),
            obligation_count=raw.get("obligation_count"),
            obligations=[dict(atom_id=o.get("atom_id"),
                              mapped_field=o.get("mapped_field"),
                              law_name=o.get("law_name"),
                              law_article=o.get("law_article"),
                              evidence=o.get("evidence"),
                              applicability=o.get("applicability"),
                              triggered_by=o.get("triggered_by"),
                              source_atom_ids=o.get("source_atom_ids")) for o in obls],
            contract_valid=ct.get("valid"),
            accepted_count=ct.get("accepted_count"),
            active_fields=ct.get("active_fields"),
            unknown_fields=ct.get("unknown_fields"),
            invalid_fields=ct.get("invalid_fields"),
            missing_fields=ct.get("missing_fields"),
            provenance=dict(release_version=pv.get("release_version"),
                            repository_version=pv.get("repository_version"),
                            freeze_signature=pv.get("freeze_signature"),
                            repository_size=pv.get("repository_size"),
                            rc_snapshot_checksum=pv.get("rc_snapshot_checksum")),
            started_at=d.get("started_at"), finished_at=d.get("finished_at"))
        w.write(json.dumps(rec, ensure_ascii=False) + "\n")
        n += 1


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


ck = dict(extract_file="runtime_extract_1000.jsonl", records=n, sha256=sha(OUT),
          result_set=hashlib.sha256("".join(
              sha(os.path.join(RESULT_DIR, f)) for f in files).encode()).hexdigest(),
          size_bytes=os.path.getsize(OUT))
json.dump(ck, open(os.path.join(HERE, "extract_checksum.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(json.dumps(ck, ensure_ascii=False, indent=1))
print("\n※ result_set 이 RUNTIME_BASELINE_1000 Freeze 값과 일치해야 한다:")
print("   f98e5dcfb744194e75d7a5dbab5be9a5e745b22e5cb15c2932c1a9248a9c7e79")
