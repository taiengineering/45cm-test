# GENERATOR_LOG — WO-UNIVERSE-GENERATOR-1000-001

**Goal** G-mscybhg5-6c7bfe · Generator WO(분석 WO 아님) · SoT 수정 0 · 신규 Master 0

## 종료 조건 대비

| 조건 | 결과 |
|---|---|
| 1,000개 생성 완료 | **1,000** (제조 500 · 건설 300 · 건축물 200) |
| REALISTIC 통과 | **1,000 / 1,000** |
| 중복 0 | **duplicates 0** · 회사명 고유 1,000 |
| Provenance 100% | provenance 6,778건 전건 `source_row_id` 보유 · **UNTRACED 0** |
| Observation 기록 완료 | **4건** |

## SoT 입력 (읽기만)

| Source | Table | Rows | 용도 |
|---|---|---|---|
| R-MFG | `public.industry_master` + `public.process_equipment_map` | 1,948 (182 업종) | 제조 업종·공정·설비 |
| R-CON | `public.kcsc_process_master` + `public.kcsc_work_master` | 372 (공정 161 · 작업 243) | 건설 공종·작업 |

업종·공정·설비·작업은 **한 건도 생성하지 않았다.** 전부 위 두 스냅샷에서 읽었다.

## 생성한 것 (회사속성만)

회사명 · 지역 · 사업장명 · 근로자수 · 연면적 · 층수 · 운영형태 · 준공연도 · 교대형태 · 외주비율 · 공정률 · 가동상태

## SoT 산출 규모

| 축 | 건수 |
|---|---|
| 공정 | 1,301 |
| 설비 | 3,460 |
| 작업 | 1,517 |
| **MASTER_ABSENT 기록** | **2,011** |

### MASTER_ABSENT 내역

| 축 | 상태 | 건수 |
|---|---|---|
| work | MASTER_ABSENT | 700 (제조 500 + 건설 일부) |
| equipment | MASTER_ABSENT | 500 |
| project_type | MASTER_ABSENT | 300 |
| building_use | MASTER_ABSENT | 200 |
| process | MASTER_ABSENT | 200 |
| work | MASTER_EXISTS_BUT_NOT_CONNECTED | 111 |

대체·추론 **0건**. 없는 것은 없는 상태로 기록했다.

## 생성 중 자체 교정 2건 (제출 전)

1. **회사명 중복 75건** — 1차 실행에서 distinct_names 925. 회사명은 생성 허용 항목이므로 유일성 보장 로직 추가 → 1,000.
2. **`traceable` 공허 참** — BUILDING은 provenance가 0건이라 `all([])`이 True가 되어 200건이 추적 성공으로 잡혔다. `TRACEABLE` / `N/A_NO_SOT_AXIS` / `UNTRACED` 3상태로 분리 → TRACEABLE 800 · N/A 200 · UNTRACED 0.

## 산출물 체크섬

| 파일 | sha256(앞 16) | bytes |
|---|---|---|
| `UNIVERSE_1000.json` | `f37824b8f9675ade` | 3,231,570 |
| `UNIVERSE_1000.csv` | `cffadf26223f5100` | 252,002 |
| `generate.py` | `07bbd3d5437509ed` | 14,081 |

## 준수 확인

SoT 품질 평가 · Mapping 평가 · Coverage/Gap/Runtime/Adapter/법령/Repository/우선순위 분석 **일절 수행하지 않았다.** 이상 현상은 `OBSERVATION_LOG.md`에 증상만 기록했고 원인은 분석하지 않았다.
