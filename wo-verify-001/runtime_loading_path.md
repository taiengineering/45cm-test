# WO-VERIFY-001 — Runtime Loading Path (읽기 경로 사실 확정)

증거원: 45cminc/leg (default branch main) 코드·infra 문서 read-only. /rtm/evaluate 경로 한정. 추측·RCA·해결책 없음.

## STEP1 — 현재 Runtime Provenance (재확인)
release=SEMREPO-RC1-2026.07.20 · freeze=15cd17e871b6885d34214c84a58adf47 · repository_size=337. (WO-RELOAD-001 실측)

## STEP2 — Loading Source (증거)
| 항목 | 값 | 증거 |
|---|---|---|
| 종류 | DATABASE (Postgres, psycopg2) | api/rtm_router.py `_fetch_rows()` |
| 접속 env | `SUPABASE_DB_URL` or `RTM_DATABASE_URL` | rtm_router.py: `dsn = os.environ.get("SUPABASE_DB_URL") or os.environ.get("RTM_DATABASE_URL")` |
| 쿼리 | `SELECT ... FROM public.production_semantic_repository ORDER BY atom_id` | rtm_engine/rtm/production_repository.py `PRODUCTION_QUERY` |
| 읽기 성격 | 읽기 전용 SELECT (SELECT ONLY) | production_repository.py 주석·쿼리 |
| 메모리 캐시 | 모듈 전역 `_engine` 1개에 보관 | rtm_router.py `_engine = None` + `_get_engine()` |
| provenance 산출 | 보관된 repository.provenance에서 생성 | rtm/engine.py `_provenance()` |

※ 부수 관찰(사실): _fetch_rows는 `SUPABASE_DB_URL`/`RTM_DATABASE_URL`을 쓰고, infra/deployment/env.contract.md는 `LEG_DATABASE_URL`을, api/runtime_service.py(별개 /evaluate 경로)는 `DATABASE_URL`을 쓴다 — 코드베이스에 3개 env 변수명이 병존. (해석·원인판단은 하지 않음.)

## STEP3 — 읽는 시점 (증거)
**BOOT / 프로세스 수명 캐시 (lazy singleton).**
- rtm_router.py: `_engine`은 모듈 전역. `_get_engine()`은 `if _engine is None:`일 때만 `RuntimeMatchingEngine.from_production(_fetch_rows, strict_baseline=True)`를 호출.
- rtm/engine.py: `from_production`은 `load_production_repository(fetch_rows)`를 호출해 저장소를 생성 시 1회 적재, 인스턴스에 보관.
- 결과: DB SELECT는 **프로세스당 1회**(최초 `/rtm/*` 요청 시) 실행되고, 이후 요청은 메모리의 `_engine`을 재사용한다. **요청마다 DB를 다시 읽지 않는다.**
- 판정 시점: 저장소 적재 시점 = 최초 요청(프로세스 기동 후 첫 호출). Background/주기적 재적재 코드는 관찰되지 않음.

## STEP3-보강 — 적재기 무결성 게이트 (사실, 코드에 존재)
production_repository.py `load_production_repository(strict_baseline=True)`는 하드코딩 상수와 대조하여 불일치 시 `ProductionRepositoryError`를 발생시킨다:
- `EXPECTED_ROW_COUNT=337`, `EXPECTED_FREEZE=15cd17e8...`, `EXPECTED_RELEASE=SEMREPO-RC1-2026.07.20`, `EXPECTED_IDSET=15cd17e8...`.
- freeze/release가 상수와 다른 행이 있으면 "freeze/release 불일치 행 …(기준선 미일치 배포)"로 raise.
(코드에 존재하는 사실만 기록 — 이 게이트가 특정 현상의 원인이라는 판단은 하지 않음.)

## STEP4 — Repository ↔ Runtime Source 동일성
| 대상 | 판정 | 근거 |
|---|---|---|
| 테이블 | **SAME** | 런타임 쿼리 대상 = `public.production_semantic_repository` = WO-CHG-010B UPDATE 대상 테이블 |
| DB 인스턴스 | **SAME (문서 기준)** | infra/db/database.md: LEG 런타임 DB = leg-prod, Ref=`wrfcedzgdrfupenzqhur` (대표 승인 2026-06-11) = 우리가 UPDATE한 DB ref |
| 라이브 env 값 | **UNVERIFIED** | `SUPABASE_DB_URL`/`RTM_DATABASE_URL`의 실제 런타임 값은 Railway 시크릿으로 repo/문서에 없음. 문서상 DB는 wrfcedzgdrfupenzqhur이나, 라이브 env가 정확히 그 ref를 가리키는지는 본 WO에서 미확인. |

종합: 런타임이 읽는 테이블·문서상 DB는 우리가 교정한 것과 동일(SAME). 유일한 미확인 링크는 라이브 env 시크릿 값 1건.
