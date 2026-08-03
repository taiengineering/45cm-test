# WO-E2E-LEG-1000-002 · 1,000건 완성 — Gap Heatmap · 5계층 우선순위

**Goal** G-mscro68p-fcf706 · **Runtime 미실행** · 코드·엔진·Repository 수정 0.

> 본 문서의 모든 도달 수치는 **Estimated Reachability**다. Runtime 실행 결과가 아니다.

## 1. Universe 완성

| 항목 | 값 |
|---|---|
| 사업체 | **1,000** (제조 500 · 건설 300 · 건축물 200) |
| 판정 | **REALISTIC 1,000 / QUESTIONABLE 0 / INVALID 0** |
| 복제 | **0** |
| 감사 run_id | `61c1f54529de` (exit_code 0, verify_gate PASS) |
| UNIVERSE_500 무결성 | `79f02efe3a032896…` 일치 — Batch 1~10 미변경 확인 |

## 2. Estimated Reachability 추이 — 4배 표본에서 불변

| 누적 | 기대 의무 | 도달 가능 | 비율 |
|---|---|---|---|
| 250사 | 1,017 | 122 | 12.0% |
| 500사 | 2,498 | 297 | 11.9% |
| **1,000사** | **4,970** | **595** | **12.0%** |

| Sector | 기대 | 도달 | 비율 |
|---|---|---|---|
| 제조 | 1,655 | 103 | 6.2% |
| 건설 | 1,890 | **0** | **0.0%** |
| 건축물 | 1,425 | 492 | 34.5% |

건설 300개 현장 **전건**에서 기대 의무 도달 0.

## 3. 신규 Pattern — 0건

| Pattern | Layer | Scope | occurrence |
|---|---|---|---|
| P-Q-001 | Question | CONSTRUCTION | 1,890 |
| P-Q-002 | Question | MANUFACTURING | 1,552 |
| P-Q-003 | Question | ALL (ABSENT) | 733 |
| P-R-001 | Repository | BUILDING | 200 |

Batch 5부터 Pattern Freeze 적용. **1,000건 전 구간에서 신규 Pattern 후보 0건.**

## 4. Gap Heatmap

```
MANUFACTURING   Question   ■■■■■■■■■■■■■■■■■■■■  1,552   (100%)
                Adapter    □                          0
                Repository □                          0
                Runtime    □                          0

CONSTRUCTION    Question   ■■■■■■■■■■■■■■■■■■■■  1,890   (100%)
                Adapter    □                          0
                Repository □                          0
                Runtime    □                          0

BUILDING        Question   ■■■■■■■■■■■■■■■■        733   ( 79%)
                Repository ■■■■                    200   ( 21%)
```

제조·건설은 **단일 계층에 100% 집중**. 건축물만 두 계층으로 갈린다.

**Adapter가 0인 것은 Adapter가 정상이라는 뜻이 아니다.** 기대 의무를 구동하는 필드가 전부 boolean `has_*`여서 질문만 열리면 Adapter를 통과하기 때문이다. Adapter 결함(OBS-A1·A2·A3·A8)은 수치·목록 입력에서 발생하며, 이 KPI가 아니라 입력 손실 축(`stage_trace`)에서 관측된다 — 소비자 입력의 **75.5%가 Runtime에 도달하지 못한다**는 수치가 그것이다.

## 5. Top 20 Gap — Occurrence와 Impact 분리

| field | occ | layer | impact | recovery | prio | repo atom |
|---|---|---|---|---|---|---|
| has_excavation | 421 | Question | High | Immediate | P1 | 23 |
| has_confined_space | 389 | Question | High | Short | P1 | 15 |
| has_forklift | 319 | Question | High | Immediate | P1 | 7 |
| **has_temp_electric** | **300** | Question | **Low** | Medium | **P4** | **0** |
| has_concrete_work | 270 | Question | High | Immediate | P1 | 13 |
| has_scaffold | 270 | Question | High | Immediate | P1 | 18 |
| has_pile_work | 240 | Question | High | Immediate | P1 | 14 |
| has_crane | 239 | Question | High | Immediate | P1 | 23 |
| has_conveyor | 211 | Question | Medium | Immediate | P2 | 6 |
| **has_sprinkler** | **200** | Repository | Medium | Medium | P3 | **0** |
| has_high_place_work | 200 | Question | Medium | Short | P2 | 4 |
| has_elevator | 196 | Question | Medium | Short | P2 | 19 |

`has_temp_electric`은 차단 300건으로 4위지만 저장소 atom이 0이라 질문을 열어도 회복이 없다 → **P4**. 빈도만으로 우선순위를 정했다면 P1으로 잘못 올렸을 항목이다.

## 6. Recovery Score

| Score | 차단 건수 | 비율 | 조치 |
|---|---|---|---|
| **Immediate** | 2,862 | **65.4%** | `is_active=true` 전환 |
| Short | 922 | 21.1% | 질문 항목 신설 / Adapter 교정 |
| Medium | 591 | 13.5% | 저장소 atom 신설 |
| **Long** | **0** | **0.0%** | Runtime 변경 |

| Priority | 차단 건수 |
|---|---|
| P1 | 2,148 |
| P2 | 1,237 |
| P3 | 599 |
| P4 | 391 |

## 7. 5계층 개선 우선순위 (확정)

| 순위 | 계층 | 조치 | 회복 규모 | 근거 |
|---|---|---|---|---|
| **1** | Consumer / Question | `diagnosis_input_fields.is_active` 개방 — 단, **저장소 atom 보유 필드만** | 2,862건 (65.4%) | INACTIVE 다수가 atom 보유. `has_temp_electric`류(atom 0)는 제외해야 헛일을 피한다 |
| **2** | Question | ABSENT 항목 신설 — `has_confined_space`(제조)·`has_elevator`(건축)·`has_high_pressure_gas` | 922건 일부 | 저장소 atom 15·19·3 기보유 |
| **3** | Repository | atom 0 필드 신설 — `has_sprinkler`·`has_fire_hydrant`·`has_smoke_control`·`has_temp_electric` | 591건 | 질문은 있으나 mapped_field 0 |
| **4** | Adapter | `elevator_count→has_elevator` 형식 변환, 명칭 3종 정합, 수치·목록 계약 적재, synonym 치환 재검토 | 이 KPI 밖 · 입력 손실 최대 | OBS-A1·A2·A3·A4·A8 |
| **5** | Runtime | Presence-only 해소(임계 컬럼 도입) | 0건 (현 KPI 기준) | 규모·금액이 판정에 영향 없음 |

**순서가 핵심이다.** 1을 열면 4가 즉시 다음 병목으로 드러난다(공정·설비 목록이 여전히 평탄화되지 않으므로). 1 → 3 → 4 → 5 순으로 가야 회복량이 계단식으로 검증된다. 5는 이 조사에서 차단 0건이지만, 규모 무관 판정이라는 별개 품질 이슈로 남는다.

## 8. 이 WO의 결론

- **엔진 문제가 아니다.** Runtime 변경이 필요한 차단은 0건이다.
- **질문 설계 문제다.** 차단의 87.5%가 Question 계층이고, 그중 65.4%는 플래그 전환만으로 즉시 회복된다.
- **1,000건이 필요했던 이유**는 도달률 확인이 아니라(250건에서 이미 수렴) **축별 분해와 회복 우선순위의 신뢰도** 확보였다. 결과적으로 신규 Pattern 0건으로 구조가 확정됐다.

## 9. 다음 (별도 승인 사항 — 본 WO 범위 밖)

1. **Runtime 실행** — Operator가 1,000건을 `/rtm/evaluate`로 실행하고 결과 전수 정독. 그때 비로소 Estimated → Runtime Reachability로 확정된다.
2. Track B BACKLOG 8건 입력모델 설계와 본 결과의 통합.
3. 개선은 **기록만 했고 수행하지 않았다** — 수정은 별도 CHG WO로 승인 후.

## 10. 산출물

`batch1~20_companies.json`(1,000사) · `batch20_audit_cumulative.csv` · `batch20_gate.json` · `gap_impact_1000.csv` · `checkpoint_1000.json` · `UNIVERSE_500_FREEZE.json` · 생성기·감사기 일체
