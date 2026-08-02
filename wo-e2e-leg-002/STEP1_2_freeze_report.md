# WO-E2E-LEG-002 STEP1/2 — Freeze & Baseline (Goal G-msb2l2p0-5a2edf)

## STEP 2 Runtime Baseline (FROZEN)
- endpoint: https://leg-runtime-production.up.railway.app/rtm/evaluate
- expected provenance: release SEMREPO-RC1-2026.07.20 / freeze 15cd17e871b6885d34214c84a58adf47 / size 337
- repository_size CONFIRMED = 337 (DB vwlahtguyggrhvslabax.production_semantic_repository)
- distinct mapped_field = 39
- request contract = {"facility": {<mapped_field>: value}} (per LEG-001)

## STEP 1 Profile Universe (300) — Integrity Gate
- total profiles: 300  (anchor 112 + new coverage 188)      PASS(=300)
- duplicate profile_id: 0                                    PASS
- empty facility input: 0                                    PASS
- profile_id / selection_reason / input_checksum missing: 0  PASS
- uncovered mapped_field (True side): 0 / 39                 PASS (all COVERED, none BLOCKED)
=> STEP1 INTEGRITY GATE: PASS

## Engine & Anchor decisions (operator-confirmed)
- target engine = /rtm/evaluate (LEG runtime)
- anchor before (STEP6.1) = derive Expected from fixed RC1; NO prior LEG atom baseline; STEP6.1 = Expected comparison

## Coverage design (new 188)
- single_true x37 (all 36 boolean + is_multi_use)
- single_false x20 (previously-missing fields + is_multi_use)
- boundary x13 (worker_count / total_floor_area sweeps beyond anchor)
- zero_obligation x5
- multi_condition x113 (2-3 field combos, multi-atom/multi-law co-firing)

## Observations (registered, NOT analyzed/fixed in this WO)
- OBS-LEG002-001: 36 anchor profiles collapse to identical /rtm/evaluate input (300 profiles -> 278 distinct inputs). Non-mapped attributes (contract amount, industry, use-type) are outside the repo mapped_field contract.
- OBS-LEG002-002: 5 anchor input codes not in repo 39 (has_high_work, has_chemical_substance, has_sprinkler, has_mech_parking, boiler_capacity_kw) -> confirm unknown-handling at STEP4.

## Anchor input-duplicate groups (OBS-LEG002-001 detail)
PF-0002=PF-0071 | PF-0004=PF-0079 | PF-0007=PF-0039=PF-0077=PF-0087 | PF-0009=PF-0015 |
PF-0011=PF-0111 | PF-0020=PF-0021=PF-0084 | PF-0024=PF-0081 | PF-0025=PF-0082 |
PF-0030=PF-0036 | PF-0031=PF-0101 | PF-0041=PF-0059=PF-0060 | PF-0044=PF-0061 |
PF-0052=PF-0053=PF-0054=PF-0055=PF-0056=PF-0057 | PF-0069=PF-0073

## Next
- STEP 3: derive Expected Semantic per profile from fixed RC1 repository (atom_id / law / article / evidence / obligation_key), pre-execution.
- STEP 4: operator runs A/B/C on mac; JSON returned for STEP5-10 validation.
