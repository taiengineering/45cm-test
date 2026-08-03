# LEG E2E 아크 통합본 — 작업방식 · 내역 종합

**대상 프로젝트:** taiengineering / 45CM LEG (법령·안전진단 엔진)
**기간:** 2026-08-02 ~ 08-03
**Operator:** taiwang(심태왕) · **Recorder/Implementer:** Claude
**아티팩트 리포:** taiengineering/45cm-test (wo-*/ 폴더)
**최종 상태:** CHG_SUCCESS (산안524 교정) · 300 Regression BLOCKED(baseline provenance) · RC2 Candidate 기록

---

## 1. 거버넌스 · 작업방식 (표준)

- **WO(Work Order) 거버넌스:** 모든 변경은 명명된 WO로. 각 WO는 하나의 좁은 목적. 설계 확정 전 구현 없음. Claude는 병합·태그·Goal 종료를 독단하지 않음. Operator가 유일 결정권자(승인 트리거 "승인/고/진행").
- **Goal 규율(CONST-GOAL-001):** project 작업은 Goal이 선행. 활성 Goal 없으면 read-only SELECT도 차단. 한 번에 하나의 활성 Goal. 새 WO 지시가 곧 전환 신호. 모든 guri-cf 호출에 goal=<G-code> + project="test-universe" 필수.
- **MCP 전용:** guri-cf만 사용. kn541-cf·범용 Supabase/Railway MCP 금지(다운 시에도 폴백 금지).
- **관측 우선·미확인 명시:** 도구 출력에서 관측을 먼저 기록 후 추론. "미확인은 미확인으로" 표기.
- **표준 원칙 "우리가 작업한 DB ≟ 런타임 DB":** 작업 DB가 런타임 DB와 다를 수 있음(이 프로젝트에서 실제 발생). 변경 전 대상 DB=런타임 연결처 재확인.
- **반복 금지:** 동일 수준 재검증(분석 루프) 회피. 확정된 단계는 닫고 다음으로.
- **승인 게이트:** 실제 DB 변경(UPDATE)은 Operator 명시 승인 후에만. dry-run/트랜잭션+assertion으로 안전 확인.
- **Presence-only Oracle:** RC1 repository에 수치 임계값(operator/threshold) 컬럼 없음. 수치 발화 차이는 CHG 트리거 아님.

## 2. 인프라 · 참조

- **LEG DB (런타임 소스):** wrfcedzgdrfupenzqhur — public.production_semantic_repository, 337행, RC1, freeze 15cd17e871b6885d34214c84a58adf47, release SEMREPO-RC1-2026.07.20, repo_version SEMREPO-CAL022-2026.07.20. 컬럼: atom_id(PK)·mapped_field·semantic_clause_id·law_name·law_article·evidence·repository_version·release_version·freeze_signature·is_readonly·loaded_at. (수치 임계 컬럼 없음)
- **구 DB / TAI source:** vwlahtguyggrhvslabax — 과거 런타임이 잘못 연결됐던 대상. Wiring-Fix로 연결 이탈.
- **런타임:** https://leg-runtime-production.up.railway.app (/rtm/health, /rtm/evaluate). Railway: project tai-api / env production / service leg-runtime(repo 45cminc/leg). 재배포·curl은 Operator(맥 ~/rtm_debug). guri-cf는 leg-runtime Railway workspace 접근 불가. execute_sql은 wrfced 읽기/쓰기 가능.
- **RTM 로더 dsn 우선순위:** SUPABASE_DB_URL or RTM_DATABASE_URL.
- **커밋 방식:** github_put_file(평문 content) 사용 가능. 또는 github_api PUT + base64. 기존 파일 수정은 sha 필요(put_file은 자동 조회).
- **유효 입력 필드 어휘:** distinct mapped_field 38종(has_hazardous_material 45 … total_floor_area 1). has_height_work 없음(실제 has_high_place_work). 수동중량물취급·응급의료·상시근로 대응 필드 없음.

## 3. WO별 내역 (시간순)

### WO-WIRING-FIX-001 (G-msbwjfy2-d17f6c) — LEG_RUNTIME_TARGET_RESTORED
- law_name 교정이 런타임 미반영된 근본원인 = 런타임 env가 구 DB(vwlaht)를 가리킴. SUPABASE_DB_URL을 wrfced로 복원.
- 검증-우선(verify-first): DATABASE_URL==wrfced 실측 PASS → SUPABASE_DB_URL을 wrfced로 set → 재배포. deployment b94a0741, Online, repo_size 337, freeze 15cd17e8. 23개 law_name이 개별법으로 교정 확인. 코드 0·DB행 0(env-only).

### WO-RUNTIME-BACKFILL-VERIFY-001 (G-msbxwpww-de1ee7) — RUNTIME_BACKFILL_INCOMPLETE
- 337 전수 Repository→Runtime 전달 검증(read-only). 런타임 census 328/337 관측, law_name/article mismatch 0. 9 atom 미발화.
- 판정 INCOMPLETE: 전달 실패 아님, 단 9개 미관측으로 PASS 증거 불충분.

### WO-RUNTIME-COVERAGE-001 (G-msbzipnj-6b819d) — COVERAGE_ROOT_CAUSE_CONFIRMED
- 미발화 9개 원인 = RULE_DESIGN(mapped_field 의미 오매핑). 근거: repo에 임계 컬럼 부재; worker_count-mapped=정확히 9개=미발화와 동일; 대조군 total_floor_area-mapped 1개는 정상 발화. 전달 실패 아님.

### WO-MAPFIELD-RESOLVE-001 (G-msccvrgz-363436) — 정답 후보 분류
- 9개 → CONFIRMED 0 / CANDIDATE_ONLY 3 / NO_VALID_FIELD 6. 단순 일괄 재매핑 부적절, (재매핑)/(스키마 설계)로 분리 권고. 산출물: mapfield_resolution.csv 691fc40 등.

### WO-TRACK-A-001 (G-mscgvgtq-2e549d) — TRACK_A_COMPLETE
- CANDIDATE 3건 판정. **CONFIRMED: 산안524→has_diving**(기압조절실이 has_diving에 다수 매핑). **REJECTED: 산안49·산안187**(has_high_place_work 실사용이 고소작업대 장비 한정 → 확장 증거 부족, Track B 이관). 산출물: trackA_decision.csv 5d864c5 등.

### WO-TRACK-B-001 (G-mschiisy-3d129c) — TRACK_B_COMPLETE
- 8건(NO_VALID 6 + REJECTED 2) BACKLOG_CONFIRMED. 분류 NEW_BOOLEAN 5 / INPUT_MODEL_CHANGE 3. 부족원인: 근로정책 4·Hazard 2·작업환경 1·도메인확장 1. 근로기준법 4건=hazard 아닌 운영/근로정책(입력모델 범위 이슈). 산출물: trackB_requirements.csv 1d0bc0a 등.

### WO-CHG-READINESS-001 (G-mschun4d-3f9bdc) + -R (G-mscil8ri-c37ca6) — READINESS COMPLETE
- 산안524 단건 변경 적합성 4 Gate. STEP1 격리성 PASS(단건 1행, 336 무변경). STEP2 충돌 PASS(has_diving 25 무영향, scid 충돌 0). STEP3 예측 PASS(328→329 +1, 나머지 0; 실제 관측은 post-apply 이관). STEP4 Rollback Readiness PASS(스냅샷 row md5 **d276ebedfc2fd4ff9d3bbe0308c1f0ae**, Rollback SQL, 성공/Rollback 조건 고정). is_readonly=true 발견하되, 기 확인된 메타필드(RLS/트리거/CHECK/함수 강제 아님)로 재조사 안 함. 산출물: readiness_* 7a3b425·503a84f·876686a·d51c839·1f28fa1·c435dc9.

### WO-CHG-MAPFIELD-001 (G-mscj31dw-830794) — CHG_SUCCESS (첫 실제 DB 변경)
- 산안524(5b849b3e) mapped_field worker_count→has_diving. 승인 게이트 후 단일 트랜잭션 DO block + assertion(affected=1 AND wc=8 AND diving=26 AND total=337 AND field=has_diving) → COMMIT.
- Repository PASS: wc 9→8, diving 25→26, 337 불변, 중복 0, 산안524 외 0, law_name/article(524)/evidence/scid 불변. 변경 후 md5 3cfb0750cd014d287198cd2d0edb5994.
- Runtime PASS: leg-runtime 재배포 후 has_diving payload → obligation_count **329**, 산안524 신규 발화(law_name·article 524), delta=+1만, dropped 0, 기존 328 전부 보존(drift 0). 결정성 1회 329로 갈음(Operator).
- 산출물: chg_snapshot_precheck.md 0cc4b05·chg_apply_result.md ddbb118·chg_runtime_verify.md bec629c·chg_verdict.md bf91dad. Release Note: CHANGELOG_CHG-MAPFIELD-001.md 229af96.
- **Rollback SQL(미발동):** UPDATE ... SET mapped_field='worker_count' WHERE atom_id='5b849b3e...'; 원복 후 md5==d276ebed.

### WO-REGRESSION-300-001 (G-mscovd31-e8e36c) — BLOCKED (Baseline Provenance Mismatch)
- 유일 300 baseline(e2e_300_run_A/B/C, 2026-08-02 03:15, source=vwlaht)은 WIRING-FIX 이전 → CHG 회귀만 분리 불가(wiring 23 + CHG 혼재). post-wiring&pre-CHG 300 부재, 재캡처 불가 → 억지 수행·보정 없이 BLOCKED.
- 조치: 현재 상태를 RC2 Candidate로 기록, 300 Baseline Capture는 별도 WO. 산출물: regression_blocked.md 0197270·rc2_candidate.md 23e7c3e.
- 주의: BLOCKED는 300 비교 불가일 뿐 CHG 성공을 뒤집지 않음.

## 4. 핵심 학습

- law_name 데이터가 맞아도 런타임 env가 다른 DB를 가리키면 미반영("데이터는 맞고 대상이 틀림"). 변경 전 런타임 연결처 실측 필수.
- mapped_field 의미 오매핑(9건)은 law_name 결함과 별개의 데이터 결함. 그중 6건은 입력 스키마 부재(설계 이슈), 3건 중 1건만 재매핑 확정(산안524).
- 근로기준법류는 hazard 입력모델에 없는 것이 자연스러움 → 입력모델 범위 설계 문제.
- 첫 DB 변경은 격리성·충돌·예측·Rollback Readiness 4 Gate 후 승인 게이트 → 트랜잭션+assertion으로 안전 실행.
- Regression은 baseline provenance가 변경 직전 상태와 일치해야 유효. 불일치 시 억지 보정 대신 BLOCKED + 새 baseline(RC2) 확립.

## 5. 현재 상태 · 다음 단계

**현재 (RC2 Candidate):** wrfced + WIRING-FIX + CHG_SUCCESS. repo_size 337, has_diving 26, worker_count 8, 단일 프로파일 obligation 329, freeze 15cd17e8(RC2 승격 시 갱신 여부 미정).

**다음 (예정 WO):**
1. WO-BASELINE-CAPTURE-300-001(가칭): wrfced+CHG 상태 300 프로파일 실측 → RC2 Baseline 확정. 이후 모든 CHG Regression은 RC2 기준.
2. Track B BACKLOG 8건 입력모델 설계(NEW_BOOLEAN 5 / INPUT_MODEL_CHANGE 3) — Engine/Repository/Runtime/UI 4계층.

**표준 흐름:** CHG → Release Note → Regression(RC 기준) → PASS → 새 RC Baseline → 다음 CHG.
