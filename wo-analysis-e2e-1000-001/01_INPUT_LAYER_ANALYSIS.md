# 01 INPUT_LAYER_ANALYSIS — WO-ANALYSIS-E2E-1000-001

분석 전용. 수정·설계·개선안 0.

## 계층별 입력·출력·전달·소실 (1,000사 · 추적 16,400행)

| # | Layer | 입력 | 출력 | 전달 | 소실 |
|---|---|---|---|---|---|
| 0 | Universe (SoT) | SoT 조회 결과 | 공정 1,301 · 설비 3,460 · 작업 1,517 | 회사속성 12종 + SoT 3축 | — |
| 1 | Consumer Question | 활성 질문 44종 × 1,000사 | 16,400 질문 | 5,000 응답 | **11,400 NOT_ANSWERABLE** |
| 2 | Canonicalizer | 5,000 | 5,000 | CONVERT 3,700 · PASS 1,300 | **0** |
| 3 | Adapter (`build_input_contract`) | 5,000 | 1,000 | worker_count | **4,000 DROP** |
| 4 | Runtime | 1,000 | 1,000 | worker_count | 0 |
| 5 | Repository (337 atom) | 1,000 | worker_count 매칭 8 atom | — | — |
| 6 | Result | 1,000사 | 필드 1종 | — | — |

## 계층 구조 사실

- **Layer 0의 산출(공정·설비·작업 6,278건)은 Layer 1의 입력 형식과 축이 다르다.** Layer 0은 명칭 문자열, Layer 1은 `has_*` boolean과 목록 필드다.
- **Layer 2는 값을 버리지 않는다.** ALIASES 13종의 이름 정규화만 수행한다.
- **Layer 3이 계약에 싣는 키는 `sector`·`ksic_code`·`worker_count`·`has_*`뿐이다.** Layer 1이 수집한 44종 중 25종이 이 집합 밖이다.
- **Layer 5는 39종 `mapped_field`로만 판정한다.** Layer 3의 출력 21종 중 12종이 이 집합과 교집합을 갖는다.

## 전달률

| 구간 | 전달 | 비율 |
|---|---|---|
| Layer 1 → 2 | 5,000 / 16,400 | 30.5% |
| Layer 2 → 3 | 5,000 / 5,000 | 100% |
| Layer 3 → 4 | 1,000 / 5,000 | 20.0% |
| Layer 4 → 6 | 1,000 / 1,000 | 100% |
| **Layer 1 → 6** | **1,000 / 16,400** | **6.1%** |
