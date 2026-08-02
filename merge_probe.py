import json, glob
from collections import defaultdict
s = json.load(open(glob.glob('before_clean/SNAP-0019-001.json')[0], encoding='utf-8'))
r = (s.get('response') or {}).get('partialResult') or {}
REQ = ('appointment_required', 'inspection_required', 'action_required', 'report_required')
out = []
n = sum(len(r.get(f) or []) for f in REQ)
out.append(f'PF-0019 *_required total={n} applicable_count={r.get("applicable_count")}')
# 첫 항목 키
for f in REQ:
    arr = r.get(f) or []
    if arr:
        out.append(f'{f} keys: {list(arr[0].keys())}')
        break
# 중복 그룹
items = []
for fld in REQ:
    for x in (r.get(fld) or []):
        if isinstance(x, dict):
            items.append((fld, x))
g = defaultdict(list)
for fld, x in items:
    key = (x.get('law_name'), x.get('law_article'), x.get('obligation_summary'))
    g[key].append((fld, x))
KEYS = ('rule_id', 'then_action_token', 'inspection_cycle_value', 'inspection_cycle_unit_code',
        'condition_code', 'condition_value', 'source_action_family', 'rule_type', 'category')
dupn = sum(1 for k, v in g.items() if len(v) > 1)
out.append(f'중복 그룹 수: {dupn}')
for key, rows in g.items():
    if len(rows) > 1:
        out.append(f'== {key[0]} / {key[1]} / {str(key[2])[:45]} (x{len(rows)}) ==')
        for fld, x in rows:
            fields = {k: x.get(k) for k in KEYS if x.get(k) not in (None, '', 0)}
            out.append(f'   [{fld.replace("_required","")}] {fields}')
open('merge_probe_out.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('wrote merge_probe_out.txt lines=', len(out))
