# 06 OBSERVATION_VALIDATION — WO-ANALYSIS-E2E-1000-001

OBS-A1~A13 전건에 대해 **어떤 Trace에서 재현되는지**를 증명한다. 신규 Observation은 A14부터.

| ID | 재현 Trace | 증거 | 본 E2E 재현 |
|---|---|---|---|
| **A1** 공정·설비 목록 미평탄화 | `e2e_stage_trace.csv` field=`process_list`·`equipment_list`, s2=CONVERT · s3=DROP | Canonicalizer 통과 후 Adapter에서 계약 미적재 | **재현 1,300건** |
| **A2** Adapter 필드명 ≠ 저장소 필드명 | 어휘 교집합 — `has_tower_crane`·`has_asbestos_demo`·`has_chemical_substance`가 Repository 39종에 부재 | `vocabulary_sets.json` | **미발화** (해당 필드가 L1에서 NOT_ANSWERABLE) |
| **A3** `elevator_count`(number) ↔ `has_elevator`(boolean) | Question active에 `elevator_count` 존재, Repository에 `has_elevator` 존재, 변환 코드 부재 | 어휘 교집합 | **미발화** (L1 NOT_ANSWERABLE 700건) |
| **A4** `has_gas`→`has_high_pressure_gas` 강제 치환 | `constants/exists_mvp_fields.py` FIELD_CODE_SYNONYMS | 코드 상수 | **미발화** (L1 NOT_ANSWERABLE 500건) |
| **A5** Presence-only | Repository에 임계 컬럼 부재, `worker_count` 8 atom 매칭 | RUNTIME_TRACE | **재현 1,000건** |
| **A6** 제조 설비·작업 질문 `is_active=false` | Q_inactive ∩ Repository = 27종 | `diagnosis_input_fields` | **간접 재현** (Repository 25종이 활성 질문에 부재) |
| **A7** 건설 공종 질문 `is_active=false` | `has_excavation`·`has_scaffold`·`has_pile_work`·`has_concrete_work`·`has_steel_frame`가 활성 질문 밖 | 어휘 교집합 | **간접 재현** |
| **A8** 수치·텍스트 계약 미적재 | Adapter DROP 25종 목록 | `input_contract_builder.py` | **재현 2,700건** |
| **A9** 소방 3종 `mapped_field` 부재 | `has_sprinkler`·`has_fire_hydrant`·`has_smoke_control`가 Repository 39종에 부재 | 어휘 교집합 | **미발화** (건축물 L1 NOT_ANSWERABLE) |
| **A10** 건물 관리·법정검사 축 부재 | 활성 질문에 점검·검사·관리주체 항목 없음 | `diagnosis_input_fields` BUILDING | **재현** (Universe 건축물 200사 전건 축 부재) |
| **A11** SoT 어휘 ↔ 판정 어휘 변환 경로 없음 | SoT 396종 ∩ (Question 44 ∪ Repository 39) = **0** | `vocabulary_sets.json` | **재현 1,000사 전건** |
| **A12** NOT_ANSWERABLE | 활성 질문 중 11,400건 응답 불가 | `e2e_stage_trace.csv` status=NOT_ANSWERABLE | **재현 11,400건** |
| **A13** Adapter 소실률 80% | 응답 가능 5,000 중 DROP 4,000 | ADAPTER_TRACE | **재현** |

## 재현 상태 요약

| 상태 | ID | 건수 |
|---|---|---|
| 본 E2E에서 직접 재현 | A1 · A5 · A8 · A10 · A11 · A12 · A13 | 7 |
| 어휘 대조로 간접 재현 | A6 · A7 | 2 |
| 미발화 (선행 단계 단절로 도달 못 함) | A2 · A3 · A4 · A9 | 4 |

**"미발화"는 해당 Observation이 해소되었다는 뜻이 아니다.** 해당 필드가 Layer 1에서 `NOT_ANSWERABLE`로 끊겨 Adapter·Repository 단계에 도달하지 못했기 때문이며, 어휘 대조에서는 여전히 성립한다.

## 신규 Observation

**OBS-A14 · 계층별 어휘 체계가 3종으로 분기하며 SoT 축과의 교집합이 0이다**

| 항목 | 값 |
|---|---|
| 발견 위치 | Universe(Layer 0) ↔ Question(Layer 1) ↔ Repository(Layer 5) 경계 |
| 증상 | SoT 어휘 396종(설비 62·공정 119·작업 215), Question 어휘 99종, Repository 어휘 39종. SoT ∩ Question = 0, SoT ∩ Repository = 0. Question ∩ Repository = 41(active 14 + inactive 27) |
| 재현 여부 | 재현됨 (1,000사 전건, `vocabulary_sets.json`) |
| 상태 | OBSERVED — 원인분석·해결책 없음 |

A11이 "변환 경로 없음"을 관측한 것이라면, A14는 **어휘 체계 자체가 3개로 분기해 있다**는 구조를 관측한 것이다.
