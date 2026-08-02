# WO-CHG-010A — CHG Success Criteria (STEP3-4) [rev.1 보완]

## STEP1 인용 근거 (기존 WO)
- RCA: blank law_name 컬럼(L3)이 근본 원인, 조인으로 참법 327/327 해소.
- IMPACT: METADATA ONLY, 23 오표기(36.3% 프로파일), semantic/runtime/firing 무영향.
- ALT/DECISION: S1 선택(blank-only backfill, 비공란 보호, Runtime 무변경).

## STEP3-4 성공 조건 (Repository / Runtime 분리 독립 정의)

### Repository Success  (데이터 계층)
- 기준: 대상 325 blank -> blank 0, 비공란 12 unchanged, 총 337행 유지, law_name 외 컬럼 불변.
- PASS: 위 전부 충족. FAIL: blank>0(대상 내) 또는 12 변경 또는 행수!=337 또는 타 컬럼 변경.

### Runtime Success  (서빙 라벨 — 실제 실행 결과 기준) [보완 #1]
- Runtime Success는 Repository Success에 종속되지 않는다. 반드시 실제 /rtm/evaluate 실행 결과로 판정한다.
- 기준: Repository 변경 후 실제 /rtm/evaluate 출력에서 23개 atom의 law_name이 참법(조인값)으로 변경되었음을 확인한다. mismatch 23 -> 0.
- Repository만 수정되고 Runtime 출력(law_name)이 이전과 동일하면 FAIL (변경이 서빙에 반영되지 않은 것).
- 동시에 article/evidence/applicability/atom_id 불변, A/B/C 결정성 유지. 292 blank-default-correct 정확 유지, 12 nonblank 불변.
- PASS: 실제 실행 출력 기준 mismatch 0 + 위 불변 유지. FAIL: Runtime 출력 미반영(동일) 또는 mismatch>0 또는 article/evidence/applicability/firing 변화 또는 비결정성.

### Metadata Success
- 기준: 23 atom 법령명 인용 정확 회복(36.3% 프로파일). PASS: 23/23 정확. FAIL: 잔여 오표기.

### Semantic Success
- NOT_TARGET — 이번 CHG의 목적 아님. (obligation identity/firing/적용은 변경 대상이 아니며, drift=0이 가드레일.)

## 주의 (경계)
Metadata(라벨) 개선을 Semantic 변경으로 확대 해석하지 않는다. Repository Success(공란 0)와 Runtime Success(실제 실행 출력에서 라벨 23 교정 반영)는 별개·독립 기준이며, Runtime은 DB 상태가 아니라 /rtm/evaluate 출력으로만 판정한다.
