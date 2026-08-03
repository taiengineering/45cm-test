# WO-CHG-READINESS-001 STEP3 — 변경 델타 예측 (Prediction, 변경 없이)

## Baseline (현재, rtm_out3 = has_diving 포함 FULL payload)
- 발화 atom 총계: **328**
- 산안524(5b849b3e) 발화 여부: **미발화** (worker_count-mapped라 발화 안 함)
- has_diving 계열: 현재 발화 집합에 포함(정상 발화 중)

## 예측 델타 (worker_count → has_diving 변경 시)
| 항목 | 현재 | 변경 후(예측) | 델타 |
|---|---|---|---|
| 산안524 발화 | 미발화 | **발화**(has_diving=true 시) | +1 |
| 발화 atom 총계 | 328 | **329** | +1 |
| has_diving 기존 25건 | 발화 | 발화(불변) | 0 |
| 나머지 336행 | - | byte-identical | 0 |
| worker_count 집합 | 9 | 8 (산안524 이탈) | -1 (BACKLOG 8건은 그대로 미발화) |

## 예측 근거
- UPDATE가 1행만 수정 → 다른 atom의 발화 조건 불변.
- 산안524 law_name은 wrfced에서 이미 정답(산업안전보건기준에 관한 규칙, art524) → 발화 시 올바른 값 출력.
- has_diving 트리거로 전환되므로 has_diving=true 입력에서 신규 발화 예상.

## 미확인 (명시)
- 실제 '산안524 신규 발화 + has_diving 계열 무변화'의 **런타임 관측은 변경 없이는 불가** → CHG post-apply 단계로 이관.
