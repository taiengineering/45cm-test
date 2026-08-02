# IMPACT STEP9 — Impact Summary

## 무엇에 영향이 있는가
- law_name(법령명) 라벨: 23 atom / 301 obligation 인스턴스 / 109(36.3%) 프로파일에서 오표기.
- 사용자 표시·보고서의 상위 법령명 인용 정확성.
- repository law_name 컬럼의 데이터 정합성(Source of Truth 불일치).

## 무엇에는 영향이 없는가
- atom firing, applicability, obligation identity(semantic), article, evidence — 전 327 무영향.
- runtime 로직/라우팅, compiler/evaluator, provenance, A/B/C 결정성.
- 진단 결론(의무 적용/미적용)과 의무 내용.

## 운영 영향
기능 무영향(로직·발화·적용 정상). 데이터 정합성 결함은 상존(컬럼 vs law_master).

## 사용자 영향
36.3% 프로파일에서 23종 obligation의 상위 법령명이 틀리게 표시. article·evidence는 정확.

## 법적 영향
법령명 인용 정확성 결함. 단 조문·근거 문언·적용 판단은 정확 -> 실체적 오진단 아님, 인용 라벨 오류.
