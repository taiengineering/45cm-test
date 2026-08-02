# WO-CHG-010 STEP 3.5-4 — Apply Readiness 판정

## 판정: DIRECT_UPDATE_ALLOWED
직접 blank-only UPDATE가 기존 DB 보호정책과 충돌하지 않음.

## 근거 (읽기 전용 실측)
- RLS 비활성, UPDATE 트리거 0, CHECK/readonly 제약 0 (STEP 3.5-1).
- is_readonly = METADATA_ONLY / NOT_REFERENCED — DB 어디서도 UPDATE 차단에 사용 안 됨 (STEP 3.5-2).
- 승인 RPC·snapshot/release 인프라 부재 -> 물리적 변경 경로는 직접 UPDATE뿐 (STEP 3.5-3).
- 모든 역할 UPDATE 권한 보유.

## 따라서 Apply 방식 확정 (선택지 재확대 없음)
-> 기존 STEP4 SQL(blank-only, law_master join, 비공란 12 보호) 실행 승인 요청으로 진행.

## 실행 시 준수(기존 WO 규정, 신규 아님)
- is_readonly 컬럼은 변경하지 않음(해제 불필요 — 강제되지 않음).
- Apply 후 STEP6에서 새 release/freeze 발급(RC1 유지 불가) — governance freeze 규약 이행.
- 서빙 앱의 freeze 의존 가능성은 STEP7 Runtime Verify(23) + STEP8 Regression(300)에서 검증.

## DB 쓰기 회계
- 본 STEP 3.5: SELECT만. UPDATE/INSERT/DELETE 0, is_readonly 변경 0, 시험 UPDATE 0.
