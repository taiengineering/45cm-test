-- 미매핑 법령 중, law_article에 적용/목적/대상/범위 조문이 있는데
-- coverage_evidence 추출에서 빠졌을 가능성을 DB에서 직접 확인
WITH unmapped AS (
  SELECT lm.id AS law_id, lm.law_name
  FROM public.law_master lm
  LEFT JOIN public.law_sector_mapping lsm ON lsm.law_id=lm.id
  WHERE lsm.id IS NULL AND lm.is_active=true
),
scope_count AS (
  SELECT u.law_id, u.law_name,
    count(*) FILTER (WHERE la.article_title ILIKE '%적용%' OR la.article_title ILIKE '%목적%'
                       OR la.article_title ILIKE '%대상%' OR la.article_title ILIKE '%범위%') AS scope_arts,
    count(*) AS total_arts
  FROM unmapped u
  JOIN public.law_article la ON la.law_id = u.law_id
  GROUP BY u.law_id, u.law_name
)
SELECT law_name, scope_arts, total_arts
FROM scope_count
WHERE scope_arts = 0          -- 적용범위 조문이 아예 없는 법령
ORDER BY total_arts DESC;
