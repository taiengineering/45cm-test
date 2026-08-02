# WO-ALT-001 — Correction Strategy Comparison

## STEP1 Confirmed Facts (RCA + Impact, 재분석 없음)
- Root Cause: production_semantic_repository.law_name(비정규화 복사 컬럼)가 build/freeze 시 law_master에서 채워지지 않아 315/327 공란. 런타임이 컬럼값 읽고 공란을 하드코딩 default(산안기준규칙) 출력. (WO-RCA-001, ROOT_CAUSE_CONFIRMED)
- Collapse Point: L3 repository materialization. Join(law_master) INTACT — 정답 16종 327/327 존재.
- Impact: MEDIUM, METADATA ONLY. 오표기 23 atom, 노출 109/300(36.3%)·301/4961(6.07%). firing/article/evidence/applicability/semantic/runtime 무영향. (WO-IMPACT-001)
- 12 비공란(short-form) 보존, backfill 대상과 law_id 겹침 0.
- Serving 소스(/rtm/evaluate 앱)는 미특정(RCA STEP4 BLOCKED).
- Freeze 규칙: repo 내용 변경 시 새 freeze/release(RC1 유지 불가).

## STEP2 전략 전수 (선택 아님)
S1 Repository Backfill(325 blank->join) · S2 Repository Backfill(23-only) · S3 Snapshot Regeneration · S4 Runtime Resolver(join at read) · S5 Presentation Layer · S6 No Change.

## STEP3-4 전략별 영향·장단점 (alternative_matrix.csv 참조)
- S1: 수정=repo.law_name 325 공란행. Runtime 영향 없음(런타임 코드 불변). Regression LOW(라벨만). Metadata=23 교정+292/10 명시화. Semantic 없음. 장점: Source-of-Truth 보충, 런타임 리스크 최소. 단점/위험: 새 freeze 필요, 동시성-안전 blank-only UPDATE 필요.
- S2: repo 23행만. 292 공란 잔존->컬럼 불일치 지속. '전수/빠짐없이' 원칙과 충돌, 앞서 '23만 하드코딩 금지'로 지적됨.
- S3: 337 전량 재생성. build/materialization 소스 미특정 가능성(BLOCKED 위험), 타 컬럼 변동 위험, 300 전면 재검증 필요(Regression MEDIUM).
- S4: 런타임 read를 조인으로 변경. repo 불변->freeze 보존 장점. 그러나 serving 소스 미특정(BLOCKED), 런타임 로직 변경, 조인-at-read 동작/성능 변화(Regression MEDIUM-HIGH).
- S5: 표시/보고서 계층만 교정. repo·runtime Source-of-Truth 여전히 오류->데이터 정합성 미해결(masks symptom).
- S6: 무변경. 23 오표기·36.3% 노출 지속.
