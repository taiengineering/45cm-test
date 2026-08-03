# 07 ROOTCAUSE_TREE · 08 CONTRADICTION · 09 EVIDENCE_INDEX

WO-ROOTCAUSE-RUNTIME-1000-001 · **Runtime 증거가 있는 것만 Root Cause로 인정한다.**

---

# 07 · ROOT CAUSE TREE

```
Runtime Result (1,000건 실측)
├─ SUCCESS_WITH_RULE 425  →  atom 0ce68131 (산안기준 19조) 1종
└─ SUCCESS_ZERO_RULE 575  →  obligations []
```

## RC-R1 · Adapter Layer — 계약 전송 키가 3종이다

| 항목 | 내용 |
|---|---|
| Runtime 증거 | `request_payload.facility` 실측 = `sector`(1,000) · `worker_count`(1,000) · `ksic_code`(500). 총 2,500키 |
| 귀속 Observation | A1 (CONFIRMED) · A8 (CONFIRMED) |
| Finding | F-R1 |

## RC-R2 · Vocabulary Layer — 전송 키의 60%가 계약 어휘 밖이다

| 항목 | 내용 |
|---|---|
| Runtime 증거 | `unknown_fields` 합 1,500 / 전송 2,500. `sector` 1,000 · `ksic_code` 500. `invalid_fields` 0 |
| 추가 증거 | `missing`38 + `active`1 = 39종이 Repository `mapped_field` 39종과 차집합 양방향 0 |
| 귀속 Observation | A11 (CONFIRMED) · A14 (CONFIRMED) |
| Finding | F-R2 |

## RC-R3 · Source/Question Layer — 요구 입력의 97.4%가 미공급이다

| 항목 | 내용 |
|---|---|
| Runtime 증거 | 요구 39종 × 1,000사 = 39,000 중 공급 1,000. `missing_fields` 합 38,000 |
| 귀속 Observation | A12 (CONFIRMED) · A6 · A7 (PARTIAL — 질문 비활성과 소스 부재가 중첩되어 단독 효과 분리 불가) |
| Finding | F-R3 |

## RC-R4 · Repository Layer — 계약 어휘에 없는 축이 존재한다

| 항목 | 내용 |
|---|---|
| Runtime 증거 | Runtime 계약 39종에 `has_sprinkler`·`has_fire_hydrant`·`has_smoke_control` 및 점검·검사·관리주체 항목 **부재** |
| 귀속 Observation | A9 (CONFIRMED) · A10 (CONFIRMED) |
| Finding | F-R4 |

## RC-R5 · Runtime Layer — 임계 조건이 실재한다

| 항목 | 내용 |
|---|---|
| Runtime 증거 | `worker_count>=50`에서만 `APPLICABLE`. 425/575 분기, 경계 위반 0건, sector·KSIC 무관(KSIC lv2 25종 중 24종 혼재) |
| 귀속 Observation | A5 (**CONTRADICTED**) |
| Finding | F-R5 |

## Root Cause로 인정하지 않은 것

| Layer | 사유 |
|---|---|
| Canonicalizer | Runtime 증거상 손실 0. 귀속 Observation 없음 |
| Consumer / Universe | Runtime 응답에 해당 계층의 직접 증거 없음. A2·A3·A4는 NOT_TRIGGERED로 Runtime 증거 부재 → **Root Cause 미인정** |

---

# 08 · CONTRADICTION

기존 추정과 실측이 다른 것을 **전부** 기록한다. 은폐 없음.

## C-001 · OBS-A5 — CONTRADICTED

```
기존 (추정)  Presence-only. Repository에 임계 컬럼이 없어 값의 크기는 판정에 반영되지 않음.
             → WO-E2E-CONSUMER-1000-001 등에서 확정 Pattern으로 사용
실측         worker_count >= 50 에서만 obligation 발화. 경계 위반 0/1000.
             evidence 원문 "연면적 400제곱미터 이상이거나 상시 50명 이상"
STATUS       CONTRADICTED
```

## C-002 · 도달률 수치 — 모수 불일치로 비교 불가

```
기존 (추정)  Estimated Reachability 12.0% (RC2) / 88.1% (RC3)
             Consumer E2E 추정: 16,400 중 도달 1,000 (6.1%)
실측         Runtime 요구 39,000 중 공급 1,000 (2.6%) / 전송 2,500 중 수용 1,000 (40%)
STATUS       NOT_COMPARABLE — 분모 정의가 서로 다름. 기존 수치를 실측으로 갱신했다고 볼 수 없음
```

## C-003 · OBS-A13 Adapter 소실률 — 모수 불일치

```
기존 (추정)  응답 가능 5,000 중 Adapter 소실 4,000 (80%)
실측         Adapter 전송 2,500. "응답 가능 5,000"은 Runtime 응답으로 확인되지 않음
STATUS       PARTIAL — 방향은 일치하나 수치는 재산정 필요
```

## C-004 · Rule 다양성 가정 — 근거 없었음

```
기존 (암묵)  obl=1 425건의 Rule 구성은 확인되지 않았음
실측         distinct rule 1종. 425건 전부 동일 atom
STATUS       RESOLVED — 전수 확인으로 확정
```

---

# 09 · EVIDENCE INDEX

모든 Finding은 아래 경로로 100% 역추적된다.

| Finding | Runtime JSON | Rule | Repository | Adapter | Question | Consumer | Universe |
|---|---|---|---|---|---|---|---|
| **F-R1** Adapter 전송 키 3종 | `request_payload.facility` (1,000건) | — | — | `input_contract_builder.py` 적재 키 | 활성 질문 44종 | 응답 5,000 추정 | `UNIVERSE_1000.json` |
| **F-R2** unknown 1,500 / 어휘 불일치 | `contract.unknown_fields` (1,500) · `missing_fields`(38,000) | — | `mapped_field` 39 = missing38+active1 | 전송 `sector`·`ksic_code` | — | — | SoT 어휘 396종 |
| **F-R3** 요구 39,000 중 공급 1,000 | `accepted_count`(1,000) · `missing_fields`(38,000) | — | 337 atom / 39 field | 전송 2,500 | 활성 질문 16,400 | — | `NO_GENERATOR_SOURCE` 2,011 |
| **F-R4** 계약 어휘 부재 축 | `missing_fields` 38종 목록 | — | `has_sprinkler` 등 부재 | — | 질문에는 존재 | — | 건축물 4축 부재 |
| **F-R5** worker 50 임계 | `obligation_count` 0/1 × `worker_count` | atom `0ce68131` · article 19 · `triggered_by:["total_floor_area"]` | 337 atom 중 1 발화 | `worker_count` 전송 | `worker_count` 질문 | — | 회사속성 `worker_count` |

## 산출물 체크섬

| 항목 | 값 |
|---|---|
| 입력 `runtime_extract_1000.jsonl` | 1,000 records · 1,717,276 bytes |
| `runtime_trace/` 1,000건 set checksum | `9455d03b77f242066f3ed9fb27f420b5…` |
| RUNTIME_BASELINE_1000 result_set | `f98e5dcfb744194e75d7a5dbab5be9a5e745b22e5cb15c2932c1a9248a9c7e79` |

## 준수 확인

Question·Adapter·Repository·Runtime·Master·Generator 수정 **0**. Coverage·Priority·Recovery 계산 **0**. 개선안·설계안·Action Plan **0**. 모든 수치는 Runtime 응답 또는 Freeze 자산에서 직접 읽었으며 추정치는 `기존(추정)`으로 명시 구분했다.
