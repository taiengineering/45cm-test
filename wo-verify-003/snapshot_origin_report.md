# WO-VERIFY-003 — RC1 Snapshot Origin Report

목적: SEMREPO-RC1(public.production_semantic_repository, 337)의 생성 출처를 운영 흔적(메타데이터·DB 이력·마이그레이션)으로 확정. 코드 재검색 없음.

## STEP2·3 — DB 내부 생성 흔적 탐색
런타임 DB(wrfcedzgdrfupenzqhur) 전 스키마에서 history/audit/release/snapshot/operation/job/pipeline-log 테이블 조회:
- **전용 이력/audit/release/snapshot/operation/job 테이블 없음** (앱 레벨). 존재하는 것은 Supabase 내부(auth.audit_log_entries, auth/realtime/storage/supabase_migrations schema_migrations)뿐.
- 유일한 앱 관련 이력 = **supabase_migrations.schema_migrations** (20건).

### 마이그레이션 이력 중 RC1 관련
전 마이그레이션 statement에서 production_semantic_repository / SEMREPO / freeze_signature / release_version 검색 → **단 1건 매치**:
- **20260725111515 `exe001_m07_create_output_repository`** — statement는 **DDL 전용 1개**:
  - `CREATE TABLE IF NOT EXISTS public.production_semantic_repository (...)`
  - `COMMENT ON TABLE ... IS 'LEG Output Repository (M-07 migration from tai-api, AC-001 §3). RC1 SEMREPO-RC1-2026.07.20, freeze 15cd17e8. LEG-owned authoritative store.'`
  - **INSERT/데이터 없음. freeze/release 값 세팅 없음(컬럼 정의만).**
- 337행을 INSERT 하는 마이그레이션은 **존재하지 않음**.

## STEP4 — 시점 대조 (핵심)
| 이벤트 | 시각 | 성격 |
|---|---|---|
| **데이터 적재(loaded_at)** | 2026-07-20 08:58~11:21 | 337행, 8배치 INSERT |
| **테이블 스키마 마이그레이션** | 2026-07-25 (exe001_m07) | CREATE TABLE IF NOT EXISTS (멱등), 데이터 없음 |

- 마이그레이션(07-25)이 데이터 적재(07-20)보다 **5일 늦음** + `IF NOT EXISTS` + INSERT 없음.
- 따라서 **데이터 337행은 이 마이그레이션이 생성한 것이 아님.** 마이그레이션은 이미 존재하던 테이블 스키마를 **사후에 마이그레이션 시스템에 등록·문서화**한 것(멱등 CREATE).

## STEP5 — 출처 분류 (증거만)
| 대상 | 출처 | 근거 |
|---|---|---|
| **테이블 스키마** | **Supabase Migration** (exe001_m07, 07-25, DDL-only) | schema_migrations 등록 |
| **데이터 337행** | **tai-api로부터의 데이터 이관(M-07), 07-20 배치 적재** | 테이블 COMMENT "M-07 migration from tai-api, AC-001 §3" + loaded_at 8배치(07-20) + repository_version SEMREPO-CAL022 |
| 적재 방식 | 페이지 단위 INSERT(8배치) — Supabase 마이그레이션 밖 | loaded_at 분포; 07-20 마이그레이션 부재 |
| 원천 DB | tai-api (COMMENT 명시; 프로젝트 vwlahtguyggrhvslabax) | COMMENT "from tai-api" |

**분류 결론:**
- "자동 생성(CI/Scheduler/Pipeline)" — 해당 흔적 없음.
- "Migration" — **스키마 한정**(exe001_m07). 데이터 아님.
- 데이터 = **tai-api → leg-prod 데이터 이관(M-07)**, 2026-07-20 배치 적재. Supabase 마이그레이션 시스템 밖의 적재 프로세스.

## 미기록 잔여 (사실)
- 07-20 배치 적재를 실행한 **정확한 스크립트/주체**는 DB 흔적에 없음(created_by/loaded_by 컬럼 부재, 전용 operation-log 테이블 부재). 원천·시점·방식(tai-api 이관, 07-20, 8배치)은 확정되나, 적재 도구의 식별자는 DB 흔적만으로는 미확정 → M-07 실행 리포트/운영 런북 영역(본 WO 범위 밖, Operator 판단).
