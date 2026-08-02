# WO-RUNTIME-DEBUG-001 — Runtime Repository Reload Verification

## 완료 조건 질문
**"Repository가 변경된 후, Runtime는 어떤 조건에서 새 Repository를 다시 읽는가?"** — 실동작 실험으로 증거만 수집해 답한다.

## STEP4 — 동작별 비교 (baseline 대비)
| 동작 | 수행 가능 | release/freeze/repository_size | obligation_count | law_name / article / evidence (152) | 전체 응답 바디 |
|---|---|---|---|---|---|
| Reload | **불가 (404x5)** | — | — | — | — |
| Restart | 수행 시도됨 | SAME | 152=152 | **0 diff** | **바이트 일치** |
| Deploy | 수행 시도됨 | SAME | 152=152 | **0 diff** | **바이트 일치** |

- release_version / repository_version / freeze_signature / repository_size: 세 동작 모두 baseline과 동일 (RC1 / CAL022 / 15cd17e8 / 337).
- 152개 의무의 atom_id 집합·law_name·law_article·evidence: Restart/Deploy 후 baseline과 **완전 동일 (0 diff)**.
- distinct law_name: 세 관측 모두 {산업안전보건기준에 관한 규칙:150, 실내공기질법:2}로 동일.

## STEP5 — 증거로만 답: Runtime은 언제 Repository를 다시 읽는가?
관측된 사실만:
1. **Reload로는 재적재 경로가 없다.** in-process reload/refresh 엔드포인트 5종이 전부 404 (leg-runtime 로그에 404로 기록). 따라서 "Reload"라는 동작으로 Runtime이 Repository를 다시 읽는 일은 일어나지 않는다(경로 부재).
2. **우리가 수행한 Restart·Deploy 후, Runtime이 내보내는 Repository 내용은 baseline과 바이트 단위로 동일했다.** 어떤 필드도 바뀌지 않았다.
3. **leg-runtime 자기 로그에 부팅/적재 라인이 관측되지 않았다.** 조회 가능한 구간에 startup 배너(Uvicorn/Application startup)·적재 라인(loaded/production_semantic_repository)이 없고, restart·deploy 시각(12:58/13:00) 구간에 요청 로그가 끊김 없이 이어졌다.

→ 종합: **본 실험에서 Reload·Restart·Deploy 어느 동작에서도 Runtime이 (이미 수정된) Repository를 새로 반영하는 것을 관측하지 못했다.** Reload는 경로 자체가 없고, Restart/Deploy 후 출력은 baseline과 동일했으며, 그 구간에서 프로세스 재부팅·재적재의 로그 증거가 나타나지 않았다.

## 미해결/경계 (사실 기록, 추측 아님)
- restart/deploy가 **leg-runtime 프로세스를 실제로 교체**했는지는 로그로 확정되지 않음 (startup 배너 미관측, 요청 로그 연속). 초기 railway CLI 링크가 다른 서비스를 가리켰던 사실도 함께 기록.
- "출력이 왜 동일한가"(수정이 런타임이 읽는 DB에 반영됐는지 등)는 **본 WO 범위 밖**(Repository 분석·RCA·production_semantic_repository 분석 금지)이므로 판단하지 않음.

## STEP7 — 최종 판정: **RUNTIME_RELOAD_NOT_CONFIRMED**
근거: Reload 경로 부재(404x5) + Restart/Deploy 후 출력 baseline과 바이트 동일(0 diff) + 부팅/적재 로그 미관측. 본 실험은 Runtime이 변경된 Repository를 다시 읽는 조건을 **관측으로 확인하지 못했다.**

의미(정확히): "Runtime이 절대 재적재하지 않는다"가 아니라, "이 실험에서 수행한 Reload·Restart·Deploy로는 재적재(=변경 반영)를 관측하지 못했다"이다.
