\echo == 매핑 없는 법령 규모 (law_master에 있으나 law_sector_mapping에 없음) ==
SELECT count(*) AS unmapped
FROM public.law_master lm
LEFT JOIN public.law_sector_mapping lsm ON lsm.law_id = lm.id
WHERE lsm.id IS NULL AND lm.is_active = true;

\echo == 전체 활성 법령 수 ==
SELECT count(*) AS active_laws FROM public.law_master WHERE is_active = true;

\echo == 에너지절약형주택 article이 executable_draft로 존재하는지 (도달 경로 상류) ==
SELECT ed.id AS draft_id, ed.article_id, ed.status
FROM engine_isolated.executable_draft ed
JOIN public.law_article la ON la.id = ed.article_id
JOIN public.law_master lm ON lm.id = la.law_id
WHERE lm.law_name ILIKE '%에너지절약형%'
LIMIT 5;
