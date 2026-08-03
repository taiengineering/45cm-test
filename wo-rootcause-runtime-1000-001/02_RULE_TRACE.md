# 02 RULE_TRACE — WO-ROOTCAUSE-RUNTIME-1000-001

SUCCESS_WITH_RULE 425건 **전수** 추출. 샘플링 없음.

## 발화 Rule — distinct **1종**

425건의 `obligations[]`를 전부 추출해 `(atom_id, mapped_field, law_name, law_article, triggered_by, applicability, evidence)` 튜플로 집계한 결과 **distinct 1종**이다.

| 항목 | 값 |
|---|---|
| Rule ID (`atom_id`) | `0ce68131-3ec9-5bed-af04-755550683691` |
| `source_atom_ids` | `["0ce68131-3ec9-5bed-af04-755550683691"]` (자기 1건) |
| Law | 산업안전보건기준에 관한 규칙 |
| Article | 19 |
| Requirement (`evidence`) | `사업주는 연면적이 400제곱미터 이상이거나 상시 50명 이상의 근로자가 작업하는 옥내작업장` |
| `mapped_field` | **`total_floor_area`** |
| `triggered_by` | **`["total_floor_area"]`** |
| `applicability` | `APPLICABLE` |
| 발화 건수 | **425 / 425** (전건 동일) |

## Condition / Evaluation (Runtime 응답 기준)

| 관측 | 값 |
|---|---|
| Runtime이 수용한 필드 | `worker_count` 단 1종 (`active_fields`, `accepted_count=1`) |
| `total_floor_area` 의 계약 상태 | **`missing_fields`에 포함** (1,000건 전건) |
| 발화 조건 실측 | `worker_count >= 50` 에서만 `APPLICABLE`, 경계 위반 0건 |

## 기록되는 사실 (해석 없음)

- 이 Rule은 `mapped_field`·`triggered_by`가 모두 `total_floor_area`인데, **`total_floor_area`는 요청에 포함되지 않았고 Runtime이 `missing_fields`로 반환했다.**
- 그럼에도 425건이 `APPLICABLE`로 발화했고, 발화 여부는 `worker_count` 50 경계와 정확히 일치한다.
- `evidence` 원문에는 `연면적 400제곱미터 이상` **또는** `상시 50명 이상`의 두 조건이 포함되어 있다.

위 세 항목은 Runtime 응답에서 직접 읽은 것이며, 왜 이런 조합이 나오는지는 본 WO에서 판단하지 않는다.

## Repository 대조

`repository_size` 337 (provenance 전건 동일). 337 atom 중 본 실행에서 발화한 것은 **1 atom**이다.
