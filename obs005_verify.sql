\echo == '선임'을 포함한 조문 중 제목에 '신고/신청/제출'이 함께 있는 비율 ==
SELECT
  count(*) FILTER (WHERE la.article_title ILIKE '%선임%') AS 선임포함,
  count(*) FILTER (WHERE la.article_title ILIKE '%선임%' AND (la.article_title ILIKE '%신고%' OR la.article_title ILIKE '%신청%' OR la.article_title ILIKE '%제출%')) AS 선임_그리고_신고류
FROM public.law_article la
WHERE la.article_title ILIKE '%선임%';

\echo == 순수 '선임'(신고 아님)인데 THEN_ACTION이 REPORT인 경우가 있는지 (있으면 이상) ==
SELECT lm.law_name, la.article_title, ds.raw_token
FROM public.law_article la
JOIN public.law_master lm ON lm.id = la.law_id
JOIN engine_isolated.executable_draft ed ON ed.article_id = la.id
JOIN engine_isolated.draft_slot ds ON ds.draft_id = ed.id
WHERE la.article_title ILIKE '%선임%'
  AND la.article_title NOT ILIKE '%신고%'
  AND la.article_title NOT ILIKE '%신청%'
  AND la.article_title NOT ILIKE '%해임%'
  AND ds.section='THEN_ACTION' AND ds.family_name='REPORT_FAMILY'
LIMIT 15;
