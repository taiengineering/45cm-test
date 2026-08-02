\echo == '안전보건관리규정의 작성' — 법 vs 시행규칙 각 조문의 THEN_ACTION/내용 ==
SELECT lm.law_name, la.article_no, la.article_title,
       ds.section, ds.family_name, ds.raw_token
FROM public.law_article la
JOIN public.law_master lm ON lm.id = la.law_id
JOIN engine_isolated.executable_draft ed ON ed.article_id = la.id
JOIN engine_isolated.draft_slot ds ON ds.draft_id = ed.id
WHERE la.article_title ILIKE '%안전보건관리규정의 작성%'
  AND lm.law_name ILIKE '%산업안전보건법%'
  AND ds.section IN ('THEN_ACTION','IF_ACTOR','THEN_DEADLINE')
ORDER BY lm.law_name, ds.section
LIMIT 40;
