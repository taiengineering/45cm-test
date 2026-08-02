# WO-CHG-001: extract_meta를 preview(rules_table) → full(*_required) 집계로 교체
# Runner only. Snapshot 구조 불변. Engine/Rule/Query 무관.
import re
src = open("e2e_runner_all.py", encoding="utf-8").read()

new_func = '''def extract_meta(body):
    """Snapshot 메타데이터 수집 (판정 없음, 사실만).
    WO-CHG-001: preview(rules_table) 대신 full 의무(*_required)를 집계한다.
    스냅샷 구조는 바꾸지 않는다(response 전체는 그대로 저장).
    """
    if not isinstance(body, dict): return {}
    r = body.get("partialResult") or {}
    REQ = ("appointment_required", "inspection_required", "action_required", "report_required")
    full = []
    for fld in REQ:
        for x in (r.get(fld) or []):
            if isinstance(x, dict):
                full.append({
                    "cat": fld.replace("_required", ""),
                    "law_name": (x.get("law_name") or x.get("law") or "").strip(),
                    "obligation_summary": (x.get("obligation_summary") or x.get("title")
                                           or x.get("description") or x.get("name") or "").strip(),
                })
    laws = set(r.get("law_badges") or [])
    evidence = sum(1 for x in full if x["obligation_summary"] and x["law_name"])
    s = r.get("summary") or {}
    return {
        "obligation_total": r.get("applicable_count") or s.get("total") or 0,
        "law_count": len(laws),
        "rule_count": len(full),          # full 집계 (preview 아님)
        "full_count": len(full),          # 명시적 full 카운트
        "evidence_count": evidence,       # full 기준
        "preview_count": len(r.get("rules_table") or []),  # 참고용(정보)
        "risk_level": r.get("risk_level"),
        "engine_version": r.get("engine_version"),
        "summary": s,
    }'''

# 기존 extract_meta 함수 블록을 통째로 교체 (def extract_meta ... 다음 def 전까지)
pat = re.compile(r"def extract_meta\(body\):.*?(?=\ndef )", re.S)
if not pat.search(src):
    raise SystemExit("extract_meta 블록을 찾지 못함 — 수동 확인 필요")
src2 = pat.sub(new_func + "\n\n", src, count=1)
open("e2e_runner_all.py", "w", encoding="utf-8").write(src2)
print("extract_meta 교체 완료")
