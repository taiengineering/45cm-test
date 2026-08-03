# WO-CHG-MAPFIELD-001 STEP5~7 — Runtime 검증

## STEP5 leg-runtime 재배포 (Operator)
- service = leg-runtime, startup 정상(Application startup complete, Uvicorn 0.0.0.0:8080), /health 200.
- repo_size 337 로드 확인.

## STEP6 Target Runtime Verify (has_diving=true FULL payload, rtm_chg.json)
| 항목 | 기대 | 실측 | 판정 |
|---|---|---|---|
| obligation_count | 329 | 329 | PASS |
| 산안524 신규 발화 | 발화 | 발화 | PASS |
| 산안524 law_name | 산업안전보건기준에 관한 규칙 | 동일 | PASS |
| 산안524 article | 524 | 524 | PASS |
| newly fired delta | {산안524}만 | 정확히 1건, 산안524 | PASS |
| dropped | 0 | 0 | PASS |
| 기존 328 보존 | base ⊆ now | True(전부 보존) | PASS |

baseline(pre-CHG rtm_out3) 328 → post-CHG 329, drift 0. 델타 = 산안524 1건 신규 발화만.

## STEP7 결정성
- Operator 결정: 이번 1회 obligation_count=329 결과로 갈음(A/B/C 3회 생략).
- 근거: obligation_count·atom set이 예측(328→329, 산안524만 추가)과 정확히 일치. 미확인으로 남기는 부분: 3회 반복 재현은 본 WO에서 실행하지 않음(Operator 판단).

## Runtime 검증: PASS
