\echo == task_candidate.id 매칭 ==
SELECT id, task_type, source_action_family, obligation_family, applicability_status, status
FROM public.task_candidate
WHERE id IN ('bdec4d90-6ac3-4f09-ae1f-1da02fab8900','9287b84b-31e9-4508-b915-74a0e6028e62','68345136-cd5d-4ef4-8682-f1d5463f2e6e');

\echo == task_candidate 스키마가 public인지 engine_isolated인지 ==
SELECT table_schema, table_name FROM information_schema.tables WHERE table_name='task_candidate';
