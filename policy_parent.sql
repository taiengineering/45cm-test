WITH unmapped AS (
  SELECT lm.id AS law_id, lm.law_name,
         regexp_replace(lm.law_name, '\s*(시행령|시행규칙).*$','') AS base_name
  FROM public.law_master lm
  LEFT JOIN public.law_sector_mapping lsm ON lsm.law_id=lm.id
  WHERE lsm.id IS NULL AND lm.is_active=true AND lm.law_name ~ '(시행령|시행규칙)'
)
SELECT
  count(*) AS total_sub,
  count(*) FILTER (WHERE pm.id IS NULL) AS parent_absent,
  count(*) FILTER (WHERE pm.id IS NOT NULL AND plsm.id IS NULL) AS parent_unmapped,
  count(*) FILTER (WHERE plsm.id IS NOT NULL) AS parent_mapped
FROM unmapped u
LEFT JOIN public.law_master pm ON pm.law_name = u.base_name AND pm.id<>u.law_id
LEFT JOIN public.law_sector_mapping plsm ON plsm.law_id = pm.id;
