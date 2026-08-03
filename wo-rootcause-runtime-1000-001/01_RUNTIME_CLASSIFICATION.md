# 01 RUNTIME_CLASSIFICATION — WO-ROOTCAUSE-RUNTIME-1000-001

SoT: `runtime_extract_1000.jsonl` (RUNTIME_BASELINE_1000 result_set `f98e5dcf…`에서 무손실 추출) · 추정 0

## 분류 (1,000건 전수)

| 클래스 | 건수 | 판정 근거 (Runtime 응답) |
|---|---|---|
| SUCCESS_WITH_RULE | **425** | `status=OK` · `http=200` · `runtime_status=OK` · `obligation_count=1` |
| SUCCESS_ZERO_RULE | **575** | `status=OK` · `http=200` · `runtime_status=NO_APPLICABLE` · `obligation_count=0` |
| ERROR | **0** | `error_code` 전건 null · `error` 전건 null |

`http_status` 200 × 1,000 · `contract.valid` true × 1,000 · `invalid_fields` 전건 `[]`
provenance distinct **1종**: `SEMREPO-RC1-2026.07.20` / `SEMREPO-CAL022-2026.07.20` / `15cd17e871b6885d34214c84a58adf47` / 337

## Cross Table — Sector × Worker band

| Sector | 1-4 | 5-9 | 10-29 | 30-49 | 50-99 | 100-299 | 300+ |
|---|---|---|---|---|---|---|---|
| 제조 | 0/70 | 0/67 | 0/69 | 0/83 | **69**/0 | **81**/0 | **61**/0 |
| 건설 | 0/42 | 0/36 | 0/42 | 0/49 | **39**/0 | **48**/0 | **44**/0 |
| 건축물 | 0/27 | 0/24 | 0/31 | 0/35 | **33**/0 | **23**/0 | **27**/0 |

(WITH_RULE / ZERO_RULE)

**worker band 50 미만은 전건 ZERO_RULE, 50 이상은 전건 WITH_RULE. sector 무관.**

## Cross Table — Worker 경계

| | n | worker min | worker max |
|---|---|---|---|
| obligation_count=1 | 425 | **50** | 899 |
| obligation_count=0 | 575 | 1 | **49** |

경계 위반 0건 (obl=1 & w<50 → 0 · obl=0 & w≥50 → 0)

## Cross Table — KSIC

제조 500사의 KSIC lv2 **25종 중 24종이 두 클래스 혼재**. 동일 KSIC 안에서 worker band에 따라 결과가 갈린다.

## Cross Table — Company

`accepted_count` 전건 **1**, `active_fields` 전건 `["worker_count"]`. 회사별 차이는 `worker_count` 값과 `unknown_fields` 구성뿐이다.

| unknown_fields | 건수 |
|---|---|
| `["ksic_code","sector"]` | 500 (제조) |
| `["sector"]` | 500 (건설·건축물) |
