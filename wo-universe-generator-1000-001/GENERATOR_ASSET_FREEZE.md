# GENERATOR_ASSET — UNIVERSE_1000 Freeze

**freeze_id** `GENERATOR_ASSET_UNIVERSE_1000` · **WO** WO-UNIVERSE-GENERATOR-1000-001 · **Goal** G-mscybhg5-6c7bfe · **동결일** 2026-08-03

---

## 1. 용어 교정 (승인 조건 반영)

Operator 지적을 수용해 상태값을 바꿨다. **내가 관측한 것은 "Generator가 읽을 SoT가 없다"인데, 이전 산출물은 "DB에 Master가 없다"로 읽히게 적혀 있었다.** 두 주장은 다르고, 후자는 본 WO가 조사하지 않았다.

| 이전 | 변경 후 | 의미 |
|---|---|---|
| `MASTER_ABSENT` | **`NO_GENERATOR_SOURCE`** (+ `scope: generator scope`) | Generator가 읽을 수 있는 SoT가 없음. **DB Master 부재 주장 아님** |
| `MASTER_EXISTS_BUT_NOT_CONNECTED` | **`SOURCE_EXISTS_BUT_NOT_LINKED`** | 소스 row는 조회됐으나 하위 연결 row 없음 |

`PROVENANCE_LOG.md`에 용어 주의 문단과 `scope` 컬럼을 추가해, 후속 WO가 "실제 Master가 없었는가"를 별도로 조사할 수 있게 했다.

## 2. 동결 대상

| 항목 | 값 |
|---|---|
| 자산 유형 | **Generator Asset** |
| 사업체 | 1,000 (제조 500 · 건설 300 · 건축물 200) |
| full_record checksum | `ccc275c4bbcc39adc49e8dd7…` |
| REALISTIC | 1,000 / 1,000 |
| duplicates | 0 (회사명 고유 1,000) |
| provenance | 6,778건 · UNTRACED 0 |
| 추적 상태 | TRACEABLE 800 · N/A_NO_SOT_AXIS 200 · UNTRACED 0 |
| seed 규칙 | `random.Random(20260803)` + 회사별 `random.Random(20260803+i)` |

| 파일 | sha256(앞 16) | bytes |
|---|---|---|
| `UNIVERSE_1000.json` | `43e35b92ad0310a9` | 3,306,989 |
| `UNIVERSE_1000.csv` | `77b7fe4fca3b46f2` | 263,069 |
| `generate.py` | `fa48ce028747139e` | 14,419 |
| `PROVENANCE_LOG.md` | `a4cfb507ca99f98b` | 2,376 |
| `OBSERVATION_LOG.md` | `d36abe7f763e5e72` | 853 |

SoT 스냅샷: `sot_mfg_lineage.json`(1,948행 / 182 업종) · `sot_con_lineage.json`(372행 / 공정 161 · 작업 243)

## 3. NO_GENERATOR_SOURCE 내역 (2,011건)

| axis | status | scope | records |
|---|---|---|---|
| work | `NO_GENERATOR_SOURCE` | generator scope | 700 |
| equipment | `NO_GENERATOR_SOURCE` | generator scope | 500 |
| project_type | `NO_GENERATOR_SOURCE` | generator scope | 300 |
| building_use | `NO_GENERATOR_SOURCE` | generator scope | 200 |
| process | `NO_GENERATOR_SOURCE` | generator scope | 200 |
| work | `SOURCE_EXISTS_BUT_NOT_LINKED` | generator scope | 111 |

## 4. lock_rule

**재생성 금지.** 이후 모든 E2E·Coverage 평가는 본 자산을 기준으로 한다. 오류 발견 시 레코드를 조용히 수정하지 않고 Observation으로 남긴다.

**supersedes**: 이전 `UNIVERSE_1000 (GENERATOR_MODEL_BASED, NON_CANONICAL)`을 대체한다. 이전 자산은 삭제하지 않는다.

## 5. WO 종료

```
Generator     PASS
Universe      PASS
Observation   PASS
분석          미실시 (계약 준수)
```

SoT 품질·Mapping·Coverage·Gap·Runtime·Adapter·법령·Repository·우선순위 분석은 일절 수행하지 않았다.

## 6. 다음 단계 (별도 승인)

본 자산을 입력으로 `Consumer → Question → Adapter → Runtime` E2E. 앞선 WO에서 확립된 방법론(4단계 stage trace · NOT_ASKED 분리 · fail-closed audit · Pattern Freeze · Recovery Potential)은 그대로 재사용 가능하며, 수치 baseline만 본 자산 기준으로 새로 산출한다.
