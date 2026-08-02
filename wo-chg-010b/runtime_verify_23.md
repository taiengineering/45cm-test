# WO-CHG-010B STEP4 — Runtime Verify (/rtm/evaluate) : PENDING (access/reload path 필요)

## 기준 (WO-CHG-010A 보완 #1)
Runtime Success는 Repository 상태가 아니라 실제 /rtm/evaluate 출력으로 판정한다. 23 atom law_name이 참법으로 서빙에 반영되어야 PASS. Repository만 바뀌고 Runtime 출력 동일 시 FAIL.

## 현재 상태
- Repository(DB): 교정 확정 (STEP3 PASS — 23 참법 반영, blank 0).
- Runtime 출력: 미검증. 실제 /rtm/evaluate 호출 결과 필요.

## 미해결 변수 — 런타임 저장소 읽기 모델
- live-read(요청마다 DB 조회): 교정 즉시 서빙 반영 -> 라이브 호출로 PASS 확인 가능.
- boot-cache(기동 시 frozen 사본 적재): freeze_signature/is_readonly 정황상 가능. 이 경우 런타임 reload/redeploy 전까지 미반영 = Runtime FAIL. STEP6 freeze 갱신 + 런타임 재적재 선행 필요.

## 제약
- serving 소스 미특정(RCA STEP4 BLOCKED)으로 읽기 모델을 코드로 확정 불가.
- 현 도구 세트에 /rtm/evaluate(POST) 직접 호출 수단 없음.

## 필요 조치 (Operator 택일)
1. 런타임 재적재 경로 확정(freeze 갱신 후 leg-runtime redeploy) 후 23-profile /rtm/evaluate 재실행.
2. Operator 측에서 23 firing profile로 /rtm/evaluate 실행 결과(law_name) 제공 -> 대조.
3. 런타임이 live-read임이 확인되면 즉시 라이브 호출로 검증.

## 주의
Repository는 이미 변경됨. Runtime Verify 미완 상태에서 CHG_SUCCESS 판정 불가. Runtime 미반영 확인 시 Rollback 조건('mismatch 잔존')에 해당 -> 재적재로 해소하거나 ROLLBACK.
