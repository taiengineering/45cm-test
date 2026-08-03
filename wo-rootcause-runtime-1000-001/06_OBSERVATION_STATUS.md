# 06 OBSERVATION_STATUS — WO-ROOTCAUSE-RUNTIME-1000-001

OBS-A1~A14를 **Runtime Baseline 실측으로 재판정**한다. 기존 Pattern 문구는 수정하지 않고 **상태만** 부여한다.

| ID | 기존 내용(요약, 수정 없음) | 상태 | Runtime 증거 |
|---|---|---|---|
| **A1** 공정·설비 목록 미평탄화 | Adapter가 `process_list`·`equipment_list`를 계약에 싣지 않음 | **CONFIRMED** | `request_payload.facility` 키 실측: `sector`·`worker_count`·`ksic_code`만. 목록 필드 전송 0건 |
| **A2** Adapter 필드명 ≠ 저장소 필드명 | `has_tower_crane`↔`has_crane` 등 | **NOT_TRIGGERED** | 해당 필드가 전송되지 않아 Runtime이 평가할 기회 없음. `missing_fields`에 `has_crane` 포함 |
| **A3** `elevator_count`↔`has_elevator` 형식 불일치 | number↔boolean | **NOT_TRIGGERED** | `has_elevator`가 `missing_fields`에 포함, `elevator_count`는 전송 0건 |
| **A4** `has_gas`→`has_high_pressure_gas` 강제 치환 | synonym | **NOT_TRIGGERED** | 두 필드 모두 `missing_fields`. 전송 0건 |
| **A5** Presence-only (임계 부재, 값 크기 무관) | — | **CONTRADICTED** | `worker_count>=50`에서만 발화. 경계 위반 0건. 별도 문서 08 참조 |
| **A6** 제조 설비·작업 질문 `is_active=false` | — | **PARTIAL** | Runtime `missing_fields`에 `has_crane`·`has_press`·`has_forklift`·`has_conveyor`·`has_dust_work`·`has_pressure_vessel` 등 포함 확인. 다만 본 실행의 미공급 원인은 Universe 소스 부재(A12)와 중첩되어 질문 비활성 단독 효과는 분리 불가 |
| **A7** 건설 공종 질문 `is_active=false` | — | **PARTIAL** | 동일. `has_excavation`·`has_scaffold`·`has_pile_work`·`has_concrete_work`·`has_steel_frame` 전건 `missing_fields` |
| **A8** 수치·텍스트 계약 미적재 | `total_floor_area` 등 | **CONFIRMED** | `total_floor_area`가 1,000건 전건 `missing_fields`. Universe는 전건 값을 보유하나 전송 0건 |
| **A9** 소방 3종 `mapped_field` 부재 | `has_sprinkler`·`has_fire_hydrant`·`has_smoke_control` | **CONFIRMED** | Runtime 계약 39종(`missing`38+`active`1)에 3종 모두 **부재**. Repository 어휘 자체에 없음이 Runtime 응답으로 확인됨 |
| **A10** 건물 관리·법정검사 축 부재 | — | **CONFIRMED** | Runtime 계약 39종에 점검·검사·관리주체 항목 없음 |
| **A11** SoT 어휘 ↔ 판정 어휘 변환 경로 없음 | — | **CONFIRMED** | Universe SoT 설비 62·공정 119·작업 215가 Runtime 계약 39종과 교집합 0. 전송 0건 |
| **A12** NOT_ANSWERABLE | 질문은 있으나 답할 데이터 없음 | **CONFIRMED** | 활성 질문 16,400 대비 Runtime 도달 질문 필드 1,000 |
| **A13** Adapter 소실률 | — | **PARTIAL** | 본 실행의 Adapter 전송은 2,500키. 이전 추정치(응답가능 5,000 중 4,000 소실)와 모수가 달라 비율 직접 비교 불가. Runtime 기준 실측은 문서 05 |
| **A14** 어휘 체계 3종 분기 | SoT 396 / Question 99 / Repository 39 | **CONFIRMED** | Runtime `missing`38+`active`1 = 39종이 Repository `mapped_field` 39종과 **차집합 양방향 0**. `sector`·`ksic_code`는 `unknown_fields` |

## 상태 집계

| 상태 | 건수 | ID |
|---|---|---|
| CONFIRMED | **7** | A1 · A8 · A9 · A10 · A11 · A12 · A14 |
| PARTIAL | **3** | A6 · A7 · A13 |
| NOT_TRIGGERED | **3** | A2 · A3 · A4 |
| **CONTRADICTED** | **1** | **A5** |

`NOT_TRIGGERED`는 해소를 의미하지 않는다. 해당 필드가 Runtime에 전송되지 않아 평가 기회가 발생하지 않은 상태이며, Runtime은 이들을 `missing_fields`로 반환했다.
