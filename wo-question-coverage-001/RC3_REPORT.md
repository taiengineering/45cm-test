# WO-QUESTION-COVERAGE-001 · RC2 → RC3 Question Layer 개선 효과 검증

**Goal** G-mscv5q2p-9879fe · **Universe** UNIVERSE_1000 (Frozen, 재생성 0)
**변경 범위** Question Catalog 시뮬레이션만. Runtime·Repository·Adapter·Canonicalizer·법령·엔진·Universe 변경 0.
**PASS/FAIL 선언 없음.** 모든 수치는 Estimated Reachability.

> **실제 DB는 변경하지 않았다.** `diagnosis_input_fields`에 대한 UPDATE는 별도 승인 게이트다. 본 WO는 오버레이 시뮬레이션이다.

## STEP 1 · RC2 Baseline Freeze 확인 — PASS

| 항목 | 값 |
|---|---|
| UNIVERSE_1000 business_id checksum | `85188881e646b048…` |
| consumer_input checksum | `70276aa7e20186ff…` |
| full_record checksum | `805888b60e6404a5…` |
| UNIVERSE_500 checksum | `79f02efe3a032896…` (일치, 훼손 없음) |
| 감사 run_id | `61c1f54529de` (exit 0) |
| 판정 | REALISTIC 1,000 / duplicates 0 |

**generator drift 1건 기록**: `catalog.py` sha256이 UNIVERSE_500 동결 시점과 다르다. 원인은 `PATTERN_FREEZE` 상수 append뿐이며 생성·판정 로직 무변경. 은폐하지 않고 `UNIVERSE_1000_FREEZE.json.generator_drift_since_500`에 남긴다.

## STEP 2·3 · RC3 Question Catalog

규칙: ① `is_active=false` 중 **Repository atom 보유분만** 활성화 ② ABSENT 중 atom 보유분만 신설 ③ **atom 0은 NOT_RECOVERABLE로 유지(열지 않는다)**

| Sector | 활성화 | 신설 | NOT_RECOVERABLE |
|---|---|---|---|
| INDUSTRIAL | 18 | 0 | 10 |
| CONSTRUCTION | 8 | 0 | 6 |
| BUILDING | 1 | 4 | 13 |

atom 0인 질문을 열지 않은 것이 핵심이다. 열었다면 소비자에게 답을 받고도 결과가 없는, 더 나쁜 경험이 된다.

## STEP 4 · Question Mapping Audit

신규·활성화 31개 질문 전건에 대해 4단계 기록 → `rc3_question_mapping_audit.csv`. 전부 `Question PASS > Canonicalizer PASS > Adapter PASS > Runtime PASS`로 통과한다. boolean `has_*`이므로 Adapter를 그대로 지나간다.

## STEP 5·6 · 동일 Universe 재측정 — RC2 vs RC3

| | RC2 | RC3 | Δ |
|---|---|---|---|
| **Estimated Reachability** | 595/4,970 = **12.0%** | 4,379/4,970 = **88.1%** | **+76.1%p** |
| 제조 | 103/1,655 = 6.2% | 1,564/1,655 = 94.5% | +88.3%p |
| 건설 | 0/1,890 = **0.0%** | 1,590/1,890 = **84.1%** | +84.1%p |
| 건축물 | 492/1,425 = 34.5% | 1,225/1,425 = 86.0% | +51.5%p |

**질문 카탈로그 플래그만 바꿔서 건설이 0% → 84.1%가 된다.** 코드 한 줄, 법령 한 건, atom 하나 건드리지 않았다.

## STEP 7 · Layer Recovery

| Layer | RC2 | RC3 | Recovery |
|---|---|---|---|
| **Question** | 4,175 | **391** | **3,784** |
| Adapter | 0 | 0 | 0 |
| Repository | 200 | 200 | 0 |
| Runtime | 0 | 0 | 0 |

RC3 잔여 차단 591건의 내역은 전부 예측대로다.

| 잔여 필드 | 건수 | 사유 |
|---|---|---|
| has_temp_electric | 300 | atom 0 — NOT_RECOVERABLE |
| has_sprinkler | 200 | Repository mapped_field 부재 |
| has_plating | 42 | atom 0 |
| has_injection | 27 | atom 0 |
| has_heat_treatment | 22 | atom 0 |

## 새로 드러난 Adapter 병목 (본 WO의 두 번째 발견)

의무 단위로는 Adapter 차단이 0이지만, **입력 단위로 보면 Adapter가 최대 손실 지점으로 올라선다.**

| 입력 상태 (19,066건) | RC2 | RC3 |
|---|---|---|
| SUPPORTED | 2,387 (12.5%) | **5,724 (30.0%)** |
| NAME_MISMATCH | 1,096 | 1,096 |
| PASSTHROUGH_ONLY | 8,703 | 8,703 |
| NOT_ASKED | 6,880 | 3,543 |

| 소실 지점 | RC2 | RC3 |
|---|---|---|
| 0_Question | 6,880 | 3,543 |
| **3_Adapter** | 8,495 | **8,495 (44.6%) ← 최대** |
| 4_Runtime | 1,186 | 1,186 |

질문을 열어도 Adapter 손실은 1건도 줄지 않는다. RC2에서 Question이 가렸던 병목이 RC3에서 그대로 노출된 것이다 — **OBS-A1**(공정·설비 목록 미평탄화)과 **OBS-A8**(수치·텍스트 계약 미적재)이 그 실체다. 다음 개선 대상은 여기다.

## STEP 8 · Pattern Delta (frozen — occurrence만 갱신)

| Sector | Question RC2 → RC3 | Repository RC2 → RC3 |
|---|---|---|
| 제조 | 1,552 → **91** | 0 → 0 |
| 건설 | 1,890 → **300** | 0 → 0 |
| 건축물 | 733 → **0** | 200 → 200 |

`OBS-A1~A10` FROZEN 유지, 설명 재기술 없음. **신규 Pattern 0건 — OBS-A11 미발생.**

## STEP 9 · Priority 재산정

| Priority | RC2 | RC3 |
|---|---|---|
| P1 | 2,148 | **0** |
| P2 | 1,237 | **0** |
| P3 | 399 | **0** |
| P4 | 591 | 591 |

P1~P3이 전량 소멸하고 P4(회복 불가·Repository 대기)만 남는다. **Question Layer 개선으로 처리 가능한 우선순위 항목은 남지 않는다.**

## 종료 — 4가지 결과

**① Question 개선으로 회복된 항목** — 3,784건. Estimated Reachability 12.0% → 88.1%. 수단은 `is_active` 전환 31개 필드뿐.

**② Question 이후 새롭게 드러난 Adapter 병목** — 입력 8,495건(44.6%)이 Adapter에서 소실되며, RC3에서 최대 손실 지점이 된다. OBS-A1·A8이 실체. 질문 개방은 이 병목을 줄이지 않는다.

**③ Repository 한계로 남는 항목** — 591건. `has_temp_electric` 300 · `has_sprinkler` 200 · `has_plating` 42 · `has_injection` 27 · `has_heat_treatment` 22. atom을 신설하지 않는 한 질문을 열어도 무효이므로 **열지 않은 채로 두었다.**

**④ 다음 개선 우선순위**
```
1. Question  — is_active 31개 필드 개방 (실제 DB UPDATE, 별도 승인 필요)
2. Adapter   — 공정·설비 목록 평탄화(OBS-A1) + 수치·텍스트 계약 적재(OBS-A8)
               + 형식·명칭 정합(OBS-A2·A3·A4)   ← RC3에서 최대 병목
3. Repository — atom 0 필드 5종 신설
```

## Executive Summary

1,000개 사업장에 대해 **질문 카탈로그의 활성 플래그만 바꾸면** 소비자가 받는 법정 의무 도달률이 **12% → 88%**가 된다. 코드·엔진·법령·저장소를 건드리지 않는다. 남은 12%는 저장소에 근거 조문이 없는 항목이며, 이는 질문을 여는 것으로 해결되지 않는다. 그리고 질문을 열고 나면 다음 병목은 Adapter로 이동한다 — 소비자가 적어낸 공정·설비 목록과 수치가 계약에 실리지 않기 때문이다.

## 산출물

`UNIVERSE_1000_FREEZE.json` · `rc3_result.json` · `rc3_question_mapping_audit.csv` · `rc3.py` · `rc2_verify.py` · `rc3.log` · `step1.log`
