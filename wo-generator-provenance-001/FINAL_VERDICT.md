# WO-GENERATOR-PROVENANCE-001 · 최종 판정

**Goal** G-mscvsesw-de9b6b · 새 Matrix·공정·설비·작업 정의 0 · SoT 수정 0 · 추론 판정 0

---

# 판정: **GENERATOR_REDEFINED_SOT**

Generator는 기존 SoT를 **조회하지 않았고**, 산업 모델(공정·설비·작업)을 자체 정의했다.

---

## 결정적 증거 — STEP 1

생성기 5개 파일(`batchgen.py`·`mfg.py`·`con.py`·`bld.py`·`catalog.py`)에 대한 정적 검사:

| 파일 | DB·네트워크 호출 | 파일 I/O |
|---|---|---|
| batchgen.py | **0** | 2 (자기 배치 결과 read/write) |
| mfg.py | **0** | 0 |
| con.py | **0** | 0 |
| bld.py | **0** | 0 |
| catalog.py | **0** | 0 |

`execute_sql`·`psycopg`·`supabase`·`urllib`·`requests` 호출 **0건**. `industry_master`·`kcsc_process_master`·`kcsc_work_master`·`equipment_model_master`·`ksic_process_map`·`process_equipment_map` 참조 **0건**.

**Generator는 KSIC Source·Construction Source·Building Source 어느 것도 입력으로 받지 않는다.** 전부 Python dict/list 하드코딩이다.

- `mfg.PROCESS_EQUIP` (공정→설비 35개 키), `mfg.EQUIP_TASK` (설비→작업 59개 키), `mfg.FLOWS` (24업종 공정흐름), `mfg.ARCHETYPES` (24)
- `con.TRADES` (16 공종), `con.PIPELINES` (TUNNEL/PLANT)
- `bld.USES` (10 용도), `bld.SIZE_SPEC`, `bld.MGMT_INPUTS`

## STEP 2~4 · 출처 확인 100% (597 항목 전건)

`generator_source_inventory.csv` — 항목 1건마다 `기존 SoT` / `혼합(부분일치)` / `Generator 정의`를 부여. **Unknown 0건.**

## STEP 6·7 · SoT 사용률 및 Drift

| 축 | 총 | 기존 SoT | 혼합 | Generator 정의 | SoT 사용률 | Drift |
|---|---|---|---|---|---|---|
| mfg_ksic | 13 | 13 | 0 | 0 | **100.0%** | **NO_DRIFT** |
| mfg_process | 35 | 18 | 6 | 11 | 51.4% | MEDIUM |
| mfg_equipment | 59 | 23 | 0 | 36 | 39.0% | HIGH |
| con_task | 70 | 10 | 15 | 45 | 14.3% | HIGH |
| mfg_flow_step | 147 | 1 | 9 | 137 | 0.7% | HIGH |
| con_trade | 16 | 0 | 6 | 10 | 0.0% | FULL_REPLACEMENT |
| con_machine | 17 | 0 | 0 | 17 | 0.0% | FULL_REPLACEMENT |
| con_equip | 34 | 0 | 0 | 34 | 0.0% | FULL_REPLACEMENT |
| mfg_task | 145 | 0 | 5 | 140 | 0.0% | FULL_REPLACEMENT |
| bld_use | 10 | 0 | 0 | 10 | 0.0% | FULL_REPLACEMENT |
| bld_mech | 16 | 0 | 0 | 16 | 0.0% | FULL_REPLACEMENT |
| bld_maint | 35 | 0 | 0 | 35 | 0.0% | FULL_REPLACEMENT |
| **합계** | **597** | **65** | **41** | **491** | **10.9%** | **HIGH** |

### 대조 기준 (전부 실측)

- 공정: `kcsc_process_master.process_name`(161) + `ksic_process_map.process_lv1~lv4`
- 설비: `process_equipment_map.facility_name_std` + `equipment_model_master.equipment_std`(2,874행)
- 작업: `kcsc_work_master.title`(243) 전량
- 업종: `industry_master.lv2_code`(501행)

### 축별 사실

- **KSIC만 100% 일치.** 13개 lv2 코드 전건이 `industry_master`에 존재한다. 유일하게 SoT를 따른 축이다.
- **제조 공정 18/35 일치.** 검사·조립·도장·포장·용접·성형·혼합·반응·건조·사출·살균·열처리·염색·프레스·방적·소성·유틸리티·주조. 다만 이는 **우연한 명칭 일치**이지 조회 결과가 아니다(STEP1에서 조회 자체가 없음).
- **제조 설비 23/59 일치.** 가열로·교반기·보일러·압력용기·천장크레인·컨베이어 등.
- **건설 공종 0/16 exact.** `골조·기계설비·기초·파일·내장·소방·전기·조경·포장·조적·미장·창호·유리·해체·철거` 10건은 부분일치조차 없다. KCSC는 `가설비계 설치 및 해체` 같은 **작업 단위**인데, 내가 만든 것은 **공종 단위**라 층위 자체가 다르다.
- **제조 작업 0/145.** `kcsc_work_master`는 전량 건설 작업이라 제조 작업 SoT가 애초에 존재하지 않는다.
- **건설장비·건물용도·건물설비·유지관리작업**은 대조할 Master 테이블 자체가 taieng DB에 없다.

## STEP 8 · 판정

```
GENERATOR_SOT_CONFIRMED    ✗
GENERATOR_PARTIAL_SOT      ✗
GENERATOR_REDEFINED_SOT    ✓
```

**GENERATOR_REDEFINED_SOT** — 전체 SoT 사용률 10.9%, Drift HIGH. 유일하게 SoT를 따른 축은 KSIC 업종코드(100%)이며, 그조차 조회가 아니라 하드코딩된 값이 우연히 일치한 것이다. **UNIVERSE_1000의 공정·설비·작업 체계는 기존 SoT가 아니라 Generator(Claude)가 새로 정의한 산업 모델이다.**

## 이 판정이 기존 결론에 갖는 함의 (사실만 기록, 조치 없음)

1. **RC2/RC3의 Estimated Reachability(12.0% → 88.1%)는 SoT 기반 공정·설비 체계가 아니라 Generator 자체 모델 위에서 산출됐다.** 수치의 방향성(Question Layer 병목)은 `has_*` 필드 대조에 근거하므로 SoT 여부와 독립이지만, **회사 구성의 산업적 정확성은 SoT로 뒷받침되지 않는다.**
2. Batch 0에서 "제조 22개 업종 아키타입, 공정→설비→작업 허용관계"를 만들 때 **나는 taieng Master를 조회하지 않았고, 그 사실을 보고서에 명시하지 않았다.** 당시 근거로 든 것은 Adapter·Repository 실측뿐이었고, 산업 모델은 내가 작성한 것이다. 이는 이번 감사로 처음 드러난 사실이며 기록해 둔다.
3. 과거 `PROFILE_UNIVERSE_V1`(112 profile, 2026-07-30)은 문서상 `industry_master`·`kcsc_process_master` 실측을 사용했다고 기재돼 있다. **이번 Universe는 그 방식을 따르지 않았다.** 두 Universe는 출처 계보가 다르다.

## 산출물

`generator_provenance.md`(본문) · `generator_source_inventory.csv`(597건) · `generator_drift.csv`(12축) · `sot_usage_ratio.json` · `gen_inventory.json` · `final_verdict.md`(본 판정)
