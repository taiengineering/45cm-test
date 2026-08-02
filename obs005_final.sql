\echo == 순수 선임 의무(THEN_ACTION이 APPOINT/DESIGNATE)의 category 행선지 ==
SELECT ds.family_name, count(*) AS n
FROM public.law_article la
JOIN engine_isolated.executable_draft ed ON ed.article_id = la.id
JOIN engine_isolated.draft_slot ds ON ds.draft_id = ed.id
WHERE la.article_title ILIKE '%선임%'
  AND ds.section='THEN_ACTION'
GROUP BY ds.family_name ORDER BY n DESC;

\echo == raw_token(실제 행위 동사)별 분포 — 선임 조문의 THEN_ACTION ==
SELECT ds.raw_token, count(*) AS n
FROM public.law_article la
JOIN engine_isolated.executable_draft ed ON ed.article_id = la.id
JOIN engine_isolated.draft_slot ds ON ds.draft_id = ed.id
WHERE la.article_title ILIKE '%선임%' AND ds.section='THEN_ACTION'
GROUP BY ds.raw_token ORDER BY n DESC LIMIT 15;
