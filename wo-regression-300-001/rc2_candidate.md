# RC2 Candidate 기록

## 현재 런타임/리포지토리 상태 (RC2 Candidate)
| 항목 | 값 |
|---|---|
| DB | wrfcedzgdrfupenzqhur (LEG runtime source) |
| 연결 | WIRING-FIX 완료 (SUPABASE_DB_URL→wrfced) |
| 최종 변경 | CHG-MAPFIELD-001 (산안524 worker_count→has_diving) CHG_SUCCESS |
| repository_size | 337 |
| release_version | SEMREPO-RC1-2026.07.20 |
| repository_version | SEMREPO-CAL022-2026.07.20 |
| freeze_signature | 15cd17e871b6885d34214c84a58adf47 (RC1; RC2 승격 시 갱신 여부 별도 판단) |
| has_diving | 26 (25+산안524) |
| worker_count | 8 |
| 단일 프로파일 obligation | 329 (has_diving payload) |

## RC2 Candidate 상태의 의미
- 이 상태가 향후 Regression의 새 기준선(RC2 Baseline) 후보.
- Baseline 확정은 별도 WO(300 Profile Baseline Capture)에서 300 프로파일 실측·검증 후.
- 확정 전까지는 'Candidate'이며, freeze_signature/release/repository_version의 RC2 갱신 여부는 그 WO에서 결정(미확정).

## 다음 WO (예정)
- WO-BASELINE-CAPTURE-300-001 (가칭): wrfced+CHG 상태에서 300 프로파일 실츧�·검증 → RC2 Baseline 확정.
- 이후 모든 CHG Regression은 RC2 기준.
