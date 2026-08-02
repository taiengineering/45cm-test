# WO-CHG-010B STEP3 — Post-Apply Validation (read-only)

## Repository 전체
| 검증 | 기준 | 실측 | 판정 |
|---|---|---|---|
| total rows | 337 | 337 | PASS |
| blank | 0 | 0 | PASS |
| nonblank | 337 | 337 | PASS |
| distinct atom | 337 | 337 | PASS |
| distinct law_name | 증가 | 4->18 | PASS (실제 법령 다양성 복원) |
| null evidence | 0(불변) | 0 | PASS |

## 대상 정밀
| 검증 | 기준 | 실측 | 판정 |
|---|---|---|---|
| 23 오표기 atom -> 참법 교정 | 23 | 23 | PASS |
| 23 중 default 잔존 | 0 | 0 | PASS |
| 비공란 12 short-form 유지 | 12 | 12 | PASS |
| 비공란 12 존재 | 12 | 12 | PASS |

## 판정: Repository Success = PASS
blank 325->0, 23 교정, 12 보호, evidence/article/atom_id 불변. Rollback 가드(비공란 변경·행수·타컬럼) 미발생.

## 유의 (다음 단계)
freeze_signature/release_version은 아직 RC1 상태(STEP 이후 freeze 갱신 예정). Runtime Success는 DB 상태가 아니라 실제 /rtm/evaluate 출력으로 별도 판정(STEP4).
