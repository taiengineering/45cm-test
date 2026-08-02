# RCA STEP6 — OBS-R-01 / OBS-R-02 Relationship (evidence)

## Definitions
- OBS-R-01: runtime law_name vocabulary collapsed to 4 distinct across 327 atoms (315 blank-source defaulted + 12 short-form).
- OBS-R-02: 23 atoms whose runtime law_name (산안기준규칙) contradicts evidence-corroborated true law.

## Evidence
- All 23 OBS-R-02 atoms have repo.law_name = BLANK (rca_lineage_327.csv, class BLANK_DEFAULT_INCORRECT). Same mechanism as the other 292 blanks; they differ only in that their true (joined) law != the default.
- The 292 blank atoms whose true law IS 산안기준규칙 are indistinguishable in mechanism (blank->default) but happen to be correct.

## Judgment
OBS-R-02 ⊆ OBS-R-01 (proper subset). OBS-R-02 is exactly the subset of OBS-R-01's blank-source atoms where the hardcoded default masks a different true law. OBS-R-02 is not an independent defect; it is the visible-error portion of the single repository-materialization collapse (OBS-R-01).

Partition of 327: OBS-R-01 blank-source = 315 = [292 default-correct] ∪ [23 = OBS-R-02 default-incorrect]; plus 12 non-blank inherited (outside OBS-R-01's blank set, correct law short-form).
