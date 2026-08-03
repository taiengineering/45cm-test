# 08 EXECUTIVE_SUMMARY — WO-ANALYSIS-E2E-1000-001

**Goal** G-msczdjer-5dc7b8 · 분석 전용
**수정 0 · 설계 0 · 개선안 0 · DB 변경 0 · Runtime 변경 0**

> Runtime은 실행하지 않았다. 도달성 수치는 계약 기반 구조 분석 결과다.

## 무엇이 발생했는가

1,000개 사업체가 SoT에서 읽은 공정 1,301건·설비 3,460건·작업 1,517건 중 Repository 판정에 도달한 것은 **0건**이다. Consumer 질문 16,400건 중 완주한 것은 **1,000건(6.1%)**이며 전부 `worker_count` 하나다.

## 왜 발생했는가 — 구조 5종

| Root Cause | Layer | 구조 | Observation | 영향 |
|---|---|---|---|---|
| **RC-1** Vocabulary | Layer 경계 | 어휘 체계 3종 분기, SoT∩Question=0 · SoT∩Repository=0 | A2·A3·A4·A11·A14 | SoT 6,278건 전량 미도달 |
| **RC-2** Question | Layer 1 | Repository 39종 중 25종이 활성 질문에 부재(27종은 비활성으로 존재) | A6·A7·A9·A10 | 판정 필드 미수집 |
| **RC-3** Adapter | Layer 3 | 계약 적재 키가 `sector`·`ksic_code`·`worker_count`·`has_*`로 제한 | A1·A8·A13 | 4,000건 제거 |
| **RC-4** Source | Layer 0 | Generator가 읽을 SoT 부재 2,011건 | A12 | 11,400건 응답 불가 |
| **RC-5** Runtime | Layer 5 | 임계 컬럼 부재로 Presence-only 판정 | A5 | 도달분 1,000건의 크기 정보 미사용 |

**14개 Observation은 독립 결함이 아니라 위 5개 구조의 발현이다.**

## 소실 지점

| 지점 | 건수 | 비율 |
|---|---|---|
| Layer 1 (NOT_ANSWERABLE) | 11,400 | 69.5% |
| Layer 3 (Adapter DROP) | 4,000 | 24.4% |
| Layer 2 (Canonicalizer) | 0 | 0% |
| Layer 5 (Repository) | 0 | 0% |
| 완주 | 1,000 | 6.1% |

Layer 2의 소실이 0이고 Layer 5의 소실이 0인 것은 두 계층이 완전해서가 아니다. Layer 2는 값을 버리지 않는 설계이고, Layer 5는 앞단에서 이미 어휘가 12종 이내로 축소된 뒤 도달하기 때문이다.

## Finding 목록

F-001 어휘 3종 분기 · F-002 Adapter 계약 키 제한 · F-003 Repository 25종 미질문 · F-004 Canonicalizer 소실 0 · F-005 소스 부재의 전파 · F-006 완주 경로 1종 · F-007 Layer 5 소실 0의 성격 · F-008 5 Root Cause 수렴 · F-009 미발화 4건의 의미

## 완료 조건 대비

| 조건 | 결과 |
|---|---|
| Observation A1~A13 전건 분석 | 완료 (재현 7 · 간접재현 2 · 미발화 4) |
| Root Cause 분류 | 완료 (5종) |
| Vocabulary 분석 | 완료 |
| Information Loss 분석 | 완료 (8 상태값) |
| Lineage 분석 | 완료 (유형 3종) |
| Finding 작성 | 완료 (F-001~F-009) |
| 개선안 · 수정 · 설계 · DB 변경 · Runtime 변경 | **전부 0** |

## 산출물

`01_INPUT_LAYER_ANALYSIS.md` · `02_VOCABULARY_ANALYSIS.md` · `03_INFORMATION_LOSS_ANALYSIS.md` · `04_LINEAGE_ANALYSIS.md` · `05_ROOT_CAUSE_ANALYSIS.md` · `06_OBSERVATION_VALIDATION.md` · `07_FINDINGS.md` · `08_EXECUTIVE_SUMMARY.md` · 데이터 `vocabulary_sets.json` · `e2e_stage_trace.csv`(16,400행)

## 09 LAYER_DEPENDENCY (STEP 7 — 구조 관측만, 수정안 없음)

| 변경 대상 Layer | 구조상 다음 Layer에 나타나는 영향 |
|---|---|
| Layer 1 (Question) | 응답이 생성되면 Layer 2를 소실 없이 통과하고 Layer 3의 계약 키 집합에 걸린다. 즉 Layer 1 단독 변화는 Layer 3 제약을 만난다 |
| Layer 3 (Adapter) | 계약 키가 확장되면 Layer 5의 `mapped_field` 39종 집합에 걸린다. Adapter 단독 변화는 Repository 어휘 범위를 넘지 못한다 |
| Layer 5 (Repository) | `mapped_field`가 확장되면 Layer 1의 질문 존재 여부와 Layer 3의 계약 키에 동시에 의존한다 |
| Layer 0 (Source) | SoT 축이 채워지면 Layer 1의 `NOT_ANSWERABLE`이 감소하나, RC-1(어휘 불일치)은 그대로 남는다 |
| RC-1 (Layer 경계) | 어느 단일 Layer의 변화로도 해소되지 않는다. SoT 어휘와 field_code 어휘가 만나는 지점에 위치한다 |

위 표는 **구조적 의존 관계의 관측**이며 수정안·순서·우선순위를 제안하지 않는다.
