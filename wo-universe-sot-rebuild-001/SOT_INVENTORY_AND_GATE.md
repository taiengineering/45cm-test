# WO-UNIVERSE-SOT-REBUILD-001 · STEP 1~3 — SoT Inventory · Coverage Gate

**Goal** G-mscw5m84-942ed5 · 새 공정·설비·작업 정의 0 · SoT 수정 0 · 유사어 수동 연결 0

---

# STEP 6 판정: **SOT_GAP_REQUIRES_DESIGN**

11개 축 중 **5축 AVAILABLE · 6축 SOT_GAP**. 파일럿 50개를 SoT lineage 100%로 생성할 수 없다.

---

## 0. 선행 조치 — UNIVERSE_1000 지위 변경 (Operator 판정 반영)

```
UNIVERSE_1000
  STATUS          = NON_CANONICAL
  TYPE            = GENERATOR_MODEL_BASED
  USE             = 방법론·질문계층 관찰 참고자료
  PROHIBITED_USE  = 운영 Baseline / Golden / Regression SoT
```

**사용 중지 표현**: 대한민국 현실 사업체 1,000개 · PROFILE_UNIVERSE_V2 · RC3 Baseline · 표준 Universe
**허용 표현**: Generator-defined synthetic universe 1,000

**METHOD_VALID · NUMERIC_BASELINE_NOT_APPROVED**
유지: 4단계 stage trace · NOT_ASKED 분리 · fail-closed audit · Pattern Freeze · Recovery Potential 계산 방식
동결 금지: 12.0% · 88.1% · Question 4,175 · Recovery 3,784 · Sector별 도달률

## 1. STEP 1 — SoT Inventory (실측)

| 축 | 테이블 | 행 | 표준코드 | 매핑 | active | version | 상태 |
|---|---|---|---|---|---|---|---|
| KSIC | `industry_master` | 501 | `industry_code_full` (숫자 4자리) | — | 501 | ksic_revision 1 | **AVAILABLE** |
| KSIC→공정 | `ksic_process_map` | 6,957 | `industry_code_full` (**A0111 알파벳형**) | — | 없음 | 1 | **SOT_GAP** |
| KSIC→공정→설비 | `process_equipment_map` | 187,319 | `industry_code_full` (숫자 4자리) | 자체 | 없음 | source_type 5 | **AVAILABLE** |
| 설비→작업 | `maintenance_master` | 150 | `equipment_std` (15종) | — | is_active | — | **SOT_GAP** |
| 설비→작업 | `inspection_master` | — | `equipment_std` (1종) | — | is_active | — | **SOT_GAP** |
| 건설표준→공종 | `kcsc_process_master` | 161 | `kcs_code`·`full_code` | — | 161 | 1 | **AVAILABLE** |
| 건설공종→작업 | `kcsc_work_master` | 243 | `kcs_code` | `process_id` | 243 | 32 | **AVAILABLE** |
| 건설 프로젝트유형 | — | — | — | — | — | — | **SOT_GAP** |
| 건축물 분류 | `buildings` | 1 | — | — | — | — | **SOT_GAP** |
| 건축물→설비/관리작업 | `facility_profiles` | 104 | `use_code_value` (실값 0) | — | — | profile_version | **SOT_GAP** |

## 2. 조사 중 확인된 구조적 사실 3건

**F-1 · KSIC 코드 표기 체계 불일치 (신규 발견)**
`industry_master.industry_code_full` = `2412` 형식, `ksic_process_map.industry_code_full` = `A0111` 형식. 양쪽 모두 501종으로 동일 모집단이지만 **직접 조인 0/501**. 문자열 변환으로 붙이는 것은 본 WO가 금지한 "유사어 수동 연결"에 해당하므로 시도하지 않았다.

**F-2 · 대체 경로 존재**
`process_equipment_map`이 `industry_code_full`(숫자형, `industry_master` 조인 501/501) · `process_id`(`ksic_process_map` 조인 2,807) · `process_path` · `facility_name_std`를 **한 테이블에 함께** 보유한다. 따라서 **업종→공정→설비는 이 단일 테이블로 표기 변환 없이 lineage 확보가 가능**하다. `ksic_process_map`은 코드 조인은 불가하나 `process_id`로는 연결된다.

**F-3 · `process_equipment_map.lv2_code`는 KSIC이 아니다**
값이 `1 전기`·`2 기계`·`10 산업생산`·`12 유틸리티`로 **설비 분류 코드**다. KSIC lv2와 코드값이 겹쳐 조인하면 **의미 없는 결과가 나온다**(내가 첫 시도에서 실제로 걸렸다). 재구축 생성기는 반드시 `industry_code_full`로 조인해야 한다.

## 3. STEP 3 — SoT Coverage Gate

| Sector | 축 | SoT | 어휘 규모 | 판정 |
|---|---|---|---|---|
| 제조 | 업종(KSIC) | YES | 182 industry_code / 25 lv2 | AVAILABLE |
| 제조 | 공정 | YES | 124 process_path | AVAILABLE |
| 제조 | 설비 | YES | 415 facility_name_std | AVAILABLE |
| 제조 | **작업** | **NO** | 0 | **SOT_GAP** |
| 건설 | **공사유형** | **NO** | 3 (BUILDING/CIVIL/COMMON) | **SOT_GAP** |
| 건설 | 공종 | YES | 161 | AVAILABLE |
| 건설 | 작업 | YES | 243 | AVAILABLE |
| 건설 | **설비·건설기계** | **NO** | 0 | **SOT_GAP** |
| 건축물 | **용도** | **NO** | 0 | **SOT_GAP** |
| 건축물 | **설비** | **NO** | 0 | **SOT_GAP** |
| 건축물 | **관리작업** | **NO** | 0 | **SOT_GAP** |

### SoT로 표현 가능한 범위

- **제조**: 업종 → 공정 → 설비까지 lineage 100% 가능. **작업 축은 불가.**
- **건설**: 공종 → 작업까지 lineage 100% 가능. **공사유형·설비 축은 불가.**
- **건축물**: **전 축 불가.** 표준 마스터가 존재하지 않는다.

## 4. STEP 6 판정 근거

```
SOT_UNIVERSE_READY        ✗  건축물 전 축 부재, 제조 작업·건설 유형/설비 부재
SOT_SOURCE_INCOMPLETE     ✗  소스는 존재하고 접근 가능하며 구조도 확인됨
SOT_GAP_REQUIRES_DESIGN   ✓
```

**파일럿 50(제조 25·건설 15·건물 10)은 현재 SoT로 생성할 수 없다.** 건물 10건은 표준 용도 분류조차 없어 lineage 0%가 되고, 제조 25건은 작업 축이, 건설 15건은 공사유형·설비 축이 각각 비어 `Unknown provenance 0` 조건을 위반한다. 없는 것을 만들어 채우는 것은 본 WO의 실패 기준(새 공정/설비/작업 정의)에 정확히 해당하므로 **STEP 4를 진행하지 않고 여기서 멈춘다.**

## 5. Operator 결정 필요 사항 (제안하되 임의 진행하지 않음)

| # | 결정 사항 | 선택지 |
|---|---|---|
| D1 | KSIC 코드 표기 불일치(F-1) | ⓐ `process_equipment_map` 단일 경로만 사용(변환 불필요) ⓑ 코드 변환 매핑을 **SoT로 신설** 후 사용 |
| D2 | 제조 작업 축 부재 | ⓐ 작업 없이 업종·공정·설비만으로 축소 Universe ⓑ 제조 작업 Master 신설 WO |
| D3 | 건설 공사유형·설비 축 부재 | ⓐ 공종·작업만으로 축소 ⓑ Master 신설 WO |
| D4 | 건축물 전 축 부재 | ⓐ 건축물 Sector를 재구축 범위에서 제외 ⓑ 건축물 Master 신설 WO |

D2~D4를 ⓐ로 가면 축소 Universe로 즉시 파일럿이 가능하지만, 구성비(제조 500·건설 300·건물 200)와 "회사→공정→설비→작업→소비자 입력" 경로가 성립하지 않는다. ⓑ는 Master 신설이므로 본 WO 범위 밖의 별도 승인이 필요하다.

## 6. 산출물

`sot_inventory.csv` · `sot_coverage_gate.csv` · 본 문서(`generator_provenance` 후속)
