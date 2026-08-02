\echo == 선임성격인데 신고category인 대표 항목의 family_name 추적 ==
-- '안전관리자의 선임 등'(산업안전보건법 시행령) → article → draft → draft_slot.family_name
SELECT lm.law_name, la.article_no, la.article_title,
       ds.family_name, ds.section, ds.raw_token
FROM public.law_article la
JOIN public.law_master lm ON lm.id = la.law_id
JOIN engine_isolated.executable_draft ed ON ed.article_id = la.id
JOIN engine_isolated.draft_slot ds ON ds.draft_id = ed.id
WHERE la.article_title ILIKE '%안전관리자의 선임%'
  AND ds.family_name IS NOT NULL
LIMIT 20;
