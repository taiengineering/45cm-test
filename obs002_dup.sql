-- 최다 중복 article_id(35 draft)의 draft들: part_id 다양성 확인
SELECT part_id, count(*) AS n
FROM engine_isolated.executable_draft
WHERE article_id = '56c87943-fd0d-425c-9d09-18e52654e746'
GROUP BY part_id ORDER BY n DESC;
