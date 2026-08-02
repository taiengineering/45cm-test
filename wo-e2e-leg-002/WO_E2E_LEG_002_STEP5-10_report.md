# WO-E2E-LEG-002 / 002A — STEP5-10 Runtime Validation Report (Goal G-msb2l2p0-5a2edf)

VERDICT: **CONDITIONAL PASS**
Core E2E (atom firing -> evidence -> determinism -> provenance) is correct and deterministic across 300 profiles.
CONDITIONAL on one registered semantic anomaly (OBS-LEG002-004, law_name mislabel). No CHG in this WO.

## Inputs (frozen)
- Universe: e2e_300_profile_universe_v2.csv (300 unique runtime inputs)
- Oracle: e2e_300_expected_presence.csv (Presence, independent; runtime_code_reused=false)
- Runtime: /rtm/evaluate (operator Mac), runs A/B/C
- Runtime baseline: RC1 / freeze 15cd17e8 / repository_size 337 (single provenance across A/B/C)

## STEP4 Execution
300/300 OK, http_fail 0, provenance single = [SEMREPO-RC1-2026.07.20, 15cd17e871b6885d34214c84a58adf47, 337] for A, B, C.
applicability = APPLICABLE for all 5,232 obligations (RUN A). Schema: obligations[{atom_id, mapped_field, law_name, law_article, evidence, applicability, triggered_by}] + contract + provenance.

## STEP5 Semantic Review (300, Presence Oracle)
- Boolean/is_multi_use: 300/300 MATCH -- missing 0, unexpected 0.
- Atom coverage: 327/327 catalog atoms fired at least once (never-fired 0).
- mapped_field mismatch 0; empty evidence 0.
- Boolean presence model CONFIRMED: field=true -> all its atoms fire; field=false/absent -> none.

## STEP6 Before/After
No prior LEG atom baseline -> Before = Expected (Presence). Anchor (90 reps) + new (210) both MATCH Expected. No regression.

## STEP7 Determinism / Regression (A/B/C)
300/300 DETERMINISTIC on (atom_id + evidence + applicability + law_name + law_article). ORDER_ONLY 0, SEMANTIC_VARIANCE 0, obligation_count diff 0.

## STEP4-Responsibility Numeric (empirical, per DECISION)
- total_floor_area atom (제19조): fires iff worker_count>=50 OR total_floor_area>=400 -- 0 violations / 300 (fired 271 / not 29).
- worker_count-mapped atoms (9): 0 firings (조건 높이2m/중량5kg/야간 unmet).
- Runtime DOES condition-evaluate numerics -> OBS-LEG002-003 (Observation, not FAIL). Boolean Presence Oracle unaffected.

## STEP4 Unknown contract
contract.unknown captured: has_sprinkler 16, has_high_work 8, has_chemical_substance 8, has_mech_parking 4, boiler_capacity_kw 1. No auto-alias. OBS-LEG002-002. Correct handling.

## STEP5 SEMANTIC anomaly (KEY FINDING) -- OBS-LEG002-004
Runtime labels 23 atoms (8 fields) law_name="산업안전보건기준에 관한 규칙" contradicting own evidence + article. True laws (evidence-corroborated, matches independent catalog via law_master join): 어린이놀이시설안전관리법, 수도법 시행규칙, 화학물질관리법, 건설기계 안전기준에 관한 규칙, 건설산업기본법, 도시가스사업법 / 시행규칙, 정보통신공사업법, 소방시설공사업법, 석면안전관리법, 건축법, 산업안전보건법. Runtime's own evidence is the specific-law text -> internal inconsistency (law_name vs evidence). atom_id/article/evidence/applicability/firing correct; label only. Deterministic A/B/C. Detail: e2e_law_name_mismatch.csv. SEMANTIC_MISMATCH. Separate CHG WO recommended; NOT fixed here.

## STEP8 QA
Structural census 300/300 (obligations+provenance+contract present). Anomaly review 100% (full census, not sampled).

## STEP9 Observation Inventory (registered, no CHG) -- e2e_observation_inventory_v2.csv
- OBS-LEG002-001 (INFO) anchor dup inputs -- resolved in v2 appendix.
- OBS-LEG002-002 (INFO) unknown codes -- correct contract.unknown handling.
- OBS-LEG002-003 (INFO) numeric value-dependent firing.
- OBS-LEG002-004 (SEMANTIC_MISMATCH) law_name mislabel, 23 atoms -- separate CHG WO.

## STEP10 Verdict
CONDITIONAL PASS. Runtime delivers correct, deterministic obligations for all 300 profiles with single RC1 provenance; Presence Oracle validated 300/300 on booleans, 327/327 atom coverage. CONDITIONAL solely on OBS-LEG002-004 (law_name attribution), deterministic and scoped to a follow-up CHG WO. Numeric/unknown are Observations per DECISION, not failures. Code/DB/Pipeline changes: 0.

## Deliverables
e2e_300_run_A/B/C.json (operator) - e2e_300_semantic_review_A.csv - e2e_law_name_mismatch.csv - e2e_observation_inventory_v2.csv - this report.
