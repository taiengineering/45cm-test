# WO-ALT-001 STEP8-9 — 권고 분류 & Decision Input (결정 아님)

## STEP8 권고 분류 (선택 아님)
- 권장: S1 Repository Backfill(325 blank->join) — Data-only, 런타임 리스크 최소, SoT 정합 회복, 비공란 미변경, 새 freeze 규칙 준수. (Operator가 앞서 선호한 "공란을 SoT로 보충" 방향과 정합)
- 가능: S6 No Change — MEDIUM 수용 시 방어 가능(무변경·freeze 보존).
- 가능하지만 위험: S3 Snapshot Regeneration(재검증 부담·build 소스 리스크) / S4 Runtime Resolver(serving 소스 BLOCKED·런타임 회귀).
- 비권장: S2 Backfill(23-only)(전수 원칙 위배·부분 정합) / S5 Presentation(증상 은폐·SoT 미해결).

## STEP9 Decision Input (다음 WO에서 선택)
다음 WO(전략 선택->CHG)에서 판단할 축:
1. 정합성 회복 위치: 데이터 계층(S1/S3) vs 런타임 우회(S4) vs 표시(S5) vs 미해결(S6).
2. 선행 BLOCKER: S3/S4는 각각 build 소스 / serving 소스 특정이 선행 필요(현재 미특정). S1은 선행 BLOCKER 없음(런타임 DB·조인 확보됨).
3. 범위: 공란 전수(325, 23 교정 포함) vs 23-only vs 전량 재생성. (전수 원칙상 부분보다 전수가 정합.)
4. freeze 비용: repo 변경 계열은 새 freeze/release + (필요시)E2E 재검증 필요.
5. 수용 옵션: S6는 MEDIUM 등급을 조직이 수용하는지의 정책 판단.

미결정 사항(다음 WO 소관): 실제 전략 선택, 수정 범위(23/325), freeze/release 명명, 재검증 범위.

## STEP10
ALTERNATIVES_COMPLETE.
