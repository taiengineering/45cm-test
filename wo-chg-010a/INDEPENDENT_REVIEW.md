# WO-CHG-010A — Independent Review (STEP7-8) [rev.1 보완]

| check | result |
|---|---|
| Repository Success와 Runtime Success를 혼동했는가? | NO — 별개 기준. 특히 Runtime은 실제 /rtm/evaluate 출력 기준이며, Repository만 바뀌고 Runtime 출력 동일 시 FAIL로 명시(보완 #1) |
| Metadata 변경을 Semantic 변경처럼 확대 해석했는가? | NO — Semantic=NOT_TARGET, drift 0은 가드레일로만 |
| 불필요한 Regression을 추가했는가? | NO — Repository/Runtime/Regression(300)/Freeze 4개만. Compiler/Rule/Pattern 재도출 제외 |
| Regression 허용 변화가 명확한가? | YES — law_name/release/freeze/provenance 4개만 허용, 그 외 전부 FAIL(보완 #2) |
| Rollback 기준이 있는가? | YES — mismatch 잔존/obligation count/evidence/article/firing/determinism 변화 시 즉시 Rollback(보완 #3) |
| 신규 분석/DB 쓰기? | NO — 기존 WO 인용만, UPDATE/DB/Runtime/Freeze 변경 0 |
| 변경 범위 확정? | YES — law_name 325 blank-only, 비영향 컬럼 명시 |

## 보완 반영 (Operator 검토 3건)
1. Runtime Success = 실제 /rtm/evaluate 출력 기준, Repository 종속 아님, 미반영 시 FAIL — 반영.
2. Regression 허용 변화 = law_name/release/freeze/provenance 고정, 그 외 FAIL — 반영.
3. Rollback 조건 신설(mismatch/obligation/evidence/article/firing/determinism) — 반영.

## STEP8 최종 판정: READY_FOR_APPLY
성공 기준·범위·검증계획·허용변화·Rollback 기준 고정 완료. 실제 UPDATE와 후속 검증은 다음 WO에서만 수행.
