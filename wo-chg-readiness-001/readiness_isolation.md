# WO-CHG-READINESS-001 STEP1 — 격리성 (Isolation)

대상 DB: wrfcedzgdrfupenzqhur (런타임 실제 연결처, WO-WIRING-FIX-001로 복원 완료)
변경: 산안524(atom_id=5b849b3e-a3ae-52ae-81e7-3eb4858230ab) mapped_field worker_count → has_diving

| 항목 | 값 | 판정 |
|---|---|---|
| WHERE atom_id=5b849b3e 매칭 행 | **1** | 단건 격리 |
| 현재 mapped_field | worker_count | 예상 일치 |
| law_article | 524 | 확인 |
| semantic_clause_id | 7509bca1-0700-466c-849b-de465134b186 | 확인 |
| distinct atom_id / total rows | 337 / 337 | atom_id 유일(PK) |

UPDATE ... WHERE atom_id='5b849b3e...' 는 정확히 1행에만 매칭 → 나머지 336행(worker_count 잔여 8건 포함) 무변경. 격리성 PASS.
