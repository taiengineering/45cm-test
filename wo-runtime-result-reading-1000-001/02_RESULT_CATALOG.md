# 02 RESULT_CATALOG — WO-RUNTIME-RESULT-READING-1000-001

Runtime Result JSON 1,000건을 읽어 **결과가 동일한 회사를 묶었다.** 왜 같은지는 쓰지 않는다.

## Catalog

| Catalog | runtime_status | obligation_count | 발화 의무 | active_fields | unknown_fields | missing_fields | 건수 |
|---|---|---|---|---|---|---|---|
| **CAT-001** | `NO_APPLICABLE` | 0 | 없음 | `worker_count` | `ksic_code`, `sector` | 38 | **289** |
| **CAT-002** | `NO_APPLICABLE` | 0 | 없음 | `worker_count` | `sector` | 38 | **286** |
| **CAT-003** | `OK` | 1 | 산업안전보건기준에 관한 규칙 제19조 (`0ce68131…`) | `worker_count` | `sector` | 38 | **214** |
| **CAT-004** | `OK` | 1 | 산업안전보건기준에 관한 규칙 제19조 (`0ce68131…`) | `worker_count` | `ksic_code`, `sector` | 38 | **211** |

합계 1,000. **결과 그룹은 4종이다.**

## 상위 묶음 (의무 유무 기준)

| 묶음 | 건수 |
|---|---|
| 의무 없음 (CAT-001 + CAT-002) | **575** |
| 산안 제19조 1건 (CAT-003 + CAT-004) | **425** |

## 08 · Reading Quality

| Catalog | 판정 |
|---|---|
| CAT-001 | **모호함** |
| CAT-002 | **모호함** |
| CAT-003 | **읽기 어려움** |
| CAT-004 | **읽기 어려움** |

## Provenance (1,000건 전건 동일)

```
release_version     SEMREPO-RC1-2026.07.20
repository_version  SEMREPO-CAL022-2026.07.20
freeze_signature    15cd17e871b6885d34214c84a58adf47
repository_size     337
```

## Reading Sheet

`01_READING_SHEETS/U1K-0001.md` ~ `U1K-1000.md` **1,000건**
set checksum `bbd557e8140904cae989ee93d15097d16051f7b4858d61e68986d9e3e97ab4b1`
