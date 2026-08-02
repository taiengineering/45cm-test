# WO-CHG-010 STEP 3.5-3 — 승인된 변경 경로 확인 (기존 경로만, 신규 설계 없음)

| 후보 경로 | DB 내 존재 여부 |
|---|---|
| 직접 UPDATE | 존재 — 모든 역할 UPDATE 권한 보유, 차단 장치 없음 |
| 승인 RPC (freeze/backfill 함수) | 부재 — production_semantic_repository를 UPDATE/INSERT 하는 함수 0 |
| 새 Snapshot 생성 (snapshot 테이블) | 부재 — snapshot/release 형제 테이블 0 |
| 새 Release 생성 (release 테이블) | 부재 — freeze/release 컬럼 보유 별도 테이블 0 |
| 기존 Repository 복제 후 승격 | 부재 — 복제/승격 대상 테이블·함수 0 |

## 결론
DB에 물리적으로 존재하는 유일한 비충돌 변경 경로 = 직접 UPDATE. 승인 RPC나 snapshot/release 생성 인프라는 이 DB에 구현되어 있지 않음. (freeze는 컬럼값 규약으로 관리되는 governance 프로세스이지 DB 강제 장치가 아님.)
