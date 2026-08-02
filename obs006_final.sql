\echo == 같은 제목이 법+시행규칙 양쪽에 있을 때, 시행규칙만 THEN_DEADLINE/추가조건 갖는지 (기계설비법 예) ==
SELECT lm.law_name, la.article_title, ds.section, ds.family_name, ds.raw_token
FROM public.law_article la
JOIN public.law_master lm ON lm.id = la.law_id
JOIN engine_isolated.executable_draft ed ON ed.article_id = la.id
JOIN engine_isolated.draft_slot ds ON ds.draft_id = ed.id
WHERE la.article_title ILIKE '%기계설비유지관리자%선임%'
  AND ds.section IN ('THEN_ACTION','THEN_DEADLINE','IF_NUMERIC')
ORDER BY lm.law_name, ds.section
LIMIT 30;
