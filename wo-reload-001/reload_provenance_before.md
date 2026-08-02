# WO-RELOAD-001 STEP1 — Runtime Provenance (Reload 전 baseline)

실측 출처: run_A endpoint(leg-runtime-production.up.railway.app/rtm/evaluate) + WO-CHG-010B STALE_RUNTIME 검증.

## Reload 전 런타임 상태 (현재)
| 항목 | 값 |
|---|---|
| Release | SEMREPO-RC1-2026.07.20 |
| Freeze | 15cd17e871b6885d34214c84a58adf47 |
| Repository Size | 337 |
| 23 atom law_name | 전부 옛 default (산업안전보건기준에 관한 규칙) = LABEL_UNCHANGED |
| article / applicability | 23/23 expected와 동일 (article 정상, APPLICABLE) |

## DB(Repository) 현재 상태 (참고, 이미 교정 완료 — 이번 WO에서 변경 안 함)
- law_name: 23 오표기 -> 참법 교정, blank 0 (RC2 내용).
- freeze_signature/release_version: 아직 RC1 그대로 (이번 WO 미변경).

## 검증 가설
Runtime이 boot-cache이면, Reload(Deploy/Restart) 후 저장소를 다시 적재하여 교정된 law_name(RC2 내용)을 서빙해야 한다. Reload 전후 동일 23 profile 출력의 law_name 변화 여부로 판정.
