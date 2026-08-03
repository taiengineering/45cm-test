# WO-REGRESSION-300-001 — BLOCKED

## 판정: BLOCKED (사유: Baseline Provenance Mismatch)

CHG-only Regression의 전제(깨끗한 CHG-직전 baseline ↔ CHG 이후 비교)가 성립하지 않아 종료.

## STEP1 소스 확인 결과
| baseline 후보 | 시점 | 소스 | 유효성 |
|---|---|---|---|
| e2e_300_run_A/B/C.json | 2026-08-02 03:15 | vwlahtguyggrhvslabax (구 DB) | 무효 — WIRING-FIX 이전 |
| post-wiring & pre-CHG 300 | — | — | 부재(존재하지 않음) |
| post-CHG 300 | — | — | 미실행 |

## 사유 상세
- 기존 300 Baseline(e2e_300_run_A/B/C)은 **WIRING-FIX 이전** 데이터(런타임이 vwlaht 연결).
- 이후 WIRING-FIX(23 law_name 교정) → CHG(산안524) 순으로 상태가 두 번 이동.
- 이 baseline과 post-CHG를 비교하면 diff에 (1)wiring 23건 + (2)CHG 산안524가 혼재 → CHG 회귀만 분리 불가.
- CHG가 이미 적용되어, 이제 와서 'post-wiring & pre-CHG 300'을 새로 캡처할 수 없음.
- 따라서 이번 CHG Regression은 억지 수행·보정 없이 BLOCKED.

## 조치
1. 현재 상태(wrfced + WIRING-FIX + CHG_SUCCESS)를 **RC2 Candidate**로 기록.
2. 별도 WO에서 **300 Profile Baseline Capture** 수행(RC2 Baseline).
3. RC2 Baseline 승인 이후 모든 Regression은 **RC2 기준**으로 수행.

## 확정 사실 (변함 없음)
- CHG 자체는 검증 완료: Repository 단건 교정 PASS, Runtime 단일 프로파일 328→329 PASS(산안524 신규발화, drift 0). 본 BLOCKED는 '300 회귀 비교 불가'일 뿐 CHG 성공을 뒤집지 않음.
