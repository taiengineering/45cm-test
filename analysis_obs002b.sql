-- 동일 article_id를 가진 executable_draft가 여러 개인 경우 (중복 draft 규모)
SELECT article_id, count(*) AS n
FROM engine_isolated.executable_draft
WHERE article_id IS NOT NULL
GROUP BY article_id
HAVING count(*) > 1
ORDER BY n DESC
LIMIT 15;
