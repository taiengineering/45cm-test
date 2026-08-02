\echo == sectors 값 형태 샘플 ==
SELECT law_name, sectors FROM public.law_sector_mapping LIMIT 8;
\echo == sectors에 모든 sector 다 들어간(전역) 매핑 규모 ==
SELECT count(*) AS total_mappings FROM public.law_sector_mapping;
\echo == sectors 고유값 분포 (상위) ==
SELECT sectors::text, count(*) AS n FROM public.law_sector_mapping
GROUP BY sectors::text ORDER BY n DESC LIMIT 15;
