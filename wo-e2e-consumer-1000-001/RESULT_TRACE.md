# RESULT_TRACE — WO-E2E-CONSUMER-1000-001

**Goal** G-mscyylj6-2ebb9b · 입력 `GENERATOR_ASSET_UNIVERSE_1000`(수정 0) · Generator·Universe·엔진·Question 수정 0
**Runtime 미실행.** 아래 수치는 계약 기반 추정이며 실행 결과가 아니다. 카운트로 PASS/FAIL을 선언하지 않는다.

## 전 구간 흐름 (1,000사 · 추적 16,400행)

```
Consumer Question   16,400
   ├ NOT_ANSWERABLE  11,400   ← Universe에 답할 데이터 없음
   └ 응답 가능        5,000
        ↓
Canonicalizer        5,000    DROP 0  (CONVERT 3,700 · PASS 1,300)
        ↓
Adapter              5,000
   ├ DROP            4,000    ← process_list·equipment_list·address·total_floor_area·ksic_major 등
   └ PASS            1,000
        ↓
Runtime              1,000    worker_count (8 atom, Presence-only)
        ↓
Result               1,000사 × 필드 1종
```

## 소실 지점

| 단계 | 건수 | 비율 |
|---|---|---|
| 1_Consumer (NOT_ANSWERABLE) | 11,400 | 69.5% |
| 3_Adapter | 4,000 | 24.4% |
| 4_Runtime | 0 | 0% |
| 끝까지 도달 | 1,000 | 6.1% |

## sector별

| Sector | 추적 | NOT_ANSWERABLE | PASSTHROUGH(Adapter DROP) | 도달 |
|---|---|---|---|---|
| 제조 500사 | 7,000 | 4,000 | 2,500 | 500 |
| 건설 300사 | 3,600 | 2,400 | 900 | 300 |
| 건축물 200사 | 5,800 | 5,000 | 600 | 200 |

## Runtime에 도달한 것

| field | 회사 수 | 저장소 atom |
|---|---|---|
| `worker_count` | 1,000 | 8 (Presence-only) |

**1,000개 사업체가 SoT에서 읽어온 공정 1,301건·설비 3,460건·작업 1,517건 중 Runtime 판정에 도달한 것은 0건이다.** 도달한 유일한 필드는 회사속성인 근로자 수다.

## 읽고 기록한 것 (카운트 아님)

`U1K-0001`(제조, 식료품)은 SoT에서 공정 `가공>배합>혼합기 운전>원료 배합 및 혼합`과 설비 `교반기·원료호퍼·혼합탱크`를 보유한다. 소비자는 이를 `process_list`·`equipment_list`로 답할 수 있고 Canonicalizer도 통과한다. 그러나 Adapter가 계약에 싣지 않아 Runtime은 이 회사를 근로자 수만 아는 상태로 판정한다. 건설 `U1K-0501`은 SoT 작업 `해체 전 안전점검` 등을 보유하나 동일하게 도달하지 않는다.

## 산출물

`e2e_stage_trace.csv`(16,400행) · `e2e_summary.json` · `e2e_field_status.json` · `QUESTION_TRACE.md` · `CANONICALIZER_TRACE.md` · `ADAPTER_TRACE.md` · `RUNTIME_TRACE.md` · `OBSERVATION_DELTA.md`
