# WO-E2E-LEG-1000-002 · Batch 3~4 + 200건 중간 분석

**Goal** G-mscro68p-fcf706 · Runtime 미실행 · 코드·엔진·Repository 수정 0.

## 1. 누적 정독 (200/200)

| 판정 | 건수 |
|---|---|
| REALISTIC | **200** |
| QUESTIONABLE / INVALID | 0 / 0 |
| 복제 | 0 |

제조 100 · 건설 60 · 건축물 40. 소비자 입력 누적 3,855건.

**Batch3~4 생성 중 교정 1건 (규칙 추가)**: 건물 4건이 복제로 적발. 원인은 `AREA_CAP`/`FLOOR_CAP`에 **clamp**하는 방식이라 초대형 건물끼리 연면적·층수가 동일값으로 수렴한 것. 상한 이내 **분산 표집**으로 변경. RULE_SOURCE=AUTO(감사기 적발), 규칙 결함은 HUMAN 설계 오류.

## 2. 도달률 안정화 — 수렴 확인

| 누적 | 기대 | 도달 | 도달률 |
|---|---|---|---|
| 50사 | 258 | 27 | 10.5% |
| 100사 | 502 | 58 | 11.6% |
| 150사 | 757 | 91 | 12.0% |
| **200사** | **1,017** | **122** | **12.0%** |

150건에서 12.0%로 수렴해 200건까지 변동 없음. **표본을 4배 늘려도 도달률이 움직이지 않는다** — 우연이 아니라 구조다. 남은 800건은 도달률을 바꾸지 못하며, 축별 세분화와 희소 조합 발견에 기여한다.

## 3. 미도달 원인 (895건)

| reason | 건수 | cause_layer |
|---|---|---|
| NOT_ASKED_INACTIVE | 708 | Question |
| NOT_ASKED_ABSENT | 147 | Question |
| REPOSITORY_MISSING | 40 | Repository |

**Question 855 (95.5%) · Repository 40 (4.5%) · Adapter 0.**

Adapter 계층 미도달이 0인 이유는 기대 의무를 구동하는 필드가 전부 boolean `has_*`이고, 이들은 질문만 열리면 Adapter를 통과하기 때문이다. Adapter 문제(OBS-A1·A2·A8)는 **수치·목록 입력**에서 발생하며, 그건 기대 의무를 직접 구동하지 않아 이 KPI에는 잡히지 않는다. 별도 축으로 관리한다.

## 4. 축별 Heatmap (`heatmap_200.csv`)

**도달률 0% 축 — 건설 10개 유형 전부 + 제조 다수**

| 축 | 사업체 | 기대 | 도달 | Question |
|---|---|---|---|---|
| 건설 대형 복합개발 | 8 | 72 | 0 | 72 |
| 건설 중소형 공동주택 | 7 | 49 | 0 | 49 |
| 건설 플랜트 | 6 | 42 | 0 | 42 |
| 건설 대형 공동주택단지 | 6 | 42 | 0 | 42 |
| 건설 물류센터 신축 | 5 | 40 | 0 | 40 |
| 제조 용접구조물 | 6 | 23 | 0 | 23 |
| 제조 금속열처리 | 7 | 23 | 0 | 23 |
| 제조 자동차부품조립 | 4 | 21 | 0 | 21 |

**도달률 상위 — 건축물 전 용도 30%대**
학교 38.9% · 병원 37.5% · 지식산업센터 37.5% · 공장 건축물 37.5% · 호텔 37.5%.

건축물만 유의미하게 도달하는 이유는 저수조·비상발전기·비상방송이 boolean으로 질문되고 저장소에 동일 이름이 있어서다. 제조·건설은 그 조건을 만족하는 필드가 사실상 없다.

## 5. 회복 우선순위 — 미도달 구동필드 상위

| 필드 | 차단 | 계층 | reason | 저장소 atom |
|---|---|---|---|---|
| has_excavation | 85 | Question | INACTIVE | 23 |
| has_confined_space | 79 | Question | ABSENT(제조) | 15 |
| has_forklift | 69 | Question | INACTIVE | 7 |
| has_temp_electric | 60 | Question | INACTIVE | **0** |
| has_crane | 53 | Question | INACTIVE | 23 |
| has_concrete_work | 53 | Question | INACTIVE | 13 |
| has_scaffold | 53 | Question | INACTIVE | 18 |
| has_pile_work | 48 | Question | INACTIVE | 14 |
| has_conveyor | 45 | Question | INACTIVE | 6 |
| has_sprinkler | 40 | Repository | MISSING | **0** |
| has_elevator | 39 | Question | ABSENT | 19 |

`has_temp_electric`·`has_sprinkler`는 **질문을 열어도 저장소에 atom이 0**이라 회복되지 않는다. Question과 Repository를 동시에 봐야 실제 회복량이 나온다는 근거다.

## 6. 5계층 개선 우선순위 (초안 — 1,000건 완료 시 확정)

| 순위 | 계층 | 조치 | 예상 회복 | 근거 |
|---|---|---|---|---|
| 1 | **Question** | `diagnosis_input_fields.is_active` 개방 (저장소 atom 보유 필드 우선) | 최대 708건 중 atom 보유분 | INACTIVE 708건, 대부분 저장소에 atom 존재 |
| 2 | **Question** | 제조 `has_confined_space`·건축 `has_elevator` 등 ABSENT 항목 신설 | 147건 일부 | 저장소 atom 15·19 보유 |
| 3 | **Repository** | `has_sprinkler`·`has_fire_hydrant`·`has_smoke_control`·`has_temp_electric` atom 신설 | 40건+ | 질문은 있으나 mapped_field 0 |
| 4 | **Adapter** | `elevator_count→has_elevator`, 명칭 3종 정합, 수치·목록 계약 적재 | OBS-A2·A3·A8 | 기대 의무 KPI 밖이나 입력 손실 최대 |
| 5 | **Runtime** | Presence-only 해소(임계 컬럼) | 별건 | 규모 무관 판정 구조 |

순서가 중요하다. 1을 먼저 열면 4가 즉시 다음 병목으로 드러나므로, 1 → 3 → 4 → 5 순으로 가야 회복량이 계단식으로 확인된다.

## 7. 산출물

`batch3_companies.json` · `batch4_companies.json` · `batch4_audit_cumulative.csv`(200사) · `batch4_gate.json` · `heatmap_200.csv` · `analysis_200.json` · `analyze200.py`

## 8. 다음

Batch 5~20(201~1,000). 완료 시 Gap Heatmap 확정 + 5계층 우선순위 확정.
