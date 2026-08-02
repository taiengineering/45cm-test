-- 중복 rule_id 3개가 실제로 별개 rule인지, 무엇이 다른지
SELECT id, article_id, rule_candidate_id, part_id
FROM engine_isolated.executable_draft
WHERE id IN ('bdec4d90-6ac3-4f09-ae1f-1da02fab8900',
             '9287b84b-31e9-4508-b915-74a0e6028e62',
             '68345136-cd5d-4ef4-8682-f1d5463f2e6e');
