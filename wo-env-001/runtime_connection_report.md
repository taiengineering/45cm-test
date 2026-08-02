# WO-ENV-001 — Runtime Connection Report

## STEP2 — 수정 DB와 비교
- 우리가 수정한 DB (325 backfill): **wrfcedzgdrfupenzqhur** (= DATABASE_URL)
- RTM loader 실제 연결 (SUPABASE_DB_URL, 1순위): **vwlahtguyggrhvslabax**

| 비교 항목 | 수정 DB | RTM loader 연결 DB | 동일? |
|---|---|---|---|
| project_ref | wrfcedzgdrfupenzqhur | vwlahtguyggrhvslabax | **다름** |
| host | aws-1-ap-northeast-2.pooler.supabase.com | db.vwlahtguyggrhvslabax.supabase.co | 다름 |

## STEP3 — 동일 여부 판정: **DIFFERENT_DATABASE**

## STEP4 — 실제 연결 DB(vwlaht) SELECT read-only 확인
`SELECT count(*), count(DISTINCT atom_id), freeze_signature, release_version FROM public.production_semantic_repository` @ vwlahtguyggrhvslabax:
| 항목 | 값 |
|---|---|
| rows | **337** |
| distinct atom_id | 337 |
| distinct freeze | 1 → **15cd17e871b6885d34214c84a58adf47** |
| distinct release | 1 → **SEMREPO-RC1-2026.07.20** |

→ 런타임이 내보내던 provenance(337 / 15cd17e8 / RC1)와 **정확히 일치**. 런타임 출력의 실제 출처 = vwlaht 확정.

## 결론
leg-runtime의 /rtm loader는 **SUPABASE_DB_URL = vwlahtguyggrhvslabax**에 연결하며, 우리가 수정한 **wrfcedzgdrfupenzqhur를 읽지 않는다**. (SELECT read-only만 수행, DB 쓰기 0.)
