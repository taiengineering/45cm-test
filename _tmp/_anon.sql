-- 익명 임시 factory 현황
SELECT count(*) AS anon_temp_factories
FROM public.factories WHERE status_code = 'ANON_TEMP';

-- 그 임시 factory들에 붙은 applicability (정리 안 되고 남은 것)
SELECT count(*) AS orphan_anon_fa
FROM engine_isolated.facility_applicability fa
JOIN public.factories f ON f.id = fa.factory_id
WHERE f.status_code = 'ANON_TEMP';

-- factory별 applicability가 정확히 738로 일정한지(=전 draft 무조건 적재) 분포 확인
SELECT cnt, count(*) AS factories_with_this_count FROM (
  SELECT factory_id, count(*) cnt FROM engine_isolated.facility_applicability GROUP BY factory_id
) g GROUP BY cnt ORDER BY factories_with_this_count DESC LIMIT 5;

-- applicability_status 분포 (MATCH/POSSIBLE만 저장되는 구조인데 실제론?)
SELECT applicability_status, count(*) FROM engine_isolated.facility_applicability
GROUP BY applicability_status ORDER BY count(*) DESC;
