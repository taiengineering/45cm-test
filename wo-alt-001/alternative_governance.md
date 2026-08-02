# WO-ALT-001 STEP5 — Governance / Architecture 적합성

기준: Architecture(계층 책임) · Freeze(RC1 동결) · Repository(Source-of-Truth) · Pipeline(무변경 원칙) · WO 거버넌스(Data-only 우선, 비공란 덮어쓰기 금지, 논리귀속 금지).

| 전략 | Freeze | Repository SoT | Runtime/Pipeline | 적합성 |
|---|---|---|---|---|
| S1 Backfill(325) | 새 freeze/release 발급(규칙 준수) | 공란을 law_master로 보충 = SoT 정합 회복 | 무변경 | 높음 — Data-only, 비공란 미변경 |
| S2 Backfill(23) | 새 freeze | 부분 보충 -> SoT 불완전 잔존 | 무변경 | 낮음 — 전수 원칙 위배 |
| S3 Regeneration | 새 freeze | 전면 재생성 | build 파이프라인 필요(소스 미특정 위험) | 중 — 재검증 부담·소스 리스크 |
| S4 Runtime Resolver | repo 불변->freeze 보존 | repo SoT는 여전히 공란(런타임이 조인으로 우회) | 런타임 로직 변경(serving 소스 BLOCKED) | 중-낮음 — 소스 미특정, 런타임 변경 거버넌스 |
| S5 Presentation | freeze 보존 | SoT·runtime 여전히 오류 | 표시 계층 변경 | 낮음 — 증상 은폐, 정합성 미해결 |
| S6 No Change | 보존 | 미해결 | 무변경 | 조건부 — MEDIUM 수용 시만 |

핵심: repo가 SoT를 복사·동결하는 아키텍처이므로, 정합성 회복은 데이터 계층(S1/S3)이 아키텍처 정합. 런타임 우회(S4)·표시 교정(S5)은 SoT 결함을 남김. 단 어떤 repo 변경도 새 freeze를 요구.
