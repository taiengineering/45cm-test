\echo == 에너지절약형주택 law/article + domain_code ==
SELECT la.id AS article_id, lm.law_name, lm.domain_code, la.article_no, la.article_title
FROM public.law_article la
JOIN public.law_master lm ON lm.id = la.law_id
WHERE lm.law_name ILIKE '%에너지절약형%'
LIMIT 10;

\echo == 잠수작업 ==
SELECT la.id AS article_id, lm.law_name, lm.domain_code, la.article_no, la.article_title
FROM public.law_article la
JOIN public.law_master lm ON lm.id = la.law_id
WHERE la.article_title ILIKE '%잠수작업%'
LIMIT 5;

\echo == 방사선 화재방호시설 ==
SELECT la.id AS article_id, lm.law_name, lm.domain_code, la.article_no, la.article_title
FROM public.law_article la
JOIN public.law_master lm ON lm.id = la.law_id
WHERE lm.law_name ILIKE '%방사선%' AND la.article_title ILIKE '%화재%'
LIMIT 5;
