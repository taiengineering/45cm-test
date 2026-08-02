# WO-CHG-011 STEP1 — Target Lock

| 항목 | 값 |
|---|---|
| Target DB | **vwlahtguyggrhvslabax** (RTM loader 실제 연결처, SUPABASE_DB_URL) |
| Consumer | /rtm/evaluate |
| DSN source | SUPABASE_DB_URL (loader 1순위) |
| 실행 금지 DB | wrfcedzgdrfupenzqhur (DATABASE_URL, RTM 미사용 — 본 WO 대상 아님) |
| 대상 테이블 | public.production_semantic_repository |
| 변경 컬럼 | law_name (공란만) |
| 조인 정답 경로 | semantic_clause_id → semantic_clause.source_article_id → law_article.law_id → law_master.law_name (= COALESCE(law_name, law_name_short)) |

근거: WO-ENV-001 RUNTIME_DATABASE_MISMATCH (loader가 SUPABASE_DB_URL=vwlaht에 연결). wrfced 325건은 본 복구와 분리(별도 정합성).
