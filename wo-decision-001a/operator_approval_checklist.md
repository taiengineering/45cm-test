# Operator Approval Gate

## Selected Strategy
**S1 — Repository Backfill (production_semantic_repository.law_name 공란 325행 → law_master 조인값)**
Target DB: wrfcedzgdrfupenzqhur (leg-runtime). Runtime 코드·Pipeline 무변경.

## Approval Checklist (Operator 확인 항목)
- [ ] Scope 확인 — 대상: 공란 325행(23 오표기 교정 포함 + 292 default 명시화 + numeric 10). 범위 외 컬럼(atom_id/mapped_field/semantic_clause_id/evidence/article) 미변경.
- [ ] Blank-only Update 확인 — law_name IS NULL OR btrim(law_name)='' 행만 갱신.
- [ ] NonBlank 12 보호 확인 — 승강기법/고압가스법/실내공기질법(short-form) 12행 미변경(덮어쓰기 금지).
- [ ] Snapshot Freeze 확인 — 변경 전 337행 스냅샷 보존(content_md5 = 3c63b36321dca7af96bf49622190eeb8).
- [ ] Rollback 준비 확인 — 스냅샷 기반 원복 경로 확보.
- [ ] Runtime Verify 수행 예정 — 23 발화 Profile로 law_name==joined·article·evidence·atom_id·applicability 동일, mismatch 23->0.
- [ ] 300 Regression 수행 예정 — 동일 Runner 재실행; 허용 변화 = 23 law_name 교정 + 새 provenance, 그 외 변화 = FAIL.
- [ ] Freeze 갱신 예정 — RC1 유지 불가, 새 release/freeze를 Governance 규칙으로 발급.
- [ ] Operator 승인 — 위 전 항목 확인 후 실행 승인.

## 주의
실제 프로덕션 DB 쓰기. 본 게이트 승인 후 WO-CHG-010(S1 실행)에서 Apply 단계 재확인.
