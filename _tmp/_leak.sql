SELECT count(*) AS fa_rows FROM engine_isolated.facility_applicability;
SELECT factory_id, count(*) FROM engine_isolated.facility_applicability
GROUP BY factory_id ORDER BY count(*) DESC LIMIT 10;
SELECT count(*) AS temp_factories FROM public.factories
WHERE status_code = 'ANON_TEMP' OR is_active = false;
