# RUNBOOK 부록 — R-008 위반 교정

**Goal** G-msczuepg-14f70d

## 위반 내용

RUNBOOK 커밋 시 거버넌스 경고가 발생했다.

```
⚠️ R-008 하드코딩 금지 — 설정값·URL·경로를 코드에 직접 작성할 수 없다.
```

`runtime_execute.py`에 다음이 하드코딩돼 있었다.

- 엔드포인트 URL 기본값 (`https://leg-runtime-production.up.railway.app/rtm/evaluate`)
- 입력 파일 경로 · 결과 디렉토리 경로
- worker 상한 상수

## 교정

전부 환경변수로 이동하고, URL은 **기본값 없이 필수**로 바꿨다.

| 항목 | 변경 후 |
|---|---|
| 엔드포인트 | `LEG_RTM_URL` **필수**. 없으면 즉시 종료하며 R-008을 명시한 메시지 출력 |
| 입력 파일 | `RUNTIME_INPUT` (미지정 시 스크립트 위치 기준 상대경로) |
| 결과 디렉토리 | `RUNTIME_RESULT_DIR` (미지정 시 스크립트 위치 기준 상대경로) |
| worker | `RUNTIME_MAX_WORKERS`, 단 **4 초과 시 4로 클램프**(R2 상한은 코드로 강제 유지) |

환경변수 미주입 실행 시 동작 확인:

```
$ python3 runtime_execute.py
LEG_RTM_URL 환경변수가 없습니다. railway run 으로 실행하거나 변수를 주입하십시오.
(R-008: URL을 코드에 하드코딩하지 않습니다)
```

## 실행 명령 (갱신)

```bash
cd ~/45cm-test/wo-runtime-baseline-1000-001
railway run python3 runtime_execute.py
railway run python3 runtime_execute.py --retry retry_queue.json
```

`railway run`이 `LEG_RTM_URL`을 주입하지 않는 환경이라면 Railway 변수에 해당 키가 있어야 한다. **변수 설정은 운영자 권한이며 본 WO에서 수행하지 않았다.**

## 체크섬 갱신

| 파일 | sha256(앞 24) |
|---|---|
| `runtime_execute.py` | `a5e1a1df0aa8ae07f3f82c22` (이전 `f2fcc8615a3d91938bf55f00`) |
| `runtime_input_1000.jsonl` | `c674e5b67854230af78b9d24` (변경 없음) |

R2 상한 4는 코드로 강제 유지된다(환경변수로 상향 불가).
