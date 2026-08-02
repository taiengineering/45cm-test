# IMPACT STEP5 — 운영 영향 분석

| 영역 | 영향 | 근거 |
|---|---|---|
| Runtime (firing/applicability) | 없음 | 327/327 발화, 전 obligation APPLICABLE, 라벨은 로직에 무관 |
| Compiler/Evaluator | 없음 | atom 평가·obligation 생성 로직 라벨 미사용; A/B/C 결정적 동일 |
| Repository (데이터 무결성) | 국소 | law_name 컬럼 315 공란(비정규화 복사 미채움). atom_id/mapped_field/semantic_clause_id/evidence/article 무결 |
| Regression 위험 | 낮음 | 라벨 외 semantic 요소 불변 — 라벨만 다루는 변경이라면 회귀 표면적 최소(단, 이는 영향분석 관찰이지 수정안 아님) |
| 기존 결과(run_A/B/C) | 불변 | provenance/obligation set 동일, 결정적 |

## 운영 판단 근거 (STEP6)
- 운영 로직(발화·적용·라우팅)에는 영향 없음 -> 시스템 기능 관점에서 "반드시 수정" 압력은 낮음.
- 그러나 repository의 law_name 컬럼은 Source of Truth(law_master)와 불일치 상태로 동결되어 있어, 데이터 무결성/정합성 관점에서는 결함이 상존(런타임이 조인 대신 컬럼+default 사용).
- 즉 "기능적 필수 수정"은 아니나 "데이터 정확성 결함"은 실재. (수정 여부·범위는 본 WO 판단 아님 — CHG Decision 트랙.)
