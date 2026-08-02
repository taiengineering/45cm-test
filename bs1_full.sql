SELECT lm.law_name,
       count(*) FILTER (WHERE la.article_title ILIKE '%적용%' OR la.article_title ILIKE '%목적%' OR la.article_title ILIKE '%대상%' OR la.article_title ILIKE '%범위%') AS scope_articles,
       count(*) AS total_articles
FROM public.law_article la
JOIN public.law_master lm ON lm.id = la.law_id
WHERE la.law_id IN ('')
GROUP BY lm.law_name
HAVING count(*) FILTER (WHERE la.article_title ILIKE '%적용%' OR la.article_title ILIKE '%목적%' OR la.article_title ILIKE '%대상%' OR la.article_title ILIKE '%범위%') > 0
ORDER BY scope_articles DESC;
