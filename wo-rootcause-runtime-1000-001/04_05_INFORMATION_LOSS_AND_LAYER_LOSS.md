# 04 INFORMATION_LOSS · 05 LAYER_LOSS — WO-ROOTCAUSE-RUNTIME-1000-001

## 04 · 회사별 Trace (STEP 4)

`runtime_trace/<business_id>_trace.json` **1,000건 생성**. trace set checksum `9455d03b77f242066f3ed9fb27f420b5…`

각 파일 구조 — 실제 전달 payload와 Runtime 응답을 계층별로 보존:

```
L0_universe      standard_code · processes · equipment · works · no_generator_source · worker_count · total_floor_area
L1_question      asked · answerable · not_answerable
L2_canonicalizer input · output · dropped
L3_adapter       emitted(실제 전송 키) · count
L4_runtime       accepted · active_fields · unknown · missing · runtime_status · trace_id
L5_repository    repository_size · freeze
L6_result        obligation_count · obligations[]
evidence         runtime_ms · http · started_at · finished_at
```

예 (`U1K-0501_trace.json`): L0 공정 1·설비 0·작업 5 → L3 emitted `{sector, worker_count}` → L4 accepted 1 / unknown `["sector"]` / missing 38 → L6 obligation 1.

## 05 · Layer Loss (실측, STEP 5)

| Layer | Input | Output | Loss | Loss % | 근거 |
|---|---|---|---|---|---|
| L1 Question (노출된 질문) | **16,400** | 1,000 | 15,400 | 93.9% | `diagnosis_input_fields` 활성 질문 × 1,000사 vs Runtime 도달 질문 필드 |
| L2 Canonicalizer | 2,500 | 2,500 | **0** | 0% | 요청 payload 키 수 |
| L3 Adapter (전송) | — | **2,500** | — | — | `request_payload.facility` 키 실측 (sector 1,000 · worker_count 1,000 · ksic_code 500) |
| L4 Runtime 수용 | 2,500 | **1,000** | 1,500 | 60.0% | `accepted_count` 합 1,000 · `unknown_fields` 합 1,500 · `invalid` 0 |
| L5 Repository 요구 대비 공급 | **39,000** | 1,000 | **38,000** | 97.4% | Runtime 요구 39종 × 1,000사 vs 공급 1,000 |
| L6 Result | 1,000 | **425 의무** | — | — | `obligation_count` 합 |

### 핵심 실측 3항

1. **Runtime이 요구한 입력 39,000건 중 실제로 공급된 것은 1,000건(2.6%)이다.** 나머지 38,000건은 Runtime이 스스로 `missing_fields`로 반환했다.
2. **전송한 2,500키 중 1,500키(60%)를 Runtime이 `unknown_fields`로 반환했다.** `sector` 1,000 · `ksic_code` 500. 전송했으나 계약 어휘가 아니다.
3. **Canonicalizer 손실은 0이다.** 전송 키가 그대로 Runtime에 도달했다.

### 337 atom 대비

Repository 337 atom 중 본 실행에서 평가 가능했던 조건은 `worker_count` 계열이며, 발화한 것은 **1 atom**이다.
