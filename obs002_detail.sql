-- (매칭 테이블이 rule_candidate라고 가정 — 아니면 위 결과의 테이블로 교체)
SELECT * FROM public.rule_candidate
WHERE id::text IN ('bdec4d90-6ac3-4f09-ae1f-1da02fab8900','9287b84b-31e9-4508-b915-74a0e6028e62','68345136-cd5d-4ef4-8682-f1d5463f2e6e');
