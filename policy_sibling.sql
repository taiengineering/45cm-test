-- 미매핑 법령과 같은 base_name을 가진 '이미 매핑된' 형제(본법/다른 시행령 등)
WITH unmapped AS (
  SELECT lm.id AS law_id, lm.law_name,
         regexp_replace(lm.law_name, '\s*(시행령|시행규칙|고시|규정).*$', '') AS base_name
  FROM public.law_master lm
  LEFT JOIN public.law_sector_mapping lsm ON lsm.law_id=lm.id
  WHERE lsm.id IS NULL AND lm.is_active=true
)
SELECT count(DISTINCT u.law_id) AS unmapped_with_mapped_sibling
FROM unmapped u
JOIN public.law_master sm ON regexp_replace(sm.law_name,'\s*(시행령|시행규칙|고시|규정).*$','')=u.base_name AND sm.id<>u.law_id
JOIN public.law_sector_mapping slsm ON slsm.law_id=sm.id;
