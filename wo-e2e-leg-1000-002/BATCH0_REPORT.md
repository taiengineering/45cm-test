# WO-E2E-LEG-1000-002 · Batch 0 — 매트릭스 검토 요청

**Goal** G-mscro68p-fcf706 · **작성** Claude(Recorder) · **판정권자** Operator
**성격** 조사(Gap Discovery). PASS/FAIL 선언 없음. 엔진·Repository·코드 수정 0.

## 0. 근거 (전부 실측, 추정 0)

| 축 | 출처 |
|---|---|
| 소비자 질문 카탈로그 | taieng `public.diagnosis_input_fields` (sector·field_code·is_active) |
| Adapter 정규화 | tai-api `services/consumer_input_canonicalizer.py` ALIASES 13 |
| Adapter 동의어 치환 | tai-api `constants/exists_mvp_fields.py` FIELD_CODE_SYNONYMS |
| Contract 조립 | tai-api `services/input_contract_builder.py` |
| Runtime 저장소 | leg-prod `public.production_semantic_repository` 337 atom / mapped_field 39 / freeze 15cd17e8 |

## 1. 승인 조건 대비

| 조건 | 요구 | 실제 | 충족 |
|---|---|---|---|
| 제조 업종 아키타입 | ≥22 | **24** | O |
| 건설 프로젝트 유형 | ≥9 | **10** | O |
| 건설 공종 | ≥15 | **16** | O |
| 건축물 용도 | ≥10 | **10** | O |
| 공정↔설비 모순 | 0 | **0** | O |
| 설비↔작업 모순 | 0 | **0** | O |
| 규모 불일치 | 0 | **0** | O |
| 소비자 입력 누락 | 0 | **0** | O |
| Adapter 상태 미기재 | 0 | **0** (2,464건 전건 기재) | O |

매트릭스 행: 제조 78 · 건설 30 · 건축물 29 = 137행(규모대/금액대 전개 포함).

초안 1차 생성 시 Gate가 27건 모순을 적발했고(천장크레인 공정 근거 부재, 소규모 사업장 대형설비, 폐수처리설비 공정 미귀속 등) 전건 교정 후 0이 되었다. 교정 방식은 ① 운반·보관/유틸리티/환경처리 공정 신설 ② 규모 미달 보조설비 자동 제외(제외분은 `equipment_dropped_by_scale`에 기록) ③ 규모별 위험작업 필터(`hazard_dropped_by_scale`에 기록).

## 2. Adapter 관찰 결과 (소비자 입력 2,464건)

| 상태 | 건수 | 비율 |
|---|---|---|
| SUPPORTED | 451 | 18.3% |
| NAME_MISMATCH | 151 | 6.1% |
| PASSTHROUGH_ONLY | 1,112 | 45.1% |
| UNSUPPORTED | 750 | 30.4% |

**소비자가 말하는 것의 75.5%가 Runtime 판정에 도달하지 못한다**(PASSTHROUGH+UNSUPPORTED).

## 3. 확정 Pattern (OBS-A1~A7) — 회사별 중복 생성 금지, occurrence만 기록

| ID | Pattern | 근거 | occurrence |
|---|---|---|---|
| OBS-A1 | 공정·설비 목록이 has_*로 평탄화되지 않음 | canonicalize는 통과만, contract_builder는 has_*만 읽음 | process_list 108 · equipment_list 78 |
| OBS-A2 | Adapter 필드명 ≠ 저장소 필드명 | has_chemical_substance↔has_chemical, has_tower_crane↔has_crane, has_asbestos_demo↔has_asbestos | 105 |
| OBS-A3 | 승강기를 대수(number)로만 묻고 has_elevator(boolean, 19 atom)로 변환 없음 | diagnosis_input_fields.elevator_count | 29 |
| OBS-A4 | has_gas → has_high_pressure_gas 강제 치환 | FIELD_CODE_SYNONYMS | 17 |
| OBS-A5 | 수치 입력 전부 발화 무영향(Presence-only) | 저장소에 임계 컬럼 부재 | worker_count 137 · total_floor_area 107 |
| OBS-A6 | 제조 설비·작업 질문이 카탈로그에 있으나 is_active=false | has_crane·has_press·has_forklift·has_conveyor·has_dust_work·has_pressure_vessel 등 | 272 |
| OBS-A7 | 건설 핵심 공종 질문이 is_active=false | has_excavation(23 atom)·has_scaffold(18)·has_pile_work(14)·has_concrete_work(13)·has_steel_frame(4) = 72 atom 미도달 | 285 |

## 4. 주요 미도달 항목 (상위)

- 제조: has_forklift(62) · has_confined_space(61) · has_conveyor(39) · has_crane(34) · has_dust_work(28) · has_pressure_vessel(17)
- 건설: has_temp_electric(30) · max_work_height(30) · 화기작업(30) · has_excavation/excavation_depth(27+27) · has_scaffold(27) · has_concrete_work(27) · has_pile_work(24) · 흙막이(15)
- 건축물: 정화조(29) · 중앙공조(29) · 유지관리작업(29) · 고소작업(29) · 냉동기(20) · 기계식주차(20) · 의료가스(3) · 에스컬레이터(2)
- 소방설비 4종 중 저장소 도달은 has_emergency_broadcast 1종뿐. 스프링클러·소화전·제연은 질문하나 mapped_field 없음.

## 5. 산출물

`matrix_manufacturing.csv` · `matrix_construction.csv` · `matrix_building.csv` · `field_status.json` · `batch0_gate.json` · 생성기(`catalog.py`·`mfg.py`·`con.py`·`bld.py`·`build.py`)

## 6. Batch 1 이후 (승인 후)

50건 생성 → 50건 현실성 전수 정독 → INVALID 재생성 → Operator 승인 → 다음 Batch.
1,000건 완성 전 Runtime 실행 없음.
