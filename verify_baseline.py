import json, glob
def ac(d, pid):
    fs = glob.glob(f"{d}/SNAP-{pid.split('-')[1]}-001.json")
    if not fs: return None
    s = json.load(open(fs[0], encoding="utf-8"))
    return (s.get("response") or {}).get("partialResult", {}).get("applicable_count")
pids = ["PF-0020","PF-0023","PF-0027","PF-0030","PF-0031","PF-0032","PF-0033","PF-0034","PF-0036","PF-0038","PF-0021","PF-0019","PF-0001"]
print(f"{'pid':9} {'old_before':>10} {'after':>7} {'new_before(main,seq)':>20}  판정")
same_after = same_old = 0
for pid in pids:
    ob = ac("before_clean", pid); af = ac("after_obs003", pid); nb = ac("newbefore_seq", pid)
    tag = ""
    if nb == af and nb != ob: tag = "A: after와 일치, old와 다름 (오염 확정 지지)"; same_after += 1
    elif nb == ob and nb != af: tag = "B: old와 일치 (오염 재현 → RootCause 재검토)"; same_old += 1
    elif nb == af == ob: tag = "동일(편차 아니었음)"
    else: tag = "혼합"
    print(f"{pid:9} {str(ob):>10} {str(af):>7} {str(nb):>20}  {tag}")
print(f"\n요약: new==after&!=old = {same_after} / new==old = {same_old} / 총 {len(pids)}")
