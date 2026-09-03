-- SUPERSEDED 2026-09-01 — see docs/ARCHITECTURE_PIVOT.md
-- Not currently run. The active schema is scripts/init_db.py (WitcherPortal-style
-- flat entities + bruno_seed.json). This file documents a fuller normalized
-- provenance/dispute model to revisit if the flat model proves too limiting.
--
-- BRUNOMEMAPP SQLite Schema
-- Canonical research database for Bruno's memory, imagination, and magic
--
-- Design principle: Separate PRIMARY SOURCE → INTERPRETATION → RECONSTRUCTION → EXPERIMENT
-- Every claim retains provenance to source passages

CREATE TABLE IF NOT EXISTS authors (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  role TEXT CHECK(role IN ('primary', 'secondary', 'scholar')),
  language TEXT,
  active_period TEXT,
  biography_url TEXT,
  authority_key TEXT UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS works (
  id INTEGER PRIMARY KEY,
  author_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  subtitle TEXT,
  title_alt TEXT,
  work_type TEXT CHECK(work_type IN ('mnemonic_treatise', 'philosophical_dialogue', 'magical_text', 'poetry', 'correspondence', 'lost_work', 'secondary_study')),
  date_written TEXT,
  date_published TEXT,
  language TEXT,
  is_primary_source INTEGER DEFAULT 1,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (author_id) REFERENCES authors(id)
);

CREATE TABLE IF NOT EXISTS editions (
  id INTEGER PRIMARY KEY,
  work_id INTEGER NOT NULL,
  edition_type TEXT CHECK(edition_type IN ('manuscript', 'first_printing', 'critical_edition', 'modern_translation', 'scholarly_reprint')),
  title_edition TEXT,
  editor TEXT,
  publication_year INTEGER,
  publisher TEXT,
  place_published TEXT,
  language_edition TEXT,
  page_count INTEGER,
  isbn TEXT,
  url TEXT,
  is_canonical INTEGER DEFAULT 0,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (work_id) REFERENCES works(id)
);

CREATE TABLE IF NOT EXISTS sources (
  id INTEGER PRIMARY KEY,
  filename TEXT NOT NULL,
  file_type TEXT CHECK(file_type IN ('pdf', 'txt', 'epub', 'docx', 'html')),
  file_hash TEXT UNIQUE,
  file_size INTEGER,
  extraction_status TEXT DEFAULT 'pending' CHECK(extraction_status IN ('pending', 'extracted', 'OCR_required', 'failed')),
  ocr_status TEXT DEFAULT 'none' CHECK(ocr_status IN ('none', 'pending', 'completed', 'failed')),
  ocr_confidence REAL DEFAULT 0.0,
  edition_id INTEGER,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (edition_id) REFERENCES editions(id)
);

CREATE TABLE IF NOT EXISTS pages (
  id INTEGER PRIMARY KEY,
  source_id INTEGER NOT NULL,
  edition_id INTEGER,
  page_number INTEGER NOT NULL,
  page_label TEXT,
  extracted_text TEXT,
  ocr_confidence REAL DEFAULT 0.0,
  has_diagram INTEGER DEFAULT 0,
  has_figure INTEGER DEFAULT 0,
  has_marginal_notes INTEGER DEFAULT 0,
  image_filename TEXT,
  image_hash TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (source_id) REFERENCES sources(id),
  FOREIGN KEY (edition_id) REFERENCES editions(id)
);

CREATE TABLE IF NOT EXISTS passages (
  id INTEGER PRIMARY KEY,
  source_id INTEGER NOT NULL,
  page_id INTEGER NOT NULL,
  passage_type TEXT CHECK(passage_type IN ('quote', 'claim', 'technique_description', 'diagram_caption', 'editorial_note')),
  start_line INTEGER,
  end_line INTEGER,
  extracted_text TEXT NOT NULL,
  passage_label TEXT,
  stable_passage_id TEXT UNIQUE,
  language_original TEXT,
  language_translated TEXT,
  translated_text TEXT,
  translator TEXT,
  confidence TEXT CHECK(confidence IN ('DIRECTLY_ATTESTED', 'OCR_UNCERTAIN', 'EDITORIAL_RECONSTRUCTION')),
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (source_id) REFERENCES sources(id),
  FOREIGN KEY (page_id) REFERENCES pages(id)
);

CREATE TABLE IF NOT EXISTS concepts (
  id INTEGER PRIMARY KEY,
  label TEXT NOT NULL,
  label_original TEXT,
  concept_type TEXT CHECK(concept_type IN ('memory_technique', 'philosophical_principle', 'magical_operation', 'psychological_faculty', 'cosmological_relation', 'virtue', 'vice', 'emotion', 'celestial', 'animal', 'plant', 'mineral')),
  definition_bruno TEXT,
  definition_scholarly TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS concepts_passages (
  concept_id INTEGER NOT NULL,
  passage_id INTEGER NOT NULL,
  context TEXT,
  PRIMARY KEY (concept_id, passage_id),
  FOREIGN KEY (concept_id) REFERENCES concepts(id),
  FOREIGN KEY (passage_id) REFERENCES passages(id)
);

CREATE TABLE IF NOT EXISTS techniques (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  technique_type TEXT CHECK(technique_type IN ('memory_wheel', 'image_construction', 'mnemonic_locus', 'letter_correspondence', 'seal_system', 'philosophical_ascent', 'attention_discipline', 'desire_regulation', 'image_contemplation')),
  description TEXT,
  reconstruction_level TEXT CHECK(reconstruction_level IN ('HISTORICALLY_ATTESTED', 'DIRECT_RECONSTRUCTION', 'SCHOLARLY_RECONSTRUCTION', 'SPECULATIVE_IMPLEMENTATION')),
  procedural_steps TEXT, -- JSON array
  comparison_with_classical TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS techniques_passages (
  technique_id INTEGER NOT NULL,
  passage_id INTEGER NOT NULL,
  role TEXT, -- 'primary_evidence', 'supporting', 'alternative_reconstruction'
  PRIMARY KEY (technique_id, passage_id),
  FOREIGN KEY (technique_id) REFERENCES techniques(id),
  FOREIGN KEY (passage_id) REFERENCES passages(id)
);

CREATE TABLE IF NOT EXISTS scholars (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  birth_year INTEGER,
  death_year INTEGER,
  nationality TEXT,
  primary_affiliation TEXT,
  expertise TEXT,
  major_bruno_works TEXT, -- JSON array
  interpretation_summary TEXT,
  views TEXT, -- JSON object (memory, imagination, images, magic, neoplatonism, etc.)
  url TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scholar_major_works (
  scholar_id INTEGER NOT NULL,
  title TEXT NOT NULL,
  publication_year INTEGER,
  work_type TEXT,
  notes TEXT,
  PRIMARY KEY (scholar_id, title),
  FOREIGN KEY (scholar_id) REFERENCES scholars(id)
);

CREATE TABLE IF NOT EXISTS claims (
  id INTEGER PRIMARY KEY,
  claim_type TEXT CHECK(claim_type IN ('source_claim', 'scholarly_claim', 'reconstruction_claim', 'experimental_claim')),
  claim_text TEXT NOT NULL,
  scholar_id INTEGER,
  confidence TEXT CHECK(confidence IN ('DIRECTLY_SUPPORTED', 'INFERRED', 'SPECULATIVE')),
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (scholar_id) REFERENCES scholars(id)
);

CREATE TABLE IF NOT EXISTS claims_passages (
  claim_id INTEGER NOT NULL,
  passage_id INTEGER NOT NULL,
  role TEXT, -- 'evidence', 'counter_evidence', 'source'
  PRIMARY KEY (claim_id, passage_id),
  FOREIGN KEY (claim_id) REFERENCES claims(id),
  FOREIGN KEY (passage_id) REFERENCES passages(id)
);

CREATE TABLE IF NOT EXISTS claims_related (
  claim_id_a INTEGER NOT NULL,
  claim_id_b INTEGER NOT NULL,
  relationship TEXT CHECK(relationship IN ('supports', 'contradicts', 'clarifies', 'extends')),
  PRIMARY KEY (claim_id_a, claim_id_b),
  FOREIGN KEY (claim_id_a) REFERENCES claims(id),
  FOREIGN KEY (claim_id_b) REFERENCES claims(id)
);

CREATE TABLE IF NOT EXISTS interpretations (
  id INTEGER PRIMARY KEY,
  scholar_id INTEGER NOT NULL,
  object_type TEXT CHECK(object_type IN ('technique', 'concept', 'passage', 'work', 'image', 'wheel', 'seal')),
  object_id INTEGER NOT NULL,
  interpretation_text TEXT NOT NULL,
  scholarly_source TEXT,
  confidence TEXT CHECK(confidence IN ('CONFIDENT', 'UNCERTAIN', 'CONTESTED')),
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (scholar_id) REFERENCES scholars(id)
);

CREATE TABLE IF NOT EXISTS interpretations_passages (
  interpretation_id INTEGER NOT NULL,
  passage_id INTEGER NOT NULL,
  PRIMARY KEY (interpretation_id, passage_id),
  FOREIGN KEY (interpretation_id) REFERENCES interpretations(id),
  FOREIGN KEY (passage_id) REFERENCES passages(id)
);

CREATE TABLE IF NOT EXISTS disputes (
  id INTEGER PRIMARY KEY,
  topic TEXT NOT NULL,
  position_a_scholar_id INTEGER,
  position_a_text TEXT,
  position_b_scholar_id INTEGER,
  position_b_text TEXT,
  resolution TEXT CHECK(resolution IN ('ONGOING', 'CONSENSUS', 'SUPERCEDED', 'NOT_DIRECTLY_COMPARABLE')),
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (position_a_scholar_id) REFERENCES scholars(id),
  FOREIGN KEY (position_b_scholar_id) REFERENCES scholars(id)
);

CREATE TABLE IF NOT EXISTS disputes_passages (
  dispute_id INTEGER NOT NULL,
  passage_id INTEGER NOT NULL,
  position TEXT, -- 'A', 'B', 'both', 'neither'
  PRIMARY KEY (dispute_id, passage_id),
  FOREIGN KEY (dispute_id) REFERENCES disputes(id),
  FOREIGN KEY (passage_id) REFERENCES passages(id)
);

CREATE TABLE IF NOT EXISTS experiments (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  experiment_type TEXT CHECK(experiment_type IN ('memory_wheel_configuration', 'image_construction', 'memory_palace_walk', 'seal_activation', 'scholar_comparison', 'psychological_binding')),
  scholar_mode TEXT,
  configuration_json TEXT, -- JSON serialized state
  user_notes TEXT,
  is_public INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS experiments_techniques (
  experiment_id INTEGER NOT NULL,
  technique_id INTEGER NOT NULL,
  PRIMARY KEY (experiment_id, technique_id),
  FOREIGN KEY (experiment_id) REFERENCES experiments(id),
  FOREIGN KEY (technique_id) REFERENCES techniques(id)
);

CREATE TABLE IF NOT EXISTS app_modes (
  id INTEGER PRIMARY KEY,
  mode_name TEXT NOT NULL UNIQUE,
  description TEXT,
  scholar_frames TEXT, -- JSON array of scholar IDs
  interactive_elements TEXT, -- JSON array
  entry_point TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS app_modes_concepts (
  app_mode_id INTEGER NOT NULL,
  concept_id INTEGER NOT NULL,
  PRIMARY KEY (app_mode_id, concept_id),
  FOREIGN KEY (app_mode_id) REFERENCES app_modes(id),
  FOREIGN KEY (concept_id) REFERENCES concepts(id)
);

CREATE TABLE IF NOT EXISTS app_modes_techniques (
  app_mode_id INTEGER NOT NULL,
  technique_id INTEGER NOT NULL,
  PRIMARY KEY (app_mode_id, technique_id),
  FOREIGN KEY (app_mode_id) REFERENCES app_modes(id),
  FOREIGN KEY (technique_id) REFERENCES techniques(id)
);

-- Full-text search tables (FTS5)

CREATE VIRTUAL TABLE IF NOT EXISTS passages_fts USING fts5(
  passage_id UNINDEXED,
  extracted_text,
  passage_label,
  content='passages',
  content_rowid='id'
);

CREATE VIRTUAL TABLE IF NOT EXISTS concepts_fts USING fts5(
  concept_id UNINDEXED,
  label,
  label_original,
  definition_bruno,
  definition_scholarly,
  content='concepts',
  content_rowid='id'
);

CREATE VIRTUAL TABLE IF NOT EXISTS claims_fts USING fts5(
  claim_id UNINDEXED,
  claim_text,
  content='claims',
  content_rowid='id'
);

-- Indices for common queries

CREATE INDEX IF NOT EXISTS idx_pages_source ON pages(source_id);
CREATE INDEX IF NOT EXISTS idx_pages_edition ON pages(edition_id);
CREATE INDEX IF NOT EXISTS idx_passages_source ON passages(source_id);
CREATE INDEX IF NOT EXISTS idx_passages_page ON passages(page_id);
CREATE INDEX IF NOT EXISTS idx_passages_stable_id ON passages(stable_passage_id);
CREATE INDEX IF NOT EXISTS idx_concepts_passages_concept ON concepts_passages(concept_id);
CREATE INDEX IF NOT EXISTS idx_concepts_passages_passage ON concepts_passages(passage_id);
CREATE INDEX IF NOT EXISTS idx_techniques_passages_technique ON techniques_passages(technique_id);
CREATE INDEX IF NOT EXISTS idx_techniques_passages_passage ON techniques_passages(passage_id);
CREATE INDEX IF NOT EXISTS idx_claims_scholar ON claims(scholar_id);
CREATE INDEX IF NOT EXISTS idx_claims_passages_claim ON claims_passages(claim_id);
CREATE INDEX IF NOT EXISTS idx_claims_passages_passage ON claims_passages(passage_id);
CREATE INDEX IF NOT EXISTS idx_interpretations_scholar ON interpretations(scholar_id);
CREATE INDEX IF NOT EXISTS idx_interpretations_passages_interpretation ON interpretations_passages(interpretation_id);
CREATE INDEX IF NOT EXISTS idx_interpretations_passages_passage ON interpretations_passages(passage_id);
CREATE INDEX IF NOT EXISTS idx_disputes_scholar_a ON disputes(position_a_scholar_id);
CREATE INDEX IF NOT EXISTS idx_disputes_scholar_b ON disputes(position_b_scholar_id);
CREATE INDEX IF NOT EXISTS idx_experiments_techniques_experiment ON experiments_techniques(experiment_id);
CREATE INDEX IF NOT EXISTS idx_experiments_techniques_technique ON experiments_techniques(technique_id);
CREATE INDEX IF NOT EXISTS idx_app_modes_concepts_mode ON app_modes_concepts(app_mode_id);
CREATE INDEX IF NOT EXISTS idx_app_modes_concepts_concept ON app_modes_concepts(concept_id);
CREATE INDEX IF NOT EXISTS idx_app_modes_techniques_mode ON app_modes_techniques(app_mode_id);
CREATE INDEX IF NOT EXISTS idx_app_modes_techniques_technique ON app_modes_techniques(technique_id);

-- Views for common queries

CREATE VIEW IF NOT EXISTS scholar_disagreements AS
SELECT
  d.id,
  d.topic,
  s_a.name AS scholar_a,
  d.position_a_text,
  s_b.name AS scholar_b,
  d.position_b_text,
  d.resolution
FROM disputes d
JOIN scholars s_a ON d.position_a_scholar_id = s_a.id
JOIN scholars s_b ON d.position_b_scholar_id = s_b.id;

CREATE VIEW IF NOT EXISTS technique_evidence AS
SELECT
  t.id,
  t.name,
  t.reconstruction_level,
  p.stable_passage_id,
  p.extracted_text,
  e.title_edition,
  e.publication_year
FROM techniques t
JOIN techniques_passages tp ON t.id = tp.technique_id
JOIN passages p ON tp.passage_id = p.id
JOIN pages pg ON p.page_id = pg.id
JOIN sources s ON pg.source_id = s.id
JOIN editions e ON s.edition_id = e.id
ORDER BY t.id, e.publication_year;

CREATE VIEW IF NOT EXISTS concept_definitions AS
SELECT
  c.id,
  c.label,
  c.label_original,
  c.concept_type,
  c.definition_bruno,
  c.definition_scholarly,
  COUNT(DISTINCT cp.passage_id) AS passage_count
FROM concepts c
LEFT JOIN concepts_passages cp ON c.id = cp.concept_id
GROUP BY c.id;

-- Metadata table for tracking ingestion progress

CREATE TABLE IF NOT EXISTS ingestion_log (
  id INTEGER PRIMARY KEY,
  task TEXT NOT NULL,
  status TEXT CHECK(status IN ('pending', 'in_progress', 'completed', 'failed')),
  details TEXT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
