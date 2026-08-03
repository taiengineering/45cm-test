# UNIVERSE_500 — Canonical Freeze

**WO** WO-E2E-LEG-1000-002 · **Goal** G-mscro68p-fcf706 · **동결일** 2026-08-03

## 1. 동결 대상

| 항목 | 값 |
|---|---|
| freeze_id | `UNIVERSE_500` |
| 사업체 | 500 (제조 250 · 건설 150 · 건축물 100) |
| batches | Batch 1~10 (재생성본) |
| business_id checksum | `e735e06d13f7a7e8f150cd413e6d071a104302c6b1a633905aacdca1116d1e10` |
| consumer_input checksum | `e7e9402498957b0b415b2df0b083871002e8e0b5924542fd2c9a1fc432731d18` |
| full_record checksum | `79f02efe3a032896ccba2d74ca35c096755b27708aa3335a3c7d9d5e2d8af7b7` |
| 감사 run_id | `b36dff64e23f` (exit_code 0) |
| 판정 | REALISTIC 500 / duplicates 0 / findings 0 |
| random seed 규칙 | `random.Random(20260803 + BATCH * 977)` |
| 생성기 | batchgen.py · catalog.py · mfg.py · con.py · bld.py (sha256 기록) |
| 감사기 | batch_audit.py · checkpoint.py · verify_gate.py · run.sh (sha256 기록) |

전체 sha256 목록은 `UNIVERSE_500_FREEZE.json`.

**lock_rule**: Batch 1~10은 재생성하지 않는다. 오류 발견 시 레코드를 조용히 수정하지 않고 **Observation 또는 정정 이력**으로 남긴다.

Batch 11~20 생성 후 full_record checksum을 재검증해 `79f02efe…` 일치를 확인했다(FREEZE INTACT).

## 2. 이전 산출물 지위

```
BATCH1_REPORT.md 수치
BATCH2_REPORT.md 수치
ANALYSIS_200.md 수치·산출물
   → SUPERSEDED_BY_UNIVERSE_500
```

삭제하지 않는다. 변주 축 추가로 Batch 1~10을 전체 재생성했으므로 **현재 Universe의 직접 선조가 아니며 비교 기준으로 사용하지 않는다.** 방법론 승인 이력으로만 유효하다.

## 3. 지표 명칭 정정 (중요)

```
Estimated Reachability = 12.0%
```

**Runtime Reachability 아님. 최종 E2E 결과 아님.**

정의: 생성된 회사 + 질문 카탈로그(`diagnosis_input_fields`) + Adapter 계약(`consumer_input_canonicalizer`·`input_contract_builder`) + Repository `mapped_field`로 산출한 **사전 도달 가능성**. Runtime은 실행하지 않았다. Operator가 1,000건을 실제 실행하고 결과를 전수 정독한 뒤에만 Runtime 결과로 확정한다.

## 4. 감사 실행 fail-closed 전환

두 번의 stale 판독 사고(SIGPIPE, KeyError) 후 운영 규칙으로 고정:

- 출력은 `/tmp/*.tmp.log`에 작성, **exit 0일 때만** 최종 파일명으로 이동
- gate/CSV는 `.tmp` 작성 후 `os.replace` **atomic rename**
- gate에 `run_id` · `started_at` · `completed_at` · `exit_code` 기록
- `verify_gate.py N EXPECTED` — run_id 존재 · exit_code 0 · total 일치를 assert. **실패 시 파이프라인 중단**
- 감사 성공 전 gate 파일 판독 금지

이 규칙 도입 직후 실제로 두 건을 더 잡았다: ① `source`가 sh에서 미지원이라 감사가 아예 실행되지 않은 채 freeze가 이전 gate를 읽으려 한 건 ② `BATCH` 환경변수 누락으로 감사가 Batch 1(50사)만 돌았는데 gate는 500사짜리 stale 파일이던 건. 둘 다 `verify_gate.py`의 assert가 차단했다.
