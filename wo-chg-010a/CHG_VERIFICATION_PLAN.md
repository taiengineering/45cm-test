# WO-CHG-010A — Verification Plan (STEP5-6)

## STEP5 CHG 이후 반드시 재검증할 항목만 (무관 검증 제거)
1. Repository Verify — blank 0(대상), 비공란 12 unchanged, 337행, law_name 외 컬럼 불변.
2. Runtime Verify — 23 atom law_name==조인, article/evidence/applicability/atom_id 불변 (mismatch 23->0).
3. Regression (300) — baseline 대비 허용 변화 = 23 law_name 교정 + 새 provenance뿐; Semantic/Evidence/Article/Applicability/Obligation Count/Determinism 불변.
4. Freeze Verify — 새 release/freeze 발급 확인(RC1 유지 불가).

제거된(무관) 검증: Compiler 재빌드·Rule/Pattern 재도출·Evidence 재생성 — 이번 CHG와 무관(NOT_TARGET).

## STEP6 최종 Success Matrix
| 항목 | 대상 | 성공 기준 |
|---|---|---|
| Repository | law_name | 대상 blank 0, 12 unchanged, 337행, 타 컬럼 불변 |
| Runtime | label | 23 mismatch -> 0 |
| Metadata | 법령명 인용 | 23 atom 정확(36.3% 프로파일 회복) |
| Semantic | obligation identity | NOT_TARGET (drift 0 = 가드레일) |
| Evidence | evidence | NOT_TARGET (불변) |
| Article | law_article | NOT_TARGET (불변) |
| Applicability | applicability | NOT_TARGET (불변) |
| Rule/atom | atom firing | NOT_TARGET (불변) |
| Compiler | compiler | NOT_TARGET |
| Determinism | A/B/C | 유지 (가드레일) |
| Freeze | release/freeze | 새 발급 (RC1 미유지) |
