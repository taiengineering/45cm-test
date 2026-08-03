# OBSERVATION_DELTA — WO-E2E-CONSUMER-1000-001

Pattern Freeze 유지. `OBS-A1~A10`은 설명을 재기술하지 않고 occurrence만 갱신한다. 신규는 `OBS-A11`부터.

## 1. 기존 Pattern occurrence 갱신 (재기술 없음)

| Pattern | Layer | 본 WO occurrence |
|---|---|---|
| OBS-A1 공정·설비 목록 미평탄화 | Adapter | 1,300 (process_list 800 · equipment_list 500) |
| OBS-A8 수치·텍스트 계약 미적재 | Adapter | 2,700 (address·total_floor_area·ksic_major·construction_type·project_address·floor_count) |
| OBS-A5 Presence-only | Runtime | 1,000 (worker_count) |

`OBS-A2·A3·A4·A6·A7·A9·A10`은 본 WO 경로에서 발화하지 않았다(해당 필드가 `NOT_ANSWERABLE`로 앞단에서 끊김). occurrence 0.

## 2. 신규 Observation

### OBS-A11 · SoT 설비·공정 어휘와 판정 필드 어휘 사이에 변환 경로 없음

| 항목 | 값 |
|---|---|
| 발견 위치 | Adapter ↔ Repository 경계 |
| 증상 | Universe의 SoT 설비 어휘 62종(`facility_name_std`)·공정 어휘 119종(`process_path`)이 저장소 `mapped_field` 39종과 **일치 0건**. 명칭 체계가 다르며 변환 코드가 존재하지 않음 |
| 재현 여부 | 재현됨 (1,000사 전건) |
| 상태 | OBSERVED — 원인분석·판정하지 않음 |

### OBS-A12 · 질문은 존재하나 응답 데이터가 없는 상태(NOT_ANSWERABLE)

| 항목 | 값 |
|---|---|
| 발견 위치 | Consumer 응답 단계 |
| 증상 | 활성 질문 중 11,400건이 Universe에 답할 데이터가 없어 응답 불가. 상위: annual_energy_toe·electric_capacity·elevator_count·gas_capacity_kg·has_boiler·has_safety_manager 각 700 |
| 재현 여부 | 재현됨 |
| 상태 | OBSERVED |

`NOT_ASKED`(질문 자체가 없음)와 원인이 다르므로 상태값을 분리했다. 본 WO에서 신설.

### OBS-A13 · 이전 Universe 대비 Adapter 소실 비율 상승

| 항목 | 값 |
|---|---|
| 발견 위치 | Adapter |
| 증상 | 응답 가능 입력 5,000건 중 4,000건(80%)이 Adapter에서 소실. 이전 Generator-model Universe에서는 응답 가능 입력 중 Adapter 소실이 44.6%였음 |
| 재현 여부 | 재현됨 |
| 상태 | OBSERVED — 두 Universe는 입력 구성이 달라 직접 비교 대상이 아님. 비교값은 참고로만 기록하고 판정하지 않음 |

## 3. 상태값 대장 (현행)

| 상태 | 의미 | 도입 WO |
|---|---|---|
| SUPPORTED | 끝까지 도달 | — |
| NAME_MISMATCH | 명칭·형식 불일치로 소실 | — |
| PASSTHROUGH_ONLY | 수집되나 계약 미적재 또는 mapped_field 부재 | — |
| NOT_ASKED | 질문 자체가 없음 (INACTIVE / ABSENT) | Batch2 |
| **NOT_ANSWERABLE** | **질문은 있으나 답할 데이터 없음** | **본 WO** |
| NO_GENERATOR_SOURCE | Generator가 읽을 SoT 없음 (generator scope) | WO-UNIVERSE-GENERATOR-1000-001 |
| SOURCE_EXISTS_BUT_NOT_LINKED | 소스 row는 있으나 하위 연결 row 없음 | 〃 |
| N/A_NO_SOT_AXIS | 추적 대상 축 자체가 없음 | 〃 |

## 4. 준수 확인

Generator Asset·Universe·엔진·Repository·Question **수정 0**. 발견은 전부 Observation으로만 기록했고 원인분석·우선순위·개선안을 제시하지 않았다. 카운트에 근거한 PASS/FAIL 선언 없음.
