# WO-OPS-REDEPLOY-001 — leg-runtime Deployment BEFORE

## STEP1 Target (고정)
| 항목 | 값 |
|---|---|
| Railway Project | tai-api |
| Target Service | leg-runtime |
| Environment | production |
| 무효 대상 | tai-api-prod / 그 외 서비스 재시작 |

## STEP2 재배포 전 상태
### Runtime provenance (관측 @ 2026-08-02T12:51Z, baseline)
- release_version: SEMREPO-RC1-2026.07.20
- repository_version: SEMREPO-CAL022-2026.07.20
- freeze_signature: 15cd17e871b6885d34214c84a58adf47
- repository_size: 337

### Deployment 메타 (관측 @ railway status)
- deployment_id (BEFORE): 0f5022b2-9fdc-47ec-a878-6e514b83ee3a
- service_id (leg-runtime): 856c72c7-eeb8-4241-97c6-a5250a98b715
- project_id: 7c3ab53b-feb6-40a4-a4f0-7ade3f6e524b (tai-api) / env_id: 9dacb6f0-5d2a-4064-839e-e050af50bf30 (production)
- replicas: 2/2 (sin + US West) — 관측 당시

### 23 atom law_name 상태 (BEFORE, chg010_runtime_out 기준 — 전부 동일값)
- distinct law_name: {산업안전보건기준에 관한 규칙: 23/23}
- 프로파일: PF-2109, PF-2174, PF-2162, PF-0099
- 판정 기준: 재배포·새 프로세스 확인 후 이 23개 law_name이
  - 바뀌면 → RUNTIME_REFRESHED (교정 반영)
  - 그대로면 → CONFIRMED_REDEPLOY_BUT_STALE (artifact/pin 의심 → 다음 loader-입력 Debug WO)
