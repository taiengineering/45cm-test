# WO-WIRING-FIX-001 STEP1 — Wrong Target 기록

## Loader precedence (코드 확정, LOADER_INPUT_CONFIRMED)
`_fetch_rows` = `os.environ.get("SUPABASE_DB_URL") or os.environ.get("RTM_DATABASE_URL")`
→ 우선순위: **SUPABASE_DB_URL → RTM_DATABASE_URL**

## 현재 env (WO-ENV-001)
| 변수 | project_ref | 상태 | RTM 사용 |
|---|---|---|---|
| SUPABASE_DB_URL | **vwlahtguyggrhvslabax** (구 DB) | 설정됨 | **1순위 = 실제 사용 (잘못됨)** |
| RTM_DATABASE_URL | (없음) | 미설정 | 미사용 |
| DATABASE_URL | **wrfcedzgdrfupenzqhur** (LEG DB) | 설정됨 | RTM 경로 미사용 |

## 판정: **RUNTIME_ENV_TARGET_MISMATCH**
런타임 env가 고정 LEG 경계를 벗어나 구 DB(vwlaht)를 가리킴. LEG Runtime 데이터 대상은 LEG DB여야 함.
