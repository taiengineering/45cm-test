# OBS-R-01 — Law Name Collapse Root Cause Report (Goal G-msbdqx4l-78936b)

VERDICT (STEP10): CHG_REQUIRED (data-layer root cause proven & fixable) — runtime-module source confirmation BLOCKED (STEP4).

## STEP1 Census (frozen, run_A, no re-execution)
obligations 5,232 · distinct atom 327 · runtime law_name 4종 · 산안기준규칙 label 315 atoms · evidence-contradicting 23 atoms.

## Critical DB scope correction ("작업 DB ≟ 런타임 DB")
Catalog was built on vwlahtguyggrhvslabax (tai-api-prod). The runtime (leg-runtime-production) actually reads wrfcedzgdrfupenzqhur.production_semantic_repository (freeze 15cd17e8 / RC1 / 337 — matches run_A provenance). Root-cause analysis performed on the RUNTIME DB.

## STEP2/3 Layer Census (runtime DB wrfcedzgdrfupenzqhur) — 327 atom 전량
| layer | source | distinct law_name | state |
|---|---|---|---|
| L1 | production_semantic_repository.law_name (raw COLUMN) | 4 (315 blank + 고압가스법3/승강기법7/실내공기질법2) | COLLAPSED/BLANK |
| L2 | semantic_clause->law_article->law_master.law_name (JOIN) | 16 (327/327 resolved, 0 broken links) | INTACT |
| L5 | /rtm/evaluate obligation.law_name (run_A output) | 4 (산안기준규칙315 +3+7+2) | COLLAPSED (== L1 column + blank default) |

FIRST Collapse Point = L1 (repo.law_name COLUMN). distinct drops 16->4 at the column. The correct 16-law resolution EXISTS in the same runtime DB via join (L2 INTACT) but is NOT reflected in the column. Runtime output (L5) equals L1 column, NOT L2 join.

## STEP5 — 23 atom = OBS-R-01 하위 사례 (확정)
All 23 mismatch atoms: repo_law_name = (blank); joined_law_name = a specific law (어린이놀이시설안전관리법/수도법시행규칙/화학물질관리법/건설기계안전기준규칙/건설산업기본법/도시가스사업법(시행규칙)/정보통신공사업법/소방시설공사업법/석면안전관리법/건축법/산업안전보건법); runtime = 산안기준규칙 (default). article match YES, evidence present YES (evidence text is the specific-law text). Same blank-source->default mechanism as R-01. OBS-R-02 = OBS-R-01 하위 사례 확정.

## STEP6 — 327 classification (316 동일라벨 ≠ 316 오표기)
- CORRECT (default==true): 292 — blank source, defaulted to 산안기준규칙, true law IS 산안기준규칙.
- INCORRECT (default!=true): 23 — blank source, defaulted to 산안기준규칙, true law is a different specific law. 실제 오표기 = 23개.
- CORRECT (repo nonblank preserved): 12 — 고압가스법/승강기법/실내공기질법 preserved.
315 atoms carry 산안기준규칙 but only 23 are mislabeled; 292 are correctly 산안기준규칙 despite blank source.

## STEP7 — Responsibility Layer: MULTI_LAYER
- REPOSITORY_DATA (CONFIRMED, primary): production_semantic_repository.law_name column ingested collapsed — 315/327 blank, only 3 of 16 resolvable laws carried. Specific law names (available via law_master join) not populated into column.
- Runtime default-fill layer (behavior-CONFIRMED, module UNVERIFIED): blanks output as hardcoded 산업안전보건기준에 관한 규칙 rather than resolved via join. Confirmed by output<->DB comparison; exact source module NOT confirmed (STEP4 BLOCKED). Not attributed by speculation.

## STEP8 — Impact (verified vs run_A full compare)
firing NO IMPACT (327/327) · applicability NO IMPACT (all APPLICABLE) · evidence NO IMPACT (0 empty; correct specific-law text) · article NO IMPACT (0 mismatch) · law label IMPACT 23 atoms (301 instances/109 profiles) · user display wrong law_name for those · legal misattribution risk (citing 산안기준규칙 for clauses under other laws).

## STEP10 Verdict
CHG_REQUIRED. Real deterministic data-layer collapse (repo.law_name column) + runtime blank-default; correct data exists (law_master join) and is unused. Fix direction (NOT executed): populate law_name from law_master at ingest, OR runtime resolves via join instead of column+default. Runtime-module source confirmation BLOCKED — correct serving repo/branch required before CHG design pinpoints the runtime code.
EOF
