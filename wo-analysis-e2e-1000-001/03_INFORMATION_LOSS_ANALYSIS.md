# 03 INFORMATION_LOSS_ANALYSIS — WO-ANALYSIS-E2E-1000-001

## 상태별 발생 위치·원인·다음 Layer 영향

| 상태 | 발생 위치 | 발생 원인 (구조) | 다음 Layer 영향 | 본 E2E 건수 |
|---|---|---|---|---|
| **NOT_ASKED** | Layer 1 진입 전 | 질문이 카탈로그에 없거나 `is_active=false` | 값이 생성되지 않아 Layer 2 이후 전 구간 부재 | 0 (본 Universe 축 기준) |
| **NOT_ANSWERABLE** | Layer 1 | 질문은 노출되나 Universe에 대응 데이터 없음 | 응답 없음 → Layer 2 미진입 | **11,400** |
| **PASSTHROUGH_ONLY** | Layer 3 또는 5 | 계약에 미적재(3) 또는 `mapped_field` 부재(5) | 판정에 사용되지 않음 | **4,000** |
| **DROP** | Layer 3 | `build_input_contract`가 `sector`·`ksic_code`·`worker_count`·`has_*`만 적재 | Layer 4 미도달 | **4,000** |
| **MISMATCH** | Layer 3 | 필드명·형식 불일치, 변환 코드 부재 | Layer 4 미도달 | 0 (해당 필드가 앞단 NOT_ANSWERABLE) |
| **UNSUPPORTED** | — | (구 상태값, NOT_ASKED로 분리됨) | — | 0 |
| **NO_GENERATOR_SOURCE** | Layer 0 | Generator가 읽을 SoT 없음 (generator scope) | 회사 레코드에 값 부재 → Layer 1에서 NOT_ANSWERABLE 유발 | **2,011** |
| **SOURCE_EXISTS_BUT_NOT_LINKED** | Layer 0 | 소스 row는 조회되나 하위 연결 row 없음 | 해당 축 부분 결손 | **111** |

## 인과 연쇄 (구조 관측)

```
NO_GENERATOR_SOURCE (Layer 0, 2011)
        ↓ 회사 레코드에 값 부재
NOT_ANSWERABLE (Layer 1, 11400)
        ↓ 응답 없음
(Layer 2·3·4 미진입)
```

```
응답 가능 5000 (Layer 1)
        ↓ Canonicalizer DROP 0
5000 (Layer 2)
        ↓ Adapter 계약 키 제한
DROP 4000 / PASS 1000 (Layer 3)
```

## 소실 지점 분포

| 지점 | 건수 | 비율 |
|---|---|---|
| Layer 1 (NOT_ANSWERABLE) | 11,400 | 69.5% |
| Layer 3 (Adapter DROP) | 4,000 | 24.4% |
| Layer 5 (mapped_field 부재) | 0 | 0% |
| 소실 없음 | 1,000 | 6.1% |

## 구조적 사실

- **Layer 2(Canonicalizer)의 소실은 0이다.** 정보 손실은 Layer 1과 Layer 3에 집중된다.
- **Layer 1 소실의 선행 원인은 Layer 0에 있다.** `NO_GENERATOR_SOURCE` 2,011건이 회사 레코드의 값 부재를 만들고, 그 값 부재가 `NOT_ANSWERABLE` 11,400건으로 나타난다. 두 수치의 배율 차이는 질문 수(44종)가 회사당 반복 적용되기 때문이다.
- **Layer 5 소실이 0인 것은 Repository가 완전해서가 아니라, Layer 3에서 이미 12종 도달 어휘 외 전부가 제거되었기 때문이다.**
