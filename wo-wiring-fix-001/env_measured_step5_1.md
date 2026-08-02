# WO-WIRING-FIX-001 STEP5-1 — 환경변수 실측 (변경 없음)

Operator가 leg-runtime(production) Railway variables에서 직접 확인 (URL 전문 미기록, project_ref만).

| 변수 | host / user (실측) | project_ref | 판정 |
|---|---|---|---|
| SUPABASE_DB_URL | db.vwlahtguyggrhvslabax.supabase.co:5432 | **vwlahtguyggrhvslabax** | 구 DB (현재 RTM 읽기 대상, 잘못됨) |
| DATABASE_URL | postgresql://postgres.wrfcedzgdrfupenzqhur (pooler user) | **wrfcedzgdrfupenzqhur** | **LEG DB** |
| RTM_DATABASE_URL | (화면 미표시) | unset(간주) | 미사용 |

## 확정 판정 (실측)
- SUPABASE_DB_URL -> vwlahtguyggrhvslabax
- DATABASE_URL -> wrfcedzgdrfupenzqhur
- **DATABASE_URL == wrfcedzgdrfupenzqhur ? -> PASS (실측 확인)**

전제가 아닌 실측으로 확정. STEP5-2 진행 조건 충족.
방식 A(SUPABASE_DB_URL을 DATABASE_URL과 동일한 wrfced 값으로 교체) 안전.
