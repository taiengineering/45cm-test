# WO-OPS-REDEPLOY-001 — Redeploy Verdict

## STEP6 최종 판정: **CONFIRMED_REDEPLOY_BUT_STALE**

### 근거 A — 재배포·새 프로세스 실증 (REDEPLOY_CONFIRMED)
| 증거 | 값 |
|---|---|
| deployment_id BEFORE → AFTER | 0f5022b2-9fdc-47ec-a878-6e514b83ee3a → **00f1101a-c470-474b-9443-9b6bdd11811e** (다름) |
| service_id | 856c72c7-eeb8-4241-97c6-a5250a98b715 (leg-runtime, 동일 대상) |
| startup log | Starting Container / Waiting for application startup / Started server process [1] / Uvicorn running 0.0.0.0:8080 / Application startup complete |
| replicas | US West 선삭제 → sin 단독(단일 프로세스) |
| Project/Env | tai-api(7c3ab53b) / production(9dacb6f0) |

→ 새 Deployment + 새 프로세스 기동이 로그·ID로 증명됨.

### 근거 B — 23 atom 반영 결과 (STALE)
- 23/23 atom law_name: **변화 0** — 전부 여전히 `산업안전보건기준에 관한 규칙` (BEFORE와 동일)
- law_article 변화 0 · applicability 변화 0
- provenance: SEMREPO-RC1-2026.07.20 / freeze 15cd17e871b6885d34214c84a58adf47 / repository_size 337 (baseline과 동일)
- 커버리지: 표준 payload 13/23 + full payload(39 has_* accepted)로 나머지 → **23/23 전수 확인**
- 파일: 12_after_redeploy_evaluate(13 atom) + 13_after_redeploy_full(23 atom 전수)

### 판정 의미 (WO 정의 그대로, RCA 아님)
새 프로세스가 확실히 기동됐음에도 23/23 교정 라벨이 반영되지 않음 →
**Runtime이 (재기동으로 재적재됨에도) 교정된 값을 내보내지 않는다**는 것이 실증됨.
WO 정의에 따라, 이 지점에서 비로소 **Runtime이 DB가 아닌 고정 artifact 또는 pin된 snapshot을 읽는 것**으로 범위가 좁혀지며, 다음 단계는 **loader 입력을 확인하는 Debug WO**이다. (본 WO는 실행·실증만 — RCA/loader 분석/DB·Snapshot 조사는 다음 WO 소관.)

## STEP6 분기 (지시서 대비)
- RUNTIME_REFRESHED: **아님** (23 law_name 변화 0)
- **CONFIRMED_REDEPLOY_BUT_STALE: 예** ← 확정
- REDEPLOY_NOT_CONFIRMED: 아님 (신규 deployment_id + startup log 확보)

## 남은 정합성 메모 (사실)
- 13_ 검증 probe는 새 deployment(00f1101a) startup 완료 배너 이후 실행돼 200 응답 수신. 배포 status를 SUCCESS/Online으로 대시보드에서 최종 확인하면 무결성 완결(선택).
- 이전 WO의 '2 레플리카(sin+US West)' 환경은 본 WO에서 US West 삭제로 단일화됨 → 본 STALE 관측은 단일 프로세스 기준.
