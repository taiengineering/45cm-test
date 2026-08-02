# WO-RUNTIME-DEBUG-001 — Runtime Reload Timeline (실동작 관측)

엔드포인트: `https://leg-runtime-production.up.railway.app` (`/rtm/health`, `/rtm/evaluate`)
표준 probe payload: has_* 18필드 + worker_count=450 + total_floor_area=30000 + is_multi_use=true (accepted 18 → obligation 152)

| 시각 (UTC) | 동작 | 관측 | 파일 |
|---|---|---|---|
| 2026-08-02T12:51:22Z | **STEP1 BASELINE** | health rows=337; evaluate OK, provenance=RC1/CAL022/15cd17e8/337, obligation_count=152, 첫의무 law_name=산안규칙 art4 | 01_baseline_health, 02_baseline_evaluate |
| 2026-08-02T12:55:57Z | **STEP3-① RELOAD (api probe)** | POST /rtm/reload·/rtm/refresh·/rtm/reload-repository·/reload·/admin/reload → **전부 404** (leg-runtime 로그에도 404로 기록됨) → 재적재 트리거 경로 없음 | (probe stdout) |
| 2026-08-02T12:58:18Z | **STEP3-② RESTART 후 관측** | health·evaluate가 baseline과 **바이트 동일** (provenance same, 152/152 atom 동일, law_name/article/evidence 0 diff) | 05_after_restart_health, 06_after_restart_evaluate |
| 2026-08-02T13:00:46Z | **STEP3-③ DEPLOY 후 관측** | health·evaluate가 baseline과 **바이트 동일** (동일) | 07_after_deploy_health, 08_after_deploy_evaluate |
| 2026-08-02T13:0x | **LOG boot-marker scan** | leg-runtime 자기 로그(railway logs --service leg-runtime)에 **부팅/적재 라인 없음** (Uvicorn running·Application startup·loaded·production_semantic_repository 부팅 라인 전무). 12:58~13:00 구간에 요청 액세스 로그만 연속. grep 매칭은 우리 자신의 /rtm/reload-repository 404 한 줄뿐 | 09_legruntime_boot_lines.txt (1줄) |

## 무결성 기록 (관측 사실)
- 초기 `railway logs`(서비스 링크 전)는 **다른 서비스**(`/app/routers/work_schedules.py`, postgrest APIError)를 가리켰음 → `railway service`로 leg-runtime 재링크 후에야 `/rtm/*` 로그 확인됨.
- 따라서 restart/deploy 동작이 **leg-runtime 프로세스를 실제로 교체했는지**는 로그로 확정되지 않음: leg-runtime 자기 로그에 startup 배너가 관측되지 않았고, 12:58~13:00 구간 요청 로그가 끊김 없이 이어짐.
- 대시보드 Deployments 상의 restart/redeploy 이벤트 유무는 본 기록 시점에 미확인.
