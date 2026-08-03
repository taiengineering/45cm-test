# 03 ZERO_RULE_TRACE — WO-ROOTCAUSE-RUNTIME-1000-001

SUCCESS_ZERO_RULE 575건 **전수** 관찰. **원인 판단 없음 — 관찰만.**

## Layer별 관찰 (575건 전건 동일 패턴)

| Layer | 관찰값 | 출처 |
|---|---|---|
| L0 Universe | 회사 레코드 존재. `NO_GENERATOR_SOURCE` 축 보유(제조 work / 건설 equipment·project_type / 건축물 4축) | `UNIVERSE_1000.json` |
| L1 Question | 활성 질문 수 sector별 상이(제조 14 · 건설 12 · 건축물 29). Runtime에 도달한 질문 필드는 `worker_count` 1종 | `diagnosis_input_fields` + 요청 payload |
| L2 Canonicalizer | 전송 키 손실 0 | 요청 payload |
| L3 Adapter | 전송 키 = 제조 `{sector, worker_count, ksic_code}` / 건설·건축물 `{sector, worker_count}` | `request_payload` |
| L4 Runtime | `accepted_count=1` · `active_fields=["worker_count"]` · `unknown_fields` 1~2종 · **`missing_fields` 38종** | Runtime 응답 |
| L5 Repository | `repository_size` 337 · freeze `15cd17e8…` | provenance |
| L6 Result | `runtime_status=NO_APPLICABLE` · `obligation_count=0` · `obligations=[]` | Runtime 응답 |

## Runtime이 반환한 `missing_fields` 38종 (575건 전건 동일)

`has_asbestos` `has_blasting` `has_boiler` `has_casting` `has_chemical` `has_concrete_work` `has_confined_space` `has_conveyor` `has_crane` `has_demolition` `has_diving` `has_dust_work` `has_elevator` `has_emergency_broadcast` `has_emergency_gen` `has_excavation` `has_forklift` `has_gas` `has_gondola` `has_grinding` `has_hazardous_material` `has_hazmat_storage` `has_high_place_work` `has_high_pressure_gas` `has_noise_work` `has_painting` `has_pile_work` `has_press` `has_pressure_vessel` `has_radiation` `has_rolling` `has_scaffold` `has_steel_frame` `has_subcontractor` `has_water_tank` `has_welding` `is_multi_use` `total_floor_area`

**대조 결과**: `missing_fields`(38) ∪ `active_fields`(1) = **39종**이며, `production_semantic_repository`의 `mapped_field` 39종과 **차집합 양방향 0**. 즉 Runtime이 요구하는 입력 집합은 Repository 어휘와 정확히 일치한다.

## `unknown_fields` 관찰

| 구성 | 건수 | 대상 |
|---|---|---|
| `["ksic_code","sector"]` | 500 | 제조 |
| `["sector"]` | 500 | 건설·건축물 |

전송한 `sector`(1,000)·`ksic_code`(500)는 **Runtime 계약 어휘에 없어 unknown 처리**됐다. 전송 2,500키 중 수용 1,000 · unknown 1,500 · invalid 0.

## ZERO_RULE 575건과 WITH_RULE 425건의 차이

Runtime 응답에서 두 집합의 차이는 **`worker_count` 값 하나뿐**이다. `active_fields`·`accepted_count`·`missing_fields`·`unknown_fields`·`contract_valid`·provenance는 1,000건 전건 동일하다.

| 항목 | ZERO_RULE 575 | WITH_RULE 425 |
|---|---|---|
| `worker_count` | 1~49 | 50~899 |
| 그 외 계약 필드 | **완전 동일** | **완전 동일** |
