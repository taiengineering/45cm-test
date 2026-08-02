# WO-CHG-010 STEP 3.5-2 — is_readonly 사용처 분류 (전수)

DB 내부에서 is_readonly를 참조하는 객체를 전수 검색한 결과:

| 사용처 유형 | 발견 | 분류 |
|---|---|---|
| trigger function | 없음 | NOT_REFERENCED |
| policy expression (RLS) | RLS 자체 비활성, 정책 0 | NOT_REFERENCED |
| stored procedure / RPC | is_readonly 참조 함수 0 | NOT_REFERENCED |
| view / materialized view | 참조 뷰 0 | NOT_REFERENCED |
| validation function | 없음 | NOT_REFERENCED |
| freeze function | 없음 | NOT_REFERENCED |

## 판정: METADATA_ONLY / NOT_REFERENCED
is_readonly는 DB 계층(제약·트리거·정책·함수·뷰) 어디에서도 UPDATE를 강제·차단하지 않는 순수 상태 메타 컬럼이다. is_readonly=TRUE 값 자체는 DB 쓰기를 막지 않는다.

## 정직한 한계(UNRESOLVED 영역)
- 런타임 serving 앱 소스는 미특정(RCA STEP4 BLOCKED). 앱 코드가 서빙 시 freeze_signature/is_readonly를 검증할 가능성은 DB 조사만으로 배제 불가.
- 단, 이는 "UPDATE 차단 여부"가 아니라 "변경 후 서빙 동작"의 문제로, STEP6 freeze 갱신 + STEP7 Runtime Verify + STEP8 Regression에서 포착됨.
