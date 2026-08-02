# OBS-R-01 STEP4 — Source Code Trace (STATUS: BLOCKED, 사실 기록)

## 지시서 지정 경로 부재 (사실)
지시서 고정 소스: 45cminc/leg — rtm/production_repository.py, rtm/repository.py, repository/connection.py, server.py, /rtm/evaluate response assembler.
실측(read-only, GitHub API 2026-08-02):
- 45cminc/leg 루트: .github, contracts, development, docs, infra, sql, src, tests, verification + HANDOFF/README md. server.py 없음. rtm/ 없음. repository/ 없음.
- src/ 트리(recursive): api/(health/runtime/signals 모두 .gitkeep만 = 비어 있음), check_engine/(engine/models/evidence_resolver/evidence_store/source_resolver/validator/dict_evidence_store), condition/(assemble/article_direct/run_direct/run_pilot/gate/normalize), lawdata/(migrate_raw), profile/(builder/expander/schema), registry/(ingest). 지정 경로 어느 것도 존재하지 않음.
- SESSION_HANDOFF_2026_07_05_runtime_pipeline.md: 이 repo가 기술하는 런타임은 object/registry 파이프라인(development/engine/runtime/ loader·matching·pipeline, leg_object_build/leg_registry_entry on wrfcedzgdrfupenzqhur) — production_semantic_repository 기반 /rtm/evaluate 런타임과 다른 트랙.
- Railway projects 열거: 빈 배열(이 토큰으로 leg-runtime 서비스->소스 repo 특정 불가).

## 결론
실제 /rtm/evaluate(production_semantic_repository·RC1·337 소비) serving 코드는 이 세션에서 접근 가능한 어떤 소스에서도 특정되지 않음. 지정 경로는 현재 repo 상태와 불일치.
-> STEP4 "law_name 생성·fallback·default·serialization 호출경로 파일/함수/라인 기록" = BLOCKED.
-> 논리추정 귀속 금지 원칙에 따라, default-fill(blank->산안기준규칙)의 코드 계층(loader vs assembler vs serializer)을 소스 없이 단정하지 않음.

## 소스 없이 코드-행위(behavior)로 확인된 사실 (출력·DB 대조)
- 런타임 출력 law_name distinct=4 == 런타임 DB production_semantic_repository.law_name 컬럼 distinct=4 (공란 315 + 고압가스법3/승강기법7/실내공기질법2). 조인(law_master, 16 distinct)과 불일치.
- 즉 런타임은 repo.law_name 컬럼값을 사용하고 공란은 하드코딩 default '산업안전보건기준에 관한 규칙'로 채움(45cm 원칙 "없는 값 생성 금지/하드코딩 enum 금지" 위반 정황). 존재하는 law_master 조인을 사용하지 않음. — output/DB 대조 evidence이며 source-line evidence 아님.

## 필요 조치 (다음)
정확한 serving repo/branch/경로(예: 별도 leg-runtime repo, 또는 미커밋 브랜치) 확보 시 STEP4 재개. 그 전까지 runtime-module 귀속은 UNVERIFIED.
