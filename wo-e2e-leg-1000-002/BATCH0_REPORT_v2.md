# WO-E2E-LEG-1000-002 · Batch 0 v2 — 매트릭스 검토 요청 (재제출)

**Goal** G-mscro68p-fcf706 · **성격** 조사(Gap Discovery). PASS/FAIL 선언 없음. 코드·엔진·Repository 수정 0.

## 0. v1 산출물 오류 정정 (선행)

Operator가 `batch0_gate.json`의 `violations: 9`와 보고서의 "모순 0" 불일치를 지적했다. **지적이 정확하다.**

- **원인**: 3차 빌드를 `python3 build.py | head -30`으로 실행했고, `head`가 30행에서 파이프를 닫아 SIGPIPE로 프로세스가 종료됐다. `json.dump(batch0_gate.json)`은 스크립트 말미에 있어 **도달하지 못했다.** 콘솔에는 violations 0이 출력됐으나 파일은 2차 실행분(9건)이 남았고, 그 상태로 제출됐다.
- **사실 확인**: 파이프 없이 전량 재실행 → `violations = 0`, `violation_detail = []`. 9건은 **실제로 교정 완료**돼 있었고 산출물만 stale이었다.
- **재발 방지**: 이후 모든 빌드는 파이프 없이 실행하고 로그 파일로 남긴다(`run4.log`).

## 1. v2 반영 사항 (Operator 지시 5건)

| # | 지시 | 반영 |
|---|---|---|
| 1 | Consumer→Canonicalizer→Adapter→Runtime 4단계 기록, 단계별 DROP/CONVERT/PASS/MISMATCH | `stage_trace.csv` 2,638행 신규 |
| 2 | Gap의 KNOWN / NEW 구분 | `GAP_REGISTRY` OBS-A1~A10, 전건 discovery 부착 |
| 3 | 건물 관리자 관점 입력(정기점검·자체점검·법정검사·위탁관리·외주·사용중) | `MGMT_INPUTS` 6종, 전 건축물 행에 부여 |
| 4 | 업종보다 공정 흐름 다양성 | `FLOWS` 24업종 실제 공정 순서 (예: PCB = 원판재단→드릴→무전해동→패턴도금→에칭→SR인쇄→표면처리→AOI→라우팅→전기검사) |
| 5 | 터널·플랜트를 일반 건축 순서에서 분리 | `PIPELINES` TUNNEL/PLANT 독립 스테이지·장비·작업·위험 |

## 2. 승인 조건 대비

| 조건 | 요구 | 실제 |
|---|---|---|
| 제조 아키타입 / 공정 흐름 | ≥22 | 24 / 24 |
| 건설 프로젝트 유형 / 공종 / 독립 Pipeline | ≥9 / ≥15 | 10 / 16 / 2 |
| 건축물 용도 | ≥10 | 10 |
| 공정↔설비 · 설비↔작업 · 규모 모순 | 0 | **0 / 0 / 0** (run4.log 실측) |
| 소비자 입력 누락 · Adapter 상태 미기재 | 0 | 0 / 0 (2,638건 전건) |

## 3. 4단계 경로 추적 결과 (소비자 입력 2,638건)

| 상태 | 건수 | 비율 |
|---|---|---|
| SUPPORTED | 339 | 12.9% |
| NAME_MISMATCH | 151 | 5.7% |
| PASSTHROUGH_ONLY | 1,224 | 46.4% |
| UNSUPPORTED | 924 | 35.0% |

**소실 지점**

| 단계 | 건수 | 비율 |
|---|---|---|
| 3_Adapter에서 소실 | 2,105 | 79.8% |
| 4_Runtime에서 소실 | 177 | 6.7% |
| 끝까지 도달 | 356 | 13.5% |

**소실의 92.3%가 Adapter 단계에서 발생한다.** Runtime이 병목이 아니라 Adapter가 병목이다.

대표 경로:
```
has_water_tank    PASS > PASS    > PASS     > PASS   SUPPORTED
elevator_count    PASS > PASS    > MISMATCH > —      NAME_MISMATCH   OBS-A3 / NEW
total_floor_area  PASS > CONVERT > DROP     > —      PASSTHROUGH     OBS-A8 / NEW
has_excavation    PASS > PASS    > DROP     > —      UNSUPPORTED     OBS-A7 / NEW
inspection_legal  PASS > PASS    > DROP     > —      UNSUPPORTED     OBS-A10 / NEW
```

## 4. Gap Registry — KNOWN vs NEW

| ID | 내용 | 발견 | occurrence |
|---|---|---|---|
| OBS-A1 | 공정·설비 목록 → has_* 평탄화 부재 | KNOWN | 186 |
| OBS-A2 | Adapter 필드명 ≠ 저장소 필드명 3종 | KNOWN | 105 |
| OBS-A3 | 승강기를 대수(number)로만 묻고 has_elevator(19 atom) 변환 없음 | **NEW** | 29 |
| OBS-A4 | has_gas → has_high_pressure_gas 강제 치환 | KNOWN | 17 |
| OBS-A5 | 수치 입력 발화 무영향(Presence-only) | KNOWN | 137 |
| OBS-A6 | 제조 설비·작업 질문이 is_active=false | **NEW** | 266 |
| OBS-A7 | 건설 핵심 공종 질문이 is_active=false (72 atom 미도달) | **NEW** | 150 |
| OBS-A8 | Adapter가 수치·텍스트를 Input Contract에 싣지 않음 | **NEW** | 338 |
| OBS-A9 | 소방설비 4종 중 저장소 도달 1종뿐 | **NEW** | 70 |
| OBS-A10 | 건물 유지관리·법정검사·위탁관리 입력 축 자체 부재 | **NEW** | 174 |

KNOWN 445 · **NEW 1,027**. 1,000건 실행 전 매트릭스 단계에서 이미 신규 Gap 6종이 나왔다.

**v1 대비 정정**: v1에서 `total_floor_area`를 SUPPORTED로 분류했으나, `build_input_contract` 실코드가 `sector·ksic_code·worker_count·has_*`만 계약에 싣는 것을 4단계 추적으로 확인해 PASSTHROUGH_ONLY로 정정했다(OBS-A8). SUPPORTED 451→339.

## 5. 산출물

`stage_trace.csv`(2,638) · `matrix_manufacturing.csv`(78) · `matrix_construction.csv`(30) · `matrix_building.csv`(29) · `gap_inventory.json` · `field_status.json` · `batch0_gate.json` · 생성기 5종

## 6. Batch 1 (승인 후)

50건 생성 → 50건 현실성 전수 정독 → INVALID 재생성 → Operator 승인 → 다음 Batch. 1,000건 완성 전 Runtime 실행 없음.
