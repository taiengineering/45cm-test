# WO-WIRING-FIX-001 STEP5 — 먼저 확인, 그다음 변경 (실측 우선)

## STEP5-1 (신규) — 환경변수 값 확인만 (변경 금지)
Operator가 leg-runtime(production)에서 아래 3개 변수의 연결 대상을 실측한다.
**URL 전문은 기록하지 않는다.** 각 변수당 project_ref / host / database만.

| 변수 | project_ref | host | database |
|---|---|---|---|
| SUPABASE_DB_URL | ? | ? | ? |
| RTM_DATABASE_URL | ? (미설정이면 unset) | - | - |
| DATABASE_URL | ? | ? | ? |

### 확정 판정 (실측)
- `SUPABASE_DB_URL -> ?`
- `RTM_DATABASE_URL -> ?`
- `DATABASE_URL -> ?`
- **`DATABASE_URL == wrfcedzgdrfupenzqhur ?`** <- 이 실측이 PASS여야 STEP5-2 진행

확인 명령(값 노출 최소화):
```
railway link            # tai-api / production / leg-runtime
railway variables       # 3개 변수의 host·project_ref만 눈으로 확인 (URL 전문 기록 금지)
```
※ Supabase 연결 URL의 host는 db.<project_ref>.supabase.co 또는 pooler(aws-1-ap-northeast-2.pooler.supabase.com)이며, pooler는 user 부분 postgres.<project_ref>로 project_ref가 드러남. host/user로 project_ref만 판별.

## STEP5-2 — 변경 (STEP5-1 PASS인 경우에만)
DATABASE_URL == wrfced 실측 확정 시에만:
```
SUPABASE_DB_URL : Before(vwlaht) -> wrfced DATABASE_URL과 동일한 값
```
(방식 A 기준. 기존 계약이 RTM_DATABASE_URL 표준이면 방식 B로 대체하되, 두 변수를 상충되게 두지 않음.)
- 만약 STEP5-1에서 DATABASE_URL이 wrfced가 아니면 -> **변경 중단, BLOCKED, 재보고** (두 번째 잘못된 연결 방지).

## STEP5-3 — Redeploy
```
railway redeploy --service leg-runtime
```

## Rollback
변경 전 SUPABASE_DB_URL 값(vwlaht) 별도 보존 -> 실패 시 복원 후 재배포.

## 이후
STEP6 Deployment SUCCESS 확인 -> STEP7 23 Target Verify(23/23 law_name 교정, article/evidence/applicability 0 drift, unexpected atom 0; **provenance 아닌 23 law_name이 판정 증거**) -> STEP8 300 Regression.
