# RCA STEP8 — Root Cause (analysis only; no remediation)

## 무엇이 발생했는가 (WHAT)
런타임 출력의 법령명(law_name)이 327 atom에서 4종으로 축소되어 나타나며, 그 중 23 atom은 실제 법령(어린이놀이시설안전관리법·수도법시행규칙·화학물질관리법·건설기계안전기준규칙·건설산업기본법·도시가스사업법(시행규칙)·정보통신공사업법·소방시설공사업법·석면안전관리법·건축법·산업안전보건법)이 아닌 '산업안전보건기준에 관한 규칙'으로 표기된다.

## 왜 발생했는가 (WHY)
production_semantic_repository는 law_name을 자체 컬럼으로 복사·동결(materialized/frozen)하는 비정규화 스냅샷이다. 이 컬럼이 build/freeze 시점에 law_master로부터 채워지지 않아 327 중 315행이 공란으로 남았다(12행만 short-form 보유). 런타임은 이 컬럼을 그대로 읽고, 공란은 하드코딩 default('산업안전보건기준에 관한 규칙')로 채운다. 정답은 law_master 조인으로 327/327 존재하나(16종), 컬럼에 반영되지 않았고 런타임은 조인을 사용하지 않는다.

## 어느 계층에서 발생했는가 (WHERE)
- 최초 정보 손실 계층: L3 production_semantic_repository.law_name 컬럼 population (repository materialization).
- 증폭 계층: L4 runtime 공란→default-fill (표면 증상).
- Join(L0–L2)은 INTACT — 원인 아님.

## 영향 범위 (SCOPE)
- 327 semantic atom 중 출력 라벨 오표기 = 23 (블랭크 default가 실제 법과 불일치).
- 블랭크 default가 우연히 참값과 일치 = 292 (표기상 정확).
- 비블랭크 보존 = 12 (short-form, 정확 법).
- Metadata(law_name label) 한정. atom firing/article/evidence/applicability 무영향.

## 확인된 사실 (CONFIRMED)
- L2-join distinct=16, L3-column distinct=4, L4-output distinct=4 (측정).
- 315/327 repo.law_name 공란; 327/327 조인 해상; broken link 0.
- 런타임 출력 == L3 컬럼 + 공란 default (23 atom evidence가 특정법 내용과 일치, 라벨만 산안기준규칙).
- A/B/C 결정적 — 무작위 아님, 데이터 고정 상태의 결과.

## 확인되지 않은 사실 (UNCONFIRMED)
- production_semantic_repository를 build/freeze한 코드가 law_name을 왜 공란으로 남겼는지(누락 로직·의도 여부)는 소스 미특정으로 미확인(WO-OBS-006-001 STEP4 BLOCKED).
- 런타임 default-fill의 정확한 코드 위치(loader vs assembler)도 미확인 — 단, 행위는 출력·DB 대조로 확인.

(해결방법·수정범위는 본 WO 범위 아님.)
