\echo == law 관련 테이블 컬럼 ==
SELECT table_name, column_name FROM information_schema.columns
WHERE table_schema='public' AND table_name IN ('law_master','law_article')
ORDER BY table_name, ordinal_position;
\echo == executable_draft 컬럼 (조건 관련) ==
SELECT column_name FROM information_schema.columns
WHERE table_schema='engine_isolated' AND table_name='executable_draft'
ORDER BY ordinal_position;
\echo == draft_slot 컬럼 (조건/적용 관련) ==
SELECT column_name FROM information_schema.columns
WHERE table_schema='engine_isolated' AND table_name='draft_slot'
ORDER BY ordinal_position;
