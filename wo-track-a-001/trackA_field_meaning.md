# WO-TRACK-A-001 STEP2 — 후보 입력필드 의미 (기존 발화 atom 기준)

## has_high_place_work (4 atoms)
- 기존 사용처: 전부 **산안규칙 제186조 고소작업대**(설치/사용/이동/이송).
- 필드명 의미: "고소작업(high place work)" 일반.
- 관찰: 이름은 일반 고소작업이나, 실제 매핑된 atom은 고소작업대(장비)에 한정.
- 해석 유의: 필드의 정확한 정의(고소작업 일반 vs 고소작업대 장비)는 repository에 없음 → name+usage 기반 추론. 입력모델 정의로 최종 확정 권장.

## has_diving (25 atoms)
- 기존 사용처: 잠수작업 다수 + **기압조절실/고압작업**(art525 공기청정장치, art532/533 기압조절실 가압/감압, art528 계열 등).
- 필드명 의미: "잠수(diving)"이나 실제로는 잠수+고압(기압조절실) 통합 커버.
- 관찰: 기압조절실 obligation이 이미 has_diving에 다수 존재 → 기압조절실 신규 atom도 has_diving에 부합.
- 유의: 기압조절실 일부는 has_pressure_vessel에도 존재(분산). has_diving이 기압조절실 다수 포함(우세).
