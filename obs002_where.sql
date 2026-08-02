-- rule_id가 어느 테이블의 식별자인지 탐색
\echo == draft_slot.draft_id 매칭 ==
SELECT count(*) FROM engine_isolated.draft_slot
WHERE draft_id IN ('bdec4d90-6ac3-4f09-ae1f-1da02fab8900','9287b84b-31e9-4508-b915-74a0e6028e62','68345136-cd5d-4ef4-8682-f1d5463f2e6e');

\echo == executable_draft.rule_candidate_id 매칭 ==
SELECT count(*) FROM engine_isolated.executable_draft
WHERE rule_candidate_id IN ('bdec4d90-6ac3-4f09-ae1f-1da02fab8900','9287b84b-31e9-4508-b915-74a0e6028e62','68345136-cd5d-4ef4-8682-f1d5463f2e6e');

\echo == draft_slot.part_id 매칭 ==
SELECT count(*) FROM engine_isolated.draft_slot
WHERE part_id IN ('bdec4d90-6ac3-4f09-ae1f-1da02fab8900','9287b84b-31e9-4508-b915-74a0e6028e62','68345136-cd5d-4ef4-8682-f1d5463f2e6e');
