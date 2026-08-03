# WO-CHG-MAPFIELD-001 STEP2~4 — Apply 결과 (Repository)

## STEP2 트랜잭션 Apply (단일 트랜잭션, DO block + assertion)
- UPDATE ... SET mapped_field='has_diving' WHERE atom_id='5b849b3e...' AND mapped_field='worker_count'
- 영향행 = **1** (assertion 통과)
- 트랜잭션 내 assertion: affected=1 AND wc=8 AND diving=26 AND total=337 AND field=has_diving → 전부 PASS → COMMIT
- is_readonly 미변경(기 확인 메타필드, 재조사 안 함)

## STEP3 Commit 전 검증 (트랜잭션 내)
- 대상 mapped_field = has_diving
- law_name / law_article(524) / semantic_clause_id(7509bca1) 불변
- SET 절이 mapped_field만 수정 → evidence 등 타 컬럼 불변
- 전부 PASS → COMMIT 수행

## STEP4 Post-Apply Repository 검증 (커밋 후 재조회)
| 항목 | 변경 전 | 변경 후 | 판정 |
|---|---|---|---|
| 산안524 mapped_field | worker_count | has_diving | PASS |
| worker_count atom 수 | 9 | 8 | PASS |
| has_diving atom 수 | 25 | 26 | PASS |
| 전체 행 수 | 337 | 337 | PASS(불변) |
| distinct atom_id | 337 | 337 | PASS(중복 0) |
| law_name | (동일) | 산업안전보건기준에 관한 규칙 | PASS(불변) |
| law_article | 524 | 524 | PASS(불변) |
| semantic_clause_id | 7509bca1 | 7509bca1 | PASS(불변) |
| row md5 | d276ebed… | 3cfb0750cd014d287198cd2d0edb5994 | 변경(mapped_field만) |

## Repository 검증: **PASS**
산안524 외 변경 0(델타 = worker_count 9→8, has_diving 25→26, 정확히 1건 이동).
Rollback 수단 상시 유지: SET mapped_field='worker_count' → 원복 시 md5==d276ebedfc2fd4ff9d3bbe0308c1f0ae.

## 다음 (Operator 확인 후 진행)
STEP5 leg-runtime 재배포 → STEP6 Runtime Verify(has_diving payload, 산안524 신규발화·총 329·기존 328 불변) → STEP7 A/B/C 결정성 → STEP8 판정. (본 보고는 Repository 검증까지.)
