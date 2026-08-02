-- WO-CHG-009 Pattern Dictionary 운영 DB 반영
-- Snapshot: FP03-DEPLOY-001 @ 2026-08-01T12:14Z
-- 운영자 Mac(~/45cm-test)에서 psql -f 로 실행. 엔진 Supabase DB 대상.
-- idempotent: IF NOT EXISTS + 재실행 시 TRUNCATE 후 재삽입.
BEGIN;

CREATE TABLE IF NOT EXISTS pattern_dictionary (
  pattern_id   text PRIMARY KEY,
  pattern_type text NOT NULL,
  trigger      text NOT NULL,
  role         text NOT NULL,
  source_wo    text DEFAULT 'WO-PATTERN-002',
  deployed_at  timestamptz DEFAULT now()
);
TRUNCATE pattern_dictionary;
INSERT INTO pattern_dictionary (pattern_id,pattern_type,trigger,role) VALUES ('P-R1','DEFINITION','"○○"이란','REGULATED_OBJECT_ONLY');
INSERT INTO pattern_dictionary (pattern_id,pattern_type,trigger,role) VALUES ('P-R2','APPLIES_TO','○○에 적용','REGULATED_OBJECT_ONLY');
INSERT INTO pattern_dictionary (pattern_id,pattern_type,trigger,role) VALUES ('P-R3','OBJECT_PROPERTY','○○의 위해성/성능/구조/범위','REGULATED_OBJECT_ONLY');
INSERT INTO pattern_dictionary (pattern_id,pattern_type,trigger,role) VALUES ('P-R4','ENUM_OBJECT','○○ 또는/및','REGULATED_OBJECT_ONLY');
INSERT INTO pattern_dictionary (pattern_id,pattern_type,trigger,role) VALUES ('P-R5','CERTIFIED_OBJECT','인증/규격/받은 ○○','REGULATED_OBJECT_ONLY');
INSERT INTO pattern_dictionary (pattern_id,pattern_type,trigger,role) VALUES ('P-R6','COMPONENT_ENUM','구명/불꽃 ○○','REGULATED_OBJECT_ONLY');
INSERT INTO pattern_dictionary (pattern_id,pattern_type,trigger,role) VALUES ('P-R7','MEETS_STANDARD','○○이 …기준에 맞는','REGULATED_OBJECT_ONLY');
INSERT INTO pattern_dictionary (pattern_id,pattern_type,trigger,role) VALUES ('P-F1','FACILITY_MANAGEMENT','○○의 안전관리','FACILITY_ONLY');
INSERT INTO pattern_dictionary (pattern_id,pattern_type,trigger,role) VALUES ('P-F2','FACILITY_STRUCTURE','○○의 벽체/구조','FACILITY_ONLY');
INSERT INTO pattern_dictionary (pattern_id,pattern_type,trigger,role) VALUES ('P-F3','DESIGNATED_PLACE','○○ 등 특수한 장소','FACILITY_ONLY');
INSERT INTO pattern_dictionary (pattern_id,pattern_type,trigger,role) VALUES ('P-F4','PLACE_LAW','○○교통법/도로법','FACILITY_ONLY');
INSERT INTO pattern_dictionary (pattern_id,pattern_type,trigger,role) VALUES ('P-F5','INSTITUTION_BY_LAW','법에 따른 ○○','FACILITY_ONLY');
INSERT INTO pattern_dictionary (pattern_id,pattern_type,trigger,role) VALUES ('P-F6','TRANSPORT_ENUM','선박·○○·항공기','FACILITY_ONLY');

CREATE TABLE IF NOT EXISTS role_mapping (
  id          bigserial PRIMARY KEY,
  law_name    text NOT NULL,
  value       text NOT NULL,
  role        text NOT NULL,
  pattern_id  text,
  evidence_articles text,
  source_wo   text DEFAULT 'WO-VERIFY-004',
  deployed_at timestamptz DEFAULT now()
);
TRUNCATE role_mapping;
INSERT INTO role_mapping (law_name,value,role,pattern_id,evidence_articles) VALUES ('건설기계 안전기준에 관한 규칙','건설기계','REGULATED_OBJECT_ONLY','P-R1','2;5');
INSERT INTO role_mapping (law_name,value,role,pattern_id,evidence_articles) VALUES ('건설기계 안전기준에 관한 규칙','건축물','FACILITY_ONLY','P-F2','125');
INSERT INTO role_mapping (law_name,value,role,pattern_id,evidence_articles) VALUES ('건설기계 안전기준에 관한 규칙','도로','FACILITY_ONLY','P-F4','136;170');
INSERT INTO role_mapping (law_name,value,role,pattern_id,evidence_articles) VALUES ('건설기계 안전기준에 관한 규칙','설비','REGULATED_OBJECT_ONLY','P-R6','91;94');
INSERT INTO role_mapping (law_name,value,role,pattern_id,evidence_articles) VALUES ('건설기계 안전기준에 관한 규칙','자재','REGULATED_OBJECT_ONLY','P-R4','45;125');
INSERT INTO role_mapping (law_name,value,role,pattern_id,evidence_articles) VALUES ('건설기계 안전기준에 관한 규칙','제품','REGULATED_OBJECT_ONLY','P-R4','125;150');
INSERT INTO role_mapping (law_name,value,role,pattern_id,evidence_articles) VALUES ('건설기계 안전기준에 관한 규칙','항만','FACILITY_ONLY','P-F3','35');
INSERT INTO role_mapping (law_name,value,role,pattern_id,evidence_articles) VALUES ('수도용 자재와 제품의 위생안전기준 인증규칙','제품','REGULATED_OBJECT_ONLY','UNRESOLVED_PATTERN','8;16');
INSERT INTO role_mapping (law_name,value,role,pattern_id,evidence_articles) VALUES ('수도용 자재와 제품의 위생안전기준 인증규칙','학교','UNRESOLVED','NO_PATTERN','3');
INSERT INTO role_mapping (law_name,value,role,pattern_id,evidence_articles) VALUES ('어린이놀이시설 안전관리법','놀이시설','FACILITY_ONLY','P-F1','23');
INSERT INTO role_mapping (law_name,value,role,pattern_id,evidence_articles) VALUES ('제품안전기본법','의료기관','FACILITY_ONLY','P-F5','15');
INSERT INTO role_mapping (law_name,value,role,pattern_id,evidence_articles) VALUES ('제품안전기본법','제품','REGULATED_OBJECT_ONLY','P-R1','3;7;9');
INSERT INTO role_mapping (law_name,value,role,pattern_id,evidence_articles) VALUES ('제품안전기본법 시행령','제품','REGULATED_OBJECT_ONLY','P-R1','4;5;8');
INSERT INTO role_mapping (law_name,value,role,pattern_id,evidence_articles) VALUES ('제품안전기본법 시행령','철도','FACILITY_ONLY','P-F6','14');

-- Post Apply Validation (운영자: 실행 후 아래 결과를 assistant에 전달)
SELECT 'pattern_dictionary' AS tbl, count(*) AS rows FROM pattern_dictionary
UNION ALL SELECT 'role_mapping', count(*) FROM role_mapping;
COMMIT;
