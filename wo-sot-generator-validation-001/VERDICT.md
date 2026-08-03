# WO-SOT-GENERATOR-VALIDATION-001 · Generator Provenance 검증 (제조 25건)

**Goal** G-mscx9s9l-1e676b · Universe는 산출물이 아니다 · 품질·현실성·Adapter·Runtime·Question 평가 없음

---

# STEP 7 판정: **SOT_ONLY**

Generator는 도메인 하드코딩 없이 SoT 조회 결과만으로 25건을 생성했고, 194개 항목 전건이 `source_table` + `source_row_id`까지 추적된다.

---

## STEP 1 · Generator 입력원

| Source | Purpose | Read Count | DB Table | Hardcoded |
|---|---|---|---|---|
| R1 | 제조 업종 선정 (lv2 10~34, is_active) | 25 rows | `public.industry_master` | **NO** |
| R2 | 업종→공정→설비 lineage | 144 rows | `public.process_equipment_map` | **NO** |
| — | 회사명·규모·면적·지역 | 0 | 없음 | **NO** (MASTER_ABSENT) |
| — | 제조 작업 | 0 | 없음 | **NO** (MASTER_ABSENT) |

두 SQL 전문은 `sot_snapshot_meta.json`에 기록. `ksic_process_map`은 **읽지 않았다** — `industry_master`와 코드 표기가 달라(`A0111` vs `2412`) 코드 조인이 0/501이며, 문자열 변환은 금지된 유사어 연결에 해당한다. D1-ⓐ 결정대로 `process_equipment_map` 단일 경로만 사용했다.

## STEP 3 · 하드코딩 제거 — 정적 검사

`sot_generator.py` 실측 (docstring 제외):

| 검사 | 결과 |
|---|---|
| 한글 문자열 리터럴(도메인 값 후보) | **0건** |
| 도메인 dict 리터럴 | **0건** |
| 길이 4 이상 list 리터럴 | **0건** |
| if/elif 분기 | 4 (전부 존재여부 판정, 도메인 분기 아님) |

업종명·공정명·설비명·작업명이 코드에 **단 하나도 등장하지 않는다.** 이전 생성기(`mfg.py` 597항목 하드코딩)와의 차이가 이 지점이다.

## STEP 4 · 25건 생성 결과

| 항목 | 값 |
|---|---|
| 회사 | 25 (제조, lv2 10~34 각 1) |
| 공정 | 50 (SoT) |
| 설비 | 144 (SoT) |
| 작업 | **0 — NULL 유지** |
| 회사명·근로자수·면적·지역 | **NULL 유지** |
| 보완·추론 | **0건** |

## STEP 5 · Provenance 전수 검증 (샘플링 없음)

| 검증 | 결과 |
|---|---|
| standard_code 추적 | **25/25** |
| process 추적 | **25/25** (50건) |
| equipment 추적 | **25/25** (144건) |
| 미추적 항목 | **0** |

```
회사 SOT-M015
 → public.industry_master   row ecc76792-104f-4b3c-b26a-5a1d6cb2d7c8   2412 철강 압연, 압출 및 연신제품 제조업
 → public.process_equipment_map row e798a7f6-c36c-4c6b-b721-03b892a40633
      process_id KOSHA-M-184-2015-P001
      process_path 열처리>용접후열처리>가열 및 유지>용접부 열처리
      facility_name_std 열처리로
 → Generator → Output
```

## STEP 6 · Unknown 원인 분리 (혼합 없음)

| axis | 원인 | 건수 |
|---|---|---|
| company_name | MASTER_ABSENT | 25 |
| worker_count | MASTER_ABSENT | 25 |
| total_floor_area | MASTER_ABSENT | 25 |
| region | MASTER_ABSENT | 25 |
| work | MASTER_ABSENT | 25 |

`MASTER_EXISTS_BUT_NOT_CONNECTED` 0 · `GENERATOR_LOGIC` 0 · `DATA_ERROR` 0.

## STEP 7 · 판정

```
SOT_ONLY             ✓
PARTIAL_SOT          ✗
HARDCODE_REMAINING   ✗
```

**SOT_ONLY** — 생성기가 SoT만으로 동작함이 25건 전수로 증명됐다. 종료 조건(`Source → Generator → Output` 100% 추적) 충족.

## 범위 밖 Observation (기록만, 평가 아님)

SoT 조회 중 관측된 사실 2건. 본 WO는 품질평가가 금지돼 있으므로 **판정하지 않고 기록만** 한다.

- **OBS-S1**: 업종 1012(육류가공)·1112(증류주)·1310(방적)·1411(겉옷)이 `process_equipment_map`에서 **동일한 process_id·설비 집합**(`KOSHA-M-125-2012-P001` 교반기·원료호퍼·혼합탱크 / `KOSHA-M-175-2014-P001` 보일러·열교환기)을 공유한다.
- **OBS-S2**: 업종 1200(담배)·2323(요업)·2513(금속가공)·2721(정밀기기)·3402(수리업)가 동일한 `기계제조>가공>연삭/절삭` 경로와 동일 설비 3종을 공유한다.

두 관측 모두 SoT 데이터의 특성이며, 다음 WO(예: SoT 품질 검증)의 입력이 될 수 있다.

## 산출물

`sot_generator.py` · `sot_snapshot_meta.json` · `sot_R1_industry.json` · `sot_R2_process_equipment.json` · `sot_companies_25.json` · `sot_provenance_review.csv` · `gen.log` · `review.log`
