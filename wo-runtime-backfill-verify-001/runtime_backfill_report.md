# WO-RUNTIME-BACKFILL-VERIFY-001 — 전달 검증 종합 보고

## STEP1 Repository Snapshot (wrfced, LEG DB)
337 rows · blank 0 · nonblank 337 · distinct law_name 18 · release SEMREPO-RC1-2026.07.20 · freeze 15cd17e871b6885d34214c84a58adf47

## STEP2 Backfill Inventory (사전상태 기준, 337 전수)
- BACKFILLED (사전 공란 → 채워짐): 325
- NONBLANK_PROTECTED (사전 비공란, 축약형 유지): 12
- UNCHANGED: 0

## STEP3 Runtime Census (deployment b94a0741, 6개 payload 합산)
payload 밴드: FULL+gas/crane/demolition, worker_count in {1,10,50,300,1000}, 모든 has_* true
- 모든 밴드에서 obligation 최대 328 (worker_count 변화에도 328 고정)
- 관측된 atom: **328 / 337** · census 간 충돌 0

## STEP4 Repository <-> Runtime 비교 (관측된 328개)
- **law_name 불일치: 0**
- **article 불일치: 0**
- BACKFILLED 관측 316/325 -> law_name 316/316 일치
- NONBLANK_PROTECTED 관측 12/12 -> 12/12 일치

## 미관측 9개 (worker_count-gated, 전 밴드 미발화)
| law_name | atom 수 | peer 확인 |
|---|---|---|
| 산업안전보건기준에 관한 규칙 | 4 (art49/187/524/665) | **peer 293/297 확인** |
| 근로기준법 | 4 (art56/60/60/75) | **peer 없음 (0/4)** |
| 응급의료에 관한 법률 | 1 (art8) | **peer 없음 (0/1)** |

- 9개 모두 mapped_field=worker_count. worker_count 1~1000 전 밴드 + 모든 has_* true에서도 미발화.
- 추가 발화 시도는 필드조합/적용성 역추적 필요 -> Repository 구조 분석(본 WO 금지)에 해당하여 중단.
- Presence-only Oracle 원칙상 수치 임계값은 RC1로 재구성 불가·CHG 대상 아님.

## 관측 결론
- 전달 메커니즘: 328건 전수 **0-drift**로 실증. Repository law_name이 Runtime에 그대로 반영됨(개별 법령 17종 + 산안규칙 포함).
- 미관측 9개: 전달 **실패 증거 없음**. 산안규칙 4는 peer로 실증. 근로기준법 4 + 응급의료 1은 직접 관측 미확보(미확인으로 명시).

## STEP7 판정 (Operator 결정 필요)
- (a) RUNTIME_BACKFILL_CONFIRMED (scope 명시): 328/337 직접 0-drift 확인 + 메커니즘 소음 없음; 미관측 9는 worker_count 밴드 게이팅(Presence-only Oracle 범위 밖), 산안규칙 peer 확인.
- (b) RUNTIME_BACKFILL_INCOMPLETE: 근로기준법·응급의료 직접 미관측 -> 337 전수 미달.
Claude는 임의 선언하지 않고 관측 사실만 기록. 판정은 Operator.
