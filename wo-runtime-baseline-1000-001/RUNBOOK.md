# WO-RUNTIME-BASELINE-1000-001 · 실행 준비 완료 · 운영자 실행 대기

**Goal** G-msczuepg-14f70d · 분석 0 · Mock 0 · `.env` 생성 0 · 엔진/Question/Adapter/Repository 수정 0

---

## 실행 명령 (운영자 터미널)

```bash
cd ~/45cm-test/wo-runtime-baseline-1000-001
railway run python3 runtime_execute.py
```

재시도(실패분 단독 실행):

```bash
railway run python3 runtime_execute.py --retry retry_queue.json
```

**이 컨테이너는 네트워크가 차단되어 있어 실행하지 않았다.** R1(실환경 전용·Mock 금지)에 따라 로컬 대체 실행도 하지 않았다.

## 원칙 대비 구현

| 원칙 | 구현 |
|---|---|
| R1 실환경 전용 | 엔드포인트는 `LEG_RTM_URL` 환경변수(기본 `https://leg-runtime-production.up.railway.app/rtm/evaluate`). `.env` 생성·읽기 없음. Mock 코드 없음 |
| R2 worker ≤ 4 | `--workers` 지정값을 **강제로 4로 클램프**(`min(args.workers, 4)`) |
| R3 fail closed | `ThreadPoolExecutor.map` 내부에서 예외를 잡아 FAIL 레코드로 기록하고 다음 건 계속 |
| R4 retry queue | 실패 전건을 `retry_queue.json`(`business_id`·`reason`)으로 생성. `--retry` 단독 실행 가능 |
| R5 전체 결과 저장 | `runtime_result/<business_id>.json` 1,000건. request_payload·raw_response·provenance·타임스탬프 포함 |
| R6 summary | `runtime_summary.csv` — business_id·status·runtime_ms·rule_count·obligation_count·error·started_at·finished_at. **디스크의 전체 결과를 재스캔해 병합**하므로 retry 후에도 1,000행 유지 |
| R7 로그 | `runtime.log` — START/COMPANY/FINISH/WARN. append 모드 |
| R8 manifest | `runtime_manifest.json` — universe_checksum·input_file_sha256·endpoint·runtime_version·engine_version·git_commit·railway_environment·started/finished·worker·success·failed·distinct_provenance |

`rule_count`·`obligation_count`는 응답 구조를 **가정하지 않고** 후보 키를 순회해 관측한다(값이 없으면 `null`).

## 요청 계약

이전에 운영자가 직접 실행해 성공한 러너(`wo-e2e-leg-002/e2e_300_runner.py`)의 계약을 그대로 사용한다. 추측 없음.

```
POST {LEG_RTM_URL}
Content-Type: application/json
body = {"facility": { ... }}
```

## 입력 페이로드 — `runtime_input_1000.jsonl`

1,000행 · sha256 `c674e5b67854230af78b9d24…` · distinct payload 772종

페이로드는 **Adapter(`build_input_contract`)가 실제로 계약에 싣는 키만** 담았다. 추가·추론 없음.

```json
{"business_id":"U1K-0001","sector":"MANUFACTURING",
 "payload":{"facility":{"sector":"INDUSTRIAL","worker_count":28,"ksic_code":"1011"}}}
{"business_id":"U1K-0501","sector":"CONSTRUCTION",
 "payload":{"facility":{"sector":"CONSTRUCTION","worker_count":65}}}
{"business_id":"U1K-0801","sector":"BUILDING",
 "payload":{"facility":{"sector":"BUILDING","worker_count":145}}}
```

### 페이로드 구성에 대한 사실 고지 (해석·제안 아님)

`has_*` 계열은 포함하지 않았다. UNIVERSE_1000에 해당 축의 값이 없어(`NO_GENERATOR_SOURCE`) 소비자 응답이 생성되지 않고, 앞선 E2E 추적에서 `NOT_ANSWERABLE`로 관측된 것과 동일한 상태다. 없는 값을 채워 넣는 것은 본 WO의 원칙에 어긋나므로 넣지 않았다.

따라서 이번 실행은 **현재 Consumer 경로가 Runtime에 실제로 전달하는 입력 그대로의 Baseline**이다. 이전 300건 러너는 `has_*`를 직접 주입해 Adapter를 건너뛰었으므로 두 실행은 입력 성격이 다르다. **이 사실만 기록하며 어느 쪽이 옳은지 판단하지 않는다.**

## 산출물 (실행 후 생성)

```
runtime_result/           1,000건
runtime_summary.csv
runtime_manifest.json
runtime.log
retry_queue.json
```

## 다음

실행 결과(`runtime_manifest.json` · `runtime_summary.csv` 요약)를 회신해 주시면 `RUNTIME_BASELINE_1000_FREEZE.md`를 작성하고 4종 체크섬(result·summary·manifest·retry)을 고정하겠다. **분석은 다음 WO에서 수행한다.**

## 파일 체크섬

| 파일 | sha256(앞 24) |
|---|---|
| `runtime_execute.py` | `f2fcc8615a3d91938bf55f00` |
| `runtime_input_1000.jsonl` | `c674e5b67854230af78b9d24` |
