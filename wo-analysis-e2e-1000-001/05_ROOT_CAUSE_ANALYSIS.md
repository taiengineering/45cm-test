# 05 ROOT_CAUSE_ANALYSIS — WO-ANALYSIS-E2E-1000-001

Observation을 **원인이 아니라 구조 기준**으로 분류하고, 동일 Root Cause를 공유하는 것을 묶는다.

## Root Cause 구조 분류

### RC-1 · Vocabulary Layer — 어휘 체계 분기

| 항목 | 내용 |
|---|---|
| 구조 | SoT 어휘(396) · Question 어휘(99) · Repository 어휘(39)가 서로 다른 명명 체계를 사용 |
| 교집합 | SoT ∩ Question = 0 · SoT ∩ Repository = 0 · Question ∩ Repository = 41 |
| 소속 Observation | **A2 · A3 · A4 · A11 · A14** |
| 공통점 | 값이 존재하는데 **이름·형식이 달라** 다음 Layer가 인식하지 못함 |

### RC-2 · Question Layer — 질문 집합과 판정 집합의 불일치

| 항목 | 내용 |
|---|---|
| 구조 | Repository 39종 중 25종이 활성 질문에 부재. 그중 27종은 비활성 질문으로 존재 |
| 소속 Observation | **A6 · A7 · A9 · A10** |
| 공통점 | 판정에 쓰이는 필드를 **묻지 않음**. 응답 자체가 생성되지 않음 |

### RC-3 · Adapter Layer — 계약 적재 키 제한

| 항목 | 내용 |
|---|---|
| 구조 | `build_input_contract`가 `sector`·`ksic_code`·`worker_count`·`has_*`만 계약에 적재. 활성 질문 44종 중 25종이 이 집합 밖 |
| 소속 Observation | **A1 · A8 · A13** |
| 공통점 | 수집·정규화까지 성공한 값이 **계약 단계에서 제거**됨 |

### RC-4 · Source Layer — Generator 소스 부재

| 항목 | 내용 |
|---|---|
| 구조 | Universe 생성 시 4축(작업·설비·공사유형·건물용도)에 읽을 SoT 없음 → `NO_GENERATOR_SOURCE` 2,011건 |
| 소속 Observation | **A12** |
| 공통점 | 값이 애초에 존재하지 않아 질문에 **응답 불가** |

### RC-5 · Runtime Layer — 판정 방식

| 항목 | 내용 |
|---|---|
| 구조 | Repository에 임계 컬럼 부재 → 존재 여부만 판정(Presence-only) |
| 소속 Observation | **A5** |
| 공통점 | 도달한 값의 **크기 정보가 사용되지 않음** |

### Canonical Layer · Repository Layer

| Layer | 소속 Observation | 관측 |
|---|---|---|
| Canonical | **없음** | 소실 0건. 이름 정규화만 수행하며 값을 버리지 않음 |
| Repository | **없음** (본 E2E 경로 기준) | Layer 3에서 이미 어휘가 축소되어 Repository 단계 소실 0 |

## Root Cause × Observation 매트릭스

| Root Cause | Observation | 본 E2E 영향 건수 |
|---|---|---|
| RC-1 Vocabulary | A2 · A3 · A4 · A11 · A14 | SoT 6,278건 전량 미도달 |
| RC-2 Question | A6 · A7 · A9 · A10 | Repository 25종 미수집 |
| RC-3 Adapter | A1 · A8 · A13 | 4,000 |
| RC-4 Source | A12 | 11,400 |
| RC-5 Runtime | A5 | 1,000 (도달분의 판정 방식) |

## 구조적 사실

- **14개 Observation은 5개 Root Cause로 수렴한다.** 독립 결함 14건이 아니라 구조 5종의 발현이다.
- **RC-1은 다른 4개와 성격이 다르다.** RC-2~RC-5는 특정 Layer 내부의 규칙 문제이나, RC-1은 **Layer 간 경계에 존재하는 체계 불일치**다.
- **Canonical Layer와 Repository Layer에는 귀속되는 Observation이 없다.** 본 E2E 경로 기준의 관측이며, 다른 경로에서의 성립 여부는 본 WO가 조사하지 않았다.
