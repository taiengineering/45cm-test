# WO-E2E-LEG-1000-002 · Batch 1 — 50건 생성 및 전수 정독

**Goal** G-mscro68p-fcf706 · **성격** 조사(Gap Discovery). Runtime 미실행. 코드·엔진·Repository 수정 0.

## 0. Batch 0 보완 반영

Operator 지시로 **NOT_ASKED** 상태를 분리했다. "묻지도 않았다"와 "물었는데 Adapter가 버렸다"는 원인도 처방도 다르다.

| 소실 지점 | 건수(매트릭스 2,638) | 성격 |
|---|---|---|
| 0_Question NOT_ASKED | 924 (INACTIVE 595 / ABSENT 329) | **Consumer UX** — 질문 자체가 없음 |
| 3_Adapter DROP·MISMATCH | 1,181 | **Adapter** — 물었으나 Input Contract 미적재 |
| 4_Runtime DROP | 177 | **Repository** — 적재됐으나 mapped_field 부재 |
| 끝까지 도달 | 356 | |

## 1. Batch 1 구성

| Sector | 건수 | 비율 근거 |
|---|---|---|
| 제조 | 25 | 500/1000 |
| 건설 | 15 | 300/1000 |
| 건축물 | 10 | 200/1000 |

업종·프로젝트·용도 44종 사용, 회사명 50/50 고유, **복제 0**.

## 2. 전수 정독 결과 (50/50)

| 판정 | 건수 |
|---|---|
| REALISTIC | **50** |
| QUESTIONABLE | 0 |
| INVALID | 0 |

검사 항목 V1~V8(공정↔설비·설비↔작업·규모↔설비·복제·입력누락·상태미기재·건설단계·건물규모) 전건 통과. `batch1_audit.csv`에 회사별 판정·근거 기재.

**정독 중 교정한 것 2건** (자동 Gate가 못 잡고 사람이 읽어서 발견):
- 물류센터 36층·승강기 26대 → 용도별 층수 상한(`FLOOR_CAP`)과 용도별 승강기 산정계수(`ELEV_DIV`) 신설. 물류·공장은 화물용 위주로 대수가 적다.
- 학교 연면적 4.7만㎡ → 용도별 연면적 상한(`AREA_CAP`) 신설.
두 규칙 모두 감사기 검사항목(V8)에 추가해 이후 Batch에서 자동 적발되도록 했다.

## 3. 회사별 4항목 기록 (Operator 지시)

| 항목 | 필드 |
|---|---|
| ① Consumer가 입력한 내용(원문) | `consumer_input[]` = {field, question, answer} |
| ② Adapter가 실제 전달한 내용 | `adapter_contract{}` = build_input_contract 변환 결과 |
| ③ Runtime이 실제 사용한 필드 | `runtime_fields[]` = 저장소 mapped_field |
| ④ 기대 의무와 실제 차이 | `expectation_gap[]` = {기대 의무, 구동 field, 도달 여부, 소실 단계, gap_id, KNOWN/NEW} |

추가로 `input_trace[]`에 입력 1건마다 4단계 경로(`PASS>CONVERT>DROP>MISMATCH`)를 남긴다.

**실례 — B1-M004 정우세라믹 (시멘트·요업, 266명, 충북 청주)**
```
① 공정  원료 채취·저장→분쇄→조합→소성(회전로)→냉각→분쇄·혼합→저장→출하
   설비  회전로·가열로·집진기·컨베이어·성형기·저장탱크·지게차
② Adapter 전달  {worker_count: 266, sector: INDUSTRIAL, ksic_code: 23}
③ Runtime 사용  [worker_count]
④ 기대 의무 4건 전부 미도달
   지게차 안전검사·운전자격     ← has_forklift        NOT_ASKED @0_Question  OBS-A6/NEW
   컨베이어 덮개·비상정지장치    ← has_conveyor        NOT_ASKED @0_Question  OBS-A6/NEW
   분진 작업환경측정·특수건강진단 ← has_dust_work       NOT_ASKED @0_Question  OBS-A6/NEW
   밀폐공간 프로그램·산소농도측정 ← has_confined_space  NOT_ASKED @0_Question  OBS-A6/NEW
```
266명 규모의 요업 공장이 회전로·집진기·지게차를 전부 신고했는데, **Runtime에 남은 것은 근로자 수 하나뿐이다.**

## 4. 관찰 집계 (소비자 입력 970건)

| 상태 | 건수 | 비율 |
|---|---|---|
| SUPPORTED | 120 | 12.4% |
| NAME_MISMATCH | 55 | 5.7% |
| PASSTHROUGH_ONLY | 436 | 44.9% |
| NOT_ASKED | 359 | 37.0% |

**기대 의무 263건 중 도달 가능 31건(11.8%), 미도달 232건(88.2%).**

| Sector | 기대 | 도달 | 도달률 |
|---|---|---|---|
| 제조 | 90 | 5 | **6%** |
| 건설 | 100 | 0 | **0%** |
| 건축물 | 73 | 26 | 36% |

**건설은 15개 현장 전부에서 기대 의무 도달이 0이다.** 굴착·비계·항타·거푸집동바리·철골·가설전기 — 건설 재해의 핵심 축이 모두 질문되지 않는다(OBS-A7).

## 5. Gap occurrence (Batch 1)

| Gap | 발견 | occurrence |
|---|---|---|
| OBS-A8 Adapter가 수치·텍스트 미적재 | NEW | 116 |
| OBS-A6 제조 설비·작업 질문 비활성 | NEW | 88 |
| OBS-A7 건설 공종 질문 비활성 | NEW | 80 |
| OBS-A1 공정·설비 목록 미평탄화 | KNOWN | 65 |
| OBS-A10 건물 관리·법정검사 축 부재 | NEW | 60 |
| OBS-A5 Presence-only | KNOWN | 50 |
| OBS-A2 필드명 불일치 | KNOWN | 39 |
| OBS-A9 소방 3종 미도달 | NEW | 24 |
| OBS-A3 승강기 형식 불일치 | NEW | 10 |
| OBS-A4 가스 강제 치환 | KNOWN | 6 |

## 6. 산출물

`batch1_companies.json`(50사 전체) · `batch1_audit.csv`(정독 판정) · `batch1_gate.json` · `stage_trace.csv`(매트릭스 2,638) · 매트릭스 3종 · 생성기 7종

## 7. 다음

Operator 승인 시 Batch 2(51~100). 1,000건 완성 전 Runtime 실행 없음.
