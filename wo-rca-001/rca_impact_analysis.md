# RCA STEP7 — Impact Analysis

Verified against run_A full compare (327 atoms / 5,232 obligations, 300 profiles):

| dimension | impact | evidence |
|---|---|---|
| Atom (firing) | NONE | 327/327 atoms fire; presence match 300/300 |
| Applicability | NONE | all 5,232 APPLICABLE |
| Evidence | NONE | 0 empty; evidence = correct specific-law text (contradicts wrong label) |
| Article | NONE | law_article correct for all; 0 mismatch vs true |
| Semantic (obligation identity) | NONE | atom_id/source_atom_ids intact; obligation set deterministic A/B/C |
| law_name label | YES (23 atoms) | 23 output labels != true law (301 instances / 109 profiles) |
| Runtime behavior (routing/logic) | NONE | firing & applicability unaffected by label |

## Classification: METADATA ONLY
The defect is confined to the law_name metadata label. No semantic, evidence, article, applicability, atom-firing, or runtime-logic impact. User-facing consequence: 23-atom obligations display an incorrect law_name (legal misattribution risk), while article/evidence remain correct.
