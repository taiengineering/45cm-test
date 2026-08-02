# WO-DEBUG-LOADER-001 — Loader Source Report

## 종료 조건 답 (코드 근거)
**"새로 기동한 leg-runtime는 정확히 무엇을 Loader 입력으로 사용하여 Repository를 구성하는가?"**

→ **Live Postgres DB를 psycopg2로 SELECT**하여 구성한다.
- 쿼리: `SELECT atom_id, mapped_field, semantic_clause_id, law_name, law_article, evidence, repository_version, release_version, freeze_signature FROM public.production_semantic_repository ORDER BY atom_id` (rtm_engine/rtm/production_repository.py :: PRODUCTION_QUERY)
- 연결 DSN: 환경변수 **`SUPABASE_DB_URL`(우선)** 또는 **`RTM_DATABASE_URL`(대체)** (api/rtm_router.py :: _fetch_rows)
- 반환 rows만으로 ProductionRepository를 만들고, 응답 provenance(release/freeze/repository_version/size)는 그 rows에서 파생.
- **embedded 파일/artifact/pickle/JSON/YAML/CSV/memory-snapshot fallback 경로는 loader 어디에도 없다.**

## STEP2 — Loader 입력 (증거로 기록, 추측 없음)
| 후보 | 판정 | 증거 |
|---|---|---|
| Supabase / production_semantic_repository | **YES (Live DB)** | PRODUCTION_QUERY → public.production_semantic_repository, psycopg2.connect |
| JSON / YAML / CSV | NO | loader 경로에 파일 읽기 없음 |
| embedded artifact / pickle / memory snapshot | NO | from_snapshot(path)는 존재하나 /rtm 경로는 from_production만 사용 |
| other | NO | — |

## STEP3 — Source 코드
| 항목 | 값 |
|---|---|
| 파일 | api/rtm_router.py · rtm_engine/rtm/engine.py · rtm_engine/rtm/production_repository.py |
| 함수 | _fetch_rows → RuntimeMatchingEngine.from_production → load_production_repository |
| 호출 위치 | rtm_router._get_engine() (최초 /rtm 요청) |
| 입력 객체 | fetch_rows 콜러블(=_fetch_rows); DSN=env SUPABASE_DB_URL||RTM_DATABASE_URL; PRODUCTION_QUERY |
| 반환 객체 | ProductionRepository(rows, provenance) — source="PRODUCTION_SEMANTIC_REPOSITORY" |

## STEP4 — Repository 생성 시점
- **lazy loading + process-global singleton**: rtm_router `_engine` 전역, `if _engine is None`이면 1회 생성.
- 최초 **/rtm 요청** 시 생성(서버 startup warmup은 LEGACY RuntimeService만 로드; RTM 엔진은 startup에서 안 만듦).
- 이후 프로세스 수명 동안 캐시(요청마다 재조회 아님).

## STEP5 — Runtime 사용 Repository 판정
**Live DB** (psycopg2 SELECT public.production_semantic_repository @ 엔진 init).
- Startup Snapshot: 아님 · Embedded Resource: 아님 · Generated Artifact: 아님 · Other: 아님.

## 코드로는 확정되지 않는 단일 변수 (사실 기록, 분석 아님)
- loader가 읽는 **물리 DB의 정체**는 DSN 환경변수 `SUPABASE_DB_URL`(우선)/`RTM_DATABASE_URL`(대체)의 **런타임 값**에 의존한다. 이 값은 코드가 아니라 환경 설정이며, 본 WO(코드 read-only) 범위에서 확정하지 않는다.
- 또한 이 DSN 환경변수는 legacy /evaluate 경로가 쓰는 `DATABASE_URL`과 **다른 변수명**이다(서버 docstring 기준). 두 경로가 서로 다른 환경변수로 DB를 지정한다는 것은 코드 사실.
- (이 환경변수 값 확인 및 그 함의는 다음 WO 소관 — 본 WO는 Loader 입력 '무엇'까지만 확정.)
