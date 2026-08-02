# WO-DECISION-001 — Decision Basis (기존 결과만)

## STEP1 Decision Input (WO-ALT-001 인용)
5축: (1)정합성 회복 위치 (2)선행 BLOCKER (3)범위 (4)freeze 비용 (5)수용 옵션.

## STEP3 거버넌스 적합성 (WO-ALT-001 governance 인용, 재분석 없음)
S1 높음(Data-only·비공란 미변경) / S2 낮음 / S3 중 / S4 중-낮음(소스 BLOCKED) / S5 낮음 / S6 조건부.

## STEP4 비용 비교 (기존 기록)
| 축 | S1 | S6 | S3 | S4 |
|---|---|---|---|---|
| freeze | 새 freeze/release 필요 | 불필요 | 새 freeze | repo 불변(보존) |
| Regression | LOW(label-only) | 없음 | MEDIUM(300 재검증) | MEDIUM-HIGH(런타임 회귀) |
| Runtime | 무변경 | 무변경 | 무변경 | 변경(소스 BLOCKED) |
| 운영 영향 | SoT 정합 회복 | 미해결 | 재생성 부담 | 우회(SoT 잔존) |

## STEP5 위험 비교 (WO-ALT-001 risk 인용)
- S1: freeze 미발급·동시성(공란조건 변동)·numeric 라벨 채움 -> 조건부 UPDATE·freeze 규칙으로 관리 가능(관찰). 선행 BLOCKER 없음.
- S3/S4: build/serving 소스 미특정 = 실행 선행 BLOCKER.
- S5: 이중 진실원. S6: 오인용 지속.

## 종합
Root cause(L3)·Impact(MEDIUM)·Alternative(S1 권장, 선행 BLOCKER 없음)의 기존 확정 결과가 일관되게 S1을 가리킴. 신규 근거 생성 없음.
