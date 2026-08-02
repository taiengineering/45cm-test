# WO-CHG-010A — Verification Plan (STEP5-6) [rev.1 보완]

## STEP5 CHG 이후 반드시 재검증할 항목만 (무관 검증 제거)
1. Repository Verify — blank 0(대상), 비공란 12 unchanged, 337행, law_name 외 컬럼 불변.
2. Runtime Verify — 실제 /rtm/evaluate 출력 기준: 23 atom law_name==조인(변경 반영 확인), article/evidence/applicability/atom_id 불변 (mismatch 23->0). Repository만 바뀌고 Runtime 출력 동일 시 FAIL.
3. Regression (300) — baseline 대비 아래 허용 변화만.
4. Freeze Verify — 새 release/freeze 발급 확인(RC1 유지 불가).

제거된(무관) 검증: Compiler 재빌드·Rule/Pattern 재도출·Evidence 재생성 — NOT_TARGET.

## Regression 허용 변화 (고정) [보완 #2]
다음 4개만 변화 허용:
- law_name (23 atom 교정)
- release (release_version 갱신)
- freeze (freeze_signature 갱신)
- provenance (변경 이력/출처 메타)

-> 위 4개 외의 모든 변화는 FAIL. 특히 Semantic·Evidence·Article·Applicability·Obligation Count·Determinism 변화 = 즉시 FAIL.

## STEP6 최종 Success Matrix
| 항목 | 대상 | 성공 기준 |
|---|---|---|
| Repository | law_name | 대상 blank 0, 12 unchanged, 337행, 타 컬럼 불변 |
| Runtime | label (실행 출력) | /rtm/evaluate에서 23 mismatch -> 0 (미반영 시 FAIL) |
| Metadata | 법령명 인용 | 23 atom 정확(36.3% 프로파일 회복) |
| Semantic | obligation identity | NOT_TARGET (drift 0 = 가드레일) |
| Evidence | evidence | NOT_TARGET (불변) |
| Article | law_article | NOT_TARGET (불변) |
| Applicability | applicability | NOT_TARGET (불변) |
| Rule/atom | atom firing | NOT_TARGET (불변) |
| Compiler | compiler | NOT_TARGET |
| Determinism | A/B/C | 유지 (가드레일) |
| Freeze | release/freeze | 새 발급 (RC1 미유지) |

## Rollback 조건 (고정) [보완 #3]
다음 중 하나라도 발생하면 즉시 Rollback (스냅샷 md5 fc0ae59209770214d3e15c86dd8cc889 / 사전 백업 기반 원복):
- mismatch 잔존 (23 중 하나라도 교정 미반영)
- obligation count 변화
- evidence 변화
- article 변화
- firing(atom 발화) 변화
- determinism(A/B/C) 변화
- (추가 가드) 비공란 12 변경 또는 행수 != 337 또는 law_name 외 컬럼 변경

Rollback 발생 시 STEP10 판정 = ROLLBACK, freeze는 원 상태(RC1) 복원.
