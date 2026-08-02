-- 실제 factory 하나로 조회 비용 측정 (조회가 빠른지)
WITH one AS (SELECT factory_id FROM engine_isolated.facility_applicability LIMIT 1)
SELECT count(*) FROM engine_isolated.facility_applicability
WHERE factory_id = (SELECT factory_id FROM one);

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM engine_isolated.facility_applicability
WHERE factory_id = (SELECT factory_id FROM engine_isolated.facility_applicability LIMIT 1);

-- 테이블 물리 크기 / 죽은 튜플(dead tuple) — INSERT/DELETE 반복의 흔적
SELECT
  pg_size_pretty(pg_total_relation_size('engine_isolated.facility_applicability')) AS total_size,
  n_live_tup, n_dead_tup, last_autovacuum, last_vacuum
FROM pg_stat_user_tables
WHERE schemaname='engine_isolated' AND relname='facility_applicability';
