# WO-RUNTIME-BACKFILL-VERIFY-001 — 중간 보고 (census 1차)

## STEP1 Repository Snapshot (wrfced, LEG DB)
337 rows · blank 0 · nonblank 337 · distinct law_name 18 · release SEMREPO-RC1-2026.07.20 · freeze 15cd17e871b6885d34214c84a58adf47

## STEP2 Backfill Inventory (사전상태 기준, 337 전수)
| 분류 | 수 |
|---|---|
| BACKFILLED (사전 공란 → 채워짐) | 325 |
| NONBLANK_PROTECTED (사전 비공란, 축약형 유지) | 12 |
| UNCHANGED | 0 |

## STEP3 Runtime Census 1차 (rtm_out2.json, deployment b94a0741)
- payload: FULL(35 has_*) + has_gas/has_crane/has_demolition
- obligation_count 264 · repository_size 337
- Runtime에서 관측된 atom: **264 / 337**

## STEP4 Repository ↔ Runtime 비교 (관측된 264개)
- **law_name 불일치: 0**
- **article 불일치: 0**
- BACKFILLED 커버 254개 → law_name 전부 일치 (254/254)
- NONBLANK_PROTECTED 커버 10/12

## 미커버 (census 미완)
- 73 atom이 1차 payload로 미발화 (BACKFILLED 71 + PROTECTED 2)
- 미발화 원인 = 트리거 필드 미포함. 필요한 mapped_field:
  has_dust_work(20)·has_scaffold(18)·worker_count(9)·has_forklift(7)·has_boiler(5)·has_noise_work(4)·has_high_place_work(4)·has_pressure_vessel(3)·is_multi_use(2)·has_press(1)

## 잠정 판정: **RUNTIME_BACKFILL_INCOMPLETE** (census 미완 — 337 전수 필요)
관측된 264개는 전달 완벽(불일치 0). 나머지 73개는 2차 payload로 census 완성 후 재판정.
