# WO-DEBUG-LOADER-001 STEP6 Independent Review + STEP7 Verdict

## STEP6 — Independent Review
| 점검 | 답 | 근거 |
|---|---|---|
| 새 RCA를 했는가? | **NO** | "왜 STALE인가"·원인 귀속 안 함. loader 입력 '무엇'만 코드로 확인. |
| 새 VERIFY를 했는가? | **NO** | 런타임 동작 재실험 없음. 코드 read-only. |
| Repository를 재분석했는가? | **NO** | production_semantic_repository 데이터 재조회·의미 분석 안 함. loader 코드 경로만 확인. |
| DB를 수정했는가? | **NO** | 코드 read-only, DB/SQL 쓰기 0. |
| 추측을 기록했는가? | **NO** | 코드 사실만 기록. 환경변수 물리 DB 값은 '미확정(env)'으로 명시. |

## STEP7 — 최종 판정: **LOADER_INPUT_CONFIRMED**

새로 기동한 leg-runtime의 /rtm 엔진은 **Live Postgres DB**(`public.production_semantic_repository`)를 psycopg2 SELECT(PRODUCTION_QUERY)로 읽어 Repository를 구성한다. DSN은 환경변수 `SUPABASE_DB_URL`(우선)/`RTM_DATABASE_URL`(대체). 프로세스 전역 lazy singleton(최초 /rtm 요청 시 1회). embedded 파일/artifact/pickle/snapshot fallback 없음. provenance는 DB rows에서 파생.

즉 Loader 입력 = **Live DB** 로 코드상 확정. 단, 그 DB의 **물리 정체(어느 Supabase 인스턴스)**는 DSN 환경변수 값에 의존하며 코드로는 확정 불가(다음 WO의 env 확인 대상).
