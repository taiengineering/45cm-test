-- 전체 행수 vs 실제 살아있는 factory에 연결된 행수
SELECT
  (SELECT count(*) FROM engine_isolated.facility_applicability) AS total_fa,
  (SELECT count(DISTINCT factory_id) FROM engine_isolated.facility_applicability) AS distinct_factories,
  (SELECT count(*) FROM public.factories) AS live_factories;
-- 컬럼 구조 (created_at 있으면 오래된 것만 지울 수 있음)
SELECT column_name, data_type FROM information_schema.columns
WHERE table_schema='engine_isolated' AND table_name='facility_applicability'
ORDER BY ordinal_position;
