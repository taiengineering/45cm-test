# WO-CHG-010 STEP2-3 — Pre-Apply Snapshot & Validation (read-only, live runtime DB)

Target DB: wrfcedzgdrfupenzqhur · table: public.production_semantic_repository · timestamp: 2026-08-02 (session dabc5a)

## STEP1 Operator Approval
- Operator가 WO-CHG-010(Execution)을 "승인된 전략(S1) 실행"으로 발부 -> Scope/Blank-only/Snapshot Freeze/Rollback/Regression/Operator Approval 승인 확인.
- ★STEP4 Apply(프로덕션 쓰기)는 Apply 게이트에서 최종 실행 확인 후에만 수행.

## STEP2 Snapshot Freeze (실행 직전 라이브 상태)
| 항목 | 값 |
|---|---|
| total_rows | 337 |
| blank / nonblank | 325 / 12 |
| distinct_atom | 337 |
| release_version | SEMREPO-RC1-2026.07.20 |
| repository_version | SEMREPO-CAL022-2026.07.20 |
| freeze_signature | 15cd17e871b6885d34214c84a58adf47 |
| is_readonly (any) | TRUE |
| content_md5 (atom_id\|law_name\|law_article, ordered) | fc0ae59209770214d3e15c86dd8cc889 |

## STEP3 Pre-Apply Validation
| 검증 | 기대 | 실측 | 판정 |
|---|---|---|---|
| total rows | 337 | 337 | PASS |
| blank | 325 | 325 | PASS |
| nonblank | 12 | 12 | PASS |
| blank resolvable (join) | 325 | 325 | PASS |
| blank unresolvable | 0 | 0 | PASS |
| broken lineage | 0 | 0 | PASS |
| duplicate atom | 0 | 0 | PASS |

Pre-Apply 데이터 게이트 = ALL PASS. 공란 325 전부 backfill 소스 확보.

## Apply 게이트 — Operator 확인 필요 사항
- is_readonly = TRUE: 런타임 저장소가 read-only로 표시됨. blank-only UPDATE가 (a) 정책/트리거로 차단될 수 있고 (b) 현행 freeze(RC1) 보호 대상. Apply 전 처리 방침(읽기전용 해제 절차 / freeze 갱신 순서)을 Operator가 지정해야 함.
- 위 확인 및 최종 실행 승인 후에만 STEP4 Apply(프로덕션 쓰기) 수행.
