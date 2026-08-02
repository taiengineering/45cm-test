# WO-DEBUG-LOADER-001 — Loader Call Chain (STEP1)

대상: 새로 기동한 leg-runtime(45cminc/leg, uvicorn api.server:app :8080) 의 **/rtm 경로** — 우리가 STALE을 관측한 엔드포인트(/rtm/evaluate).

## Application Startup → Repository 생성 호출 흐름 (코드 확정)
```
[Procfile/entrypoint] uvicorn api.server:app  (port 8080; boot log: "Uvicorn running on http://0.0.0.0:8080" / "Application startup complete" 일치)
  |
api/server.py
  - app = FastAPI(...)
  - try: from api.rtm_router import rtm_router; app.include_router(rtm_router)   # /rtm/* 병행 마운트 (try/except 격리)
  - @app.on_event("startup") _warmup(): get_service()  # <- LEGACY RuntimeService(/health,/evaluate)만 사전 로드. RTM 엔진은 여기서 안 만듦.
  |
api/rtm_router.py   (경로: POST /rtm/evaluate, GET /rtm/health)
  - _engine = None  (모듈 전역)
  - _get_engine():
        global _engine
        if _engine is None:                                   # <- LAZY SINGLETON
            _engine = RuntimeMatchingEngine.from_production(_fetch_rows, strict_baseline=True)
        return _engine
  - _fetch_rows():
        dsn = os.environ.get("SUPABASE_DB_URL") or os.environ.get("RTM_DATABASE_URL")   # <- DSN 출처(환경변수)
        conn = psycopg2.connect(dsn)
        cur.execute(PRODUCTION_QUERY)                          # <- LIVE DB SELECT
        return [dict(r) for r in cur.fetchall()]
  |
rtm_engine/rtm/engine.py :: RuntimeMatchingEngine.from_production(fetch_rows)
  - from .production_repository import load_production_repository
  - repo = load_production_repository(fetch_rows, strict_baseline=True)
  - return cls(repo)
  |
rtm_engine/rtm/production_repository.py :: load_production_repository(fetch_rows)
  - rows = fetch_rows()                                        # <- 유일한 행 소스 (=_fetch_rows, psycopg2)
  - (strict_baseline) 무결성 검증: rows==337, distinct atom_id==337, idset md5==EXPECTED_IDSET(15cd17e8), freeze==EXPECTED_FREEZE, release==EXPECTED_RELEASE, evidence 누락 0
  - return ProductionRepository(rows, _to_provenance(rows))    # provenance = rows[0]에서 취함
  |
[Repository 완성] engine.repository.source = "PRODUCTION_SEMANTIC_REPOSITORY"
  - /rtm/evaluate 응답의 provenance(release/freeze/repository_version/repository_size)는 이 rows에서 파생
```

## 요점 (코드 사실)
- /rtm 엔진은 **최초 /rtm 요청 시 1회** 지연 생성되는 프로세스 전역 싱글턴(`_engine`).
- Repository는 **오직 `fetch_rows()`가 돌려준 DB 행**으로 구성된다. 파일/artifact 경로 없음.
- provenance 값은 DB가 돌려준 rows에서 그대로 파생된다(하드코딩 아님; 단 무결성 검증 상수는 존재).
