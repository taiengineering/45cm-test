# WO-VERIFY-002 — Runtime Snapshot Build Verification

증거원: 45cminc/leg (main) 코드·CI·운영 문서 read-only. 대상 = public.production_semantic_repository(337, freeze 15cd17e8, release SEMREPO-RC1-2026.07.20)의 생성 파이프라인.

## STEP1 — 현재 Runtime Provenance (기록)
| 항목 | 값 |
|---|---|
| release | SEMREPO-RC1-2026.07.20 |
| freeze | 15cd17e871b6885d34214c84a58adf47 |
| repository_size | 337 |
| runtime_version | provenance 응답에 별도 노출 없음(관찰된 필드=release/freeze/repository_size). production_repository는 repository_version을 행값에서 취함 — 본 WO에서 별도 값 미관찰. |

## STEP2 — Snapshot 생성 Build Process (증거 기반)
**결과: 생성부 미발견 (available sources 내).** production_semantic_repository(337) + freeze_signature + release_version을 **생성(쓰기)**하는 코드/스크립트/CI를 45cminc/leg에서 찾지 못함. 확인한 후보와 결과:

| 후보 | 실제 대상 | 판정 |
|---|---|---|
| rtm_engine/rtm/production_repository.py | public.production_semantic_repository | **읽기 전용(SELECT)** — 빌더 아님 (Loading Path, WO-VERIFY-001) |
| norm_creation_v3/tools/load_v3.py | staging.requirement_atom_v3/expression_v3/resolution_v3 (31,434) | 다른 테이블 INSERT — 빌더 아님 |
| norm_creation_v3/tools/run_full.py | in-memory Generator(31,407), DB write 없음 | 빌더 아님 |
| norm_creation_v3/baseline/RUNBOOK_STAGE-B_deployment_v1.md | staging.requirement_atom_v3 배포(31,434) | 다른 파이프라인 — 빌더 아님 |
| .github/workflows/rtm-tests.yml | pytest(테스트), SUPABASE_DB_URL로 조회 | 테스트·읽기 — 빌더 아님 |
| development/engine/Procfile | `uvicorn api.server:app` (web) | 배포 시 빌드 단계 없음 |
| docs/history/LEG_Runtime_Release_Baseline_v1.0.md | Runtime 코드 계층 freeze(v1.0) | 코드 freeze — 데이터 Snapshot 빌드 아님 |
| GitHub code search `production_semantic_repository` | — | total_count 0 (private repo 미인덱스) |
| 파일명 grep(freeze/release/snapshot/production_semantic/build) | — | production_semantic_repository writer 없음 |

참고(사실): production_repository.py 헤더 docstring은 생성 기원 WO로 "WO-DEPLOY-002 / WO-QA-INT-001"을 인용하나, 해당 테이블을 populate/freeze 하는 실행 코드·스크립트·CI는 본 repo에 커밋되어 있지 않음.

## STEP3 — 생성 시점 (증거)
**미확정 (빌더 미발견).** 단, 확인된 negative 사실:
- **Deploy 시 생성 아님**: Procfile=`uvicorn` web 단일, STAGE-B 런북 "Procfile release 훅 없음 → 배포 시 자동 migration 없음" 명시.
- Build/Pipeline/Scheduler/Manual 중 무엇인지는 빌더 코드가 없어 증거로 확정 불가.

## STEP4 — 생성 결과 저장 위치 (증거)
- 결과가 저장되는 테이블 = **public.production_semantic_repository** (런타임이 읽는 대상, 확인됨).
- 그 테이블에 **쓰는 프로세스/아티팩트/파일은 미발견** (available sources 내).

## 종합
런타임이 읽는 Snapshot(SEMREPO-RC1, 337)의 **생성 파이프라인은 available 45cminc/leg 소스에서 증거로 확정 불가**. 읽기(하류) 경로는 이미 확정(WO-VERIFY-001)이나, 쓰기(상류) 빌더는 이 repo 밖에 있거나 비커밋 1회성일 가능성 — 단, 본 WO는 위치를 추정하지 않고 "미발견" 사실만 기록.
