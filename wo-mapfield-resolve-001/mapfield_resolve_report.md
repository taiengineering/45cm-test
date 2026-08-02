# WO-MAPFIELD-RESOLVE-001 — 미관측 9개 mapped_field 정답 확정 (read-only)

## 결론 요약
- **CANDIDATE_ONLY 3** (실재 필드 있음, 법무 확인 후 확정 가능)
- **NO_VALID_FIELD 6** (대응 필드 부재 → 스키마/룰 설계 필요, 단순 재매핑 불가)
- **CONFIRMED_TARGET_FIELD 0** (100% 확정은 없음 — 후보 3개도 기존 필드 의미가 부분적으로만 일치)

## 상세 (STEP2~5)
### CANDIDATE_ONLY (3) — 필드 존재, 확인 권장
| atom | 조 | 트리거 | 후보 필드 | 유의 |
|---|---|---|---|---|
| 961c0ec1 | 산안49 | 높이 2m 작업 | has_high_place_work | 기존 필드는 art186 고소작업대(장비) 중심; 개념 일치하나 법무 확인 |
| 4b663c8e | 산안187 | 2m 화물차 상하차 | has_high_place_work | 동일 2m 트리거; 후보 타당 |
| 5b849b3e | 산안524 | 기압조절실 1인당 면적 | has_diving | 기압조절실이 has_diving/has_pressure_vessel에 분산 → 택1 확인 |

### NO_VALID_FIELD (6) — 대응 필드 부재, 설계 필요
| atom | 조 | 트리거 | 사유 |
|---|---|---|---|
| e665bb81 | 산안665 | 5kg 중량물 인력 | 수동취급 필드 없음(기계 필드만 존재) |
| fdb63aa2 | 응급의료8 | 응급환자 2명 우선순위 | 응급의료 대응 필드 없음(방송·발전기 장비뿐) |
| 1d6a70e6 | 근기56 | 야간근로 가산임금 | 상시적용 근로조건; always/labor 필드 없음 |
| cfbfa1fb | 근기60 | 1년미만 유급휴가 | 상동 |
| bca5d9ca | 근기60 | 연차 15일 | 상동 |
| acc26661 | 근기75 | 육아 수유시간 | 상동 |

## 판정과 다음 단계 (STEP7)
- 단순 mapped_field 재매핑(CHG)으로 해결 가능한 것은 **최대 3개(CANDIDATE_ONLY)** 뿐이며, 그것도 법무 확인이 선행되어야 함.
- **6개는 재매핑 불가** — 입력 스키마에 대응 필드가 없어, 스키마/룰 확장(예: has_manual_handling, 응급의료 필드, 상시적용 표현) 설계가 필요.
- 따라서 다음 WO-CHG-MAPFIELD-001은 '9개 일괄 재매핑'이 아니라: (a) CANDIDATE 3개 법무 확인 후 재매핑, (b) NO_VALID_FIELD 6개는 별도 스키마 설계 WO로 분리, 로 나눠야 함.
- 337/337 전달 CONFIRMED는 이 설계·재매핑·재관측 이후 가능. (전달 메커니즘 자체는 328건 0-drift로 이미 건전)

## 미확인 (명시)
- CANDIDATE 3개의 최종 정답은 법령 해석·Operator 확인 필요(본 WO는 후보까지만).
- 런타임이 worker_count-mapped atom을 애초 발화시키는 경로 유물는 코드분석 영역(범위 밖).
