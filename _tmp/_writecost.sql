-- 익명진단이 매번 하는 일: 임시 factory에 738행 INSERT → 조회 → DELETE
-- 그 INSERT/DELETE 자체 비용을 재현 측정 (실제 factory_id 하나 복제)
\timing on
-- 1) 임시 테스트 factory_id
SELECT gen_random_uuid() AS test_fid \gset
-- 2) 실제 한 factory의 738행을 test_fid로 복제 INSERT (매 진단의 쓰기 재현)
INSERT INTO engine_isolated.facility_applicability (id, factory_id, draft_id, part_id, applicability_status, match_details, created_at)
SELECT gen_random_uuid(), :'test_fid', draft_id, part_id, applicability_status, match_details, now()
FROM engine_isolated.facility_applicability
WHERE factory_id = (SELECT factory_id FROM engine_isolated.facility_applicability LIMIT 1);
-- 3) 조회
SELECT count(*) FROM engine_isolated.facility_applicability WHERE factory_id = :'test_fid';
-- 4) 정리(cleanup 재현)
DELETE FROM engine_isolated.facility_applicability WHERE factory_id = :'test_fid';
