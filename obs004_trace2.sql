\echo == law_sector_mapping 구조 ==
SELECT column_name FROM information_schema.columns
WHERE table_schema='public' AND table_name='law_sector_mapping'
ORDER BY ordinal_position;
\echo == domain_code 종류와 분포 ==
SELECT domain_code, count(*) AS n FROM public.law_master
GROUP BY domain_code ORDER BY n DESC LIMIT 20;
