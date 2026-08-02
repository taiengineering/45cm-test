# WO-RUNTIME-COVERAGE-001 — 미관측 9 atom 미발화 원인 확정

## 관측 사실 (read-only, 9개 조건 + 대조 1개)
- Repository 컬럼에 조건(operator/threshold) 컬럼 없음 -> 수치 조건은 RC1에 부재(Presence-only Oracle 일치).
- mapped_field=worker_count atom = repository 전체에서 정확히 9개 -> 전부 미발화(1~1000 전 밴드).
- mapped_field=total_floor_area atom = 1개(0ce68131, "연면적 400㎡ 이상") -> **정상 발화**.
  즉 "numeric이라 미발화"가 아니라 worker_count 필드에 한정된 미발화.

## 결정적 증거: mapped_field 의미 오매핑
9개 atom의 evidence(실제 법적 조건)는 worker_count와 무관:
- 근로기준법 56/60/60/75: 야간근로·유급휴가·연차·수유시간 (근로조건, 인원수 임계 아님)
- 산안규칙 49: 높이 2m 이상 작업 -> 실제 필드 has_height_work
- 산안규칙 187: 2m 이상 화물차 상하차 -> has_height_work/loading
- 산안규칙 665: 5kg 이상 중량물 인력 -> has_lifting
- 산안규칙 524: 기압조절실 1인당 면적 -> has_high_pressure/diving
- 응급의료 8: 응급환자 2명 이상 우선순위 -> emergency

-> 이들은 worker_count가 아니라 높이/중량/기압/근로조건/응급 조건으로 발화해야 함.
worker_count로 매핑되어 있어, has_height_work=true 등 올바른 입력을 줘도 발화하지 않음.

## 원인 분류 (9개 전부)
**RULE_DESIGN — mapped_field 의미 오매핑**
- NORMAL_NONFIRE 아님: 올바른 매핑이면 발화해야 할 조건(예: 높이2m 작업)이 존재하는데 미발화.
- RUNTIME_BUG 아님(주): 런타임은 mapped_field 규칙대로 동작; 데이터(매핑)가 잘못됨.
- ORACLE_LIMIT(수치 임계 부재) 아님: 문제는 수치 임계가 아니라 필드 범주 자체가 틀림.

## 발화 가능성 (STEP4)
- 현재 매핑(worker_count) 하에서 이 9개를 정상 발화시키는 입력은 **없음**(조건-필드 불일치).
- 올바른 필드로 재매핑 시 발화할 것으로 추정(예: art49 -> has_height_work; 현재 payload에 이미 true). 단 이는 추론이며, 재매핑은 본 WO 범위 밖(별도 CHG).

## 판정
- 미관측 9개 = **RULE_DESIGN (mapped_field 오매핑)** 으로 확정.
- Runtime 전달 실패 아님. Repository 매핑 결함(별도 사안, OBS-LEG002-004 계열과 유사한 데이터 결함).
- 부차적 미확인: 런타임이 worker_count-mapped atom을 애초에 발화시키는 경로가 있는지 여부는 런타임 코드 분석 필요 -> 본 WO 범위 밖(미확인).

## 권고
- 별도 **WO-CHG-MAPFIELD-001**(9개 mapped_field 교정: worker_count -> 실제 필드) 필요.
- 337 전수 전달 CONFIRMED는 그 재매핑·재관측 이후 가능.
- 300 Regression은 이 매핑 결함과 무관하게 별개 축이므로, Operator 판단에 따라 병행/후행 결정.
