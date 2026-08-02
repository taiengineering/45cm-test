-- 이미 매핑된 393 법령의 적용대상 조문 원문 + 실제 sectors (정답지)
WITH mapped AS (
  SELECT lsm.law_id, lm.law_name, lsm.sectors, lsm.mapping_method
  FROM public.law_sector_mapping lsm
  JOIN public.law_master lm ON lm.id = lsm.law_id
)
SELECT m.law_id, m.law_name, m.sectors, m.mapping_method,
       la.article_no, la.article_title,
       left(regexp_replace(la.article_text,'\s+',' ','g'),200) AS txt
FROM mapped m
JOIN public.law_article la ON la.law_id = m.law_id
WHERE la.article_no IN ('1','2','3')
   OR la.article_title ILIKE '%적용%' OR la.article_title ILIKE '%목적%'
   OR la.article_title ILIKE '%정의%' OR la.article_title ILIKE '%대상%'
   OR la.article_text ILIKE '%이 법은%' OR la.article_text ILIKE '%적용한다%'
ORDER BY m.law_name, la.article_no;
