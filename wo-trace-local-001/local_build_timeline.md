# WO-TRACE-LOCAL-001 — Local Build Timeline (증거 대조)

| 시각 (UTC) | 이벤트 | 증거원 | 성격 |
|---|---|---|---|
| 2026-07-04 | 원천 법령 26테이블(397,509행) TAIENG→LEG-PROD 이관 (postgres_fdw + migration) | LEG_Immutable_Data_Copy_Report.md | **337 아님** (원천 law 테이블) |
| 2026-07-16 | tai-api main 마지막 커밋(공백 시작) | tai-api git | — |
| **2026-07-20 08:58~11:21** | **production_semantic_repository 337행 8배치 적재(loaded_at)** | 런타임 DB 메타(VERIFY-003) | **337 적재 — DB 효과 확정** |
| 2026-07-20 | tai-api 커밋 **0건** (공백 구간 내) | tai-api git | 생성 실행이 커밋으로 안 남음 |
| 2026-07-25 11:15 | 마이그레이션 exe001_m07 (CREATE TABLE IF NOT EXISTS, DDL only) | supabase_migrations(VERIFY-003) | 스키마 사후 등록 |
| 2026-07-30 | tai-api 커밋 재개 (공백 종료) | tai-api git | — |
| 2026-07-30 23:32 | WO-E2E-RUNNER-001 실행(진단결과 스냅샷) | uploads/run_log.json | **337과 무관** |

## 핵심
- 337 적재일(07-20)은 tai-api 커밋 공백(07-16→07-30) 한가운데 → **생성 실행의 Git 흔적 없음**.
- 07-04 이관·07-25 마이그레이션은 각각 원천 law 복사·스키마 등록으로 **337 생성 자체와 다름**.
- 로컬 실행 기록(shell/cursor/terminal)은 Claude 미접근.
