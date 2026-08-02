# WO-E2E-LEG-002A STEP5 — Expected Oracle Independence Contract (FROZEN)

## oracle_source
production_semantic_repository (DB vwlahtguyggrhvslabax), read directly via SQL:
  SELECT atom_id, mapped_field, semantic_clause_id, law_name, law_article, evidence
Join semantic_clause ONLY for law_article/evidence text (no condition evaluation).
No other engine artifact is consulted.

## oracle_algorithm  (atom_id-level, deterministic set membership)
TrueFields(input) =
   { code : input.facility[code] == true }                       # explicit boolean true
 U { f in {worker_count, total_floor_area} : f present in input } # numeric = presence
Expected(input) = { atom_id : repo.atom.mapped_field in TrueFields(input) }
- boolean false OR absent  => field NOT in TrueFields => its atoms do NOT fire
- null-mapped (always-on) atoms = 0  (verified: 337 = sum atom_count over 39 fields) => no unconditional set
- is_multi_use firing cross-checked against WO-E2E-LEG-001 live result (실내공기질법 제5·12조, 2 atoms)

## runtime_code_reused = false
- NO call to /rtm/evaluate
- NO import/reuse of leg-runtime compiler / applicability / presentation functions
- NO reverse-derivation from any runtime response
- Oracle is a standalone Python script: SQL read + Python set membership only

## independence_status = INDEPENDENT

## numeric_threshold = NONE_IN_REPO  (FINDING — deviates from WO-002A STEP3 premise)
- production_semantic_repository has NO condition/operator/threshold column
  (columns: atom_id, mapped_field, semantic_clause_id, law_name, law_article, evidence, version/freeze/loaded_at)
- semantic_clause.condition_text is free-text Korean NL and is frequently NULL;
  for mapped_field=worker_count the 9 atoms' conditions are heterogeneous and UNRELATED to worker-count value
  (제49조 높이2m / 제665조 5kg / 제187조 화물2m / 제56조 야간 / 제60조 유급휴가 ...).
- Therefore structured thresholds (t-1/t/t+1) are NOT extractable from the repository.
- Oracle fires numeric-field atoms on PRESENCE, not on value.
- Numeric boundary semantics are OUT_OF_ORACLE_SCOPE and deferred to EMPIRICAL STEP-4 observation:
  the value-diversity profiles (ZERO/MIN/LOW/MID/HIGH/MAX) are compared post-hoc; any value-dependent
  firing difference the runtime shows is recorded as an Observation (it is the E2E signal, not the oracle's job).

## caveat
If STEP-4 shows runtime firing != presence model (exclusions, thresholds, sector gates),
those deltas are Observations. The presence oracle remains the declared independent Expected baseline;
divergence is exactly what this E2E is designed to surface.
