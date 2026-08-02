# WO-VERIFY-002 STEP5 — Snapshot Generation / Load Flow (확인된 단계만)

확인된 단계는 실선, 미확정 단계는 [UNCONFIRMED]로 표기. 추정 없음.

```
[UNCONFIRMED] Snapshot Build (빌더 코드/스크립트/CI 미발견)
        │  freeze_signature 생성 ?  ← 미확정
        │  release_version 생성 ?   ← 미확정
        ▼
[CONFIRMED] public.production_semantic_repository  (337행, freeze 15cd17e8, release SEMREPO-RC1)
        │        └ 이 테이블에 '쓰는' 프로세스 = 미발견
        ▼
[CONFIRMED] Runtime Load  (api/rtm_router.py _get_engine -> from_production -> _fetch_rows SELECT)
        │        └ 프로세스당 1회 (lazy singleton)          [WO-VERIFY-001에서 확정, 여기선 하류 맥락으로만 인용]
        ▼
[CONFIRMED] Memory Cache  (모듈 전역 _engine)
        │
        ▼
[CONFIRMED] Response  (/rtm/evaluate)
```

## 확정
- 하류(저장->적재->캐시->응답)는 확정. 저장 테이블 = public.production_semantic_repository.
- 배포 시 빌드 단계 없음(Procfile web only; 런북 "release 훅 없음").

## 미확정 (UNCONFIRMED)
- 상류(Snapshot Build -> freeze 생성 -> release 생성 -> production_semantic_repository 쓰기)의 실행 주체·시점·저장 경로.
- available 45cminc/leg 소스에서 해당 빌더 미발견.
