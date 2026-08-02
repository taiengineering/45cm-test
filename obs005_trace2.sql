\echo == 전기안전관리자 선임 및 해임신고 family_name ==
SELECT lm.law_name, la.article_title, ds.family_name, ds.raw_token
FROM public.law_article la
JOIN public.law_master lm ON lm.id = la.law_id
JOIN engine_isolated.executable_draft ed ON ed.article_id = la.id
JOIN engine_isolated.draft_slot ds ON ds.draft_id = ed.id
WHERE la.article_title ILIKE '%전기안전관리자%'
  AND ds.family_name IS NOT NULL
LIMIT 20;

\echo == family_name별 THEN_ACTION 종류(어떤 family가 report로 가는지) ==
SELECT ds.family_name, count(*) AS n
FROM engine_isolated.draft_slot ds
WHERE ds.section = 'THEN_ACTION' AND ds.family_name IS NOT NULL
GROUP BY ds.family_name ORDER BY n DESC LIMIT 20;
