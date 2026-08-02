WITH unmapped AS (
  SELECT lm.id AS law_id, lm.law_name,
         regexp_replace(lm.law_name, '\s*(시행령|시행규칙).*$', '') AS base_name
  FROM public.law_master lm
  LEFT JOIN public.law_sector_mapping lsm ON lsm.law_id=lm.id
  WHERE lsm.id IS NULL AND lm.is_active=true
)
SELECT u.law_name AS unmapped_law, pm.law_name AS parent_law, plsm.sectors AS parent_sectors
FROM unmapped u
JOIN public.law_master pm ON pm.law_name = u.base_name AND pm.id <> u.law_id
JOIN public.law_sector_mapping plsm ON plsm.law_id = pm.id
WHERE u.law_name <> u.base_name
ORDER BY u.law_name;
