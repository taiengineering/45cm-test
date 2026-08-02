# WO-WIRING-FIX-001 STEP2 — 기존 LEG 연결 계약 확인

(새 아키텍처 설계 없음. 기존 고정 계약에서 확인만.)

| 항목 | 값 | 근거 |
|---|---|---|
| 승인된 LEG DB 변수 | **DATABASE_URL** | server.py docstring: "DATABASE_URL leg-prod (읽기 전용 사용)" |
| LEG DB project_ref | **wrfcedzgdrfupenzqhur** (leg-prod) | WO-ENV-001 env 관측 + server.py |
| RTM loader 변수 우선순위 | SUPABASE_DB_URL → RTM_DATABASE_URL | rtm_router._fetch_rows (코드) |
| 기존 배포 환경 계약 | leg-runtime = LEG 데이터 소유 런타임 (federation runtime-owner) | infra/runtime.manifest.json |

## LEG DB 상태 검증 (read-only, 복원 대상 확증)
wrfcedzgdrfupenzqhur.public.production_semantic_repository:
- total_rows 337 / blank 0 (완전 교정) / release RC1 / freeze 15cd17e8
- 23 Target atom: 23/23 개별 법령으로 교정, 공란 0
→ 연결을 이 DB로 복원하면 교정된 값이 런타임에 반영됨.
