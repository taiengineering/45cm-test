# RUNTIME_BASELINE_1000 — Freeze

**freeze_id** `RUNTIME_BASELINE_1000` · **WO** WO-RUNTIME-BASELINE-1000-001 · **Goal** G-msczuepg-14f70d
**동결일** 2026-08-03 · **실행자** Operator (터미널) · **분석 0**

---

## 1. 4종 체크섬 (Freeze)

| 대상 | sha256 |
|---|---|
| `result_set` (runtime_result/ 1,000건 파일별 sha256 연접 해시) | `f98e5dcfb744194e75d7a5dbab5be9a5e745b22e5cb15c2932c1a9248a9c7e79` |
| `runtime_summary.csv` | `244f71f4be8b83f344362f13462d898718c8e1c54517343643a4aeb1f3aa3989` |
| `runtime_manifest.json` | `4e1436e22f2021f00adaa72e5f9cf85c93481fb09704883fbbdf3d09402c7b3d` |
| `retry_queue.json` | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` |

`retry_queue.json`의 해시는 문자열 `[]`의 sha256과 일치한다 → **실패 0건**.

## 2. 실행 사실

| 항목 | 값 |
|---|---|
| 대상 | UNIVERSE_1000 (GENERATOR_ASSET, `ccc275c4bbcc39adc49e8dd7…`) |
| 입력 파일 | `runtime_input_1000.jsonl` sha256 `c674e5b67854230af78b9d241408c71e3f0c8e0dd443471b4f5288f7f1418fea` |
| 엔드포인트 | `https://leg-runtime-production.up.railway.app/rtm/evaluate` |
| 실행 환경 | Railway `production` / service `tai-api-prod` |
| worker | 4 |
| 결과 파일 | **1,000 / 1,000** |
| status | **OK 1,000 · FAIL 0 · error 0** |
| 실행 시각 | 2026-08-03T09:09:08.544Z ~ 09:10:06.130Z (약 58초) |
| runtime_ms | min 185 · p50 202 · mean 228 · max 1,248 |

## 3. Runtime Provenance (응답 실측)

```
release_version     SEMREPO-RC1-2026.07.20
repository_version  SEMREPO-CAL022-2026.07.20
freeze_signature    15cd17e871b6885d34214c84a58adf47
repository_size     337
rc_snapshot_checksum ""   (응답에 빈 문자열)
```

## 4. 응답 계약 실측 (전건 동일)

```
contract.valid           true
contract.active_fields   ["worker_count"]
contract.accepted_count  1
contract.missing_fields  38종
contract.unknown_fields  제조 ["ksic_code","sector"] / 건설·건축물 ["sector"]
contract.invalid_fields  []
```

전송한 3개 키 중 Runtime이 **수용한 것은 `worker_count` 하나**이며, `sector`·`ksic_code`는 `unknown_fields`로 반환됐다.

## 5. 결과 분포 (실측)

| obligation_count | 건수 |
|---|---|
| 0 | 575 |
| 1 | 425 |

| Sector | obl=1 | obl=0 |
|---|---|---|
| 제조 500 | 211 | 289 |
| 건설 300 | 131 | 169 |
| 건축물 200 | 83 | 117 |

근로자수 대조:

```
obligation_count = 1  →  worker_count 50 이상 (n=425, 최소 50)
obligation_count = 0  →  worker_count 49 이하 (n=575, 최대 49)
혼재 구간 0건 · sector 무관
```

발화 의무 1종 (전 425건 동일):

```
atom_id       0ce68131-3ec9-5bed-af04-755550683691
mapped_field  total_floor_area
law_name      산업안전보건기준에 관한 규칙
law_article   19
evidence      "사업주는 연면적이 400제곱미터 이상이거나 상시 50명 이상의 근로자가 작업하는 옥내작업장"
applicability APPLICABLE
triggered_by  ["total_floor_area"]
```

`runtime_status`는 obl=0일 때 `NO_APPLICABLE`, obl=1일 때 `OK`.

**`rule_count`는 응답 계약에 존재하지 않는다.** 공란이 아니라 `NOT_PROVIDED`로 기록했다.

## 6. 실행 중 발생한 스크립트 결함 3건과 교정

| # | 결함 | 영향 | 교정 |
|---|---|---|---|
| 1 | 빈 `--retry` 실행이 전체 실행 `runtime_manifest.json`을 덮어씀 | success/failed/provenance 유실(`mode:RETRY(0)`, `targets:0`) | retry는 `runtime_manifest_retry.json`으로 분리. 유실분은 `rebuild_manifest.py`로 결과 스캔 복원(재실행 없음) |
| 2 | 빈 `--retry`가 `retry_queue.json`을 `[]`로 덮어씀 | 원본 실패 목록 소실 위험 | retry는 `retry_queue_after_retry.json`으로 분리 |
| 3 | `rule_count`를 존재하지 않는 키에서 탐색 | 전건 공란 | 응답 계약에 없음을 확인하고 `NOT_PROVIDED` 고정 |

추가로 R-008(하드코딩 금지) 위반 1건을 교정했다 — URL·경로·worker 상수를 환경변수로 이동, `LEG_RTM_URL`은 기본값 없이 필수화(R2 상한 4는 코드로 강제 유지).

## 7. 완료 조건 대비

| 조건 | 결과 |
|---|---|
| Runtime 1,000건 실행 완료 | **1,000 OK** |
| Worker ≤ 4 | 4 |
| Railway 환경변수 사용 | production / tai-api-prod |
| 전체 결과 저장 | `runtime_result/` 1,000건 |
| 실패 건 retry_queue 생성 | 생성(`[]`, 실패 0) |
| Retry 단독 실행 가능 | 가능 (실행 확인됨) |
| Manifest 생성 | 재구성 완료 |
| Freeze 완료 | 본 문서 |
| 분석 미수행 | **준수** |

## 8. lock_rule

`RUNTIME_BASELINE_1000`은 재실행하지 않는다. 이후 Question·Adapter·Repository 개선의 전/후 비교는 본 Baseline을 기준으로 한다. 오류 발견 시 결과 파일을 수정하지 않고 Observation으로 남긴다.

## 9. 다음 (별도 WO)

Runtime Result → Root Cause → Question → Adapter → Repository 순 분석. 본 WO는 실행·저장·Freeze까지만 수행했으며 `contract.unknown_fields`·`triggered_by` 관련 사실은 기록만 하고 해석하지 않았다.
