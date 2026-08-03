# WO-E2E-LEG-1000-002 · 500건 체크포인트 (Batch 1~10)

**Goal** G-mscro68p-fcf706 · Runtime 미실행 · 코드·엔진·Repository 수정 0.

## 0. 사고 보고 — 감사 스크립트 예외를 못 보고 보고할 뻔했다

Batch5~10 최초 실행에서 `batch_audit.py`가 `KeyError: 'shift'`로 죽었는데(Batch1~2에 신규 변주 필드가 없어서), 나는 종료코드를 확인하지 않고 **직전 실행의 `batch10_gate.json`을 읽어 "복제 30"으로 보고했다.** SIGPIPE 건과 동일 유형의 실수다.

- 조치: 이후 모든 생성·감사·분석은 **종료코드 검사 후에만 결과를 읽는다**(`rc=$?` 확인).
- 재발 방지가 규칙으로만 남지 않도록, 실행 래퍼에서 exit≠0이면 로그 tail을 강제 출력하도록 바꿨다.

## 1. 전 배치 재생성 (re-baseline)

변주 축 추가로 스키마가 갈라졌으므로 **Batch1~10 전부 현재 생성기로 재생성**했다. Batch1·2 보고서의 수치는 그 시점 기록으로 유지하되, 이후 모든 분석은 이 re-baseline을 기준으로 한다.

**추가한 변주 축** (전부 실제 사업장이 서로 다른 항목):
- 제조: 교대제(1/2/3), 설비별 대수, 공정 외주 구간(앞단/뒷단 선택)
- 건설: 공정률(%), 하도급 업체 수, 야간작업 여부
- 건축물: 준공연도, 관리형태(직영/위탁), 미사용 설비 수

결과: **누적 500사 REALISTIC 500/500, 복제 0.**

## 2. 체크포인트 5항목 (Operator 지정)

### ① 도달률 변화 (200 → 500)

| 누적 | 기대 | 도달 | 도달률 |
|---|---|---|---|
| 200사 | 1,017 | 122 | 12.0% |
| **500사** | **2,498** | **297** | **11.9%** |

| Sector | 기대 | 도달 | 도달률 |
|---|---|---|---|
| 제조 | 833 | 48 | 5.8% |
| 건설 | 946 | 0 | **0.0%** |
| 건축물 | 719 | 249 | 34.6% |

**변화 없음.** 200→500에서 0.1%p 이동. 건설 0%는 500사에서도 유지.

### ② 신규 Pattern 발생 여부 — **0건**

| Pattern | Layer | Scope | occurrence |
|---|---|---|---|
| P-Q-001 | Question | CONSTRUCTION | 946 |
| P-Q-002 | Question | MANUFACTURING | 785 |
| P-Q-003 | Question | ALL(ABSENT) | 370 |
| P-R-001 | Repository | BUILDING | 100 |

Pattern Freeze 적용 — 확정 Pattern은 occurrence만 누적하고 재기술하지 않는다. **신규 Pattern 후보 0건.**

### ③ Top 20 Gap 변화

순위 구성 동일. 상위 8개가 200건 시점과 같고 occurrence만 비례 증가.

| field | occ | layer | impact | recovery | prio | atom |
|---|---|---|---|---|---|---|
| has_excavation | 212 | Question | High | Immediate | P1 | 23 |
| has_confined_space | 196 | Question | High | Short | P1 | 15 |
| has_forklift | 157 | Question | High | Immediate | P1 | 7 |
| has_temp_electric | 150 | Question | **Low** | Medium | **P4** | **0** |
| has_concrete_work | 135 | Question | High | Immediate | P1 | 13 |
| has_scaffold | 135 | Question | High | Immediate | P1 | 18 |
| has_pile_work | 121 | Question | High | Immediate | P1 | 14 |
| has_crane | 120 | Question | High | Immediate | P1 | 23 |
| has_sprinkler | 100 | Repository | Medium | Medium | P3 | 0 |

**Occurrence와 Impact 분리가 효과를 냈다.** `has_temp_electric`은 차단 150건으로 4위지만 저장소 atom이 0이라 질문을 열어도 회복이 없다 → Impact Low, **P4**. 빈도만 봤으면 P1으로 잘못 올렸을 항목이다.

### ④ Priority 변경 여부 — **없음**

| Priority | 차단 건수 |
|---|---|
| P1 | 1,076 |
| P2 | 627 |
| P3 | 299 |
| P4 | 199 |

### ⑤ Recovery Score

| Score | 건수 | 비율 | 조치 |
|---|---|---|---|
| **Immediate** | 1,436 | **65.2%** | `is_active=true` 전환만으로 회복 |
| Short | 466 | 21.2% | 질문 항목 신설 또는 Adapter 교정 |
| Medium | 299 | 13.6% | 저장소 atom 신설 필요 |
| Long | 0 | 0.0% | Runtime 변경 필요 없음 |

**차단된 의무의 65%가 플래그 전환만으로 즉시 회복 가능하다.** Runtime 변경이 필요한 건은 0건 — 이 Gap은 엔진 문제가 아니다.

## 3. Sector Heatmap

```
MANUFACTURING
  Question   ■■■■■■■■■■■■■■■■■■■■  785
  Adapter    □                       0
  Repository □                       0
CONSTRUCTION
  Question   ■■■■■■■■■■■■■■■■■■■■  946
  Adapter    □                       0
  Repository □                       0
BUILDING
  Question   ■■■■■■■■■■■■■■■■      370
  Repository ■■■■                  100
```

건설·제조는 **단일 계층(Question)에 100% 집중**. 건축물만 Question 79% + Repository 21%로 갈린다.

## 4. 판단

체크포인트 5항목이 200건 분석과 **전부 동일**하다. 구조는 200건에서 이미 확정됐고, 500건은 그것을 신뢰도 있게 재확인했다. 남은 500건은 새 결론을 만들지 않을 것으로 보이며, 동일 방식으로 진행 후 최종 보고서에서 종합한다.

## 5. 산출물

`batch1~10_companies.json` · `batch10_audit_cumulative.csv`(500사) · `batch10_gate.json` · `gap_impact_500.csv` · `checkpoint_500.json` · `checkpoint.py`
