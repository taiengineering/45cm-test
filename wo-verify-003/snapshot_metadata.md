# WO-VERIFY-003 STEP1 — RC1 Snapshot Metadata (수집)

DB: leg-prod wrfcedzgdrfupenzqhur, public.production_semantic_repository. read-only.

## 컬럼 구조 (메타 컬럼 유무)
atom_id(uuid PK), mapped_field, semantic_clause_id(uuid), law_name, law_article, evidence, repository_version, release_version, freeze_signature, is_readonly(bool), loaded_at(timestamptz).
- 존재하는 생성-흔적 메타 컬럼: **repository_version, release_version, freeze_signature, loaded_at, is_readonly**.
- **부재**: created_at / created_by / loaded_by / updated_at / version / metadata (없음).

## 메타값 (전량 단일)
| 항목 | 값 |
|---|---|
| rows | 337 |
| release_version | SEMREPO-RC1-2026.07.20 |
| repository_version | SEMREPO-CAL022-2026.07.20 |
| freeze_signature | 15cd17e871b6885d34214c84a58adf47 |
| is_readonly | 전 행 true |

## loaded_at 분포 (생성 흔적)
| loaded_at (UTC) | rows |
|---|---|
| 2026-07-20 08:58:52.155 | 30 |
| 2026-07-20 11:08:54.683 | 30 |
| 2026-07-20 11:10:18.757 | 30 |
| 2026-07-20 11:13:21.918 | 60 |
| 2026-07-20 11:15:55.221 | 60 |
| 2026-07-20 11:18:26.119 | 60 |
| 2026-07-20 11:20:59.310 | 60 |
| 2026-07-20 11:21:19.455 | 7 |
| **합계** | **337** |

특성: 2026-07-20 **8배치 적재**(첫 배치 08:58 → 약 2시간 공백 → 11:08~11:21 7배치, 대부분 60행 단위 + 마지막 7). **원자적 스냅샷 스왑이 아니라 페이지 단위 INSERT 적재**. created_by/loaded_by 없음 → 적재 주체는 컬럼에 미기록.
