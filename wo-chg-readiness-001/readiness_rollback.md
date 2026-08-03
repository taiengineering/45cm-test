# WO-CHG-READINESS-001 STEP4 — Rollback Readiness

## STEP4-1 현재 행 스냅샷 (변경 전 보존)
atom_id: 5b849b3e-a3ae-52ae-81e7-3eb4858230ab
```json
{"atom_id":"5b849b3e-a3ae-52ae-81e7-3eb4858230ab","mapped_field":"worker_count","semantic_clause_id":"7509bca1-0700-466c-849b-de465134b186","law_name":"산업안전보건기준에 관한 규칙","law_article":"524","evidence":"사업주는 기압조절실의 바닥면적과 공기의 부피를 그 기압조절실에서 가압이나 감압을 받는 근로자 1인당 각각 0.3제곱미터 이상 및 0.6세제곱미터","repository_version":"SEMREPO-CAL022-2026.07.20","release_version":"SEMREPO-RC1-2026.07.20","freeze_signature":"15cd17e871b6885d34214c84a58adf47","is_readonly":true,"loaded_at":"2026-07-20T11:13:21.918054+00:00"}
```
- **row md5: `d276ebedfc2fd4ff9d3bbe0308c1f0ae`** (변경 후 이 값과 대조; mapped_field 외 컬럼은 불변이어야 함)

## ⚠️ 사전 차단 리스크 (반드시 CHG dry-run에서 확인)
- 이 행은 **is_readonly=true** (RC1 frozen). UPDATE가 트리거/제약으로 **거부될 수 있음**.
- CHG STEP3 dry-run은 트랜잭션 내 UPDATE →영향행 확인거부시은 ROLLBACK으로 **UPDATE 허용 여부를 먼저 검증**해야 함.
- 거부되면: 단순 UPDATE 불가 → 중단·재보고(Operator가 freeze/readonly 처리방침 결정는). Rollback이 아니라 pre-apply 차단으로 처리.
- (미확인: is_readonly가 애플리케이션 레벨 표식인지 DB 트리거로 강제되는지는 dry-run으로 실측 필요.)

## STEP4-2 Rollback SQL (원복용)
```sql
UPDATE public.production_semantic_repository
SET mapped_field='worker_count'
WHERE atom_id='5b849b3e-a3ae-52ae-81e7-3eb4858230ab';
-- 영향행 1 확인 후 COMMIT; 아니면 ROLLBACK
```
원복 성공 판정: 재조회 row md5 == d276ebedfc2fd4ff9d3bbe0308c1f0ae.

## STEP4-3 CHG PASS 성공조건 (전부 충족해야 PASS)
- 산안524만 신규 발화
- 발화 총계 = 329 (기존 328 + 1)
- 기존 328 발화 atom 전부 동일 (누락·추가 없음)
- has_diving 기존 25건 동일
- 산안524 article=524 동일, evidence 동일, law_name 동일
- determinism 동일 (A/B/C 재현 일치)

## STEP4-4 Rollback 조건 (하나라도 발생 시 즉시 Rollback)
- 기존 has_diving atom에 변화
- 발화 총계 329 초과
- 발화 총계 329 미만
- article 변경
- evidence 변경
- 산안524 외 다른 atom 변화
→ 즉시 STEP4-2 Rollback SQL 실행 후 재배포·재검증.
