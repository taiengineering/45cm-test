#!/usr/bin/env python3
# WO-E2E-LEG-002A STEP3 — Presence Oracle (INDEPENDENT)
# oracle_source: production_semantic_repository (+semantic_clause/law_master/law_article) -> e2e_leg_atom_map.csv (frozen SQL export, 327 atoms)
# oracle_algorithm: Expected(input) = { atom : atom.mapped_field in TrueFields(input) }
#   TrueFields = { code : facility[code] is boolean True }  (numeric EXCLUDED, false/absent EXCLUDED, unknown codes have no atoms)
# runtime_code_reused = FALSE (no /rtm/evaluate call, no compiler import, no response reverse-derivation)
# Numeric fields (worker_count,total_floor_area / 10 atoms) are NOT in Expected -> STEP4 empirical observation only.
import csv,json
NUMERIC={'worker_count','total_floor_area'}
atoms=list(csv.DictReader(open('e2e_leg_atom_map.csv')))
by_field={}
for a in atoms: by_field.setdefault(a['mapped_field'],[]).append(a)
ATOM_FIELDS=set(by_field)
uni=list(csv.DictReader(open('e2e_300_profile_universe_v2.csv')))
out=[]
for p in uni:
    fac=json.loads(p['input_payload'])['facility']
    true_fields=sorted(k for k,v in fac.items() if v is True and k in ATOM_FIELDS)
    exp=[a for f in true_fields for a in by_field[f]]
    exp_ids=sorted(a['atom_id'] for a in exp)
    law_set=sorted({f"{a['law_name']} 제{a['law_article']}조" for a in exp})
    out.append({'profile_id':p['profile_id'],'anchor_or_new':p['anchor_or_new'],'profile_type':p['profile_type'],
        'true_fields':';'.join(true_fields),'expected_atom_count':len(exp_ids),
        'expected_atom_ids':';'.join(exp_ids),'expected_law_articles':' | '.join(law_set),
        'oracle_model':'PRESENCE','runtime_code_reused':'false','independence':'INDEPENDENT'})
cols=['profile_id','anchor_or_new','profile_type','true_fields','expected_atom_count','expected_atom_ids','expected_law_articles','oracle_model','runtime_code_reused','independence']
with open('e2e_300_expected_semantic.csv','w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); [w.writerow(r) for r in out]
# STEP3 exit: 300 expected, numeric NOT in expected, single_true == field atom_count
assert len(out)==300
assert not any(a['mapped_field'] in NUMERIC for a in atoms)
print('STEP3 READY_FOR_STEP4: 300 expected, presence, independent, numeric excluded')
