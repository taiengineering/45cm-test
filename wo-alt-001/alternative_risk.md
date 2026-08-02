# WO-ALT-001 STEP4(위험) — Risk Register

| 전략 | 주요 위험 | 완화(관찰, 수정안 아님) |
|---|---|---|
| S1 Backfill(325) | (a) 새 freeze 미발급 시 provenance 불일치 (b) 동시성 중 공란조건 변동 (c) numeric 10행 라벨 채움의 의미 | blank-only 조건부·freeze 규칙·numeric은 firing 무관(관찰) |
| S2 Backfill(23) | 컬럼 부분 정합->향후 재작업 유발, 전수 원칙 위배 | — |
| S3 Regeneration | build 소스 미특정 시 실행 불가(BLOCKED), 타 컬럼(evidence/article) 변동, 300 재검증 실패 리스크 | 소스 확보 선행 필요 |
| S4 Runtime Resolver | serving 소스 미특정(BLOCKED), 런타임 로직 회귀, 조인 성능/동작 변화, 12 short-form vs full 조인 불일치 노출 | 소스 확보·회귀 검증 선행 |
| S5 Presentation | SoT·runtime 오류 잔존, 표시-데이터 이중 진실원, UI 소스 필요 | — |
| S6 No Change | 법령명 오인용 지속(36.3% 프로파일), 법적 인용 신뢰도 | — |

공통: repo 변경 계열(S1/S3)은 freeze 갱신 필수. 런타임 계열(S4/S5)은 serving 소스 특정이 선행 BLOCKER.
