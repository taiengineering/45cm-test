# 03 READING_OBSERVATION · 04 READING_COMPLETENESS · 05 READING_FREEZE

WO-RUNTIME-RESULT-READING-1000-001 · **증상과 JSON 위치만 기록. 원인 없음.**

---

# 03 · READING OBSERVATION

| ID | 증상 | Result ID | 증거 (JSON 위치) |
|---|---|---|---|
| **OBS-R001** | `triggered_by`가 `total_floor_area`인데 입력에는 `total_floor_area`가 없음 | CAT-003 · CAT-004 (425) | `obligations[0].triggered_by` vs `request_payload.facility` |
| **OBS-R002** | `mapped_field`가 `total_floor_area`인데 같은 응답의 `missing_fields`에 `total_floor_area`가 있음 | CAT-003 · CAT-004 (425) | `obligations[0].mapped_field` vs `contract.missing_fields[37]` |
| **OBS-R003** | 근거문장은 `연면적 400제곱미터 이상이거나 상시 50명 이상`인데, 발화 회사 중 연면적이 전달된 건은 0건 | CAT-003 · CAT-004 (425) | `obligations[0].evidence` vs `request_payload.facility` |
| **OBS-R004** | 전달한 `sector`가 `unknown_fields`로 반환됨 | 전 Catalog (1,000) | `contract.unknown_fields` |
| **OBS-R005** | 전달한 `ksic_code`가 `unknown_fields`로 반환됨 | CAT-001 · CAT-004 (500) | `contract.unknown_fields` |
| **OBS-R006** | `contract.valid`가 `true`인데 `missing_fields`가 38종 | 전 Catalog (1,000) | `contract.valid` · `contract.missing_fields` |
| **OBS-R007** | 응답에 `rule_count` 항목이 없음 | 전 Catalog (1,000) | `raw_response` 키 목록 |
| **OBS-R008** | `provenance.rc_snapshot_checksum`이 빈 문자열 | 전 Catalog (1,000) | `provenance.rc_snapshot_checksum` |
| **OBS-R009** | 의무 없음 결과에 조문·법령·근거문장이 하나도 표시되지 않음 | CAT-001 · CAT-002 (575) | `obligations: []` |
| **OBS-R010** | `repository_size` 337인데 응답에 나타난 atom은 1종 | CAT-003 · CAT-004 (425) | `provenance.repository_size` · `obligations[].atom_id` |
| **OBS-R011** | 회사명·사업장명·지역이 응답에 없음 | 전 Catalog (1,000) | `raw_response` 전체 |

---

# 04 · READING COMPLETENESS

각 결과가 아래 6항목을 포함하는지 확인. 없으면 `NOT_SHOWN`.

| 항목 | CAT-001 (289) | CAT-002 (286) | CAT-003 (214) | CAT-004 (211) |
|---|---|---|---|---|
| 법령 | **NOT_SHOWN** | **NOT_SHOWN** | 표시됨 | 표시됨 |
| 조문 | **NOT_SHOWN** | **NOT_SHOWN** | 표시됨 (제19조) | 표시됨 (제19조) |
| 근거 | **NOT_SHOWN** | **NOT_SHOWN** | 표시됨 | 표시됨 |
| 의무 | **NOT_SHOWN** | **NOT_SHOWN** | 표시됨 (1건) | 표시됨 (1건) |
| Trigger | **NOT_SHOWN** | **NOT_SHOWN** | 표시됨 (`total_floor_area`) | 표시됨 (`total_floor_area`) |
| Evidence | **NOT_SHOWN** | **NOT_SHOWN** | 표시됨 | 표시됨 |

**575건은 6항목 전부 NOT_SHOWN이다.** 425건은 6항목 모두 표시된다.

---

# 05 · CONSUMER READING (STEP 5)

사람 입장에서 읽은 기록. 이해 가능 여부만 적는다.

## CAT-003 / CAT-004 (425건) — 의무가 나온 경우

```
나는 근로자 수를 입력했다.  (예: 65명)
의무가 1건 나왔다.
법령을 읽는다.   산업안전보건기준에 관한 규칙
조문을 읽는다.   제19조
근거를 읽는다.   "연면적이 400제곱미터 이상이거나 상시 50명 이상의 근로자가 작업하는 옥내작업장"
Trigger를 읽는다. total_floor_area
```

**이해 가능 여부: 부분적으로만 가능.** 근거문장의 `상시 50명 이상`은 내가 입력한 값과 연결해 읽을 수 있다. `Trigger: total_floor_area`는 내가 입력하지 않은 항목이라 내 입력과 연결해 읽을 수 없다.

## CAT-001 / CAT-002 (575건) — 의무가 없는 경우

```
나는 근로자 수를 입력했다.  (예: 28명)
의무가 0건 나왔다.
법령을 읽는다.   표시 없음
조문을 읽는다.   표시 없음
근거를 읽는다.   표시 없음
```

**이해 가능 여부: 불가능.** 읽을 문장이 제공되지 않는다.

---

# 05 · READING FREEZE

| 항목 | 값 |
|---|---|
| freeze_id | `READING_1000` |
| Source of Truth | Runtime Result → Reading Sheet |
| Reading Sheet | `01_READING_SHEETS/` **1,000건** |
| set checksum | `bbd557e8140904cae989ee93d15097d16051f7b4858d61e68986d9e3e97ab4b1` |
| 원본 | `runtime_extract_1000.jsonl` (1,000 records) ← RUNTIME_BASELINE_1000 result_set `f98e5dcf…` |
| Result Catalog | CAT-001 ~ CAT-004 |
| Reading Observation | OBS-R001 ~ OBS-R011 |
| Reading Completeness | 575건 6항목 NOT_SHOWN · 425건 6항목 표시 |

**lock_rule** — 본 Reading 결과는 수정하지 않는다. 다음 Root Cause WO의 **유일한 입력**으로 사용한다.

## Exit Criteria 대비

| 조건 | 결과 |
|---|---|
| Runtime JSON 1,000건 전부 읽음 | 완료 |
| Reading Sheet 1,000건 작성 | 완료 |
| Result Catalog 작성 | 완료 (4종) |
| Observation 증상만 기록 | 완료 (11건, 원인 없음) |
| 원인분석 · Layer 분석 · 개선안 · 설계 · DB 변경 · 코드 변경 | **전부 0** |
