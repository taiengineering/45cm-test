SELECT la.law_id, lm.law_name, la.article_no, la.article_title,
       la.article_text
FROM public.law_article la
JOIN public.law_master lm ON lm.id = la.law_id
WHERE la.law_id IN (
  '4673f586-c098-4ca6-af62-a2dc9ce23797',
  '48df5a69-8ce1-490f-97a8-b2c6bc82c3d7',
  'da3d6062-5ddb-46ec-bbef-e002dd4c2c99',
  '7b51564d-0544-46f0-b288-17c44d9f4a4b',
  '7fd2c75c-09d1-44d5-a009-f8283f5ee042',
  'c95ab19f-6805-4237-892f-43146a6281d7',
  'a7520313-442d-4779-8ef4-62c9dad8fea5'
)
ORDER BY lm.law_name, la.article_no_sort;
