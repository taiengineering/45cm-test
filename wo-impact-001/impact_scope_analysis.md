# IMPACT STEP2-3,7 — Scope Analysis (327 전수)

## STEP1 RCA<->Runtime 일치 검증
rca_lineage_327 (repo/joined/runtime) 대 run_A 출력 대조: runtime_law_name, law_article 전 327 일치. RCA의 collapse(L3 repo.law_name 컬럼)·분류(292/23/12)가 Runtime 결과와 정합. PASS.

## STEP2 dimension별 영향 (impact_atom_inventory.csv, 327 전수)
| dimension | impacted atoms | note |
|---|---|---|
| Label (law_name) | 23 | BLANK_DEFAULT_INCORRECT — 참법!=표시법 |
| Evidence | 0 | evidence 텍스트는 특정법 내용, 정확 |
| Article | 0 | law_article 전 327 정확 |
| Applicability | 0 | 전 obligation APPLICABLE |
| Atom firing | 0 | 327/327 발화, presence 300/300 |
| Semantic (obligation identity) | 0 | atom_id/source_atom_ids/obligation set 불변, A/B/C 결정적 |
| Runtime logic (routing) | 0 | 라벨은 발화·적용에 무관 |

## STEP3 분류 (327 전수)
- No Impact: 304 (292 blank-default-correct + 12 nonblank-inherited; 라벨 우연·정상 정확, 전 dimension 무영향)
- Metadata Impact: 23 (라벨만 오류, semantic/runtime 무영향)
- Semantic Impact: 0
- Runtime Impact: 0

## STEP7 영향 범위 계산 (수정 범위 아님)
- 오표기 라벨 atom = 23
- 공란 소스 atom = 315 (그 중 23이 오표기, 292는 default가 참값과 일치)
- repository 전체 = 337 (numeric 10 포함)
- 영향 성격 = Metadata (법령명 라벨) 한정, Semantic/Runtime 없음
- 런타임 노출 = 109/300 프로파일(36.3%), 301/4961 obligation 인스턴스(6.07%)
