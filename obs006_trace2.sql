\echo == 법 vs 시행규칙 조문 원문(요지) ==
SELECT lm.law_name, la.article_no, la.article_title,
       left(la.article_text, 200) AS text_head
FROM public.law_article la
JOIN public.law_master lm ON lm.id = la.law_id
WHERE la.article_title ILIKE '%안전보건관리규정의 작성%'
  AND lm.law_name ILIKE '%산업안전보건법%'
ORDER BY lm.law_name;
