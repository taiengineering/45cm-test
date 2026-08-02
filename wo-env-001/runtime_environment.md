# WO-ENV-001 — Runtime Environment (STEP1)

leg-runtime (Railway: project=tai-api, service=leg-runtime, env=production) 환경변수 — 비밀번호 마스킹, host/project_ref만.

| env_var | host | project_ref | 설정 | RTM loader 우선순위 |
|---|---|---|---|---|
| **SUPABASE_DB_URL** | db.vwlahtguyggrhvslabax.supabase.co:5432 | **vwlahtguyggrhvslabax** | 설정됨 | **1순위 (실제 사용)** |
| RTM_DATABASE_URL | (없음) | (없음) | **미설정** | 2순위 (SUPABASE_DB_URL 있으므로 미사용) |
| DATABASE_URL | aws-1-ap-northeast-2.pooler.supabase.com:5432 | wrfcedzgdrfupenzqhur | 설정됨 | **RTM loader 미사용** (legacy /evaluate 경로용) |

코드 근거(LOADER_INPUT_CONFIRMED): `_fetch_rows` = `os.environ.get("SUPABASE_DB_URL") or os.environ.get("RTM_DATABASE_URL")`.
→ SUPABASE_DB_URL이 설정돼 있으므로 `or` 단락 평가로 **vwlaht에 연결**. RTM_DATABASE_URL(빈값)·DATABASE_URL(wrfced)은 RTM 경로에서 사용되지 않음.
