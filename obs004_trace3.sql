\echo == 대표 3항목: law_name / domain_code / sectors 매핑 ==
SELECT lm.law_name, lm.domain_code, lsm.sectors, lsm.mapping_method, lsm.confidence
FROM public.law_master lm
LEFT JOIN public.law_sector_mapping lsm ON lsm.law_id = lm.id
WHERE lm.law_name ILIKE '%에너지절약형%'
   OR lm.law_name ILIKE '%방사선%'
   OR lm.law_name ILIKE '%산업안전보건기준%';
