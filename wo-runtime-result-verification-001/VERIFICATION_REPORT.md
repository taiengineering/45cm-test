# WO-RUNTIME-RESULT-VERIFICATION-001 — Runtime 결과 전수 기계 검증

**Goal** G-msd3aahh-79ff1f
**Verification 이며 Reading 이 아니다.** 사람 독해·Reading Time·Reading Session 기록 없음. 원인분석·개선안 0.

---

## 0. 직전 WO 상태 정정

```
WO-RUNTIME-RESULT-READING-1000-001
  이전 STATUS  PASSED
  정정 STATUS  MISCLASSIFIED
  사유         "Reading"으로 명명했으나 실제 수행한 것은 기계 전수 검증이었다.
               사람이 개별 독해한 것은 2건(U1K-0001·U1K-0501)이며,
               나머지 998건은 집계 처리했다. 거짓 기록은 아니나 분류가 틀렸다.
  산출물       삭제하지 않는다. Verification 산출물로 재분류한다.
  Result Catalog(CAT-001~004) 및 Reading Sheet 1,000건도 동일하게 재분류.
```

사람 독해는 별도 WO(`WO-HUMAN-READING-SAMPLE-001`, 표본 50~100건)로 분리한다.

---

## 1. 검증 방법

```
Load → Parse → Schema Verify → Contract Verify → Evidence Verify → Output Verify → Save
```

입력: `runtime_extract_1000.jsonl` (1,000 records) ← RUNTIME_BASELINE_1000 result_set `f98e5dcf…`
검사 항목: 레코드당 **18개**(의무 없음) 또는 **25개**(의무 1건) · 총 검사 **20,975건**
실행 시간 601.5ms · 재현 가능(`verify.py`)

## 2. 검사 항목별 결과 (전수)

| Stage | Check | PASS | FAIL |
|---|---|---|---|
| PARSE | json_object | 1,000 | 0 |
| SCHEMA | required_keys · types | 1,000 · 1,000 | 0 · 0 |
| CONTRACT | valid_flag | 1,000 | 0 |
| CONTRACT | accepted_eq_active | 1,000 | 0 |
| CONTRACT | active_plus_missing_eq_repo (=39) | 1,000 | 0 |
| CONTRACT | active_missing_disjoint | 1,000 | 0 |
| CONTRACT | unknown_not_in_contract | 1,000 | 0 |
| CONTRACT | invalid_empty | 1,000 | 0 |
| CONTRACT | sent_accounted (전송키 = active ∪ unknown) | 1,000 | 0 |
| EVIDENCE | no_obligation_no_evidence | 575 | 0 |
| EVIDENCE | obl0_atom_id · law · evidence_text · applicability_enum | 425 각 | 0 |
| EVIDENCE | obl0_triggered_by_present | 425 | 0 |
| EVIDENCE | obl0_trigger_in_contract | 425 | 0 |
| EVIDENCE | **obl0_trigger_supplied** | **0** | **425** |
| EVIDENCE | obl0_self_source | 425 | 0 |
| OUTPUT | count_eq_len · http_200 · error_null · status_consistent | 1,000 각 | 0 |
| OUTPUT | provenance_repo_size (337) · provenance_freeze | 1,000 각 | 0 |
| OUTPUT | **rc_snapshot_checksum_present** | **0** | **1,000** |

## 3. 판정

| 판정 | 건수 |
|---|---|
| VERIFY_PASS | **0** |
| VERIFY_FAIL | **1,000** |

Fail-closed 기준상 검사 1건이라도 FAIL이면 레코드는 VERIFY_FAIL이다.

### 실패한 검사 2종

| Check | 건수 | 검증 사실 (원인 없음) |
|---|---|---|
| `OUTPUT:rc_snapshot_checksum_present` | 1,000 | `provenance.rc_snapshot_checksum` 값이 빈 문자열 `""` |
| `EVIDENCE:obl0_trigger_supplied` | 425 | `triggered_by = ["total_floor_area"]` 인데 `total_floor_area`가 `active_fields`에 없음(`missing_fields`에 존재). 실패 detail 값 전건 `total_floor_area` |

**나머지 24개 검사는 전건 PASS.** 특히 `trigger_in_contract`(triggered_by ⊆ 계약 어휘 39종)는 425건 전건 PASS이며, `trigger_supplied`(triggered_by ⊆ 실제 공급 필드)만 실패한다.

## 4. 산출물 · 체크섬

| 항목 | 값 |
|---|---|
| `runtime_verify/` | 1,000건 (`<business_id>.verify.json`) |
| verify set checksum | `7e360d5962059b7b00d42c4b8fe76c5c600fd29e97963bba426720ca90b187a3` |
| `verification_log.csv` | 20,975행 (검사 단위) |
| `verification_summary.csv` | 1,000행 (레코드 단위) |
| `verification_manifest.json` | source sha256 · 판정 집계 · 실패 검사 집계 · 체크섬 |
| `verify.py` | 검증기 (재실행 가능) |

각 `verify.json`은 `source_record_sha256`을 보유해 원본 레코드와 1:1 대조된다.

## 5. 준수 확인

'사람이 읽었다'·Reading Time·Reading Session 기록 **0**. Root Cause·Question/Adapter/Repository 분석·개선안·추론 **0**. 실패 2종은 검증 사실만 기록했고 원인을 쓰지 않았다.
