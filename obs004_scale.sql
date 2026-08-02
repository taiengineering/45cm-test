\echo == 활성 법령 중 law_sector_mapping 미매핑 규모 ==
SELECT
  (SELECT count(*) FROM public.law_master WHERE is_active=true) AS active_laws,
  (SELECT count(*) FROM public.law_master lm
     LEFT JOIN public.law_sector_mapping lsm ON lsm.law_id=lm.id
     WHERE lsm.id IS NULL AND lm.is_active=true) AS unmapped;

\echo == 대표 항목들의 매핑 부재 재확인 ==
SELECT lm.law_name,
       CASE WHEN lsm.id IS NULL THEN 'UNMAPPED' ELSE 'mapped' END AS status,
       lsm.sectors
FROM public.law_master lm
LEFT JOIN public.law_sector_mapping lsm ON lsm.law_id=lm.id
WHERE lm.law_name ILIKE '%에너지절약형%'
   OR lm.law_name ILIKE '%방사선%'
   OR lm.law_name ILIKE '%산업안전보건기준%';
