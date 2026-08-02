# WO-CHG-010B STEP4 — Runtime Target Verify Report

## STEP4-1 Target Profile Set (고정, 23 atom 전수 커버 · 누락 0)
기존 run_A + rca_lineage 기반 greedy set-cover. 신규 Profile 생성 없음.

| profile_id | 커버 atom 수 | request_payload (/rtm/evaluate) |
|---|---|---|
| PF-2109 | 11 | {"facility":{"has_excavation":true,"has_subcontractor":true,"worker_count":300}} |
| PF-2174 | 8 | {"facility":{"has_crane":true,"has_gas":true,"has_scaffold":true,"has_water_tank":true,"worker_count":450}} |
| PF-2162 | 3 | {"facility":{"has_asbestos":true,"has_chemical":true,"has_confined_space":true,"has_welding":true,"worker_count":300}} |
| PF-0099 | 1 | {"facility":{"has_crane":true,"has_demolition":true,"worker_count":75}} |

합계 23 atom / 4 profile. 상세 매핑: chg010_target_profile_set.csv.

## STEP4-2 실행 (Operator, 기존 Mac 러너)
위 4개 payload를 기존 러너로 /rtm/evaluate 호출. 새 러너·경로 변경 금지. 각 응답의 obligations[].{atom_id, law_name, law_article, evidence, applicability}만 수집.

## STEP4-3 대조 대상 (23 atom, expected)
before = '산업안전보건기준에 관한 규칙' (전 23 동일). expected(참법)·article:
- 건설산업기본법: 3c8a09fa(38) c5e81202(35) e16a2391(36) f7bb266f(37)
- 소방시설공사업법: 4a63de61(22) fd6d8b7d(21)
- 정보통신공사업법: 8802a9d1(26) a4b8422b(31)
- 도시가스사업법: dd5c7383(30) 1ba2c57e(30) 1d248a2e(12) 5e4057a7(17) 9c66dac6(41)
- 도시가스사업법 시행규칙: a233cece(15) cacdac8d(20)
- 산업안전보건법: d7be3706(38)
- 건축법: f13a858e(41)
- 건설기계 안전기준에 관한 규칙: ae0a74ad(125)
- 수도법 시행규칙: ce59b35c(22)
- 석면안전관리법: 886a5841(22)
- 화학물질관리법: a0098d92(44) e843bdd4(31)
- 어린이놀이시설 안전관리법: 21d45eb4(16)

## STEP4-4 판정 규칙 (WO-CHG-010A 고정)
- PASS: 23/23 law_name 교정(=expected) + atom_id/article/evidence/applicability/obligation count 동일.
- STALE_RUNTIME: Repository는 교정됐으나 Runtime law_name이 기존('산안기준규칙') 유지, 그 외 출력 동일 -> 즉시 Rollback 아님. 런타임 재적재 필요 상태로 기록 -> 승인된 Freeze/Reload 절차 -> 동일 23 재검증.
- FAIL: atom 누락/article/evidence/applicability/obligation count 변화/기타 Semantic 변화 -> 중단, Rollback Gate.

## 상태
STEP4-1 완료(고정). STEP4-2 Operator 실행 대기. STEP4-3/4는 Operator 출력 수령 후 Claude가 전수 대조.
