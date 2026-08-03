# 07 FINDINGS — WO-ANALYSIS-E2E-1000-001

형식: Finding ID · Title · Evidence · Trace · Observation · Conclusion. **의견·제안·우선순위 없음.**

---

## F-001

**Title** 계층별 어휘 체계가 3종으로 분기하며 SoT 축과의 교집합이 0이다
**Evidence** SoT 396종(설비 62·공정 119·작업 215) · Question 99종(active 44·inactive 55) · Repository 39종. SoT ∩ Question = 0, SoT ∩ Repository = 0
**Trace** `vocabulary_sets.json` · 02_VOCABULARY_ANALYSIS
**Observation** A11 · A14
**Conclusion** Universe가 SoT에서 읽은 공정·설비·작업 6,278건은 Question·Repository 어느 어휘와도 이름이 일치하지 않는다.

## F-002

**Title** Adapter 계약 적재 키가 활성 질문 44종 중 19종으로 제한된다
**Evidence** `services/input_contract_builder.py` — contract 구성 = `factory_id`·`sector`·`ksic_code`·`worker_count` + `has_*`. 활성 질문 25종이 이 집합 밖
**Trace** `e2e_stage_trace.csv` s3_adapter=DROP 4,000행 · 03_INFORMATION_LOSS_ANALYSIS
**Observation** A1 · A8 · A13
**Conclusion** 수집·정규화를 통과한 입력 5,000건 중 4,000건이 계약 적재 단계에서 제거된다.

## F-003

**Title** Repository 39종 중 25종이 활성 질문 집합에 없고, 그중 27종은 비활성 질문으로 존재한다
**Evidence** Question(active) ∩ Repository = 14 · Question(inactive) ∩ Repository = 27
**Trace** `diagnosis_input_fields` 실측 · 02_VOCABULARY_ANALYSIS
**Observation** A6 · A7 · A9 · A10
**Conclusion** 판정에 사용되는 필드의 다수가 소비자에게 노출되지 않는다.

## F-004

**Title** Canonicalizer 단계의 정보 소실은 0건이다
**Evidence** 응답 가능 5,000건 전건이 Layer 2를 통과(CONVERT 3,700 · PASS 1,300 · DROP 0)
**Trace** CANONICALIZER_TRACE · `e2e_stage_trace.csv` s2 컬럼
**Observation** 없음
**Conclusion** 이 계층은 이름 정규화만 수행하며 값을 버리지 않는다.

## F-005

**Title** Generator 소스 부재가 소비자 응답 불가로 전파된다
**Evidence** Layer 0 `NO_GENERATOR_SOURCE` 2,011건 → Layer 1 `NOT_ANSWERABLE` 11,400건
**Trace** `UNIVERSE_1000.json` absent_axes · `e2e_stage_trace.csv` status=NOT_ANSWERABLE
**Observation** A12
**Conclusion** Layer 1 소실의 선행 조건은 Layer 0의 소스 부재다. 두 수치의 배율 차이는 질문 44종이 회사당 반복 적용되기 때문이다.

## F-006

**Title** Consumer→Repository 완주 경로는 `worker_count` 1종이다
**Evidence** 추적 16,400행 중 status=SUPPORTED 1,000행, 전부 `worker_count`
**Trace** RESULT_TRACE · `e2e_summary.json` runtime_reached_fields
**Observation** A5
**Conclusion** Layer 1→6 전달률 6.1%이며, 도달한 유일한 필드는 회사속성인 근로자 수다. 해당 필드는 Presence-only로 판정된다.

## F-007

**Title** Layer 5(Repository) 단계 소실이 0인 것은 선행 단계의 어휘 축소 결과다
**Evidence** Adapter emit 21종 중 Repository 교집합 12종. Layer 3 통과분이 이미 12종 이내로 축소됨
**Trace** 02_VOCABULARY_ANALYSIS · 03_INFORMATION_LOSS_ANALYSIS
**Observation** 없음
**Conclusion** Layer 5 소실 0은 Repository의 완전성을 의미하지 않는다.

## F-008

**Title** 14개 Observation은 5개 Root Cause로 수렴한다
**Evidence** RC-1 Vocabulary(A2·A3·A4·A11·A14) · RC-2 Question(A6·A7·A9·A10) · RC-3 Adapter(A1·A8·A13) · RC-4 Source(A12) · RC-5 Runtime(A5)
**Trace** 05_ROOT_CAUSE_ANALYSIS
**Observation** A1~A14 전건
**Conclusion** 독립 결함 14건이 아니라 구조 5종의 발현이다. RC-1은 Layer 내부 규칙이 아니라 Layer 간 경계의 체계 불일치에 해당한다.

## F-009

**Title** Observation 4건은 본 E2E 경로에서 발화하지 않았으나 어휘 대조에서는 성립한다
**Evidence** A2·A3·A4·A9의 대상 필드가 Layer 1에서 `NOT_ANSWERABLE`로 단절되어 Adapter·Repository 단계에 도달하지 못함
**Trace** 06_OBSERVATION_VALIDATION
**Observation** A2 · A3 · A4 · A9
**Conclusion** 미발화는 해소를 의미하지 않는다. 선행 단계 단절로 관측 기회가 발생하지 않은 상태다.
