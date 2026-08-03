# Release Note — CHG-MAPFIELD-001

**Date:** 2026-08-03
**Type:** Data correction (semantic repository mapped_field)
**Status:** CHG_SUCCESS
**DB:** wrfcedzgdrfupenzqhur (LEG runtime source) · **Service:** leg-runtime

## Summary
산업안전보건기준에 관한 규칙 제524조(기압조절실 1인당 면적/부피) atom의 mapped_field를
`worker_count` → `has_diving`으로 교정. worker_count로 잘못 매핑되어 런타임에서 발화되지 않던 문제를 해소.

## Change
| 항목 | Before | After |
|---|---|---|
| atom_id | 5b849b3e-a3ae-52ae-81e7-3eb4858230ab | (동일) |
| mapped_field | worker_count | has_diving |
| law_name / article / evidence / scid | — | 불변 |
| row md5 | d276ebedfc2fd4ff9d3bbe0308c1f0ae | 3cfb0750cd014d287198cd2d0edb5994 |

## Impact
- Repository: worker_count 9→8, has_diving 25→26, 전체 337 불변, 중복 0, 산안524 외 변경 0.
- Runtime (has_diving payload): obligation_count 328 → **329**. 산안524 신규 발화. 기존 328 drift 0.

## Verification
- READINESS COMPLETE (격리성·충돌·예측·Rollback Readiness 4 Gate PASS).
- 트랜잭션 단건 UPDATE + assertion(affected=1) → COMMIT.
- Runtime 재배포 후 has_diving payload로 329·산안524 발화·기존 328 보존 확인.
- 결정성: 1회 329로 갈음(Operator 결정; A/B/C 3회 미실행).

## Rollback (미발동, 수단 유지)
```sql
UPDATE public.production_semantic_repository
SET mapped_field='worker_count'
WHERE atom_id='5b849b3e-a3ae-52ae-81e7-3eb4858230ab';
-- 원복 후 row md5 == d276ebedfc2fd4ff9d3bbe0308c1f0ae
```

## Artifacts (taiengineering/45cm-test, wo-chg-mapfield-001/)
- chg_snapshot_precheck.md (0cc4b05)
- chg_apply_result.md (ddbb118)
- chg_runtime_verify.md (bec629c)
- chg_verdict.md (bf91dad)

## Follow-ups (별도 WO)
- 300 Profile Regression (다음 단계).
- Track B BACKLOG 8건 입력모델 설계 (NEW_BOOLEAN 5 / INPUT_MODEL_CHANGE 3).
- freeze_signature 15cd17e8 정책 검토: RC1 freeze/repository_version 갱신 여부는 별도 판단 대상(본 CHG는 단건 데이터 교정이며 freeze 서명은 변경하지 않음 — 미확인/보류).
