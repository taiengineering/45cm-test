# WO-OPS-REDEPLOY-001 — leg-runtime Deployment AFTER (STEP3-4)

## STEP4 실제 기동 확인 — REDEPLOY_CONFIRMED
| 증거 | BEFORE | AFTER | 판정 |
|---|---|---|---|
| deployment_id | 0f5022b2-9fdc-47ec-a878-6e514b83ee3a | **00f1101a-c470-474b-9443-9b6bdd11811e** | 다름 ✅ |
| service_id (leg-runtime) | 856c72c7-eeb8-4241-97c6-a5250a98b715 | 856c72c7-eeb8-4241-97c6-a5250a98b715 | 동일(대상 확인) ✅ |
| region / replicas | sin + US West (2/2) | sin 단독 | US West 선삭제 반영 |
| status | Online | Online · Deploying(13s) → SUCCESS 대기 | 신규 배포 진행 ✅ |
| startup log | (직전 WO: 미관측) | **Starting Container / Waiting for application startup / Started server process [1] / Uvicorn running 0.0.0.0:8080 / Application startup complete** | 새 프로세스 기동 확인 ✅ |

Project=tai-api(7c3ab53b) · Env=production(9dacb6f0) · Service=leg-runtime(856c72c7)

### 관측 무결성 기록 (사실)
- 직전 WO(RUNTIME-DEBUG-001) 관측 시점 leg-runtime = **레플리카 2개(sin+US West, 2/2)**. 당시 /rtm 요청은 두 레플리카에 로드밸런싱 → provenance-동일 관측이 '2 레플리카 환경'에서의 것이라는 단서와 함께 보존.
- 본 WO에서 Operator가 US West 레플리카를 먼저 삭제 → sin 단일로 정리 후 redeploy → 단일 프로세스 기준 관측 가능.
- 이번 startup 배너 확보로, '새 프로세스 실제 기동'이 증명됨(직전 WO의 미확정 항목 해소).

## STEP4 판정: REDEPLOY_CONFIRMED → STEP5(23 atom Verify) 진행
