\echo == rule_id를 가진 컬럼이 있는 테이블 탐색: rule_candidate ==
SELECT table_schema, table_name FROM information_schema.tables
WHERE table_name ILIKE '%rule%candidate%' OR table_name ILIKE '%rule%';
\echo == diagnosis 관련 테이블 ==
SELECT table_schema, table_name FROM information_schema.tables
WHERE table_name ILIKE '%diagnos%' OR table_name ILIKE '%obligation%' OR table_name ILIKE '%anonymous%';
