\echo == 미매핑 법령의 domain_code 분포 (귀속 근거 후보) ==
SELECT lm.domain_code, count(*) AS unmapped_n
FROM public.law_master lm
LEFT JOIN public.law_sector_mapping lsm ON lsm.law_id=lm.id
WHERE lsm.id IS NULL AND lm.is_active=true
GROUP BY lm.domain_code ORDER BY unmapped_n DESC;

\echo == 매핑된 법령: domain_code와 sectors의 관계 (규칙 도출 가능한지) ==
SELECT lm.domain_code, lsm.sectors::text, count(*) AS n
FROM public.law_master lm
JOIN public.law_sector_mapping lsm ON lsm.law_id=lm.id
WHERE lm.is_active=true AND lm.domain_code IS NOT NULL
GROUP BY lm.domain_code, lsm.sectors::text
ORDER BY lm.domain_code, n DESC;
