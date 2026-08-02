# WO-CHG-010A — CHG Scope Matrix (STEP2)

## 변경 정의 (기존 WO 인용, 신규 분석 없음)
| 항목 | 값 |
|---|---|
| 변경 컬럼 | production_semantic_repository.law_name |
| 변경 행 수 | 325 (blank-only; 라이브 실측 blank 325) |
| 변경 전 | NULL 또는 공백('') |
| 변경 후 | law_master 조인값 COALESCE(lm.law_name, lm.law_name_short) |

## 영향 받는 컬럼
- law_name (해당 325행만)

## 영향 받지 않는 컬럼 (불변)
- atom_id · mapped_field · semantic_clause_id · evidence · law_article
- is_readonly · freeze_signature · release_version · repository_version (freeze는 STEP6에서 별도 갱신)
- 비공란 12행의 law_name (보호)

## Scope 밖 (검토 대상 아님)
Runtime Logic · Semantic · Compiler · Pattern · Rule · Evidence · Applicability
