# WO-CHG-011 STEP4 — Apply Gate (승인 대기)

## 변경 예정 (blank-only)
| 항목 | 값 |
|---|---|
| **실제 변경 예정 행 수** | **325** (law_name 공란 → 조인 정답) |
| **보호할 비공란 행 수** | **12** (미변경; 조인 정식명칭과 다르나 blank-only라 유지) |
| **미해소(UNRESOLVED) 행 수** | **0** |
| Before content_checksum | 5b4669a39bcda241c09a22679872709a |
| 대상 DB | vwlahtguyggrhvslabax (SUPABASE_DB_URL) |

## 325건 채워질 값 분포
- 산업안전보건기준에 관한 규칙 297
- 도시가스사업법 5 · 건설산업기본법 4 · 근로기준법 4
- 정보통신공사업법 2 · 소방시설공사업법 2 · 화학물질관리법 2 · 도시가스사업법 시행규칙 2
- 건축법 1 · 어린이놀이시설 안전관리법 1 · 응급의료에 관한 법률 1 · 석면안전관리법 1 · 산업안전보건법 1 · 수도법 시행규칙 1 · 건설기계 안전기준에 관한 규칙 1

## 보호되는 12개 비공란 (미변경)
- 승강기법 → (조인:승강기 안전관리법) 7건
- 고압가스법 → (조인:고압가스 안전관리법) 3건
- 실내공기질법 → (조인:실내공기질 관리법) 2건
※ blank-only 정책상 이 12건은 건드리지 않음. 정식명칭 정규화 여부는 별도 판단 사항.

## 23 Target atom 예상 (STEP7 대비)
- 23개 전부 vwlaht에서 현재 공란 → 조인값은 23개 모두 산안규칙이 아닌 개별 법령
- 현재 런타임 출력은 이 23개를 "산업안전보건기준에 관한 규칙"으로 내보냄 → backfill+재배포 후 개별 법령으로 바뀔 것으로 예상(STEP7에서 23/23 교정 확인 가능)

## Rollback snapshot (원복 근거)
- 변경 전 상태: 대상 325행 law_name = '' (공란), content_checksum = 5b4669a39bcda241c09a22679872709a
- Apply는 트랜잭션 내 실행; 영향 행수 ≠ 325이면 즉시 ROLLBACK

## 실행 예정 SQL (승인 후 STEP5)
```
BEGIN;
UPDATE public.production_semantic_repository r
SET law_name = COALESCE(lm.law_name, lm.law_name_short)
FROM public.semantic_clause sc
JOIN public.law_article la ON la.id = sc.source_article_id
JOIN public.law_master lm ON lm.id = la.law_id
WHERE r.semantic_clause_id = sc.id
  AND (r.law_name IS NULL OR btrim(r.law_name) = '');
-- 영향 행수 = 325 확인 후 COMMIT, 아니면 ROLLBACK
COMMIT;
```

## 승인 요청
위 내용(325 변경 / 12 보호 / 0 미해소)을 확인하시고 승인("고"/"승인"/"진행")해 주시면 STEP5 blank-only UPDATE를 트랜잭션으로 실행합니다. 승인 전에는 UPDATE하지 않습니다.
