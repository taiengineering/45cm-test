# RCA STEP3-4 — Layer Census & Collapse Point

## Layer responsibility (STEP1, evidence: information_schema + row counts)
- L0 law_master (768): authoritative law identity (law_name, law_name_short).
- L1 law_article (35,412): article under a law (article_no), FK law_id->law_master.
- L2 semantic_clause (58,495): decomposed clause, FK source_article_id->law_article. Carries NO law_name (by design).
- L3 production_semantic_repository (337): runtime read-source. Holds its OWN COPIED columns law_name/law_article/evidence + freeze_signature/loaded_at. A denormalized, frozen projection keyed by atom_id/semantic_clause_id.
- L4 runtime /rtm/evaluate output: obligation.law_name populated from L3 repo.law_name column.

## Layer Census (law_name), 327 atom 전수 (rca_layer_census.csv)
- L0->L1->L2: authoritative law_name reachable via join (semantic_clause_id->source_article_id->law_id->law_master). 327/327 resolve non-null (16 distinct laws). INTACT.
- L3 repo.law_name COLUMN: 315/327 BLANK, 12 non-blank (3 laws, short-form). distinct=4. Information LOSS occurs here: the copied column was not populated from law_master for 315 rows.
- L4 output: reads L3 column; blanks surfaced as hardcoded default 산업안전보건기준에 관한 규칙. distinct=4 (== L3 column).

## STEP4 — Collapse Point (evidence only)
Candidates: Repository / Join / Assembler / Presentation / Runtime Output.
- Join (L0-L2): INTACT (327/327 resolve, 16 laws). NOT the collapse.
- Runtime Output (L4): faithfully reflects L3 column (distinct 4 == 4); adds only a blank-default. Surface symptom, not origin.
- Repository materialization (L3): the law_name COLUMN was populated blank for 315/327 at build/freeze time despite law_master carrying correct names. FIRST layer where law_name information is lost (distinct 16->4).

Collapse Point = L3 production_semantic_repository.law_name column population (repository materialization/build), not the join and not the runtime resolver. The runtime default-fill is a downstream amplifier.

## Confirmed by evidence
- distinct law_name: L2-join=16, L3-column=4, L4-output=4 (measured, wrfcedzgdrfupenzqhur).
- broken join links=0; 327/327 resolvable.
- 12 non-blank rows carry short-form names; no blank row resolves to those 3 laws (no dual-naming).

## NOT confirmed (evidence gap)
- WHY the build left law_name blank (the materialization/build code populating production_semantic_repository is not located this session — WO-OBS-006-001 STEP4 BLOCKED). The collapse LAYER (L3 column) is confirmed by data; the build CODE line is not.
