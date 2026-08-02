# WO-IMPACT-001 — Final Report

## 최종 판정: MEDIUM_IMPACT

### 근거
- HIGH 아님: semantic/runtime/firing/applicability/article/evidence 전 dimension 무영향(327 전수, run_A 대조). 의무 적용·내용·근거는 정확하고 결정적. 시스템 기능·진단 결론에 위험 없음.
- LOW 아님: 결함이 제품의 핵심 출력인 법령명(법적 인용) 자체에 있으며, 109/300 프로파일(36.3%)·301 obligation(6.07%)에 노출. 법령 준수 진단 제품에서 상위 법령 오인용은 순수 cosmetic 이상.
- 따라서 MEDIUM: 운영/기능 관점 LOW + 사용자/법적 인용 정확성 관점 상승 -> 종합 MEDIUM.

### 영향 요약
- 영향 있음: law_name 라벨(23 atom), 사용자 표시·보고서 인용, repository 컬럼 정합성.
- 영향 없음: firing·applicability·semantic·article·evidence·runtime 로직·provenance·결정성.

### 성격
Metadata(법령명) 한정 결함. article·evidence 정확으로 의무 실체·근거는 보존.

### 판단 유의
등급(MEDIUM)은 제시된 근거에 기반한 분석 판단이며, 최종 수정 여부·범위(23/325 등)는 본 WO 범위가 아니라 WO-CHG-DECISION-001에서 Operator가 독립 결정한다. 본 보고서는 "고쳐야 할 정도의 영향인가"에 대한 증거를 제공할 뿐 수정안을 제시하지 않는다.
