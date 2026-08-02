# WO-WIRING-FIX-001 STEP3 — 환경변수 수정안 고정 (코드 변경 0)

목표: RTM loader가 LEG DB(wrfcedzgdrfupenzqhur)를 읽도록 env만 복원.
LEG DB URL = 현재 **DATABASE_URL 값** (host aws-1-ap-northeast-2.pooler.supabase.com, project_ref wrfced).

## 유효한 두 방식 (기존 계약에 따라 하나 선택)
### A. SUPABASE_DB_URL을 LEG DB URL로 교체
- SUPABASE_DB_URL = (LEG DB URL, = 현재 DATABASE_URL 값)
- 단일 변수 값 변경. loader 1순위가 그대로 LEG DB를 가리킴.
- 특징: 변수명(SUPABASE_DB_URL)은 TAI/Supabase 소스를 암시 — 값만 LEG DB로.

### B. SUPABASE_DB_URL 제거 + RTM_DATABASE_URL = LEG DB URL
- SUPABASE_DB_URL 삭제, RTM_DATABASE_URL = (LEG DB URL)
- loader가 SUPABASE_DB_URL 없음 → RTM_DATABASE_URL(LEG DB) 사용.
- 특징: 오해 소지 있는 SUPABASE_DB_URL 제거, RTM 전용 변수로 명확히 분리. 2개 변수 변경.

## 금지 (무효)
- SUPABASE_DB_URL(=vwlaht)을 그대로 둔 채 RTM_DATABASE_URL만 추가 → 코드가 SUPABASE_DB_URL을 우선하므로 **반영 안 됨**.

## 공통
- 코드 변경 0 · DB row 변경 0 · TAI 서비스 변경 0.
- After project_ref(양안 공통) = wrfcedzgdrfupenzqhur.
- 방식 선택은 Operator(기존 배포 계약 기준).
