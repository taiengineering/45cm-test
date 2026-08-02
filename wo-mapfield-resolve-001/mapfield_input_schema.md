# WO-MAPFIELD-RESOLVE-001 STEP1 — 런타임 유효 입력 필드 목록 (38종)

출처: production_semantic_repository의 distinct mapped_field (런타임이 실제 매칭하는 필드 어휘, read-only).

has_hazardous_material(45) · has_diving(25) · has_crane(23) · has_excavation(23) · has_dust_work(20) ·
has_elevator(19) · has_scaffold(18) · has_confined_space(15) · has_welding(15) · has_pile_work(14) ·
has_concrete_work(13) · has_asbestos(10) · worker_count(9) · has_subcontractor(8) · has_forklift(7) ·
has_radiation(7) · has_conveyor(6) · has_gas(6) · has_boiler(5) · has_grinding(5) · has_blasting(4) ·
has_high_place_work(4) · has_noise_work(4) · has_rolling(4) · has_steel_frame(4) · has_demolition(3) ·
has_gondola(3) · has_high_pressure_gas(3) · has_pressure_vessel(3) · has_chemical(2) · is_multi_use(2) ·
has_casting(1) · has_emergency_broadcast(1) · has_emergency_gen(1) · has_hazmat_storage(1) ·
has_painting(1) · has_press(1) · has_water_tank(1) · total_floor_area(1)

## 핵심 관찰 (9개 정답 확정에 직결)
- **has_height_work 없음** — 이전 검증 payload가 쓴 이름은 무효였음. 실제는 **has_high_place_work**.
- **수동 중량물취급 필드 없음** — has_crane/forklift/conveyor/gondola/elevator는 모두 기계. 5kg 인력취급(art665) 대응 없음.
- **응급의료 대응 필드 없음** — has_emergency_broadcast/gen은 방송설비·발전기(장비)로, 응급환자 처치와 무관.
- **상시적용(근로조건) 표현 없음** — 모든 필드가 해저드/장비 presence. 근로기준법(야간근로·연차·수유 등)은 대응 필드 부재.
