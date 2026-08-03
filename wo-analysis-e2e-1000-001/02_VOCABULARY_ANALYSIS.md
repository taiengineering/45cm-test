# 02 VOCABULARY_ANALYSIS — WO-ANALYSIS-E2E-1000-001

## 계층별 Vocabulary 규모 (실측)

| Layer | Vocabulary | 규모 |
|---|---|---|
| Universe (SoT) | `facility_name_std` | **62** |
| Universe (SoT) | `process_path` | **119** |
| Universe (SoT) | `kcsc_work_master.title` | **215** |
| Question | `diagnosis_input_fields` is_active=true | **44** |
| Question | is_active=false | 55 |
| Canonicalizer | ALIASES canonical key | **13** |
| Adapter | Input Contract 적재 키 | **21** |
| Repository | `mapped_field` | **39** |

## 교집합 행렬

| 비교 | 교집합 | 좌측 전용 | 우측 전용 |
|---|---|---|---|
| **SoT 설비 ∩ Question** | **0** | 62 | 44 |
| **SoT 공정 ∩ Question** | **0** | 119 | 44 |
| **SoT 작업 ∩ Question** | **0** | 215 | 44 |
| **SoT 설비 ∩ Repository** | **0** | 62 | 39 |
| Question ∩ Canonical | 10 | 34 | 3 |
| Question ∩ Adapter emit | 19 | 25 | 2 |
| Adapter emit ∩ Repository | 12 | 9 | 27 |
| Question ∩ Repository | 14 | 30 | 25 |
| Question(inactive) ∩ Repository | **27** | 28 | 12 |

## 유형 분류

| 유형 | 사례 | 건수 |
|---|---|---|
| **동일 Vocabulary** | `worker_count`·`has_boiler`·`has_gas`·`has_diving` 등 | 12 (Adapter∩Repo) |
| **Alias** | `workers→worker_count`, `floor_area→total_floor_area`, `contract_eok→project_amount` | 13 canonical key |
| **Rename** | `has_tower_crane→has_crane`, `has_asbestos_demo→has_asbestos`, `has_chemical_substance→has_chemical` | 3 |
| **강제 치환** | `has_gas→has_high_pressure_gas` (FIELD_CODE_SYNONYMS) | 1 |
| **형식 불일치** | `elevator_count`(number) ↔ `has_elevator`(boolean) | 1 |
| **Missing (질문에 없음)** | Repository 39종 중 25종이 활성 질문에 부재 | 25 |
| **Unreachable (SoT↔판정)** | SoT 설비·공정·작업 396종 전량이 Question·Repository 어느 쪽과도 교집합 0 | 396 |
| **One-to-Many** | `equipment_list` 1필드 ↔ SoT 설비 62종 | 1:62 |
| **Many-to-One** | SoT 설비 다수 ↔ `has_*` 1개 (변환 코드 부재로 미실현) | — |

## Adapter가 계약에 싣지 않는 활성 질문 25종

`address` · `annual_energy_toe` · `boiler_capacity_kw` · `building_grade` · `building_use_type` · `construction_type` · `electric_capacity` · `elevator_count` · `equipment_list` · `floor_count` · `gas_capacity_kg` · `gas_capacity_m3` · `is_energy_intensive` · `is_multi_use` · `ksic_major` · `main_structure` · `multi_use_type` · `process_list` · `project_address` · `project_amount` · `subcontractor` · `subcontractor_count` · `total_floor_area` · `transformer_capacity_kva` · `water_tank_ton`

## 도달 가능 어휘 (Adapter emit ∩ Repository = 12)

`has_blasting` · `has_boiler` · `has_chemical` · `has_confined_space` · `has_diving` · `has_emergency_broadcast` · `has_emergency_gen` · `has_gas` · `has_hazmat_storage` · `has_high_pressure_gas` · `has_water_tank` · `worker_count`

## Repository 39종 중 활성 질문에 없는 25종

`has_asbestos` · `has_casting` · `has_concrete_work` · `has_conveyor` · `has_crane` · `has_demolition` · `has_dust_work` · `has_elevator` · `has_excavation` · `has_forklift` · `has_gondola` · `has_grinding` · `has_hazardous_material` · `has_high_place_work` · `has_noise_work` · `has_painting` · `has_pile_work` · `has_press` · `has_pressure_vessel` · `has_radiation` · `has_rolling` · `has_scaffold` · `has_steel_frame` · `has_subcontractor` · `has_welding`

이 중 **27종은 비활성 질문(`is_active=false`)에 존재한다**(Q_inactive ∩ Repository = 27).

## 구조적 사실

계층은 **세 개의 서로 다른 어휘 체계**를 쓴다.

```
SoT 어휘        396종  (facility_name_std · process_path · work title)   — 명칭 문자열
Question 어휘    99종  (active 44 + inactive 55)                          — field_code
Repository 어휘  39종  (mapped_field)                                     — field_code
```

SoT 어휘와 나머지 둘 사이의 교집합은 **0**이다. Question 어휘와 Repository 어휘는 부분 교집합(active 14 · inactive 27)을 갖는다.
