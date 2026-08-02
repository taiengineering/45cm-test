# WO-CHG-010B STEP2 — Apply Result

Target DB: wrfcedzgdrfupenzqhur · table: public.production_semantic_repository · 2026-08-02 (session d42e35)

## Snapshot 재확인 (STEP1, 실행 직전)
337 rows / blank 325 / nonblank 12 / freeze 15cd17e871b6885d34214c84a58adf47 / content_md5 fc0ae59209770214d3e15c86dd8cc889 — WO-CHG-010A 고정값과 완전 일치.

## Applied SQL (blank-only, Operator "고" 승인 후 실행)
UPDATE production_semantic_repository.law_name = COALESCE(law_master.law_name, law_master.law_name_short)
via semantic_clause -> law_article -> law_master 조인
WHERE law_name IS NULL OR btrim(law_name)=''.

## 결과
- rows_updated = 325 (blank-only)
- 비공란 12행: WHERE 조건 밖 -> 미변경
- law_name 외 컬럼(atom_id/mapped_field/semantic_clause_id/evidence/law_article): SET 대상 아님 -> 불변
- is_readonly: 미변경
