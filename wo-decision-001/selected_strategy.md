# WO-DECISION-001 — Selected Strategy

## 선택: S1 — Repository Backfill (325 blank -> law_master join)
(권고. CHG_APPROVED 확정은 Operator 승인으로 성립.)

## STEP2 후보 재확인 (재평가 없음, WO-ALT-001 결과 인용)
S1 Repository Backfill(325) · S2 Backfill(23-only) · S3 Snapshot Regeneration · S4 Runtime Resolver · S5 Presentation · S6 No Change.

## STEP6 선택 근거 축약 (기존 결과만)
- Root cause 위치 = L3 repository.law_name 컬럼(RCA). -> 데이터 계층 교정이 아키텍처 정합(ALT governance: S1/S3 데이터 계층 적합).
- 선행 BLOCKER 부재: S1은 런타임 DB·law_master 조인 확보 상태로 즉시 가능. S3(build 소스)·S4(serving 소스)는 미특정 BLOCKER(RCA STEP4 BLOCKED / ALT risk).
- 거버넌스 부합: Data-only, blank-only 조건부, 비공란 12 미변경 -> '비공란 덮어쓰기 금지' 준수(ALT governance 적합성 '높음').
- 위험 최소: Runtime 무변경, Regression LOW(label-only)(ALT matrix/risk).
- Impact 근거: MEDIUM(23 오표기·36.3% 노출)은 무시할 수준 아님 -> S6 No Change보다 SoT 교정이 지속적 해소(IMPACT).

## 배제 사유 (기존 결과)
- S6 No Change: MEDIUM 결함(법령명 인용 오류) 잔존.
- S3/S4: 각각 build/serving 소스 미특정 = 선행 BLOCKER, 회귀 표면 큼.
- S2: 23-only는 292 공란 잔존, 전수 원칙 위배.
- S5: 표시 계층 교정은 repo SoT 오류 은폐.
