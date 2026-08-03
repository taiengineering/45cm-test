# 04 LINEAGE_ANALYSIS — WO-ANALYSIS-E2E-1000-001

## Lineage 유형 3종 (1,000사 실측)

### 유형 A — 완주 (Lineage 유지) · 1,000건

```
Universe 회사속성 worker_count
  → Question  worker_count        [ASKED, 응답]
  → Canonical worker_count        [CONVERT, 이름 정규화]
  → Adapter   worker_count        [PASS, Input Contract 적재]
  → Runtime   worker_count        [PASS]
  → Repository mapped_field worker_count (8 atom)
  → Obligation 판정 입력으로 사용
```
단계 5개 통과. **유일한 완주 경로.** Presence-only이므로 값의 크기는 판정에 반영되지 않는다.

### 유형 B — Layer 3 단절 · 4,000건

```
Universe SoT 공정/설비 · 회사속성 면적·업종코드·지역
  → Question  process_list · equipment_list · total_floor_area · ksic_major · address …
  → Canonical CONVERT/PASS       [소실 0]
  → Adapter   ─────────────────  ✗ 단절 (계약 적재 키 밖)
  (Runtime · Repository 미도달)
```
단계 2까지 유지, 3에서 단절.

### 유형 C — Layer 1 단절 · 11,400건

```
Universe (해당 축 NO_GENERATOR_SOURCE)
  → Question  has_boiler · elevator_count · electric_capacity · has_safety_manager …
  ─────────── ✗ 단절 (응답 데이터 없음)
```
단계 1에서 단절. Layer 0의 소스 부재가 선행 조건.

## 단계별 Lineage 상태

| 구간 | 유지 | 변경 | 단절 |
|---|---|---|---|
| Universe → Question | 5,000 | 0 | 11,400 |
| Question → Canonical | 1,300 | 3,700 (alias 정규화) | 0 |
| Canonical → Adapter | 1,000 | 0 | 4,000 |
| Adapter → Runtime | 1,000 | 0 | 0 |
| Runtime → Repository | 1,000 | 0 | 0 |

**"변경"은 Layer 2에서만 발생하며 이름 정규화에 한정된다. 값 변환은 전 구간에서 0건이다.**

## SoT 3축의 Lineage 종점

| 축 | Universe 산출 | Question 도달 | Runtime 도달 |
|---|---|---|---|
| 공정 (process_path 119종) | 1,301건 | `process_list`로 수용 | **0** |
| 설비 (facility_name_std 62종) | 3,460건 | `equipment_list`로 수용 | **0** |
| 작업 (work title 215종) | 1,517건 | 대응 질문 없음 | **0** |

SoT에서 읽어온 6,278건 중 Repository 판정에 도달한 것은 0건이다.

## 단절 지점 좌표

| 단절 | Layer | 코드 근거 |
|---|---|---|
| 유형 B | Layer 3 | `services/input_contract_builder.py` — contract 구성이 `factory_id`·`sector`·`ksic_code`·`worker_count` + `has_*`로 한정 |
| 유형 C | Layer 1 | `diagnosis_input_fields` 활성 질문 44종 대비 Universe 보유 속성 불일치 |
| 작업 축 | Layer 1 | 활성 질문에 작업 축 대응 필드 부재 |
