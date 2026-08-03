# WO-TRACK-B-001 — 입력모델 요구사항 분류 (8건 BACKLOG, 설계·구현 없음)

## 대상 8건
- 기존 NO_VALID_FIELD 6: 근로기준법56·60(1)·60(2)·75, 응급의료8, 산안665
- Track A REJECTED 2: 산안49(높이2m), 산안187(2m 화물차)

## STEP2 요구 분류
| 분류 | 건수 | 항목 |
|---|---|---|
| NEW_BOOLEAN | 5 | 근기56, 근기75, 산안665, 산안49, 산안187 |
| INPUT_MODEL_CHANGE | 3 | 근기60(1), 근기60(2), 응급의료8 |
| NEW_NUMERIC | 0 | - |
| NEW_ENUM | 0 | - |

## STEP3 부족 원인
| 원인 | 건수 | 항목 |
|---|---|---|
| 근로정책 입력 부족 | 4 | 근기56·60(1)·60(2)·75 |
| Hazard 입력 부족 | 2 | 산안665(5kg 인력), 산안49(높이2m) |
| 작업환경 입력 부족 | 1 | 산안187(화물차 상하차) |
| 도메인 확장 필요 | 1 | 응급의료8 |

## STEP4 영향 범위 (구현 방법 미기재, 영향 유무만)
8건 전부 Engine·Repository·Runtime·UI에 영향(Y). 신규 입력 수용을 위해 4계층 모두 변경 필요 대상.
- 특히 응급의료8: OSH 사업장 모델과 다른 도메인 → 영향 범위 가장 큼(도메인 확장).
- 근기 4건: 상시적용 근로권리 → 단일 boolean로 표현 애매(60(1)/60(2)는 INPUT_MODEL_CHANGE).

## 핵심 관찰
- 근로기준법 4건은 hazard가 아닌 **사업장 운영/근로정책** → 현재 hazard 기반 입력모델에 없는 것이 자연스러운 결과.
- 이는 단순 mapped_field 수정이 아니라 **입력모델 범위 결정** 이슈(설계 대상).

## STEP6 최종 등록
8건 모두 **BACKLOG_CONFIRMED**. 본 WO에서 신규 필드 설계·구현 제안·DB/Runtime 변경 없음.

## 종료 후 상태
- Track A: CONFIRMED_TARGET_FIELD 1(산안524→has_diving) / REJECTED 2
- Track B: BACKLOG_CONFIRMED 8
- 다음: WO-CHG-MAPFIELD-001 대상 = **산안524 1건만** (Track B 완료로 입력모델 부족 범위 공식 확정됨)
