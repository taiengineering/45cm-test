# WO-VERIFY-001 STEP5 — Runtime Loading Diagram (확인된 부분만)

/rtm/evaluate 경로. 각 화살표는 코드 증거로 확인된 부분만 표기. 추정 없음.

```
[Client] POST /rtm/evaluate
   │
   ▼
api/rtm_router.py : rtm_evaluate(payload)
   │   trace_id 부여, payload.facility 추출
   ▼
_get_engine()                         ← 모듈 전역 _engine
   │
   ├─ if _engine is None  ─────────────┐   (프로세스당 최초 1회만)
   │                                    ▼
   │                      RuntimeMatchingEngine.from_production(_fetch_rows, strict_baseline=True)
   │                                    │
   │                                    ▼
   │                      load_production_repository(_fetch_rows)
   │                                    │  strict_baseline 게이트(337/freeze/release/idset)
   │                                    ▼
   │                      _fetch_rows():  psycopg2.connect(SUPABASE_DB_URL or RTM_DATABASE_URL)
   │                                    │  SELECT ... FROM public.production_semantic_repository ORDER BY atom_id
   │                                    ▼
   │                      Repository(rows, provenance)  ── 메모리 보관 ──┐
   │                                                                     │
   └─ else (2회차 이후) ──────────────────────────────────────────────►│  캐시된 _engine 재사용
                                                                         ▼
                                                          rtm_api.diagnose(engine, facility)
                                                                         │  engine.run() + engine._provenance()
                                                                         ▼
                                                          JSONResponse(status, obligations, provenance, ...)
```

## 확인된 사실
- DB SELECT는 `_engine is None`인 최초 1회만 실행 → 이후 프로세스 수명 동안 메모리 `_engine` 재사용.
- provenance(release/freeze/repository_size)는 보관된 repository에서 산출.
- 읽는 테이블 = public.production_semantic_repository (교정 대상과 동일).

## 미확인 (UNVERIFIED)
- 라이브 `SUPABASE_DB_URL`/`RTM_DATABASE_URL` 시크릿 값이 wrfcedzgdrfupenzqhur를 가리키는지 (문서상은 그러함, 라이브 env 미확인).
- 프로세스 재기동(배포/재시작) 시 _engine이 새로 초기화되는지의 실제 운영 동작(코드상 전역 캐시는 프로세스 수명; 운영 재기동 실측은 다음 WO 영역).
