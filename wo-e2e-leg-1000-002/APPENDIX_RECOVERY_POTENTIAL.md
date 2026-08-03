# WO-E2E-LEG-1000-002 · 부록 — Coverage Recovery Potential · Pattern Freeze

**Goal** G-mscro68p-fcf706 · Runtime 미실행 · 코드·DB 수정 0.
> 수치는 전부 **Estimated Reachability** 기준. Runtime 실행 결과가 아니다.

## 1. Coverage Recovery Potential (1,000사)

| Layer | Block | Recoverable | 회복률 |
|---|---|---|---|
| **Question** | 4,175 | **3,784** | 90.6% |
| **Repository** | 200 | 200 | 100.0% |
| Adapter | 0 | 0 | — |
| Runtime | 0 | 0 | — |
| **계** | **4,375** | **3,984** | **91.1%** |

### 회복 수단별 분해

| 수단 | 건수 | 비율 | 필요 작업 |
|---|---|---|---|
| **`is_active` 전환만** | **3,051** | **69.7%** | 코드·DB 스키마 변경 없음. 카탈로그 플래그만 |
| 질문 항목 신설 | 733 | 16.8% | 카탈로그 row 추가 (저장소 atom 기보유) |
| 저장소 atom 신설 | 200 | 4.6% | Repository 작업 필요 |
| **회복 불가** | 391 | 8.9% | 질문을 열어도 저장소 atom 0 (`has_temp_electric` 등) |

### Sector별

| Sector | Block | Recoverable | 회복률 |
|---|---|---|---|
| 제조 | 1,552 | 1,461 | 94.1% |
| 건설 | 1,890 | 1,590 | 84.1% |
| 건축물 | 933 | 933 | **100.0%** |

건축물은 차단 전건이 회복 가능하다(Question 733 + Repository 200). 건설은 84.1%로 가장 낮은데, `has_temp_electric`(300건, atom 0)이 전량 건설에 몰려 있기 때문이다.

### 회복 가능 필드 상위 10

| field | block = recoverable | repo atom |
|---|---|---|
| has_excavation | 421 | 23 |
| has_confined_space | 389 | 15 |
| has_forklift | 319 | 7 |
| has_concrete_work | 270 | 13 |
| has_scaffold | 270 | 18 |
| has_pile_work | 240 | 14 |
| has_crane | 239 | 23 |
| has_conveyor | 211 | 6 |
| has_high_place_work | 200 | 4 |
| has_elevator | 196 | 19 |

전체 목록 `recovery_potential_1000.csv`.

## 2. Pattern Freeze

```
FROZEN: OBS-A1 ~ OBS-A10        (2026-08-03, operator 승인)
규칙  : frozen Pattern은 occurrence만 누적. 설명 재기술 금지.
신규  : OBS-A11부터 부여하며, 그때만 상세 분석 대상으로 승격.
```

`catalog.PATTERN_FREEZE`에 등록. 1,000건 전 구간에서 신규 Pattern 후보는 0건이었다.

## 3. 이 조사의 최종 결론 (정정)

당초 헤드라인으로 잡았던 "Estimated Reachability 12%"보다 **계층 분포가 본질**이다.

```
Question    4,175   (95.4%)
Repository    200   ( 4.6%)
Adapter         0
Runtime         0
```

소비자가 받는 결과의 병목은 **Runtime이 아니라 질문 설계(Question Layer)**이며, 이는 1,000개 표본에서 일관되게 나타났다. 그리고 그 병목의 **69.7%는 코드·DB 변경 없이 카탈로그 플래그 전환만으로 열린다.**

## 4. 다음 WO 제안 — WO-QUESTION-COVERAGE-001

**질문**: Question Catalog만 열었을 때(`is_active=false → true`) Estimated Reachability가 얼마나 회복되는가?

| 항목 | 내용 |
|---|---|
| 변경 범위 | `diagnosis_input_fields.is_active` **시뮬레이션만** (실제 UPDATE 없음) |
| 금지 | 코드 수정 · Repository 수정 · Runtime 수정 · Adapter 수정 |
| 입력 | UNIVERSE_1000 (본 WO 산출, 재생성 없음) |
| 산출 | 플래그 개방 전/후 Reachability, 필드별 한계효용, 개방해도 무효인 필드 목록 |
| 예상 | 3,051건 회복 → Estimated Reachability 12.0% → 약 73% (상한 추정, 실측 필요) |
| 주의 | 플래그를 열면 OBS-A1(공정·설비 미평탄화)·OBS-A8(수치 미적재)이 즉시 다음 병목으로 드러날 것. 그 2차 병목까지 같은 WO에서 계량해야 실제 효과가 나온다 |

승인 주시면 Goal을 새로 열고 착수하겠습니다. 본 WO(1,000건 Universe 조사)는 이 부록으로 종료 조건을 충족합니다.

## 5. 산출물

`recovery_potential_1000.csv` · `recovery_potential_1000.json` · `recovery.py` · `catalog.PATTERN_FREEZE`
