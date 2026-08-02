# WO-WIRING-FIX-001 STEP4 — Operator Apply Gate (승인 대기)

| 항목 | 값 |
|---|---|
| 변경 서비스 | leg-runtime |
| 변경 환경 | production (tai-api) |
| 변경 변수 | 방식 A: SUPABASE_DB_URL / 방식 B: SUPABASE_DB_URL(삭제)+RTM_DATABASE_URL |
| Before project_ref (RTM 실제 읽기) | **vwlahtguyggrhvslabax** (SUPABASE_DB_URL) |
| After project_ref (RTM 실제 읽기) | **wrfcedzgdrfupenzqhur** (LEG DB) |
| Rollback 값 | 방식 A: SUPABASE_DB_URL을 다시 vwlaht URL로 / 방식 B: RTM_DATABASE_URL 삭제 + SUPABASE_DB_URL=vwlaht 복구 |
| DB row 변경 | **0** |
| 코드 변경 | **0** |

## 선택 필요 (택1)
- **A**: SUPABASE_DB_URL 값을 LEG DB URL(= 현재 DATABASE_URL 값)로 교체
- **B**: SUPABASE_DB_URL 제거 + RTM_DATABASE_URL = LEG DB URL

## 승인 요청
방식(A 또는 B)을 지정하여 승인("고"/"승인"/"진행")해 주시면, 그 방식의 정확한 Railway 조작 절차를 드립니다.
승인 전 env 변경 없음. leg-runtime env만 수정하며 vwlaht/wrfced 데이터·코드·TAI 서비스는 건드리지 않습니다.

## 승인 후 검증 (STEP6~8) 예정 기준
- STEP6: 재배포 후 /rtm/health provenance = LEG DB(wrfced) 값(337/RC1/15cd17e8)과 일치.
- STEP7: 23 Target atom → 23/23 law_name 개별 법령으로 교정, article/evidence/applicability 변화 0, 누락 0.
- STEP8(23 PASS 후): 300 회귀 — 허용변화 law_name·provenance, 금지변화 atom firing/obligation count/article/evidence/applicability/determinism/contract.
