SELECT
  (SELECT count(*) FROM public.law_sector_mapping) AS existing_mappings,
  (SELECT count(DISTINCT sectors::text) FROM public.law_sector_mapping) AS distinct_combos;

SELECT mapping_method, count(*) AS n
FROM public.law_sector_mapping
GROUP BY mapping_method ORDER BY n DESC;
