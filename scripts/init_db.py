"""
init_db.py — Create the BRUNOMEMAPP SQLite schema.

Idempotent: safe to re-run. Mirrors the WitcherPortal / AtalantaClaudiens pattern
(flat entity tables, provenance fields on every row, polymorphic link tables for
citations and dispute evidence). Run seed_from_json.py after this to load data.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "db"
DB_PATH = DB_DIR / "bruno.db"

SCHEMA = """
-- ============================================================
-- BRUNOMEMAPP schema v1
-- Entities: works, images, scholars, dictionary_terms, disputes,
--           biographical_events, essays, app_mode_ideas, bibliography
-- Provenance: every content row carries source_method, review_status, confidence
-- Layer discipline: PRIMARY SOURCE -> SCHOLARLY INTERPRETATION -> RECONSTRUCTION -> EXPERIMENT
-- ============================================================

-- Bruno's own works: mnemonic treatises, magical texts, poetic/philosophical dialogues.
CREATE TABLE IF NOT EXISTS works (
    id                      INTEGER PRIMARY KEY,
    slug                    TEXT UNIQUE NOT NULL,
    title_original          TEXT NOT NULL,          -- Latin/Italian title
    title_english           TEXT,
    work_type               TEXT CHECK(work_type IN ('MNEMONIC_TREATISE','MAGICAL_TEXT','ITALIAN_DIALOGUE','LATIN_POEM','LETTER','OTHER')),
    language                TEXT,                    -- 'Latin', 'Italian'
    date_written            TEXT,                    -- year or range, as text (uncertainty is common)
    date_published          TEXT,
    place_published         TEXT,
    summary                 TEXT NOT NULL,           -- what the work is, in general
    memory_magic_connection TEXT NOT NULL,           -- REQUIRED: how this work bears on memory/magic specifically
    memory_magic_relevance  TEXT CHECK(memory_magic_relevance IN ('CENTRAL','MAJOR','SUPPORTING','TANGENTIAL')),
    key_editions             TEXT,                   -- JSON array of {editor, year, note}
    notable_content          TEXT,                   -- named techniques/images/concepts introduced here
    tags                     TEXT,                    -- JSON array
    source_method            TEXT DEFAULT 'SEED_DATA',
    review_status             TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED')),
    confidence                TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

-- Individual mnemonic/magical images Bruno used, as their own addressable cards.
CREATE TABLE IF NOT EXISTS images (
    id                      INTEGER PRIMARY KEY,
    slug                    TEXT UNIQUE NOT NULL,
    name                    TEXT NOT NULL,
    work_slug               TEXT,                    -- which work it comes from (soft FK -> works.slug)
    image_role               TEXT CHECK(image_role IN ('MEMORY_SUBJECT','MEMORY_ADJACENT','FIELD','WHEEL_COMPONENT','SEAL','MYTHOLOGICAL_FIGURE','PLANETARY_FIGURE','ANIMAL','OTHER')),
    description               TEXT NOT NULL,
    what_it_does              TEXT,                   -- procedural/operational function, not just iconography
    reconstruction_level      TEXT CHECK(reconstruction_level IN ('HISTORICALLY_ATTESTED','DIRECT_RECONSTRUCTION','SCHOLARLY_RECONSTRUCTION','SPECULATIVE_IMPLEMENTATION')),
    scholarly_interpretation  TEXT,                   -- short pointer; full multi-scholar comparison lives in disputes/scholarly_refs
    image_filename            TEXT,                   -- if a page scan/diagram asset exists
    tags                      TEXT,
    source_method             TEXT DEFAULT 'SEED_DATA',
    review_status              TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED')),
    confidence                 TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

-- Scholars of Bruno's memory/magic system.
CREATE TABLE IF NOT EXISTS scholars (
    id                      INTEGER PRIMARY KEY,
    slug                    TEXT UNIQUE NOT NULL,
    name                    TEXT NOT NULL,
    birth_year              INTEGER,
    death_year              INTEGER,
    affiliation              TEXT,
    interpretation_summary   TEXT NOT NULL,           -- one-paragraph stance
    view_memory               TEXT,
    view_imagination           TEXT,
    view_images                TEXT,
    view_magic                 TEXT,
    view_neoplatonism           TEXT,
    view_plotinus                TEXT,
    view_ficino                   TEXT,
    view_mnemonic_wheels           TEXT,
    view_seals_simulacra            TEXT,
    major_bruno_works                TEXT,             -- JSON array of {title, year}
    tags                              TEXT,
    source_method                    TEXT DEFAULT 'SEED_DATA',
    review_status                     TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED')),
    confidence                        TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

-- Bruno's key vocabulary (memoria, phantasia, simulacrum, signaculum, umbra, vinculum, ...).
CREATE TABLE IF NOT EXISTS dictionary_terms (
    id                      INTEGER PRIMARY KEY,
    slug                    TEXT UNIQUE NOT NULL,
    term_original           TEXT NOT NULL,           -- Latin/Italian
    language                TEXT,
    short_definition        TEXT NOT NULL,
    bruno_usage             TEXT,                     -- how Bruno specifically uses it
    scholarly_interpretation TEXT,                    -- brief note; disputes carry the full disagreement
    related_terms            TEXT,                    -- JSON array of slugs
    tags                      TEXT,
    source_method             TEXT DEFAULT 'SEED_DATA',
    confidence                 TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

-- Scholarly disagreements. Two-position model with evidence on each side.
CREATE TABLE IF NOT EXISTS disputes (
    id                      INTEGER PRIMARY KEY,
    slug                    TEXT UNIQUE NOT NULL,
    topic                    TEXT NOT NULL,
    position_a_scholar_slug   TEXT,
    position_a_text            TEXT,
    position_b_scholar_slug     TEXT,
    position_b_text               TEXT,
    resolution                     TEXT CHECK(resolution IN ('ONGOING','CONSENSUS','SUPERCEDED','NOT_DIRECTLY_COMPARABLE')),
    resolution_note                 TEXT,
    tags                              TEXT,
    source_method                     TEXT DEFAULT 'SEED_DATA',
    review_status                      TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED')),
    confidence                          TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

-- Bruno's life, filtered to events relevant to memory/magic (NOT a general biography).
CREATE TABLE IF NOT EXISTS biographical_events (
    id                      INTEGER PRIMARY KEY,
    slug                    TEXT UNIQUE NOT NULL,
    title                    TEXT NOT NULL,
    year                      TEXT,                   -- year or range as text
    place                      TEXT,
    summary                    TEXT NOT NULL,
    memory_magic_connection     TEXT NOT NULL,         -- REQUIRED: why this event matters to the memory-magic story
    related_work_slugs           TEXT,                 -- JSON array of works.slug
    tags                          TEXT,
    source_method                 TEXT DEFAULT 'SEED_DATA',
    review_status                  TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED')),
    confidence                      TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

-- Long-form essays threading multiple entities together (e.g. Plotinus <-> Bruno).
CREATE TABLE IF NOT EXISTS essays (
    id              INTEGER PRIMARY KEY,
    slug            TEXT UNIQUE NOT NULL,
    title           TEXT NOT NULL,
    subtitle        TEXT,
    summary         TEXT,
    body            TEXT NOT NULL,           -- minimal markdown
    related_entities TEXT,                   -- JSON array of {type, slug, label}
    source_method   TEXT DEFAULT 'SEED_DATA',
    review_status   TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED')),
    confidence      TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

-- Interactive tool / game-mode concepts, including explicitly humorous ones.
CREATE TABLE IF NOT EXISTS app_mode_ideas (
    id                      INTEGER PRIMARY KEY,
    slug                    TEXT UNIQUE NOT NULL,
    name                    TEXT NOT NULL,
    mode_category            TEXT CHECK(mode_category IN ('SCHOLARLY_SANDBOX','MEMORY_TOOL','IMAGE_TOOL','NARRATIVE_GAME','COMEDIC_GAME','COMPARISON_TOOL')),
    based_on_work_slugs       TEXT,                    -- JSON array of works.slug
    scholar_frames             TEXT,                    -- JSON array of scholars.slug this mode can adopt
    tone                        TEXT CHECK(tone IN ('SERIOUS','PLAYFUL','COMEDIC','SATIRICAL')),
    description                  TEXT NOT NULL,
    why_this_source_supports_it   TEXT,                 -- grounding: what in Bruno licenses this tone/approach
    status                         TEXT DEFAULT 'IDEA' CHECK(status IN ('IDEA','PROTOTYPE','BUILT')),
    tags                            TEXT,
    source_method                   TEXT DEFAULT 'SEED_DATA',
    confidence                       TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

-- Scholarly / primary-source bibliography.
CREATE TABLE IF NOT EXISTS bibliography (
    id              INTEGER PRIMARY KEY,
    source_id       TEXT UNIQUE NOT NULL,
    author          TEXT NOT NULL,
    title           TEXT NOT NULL,
    year            INTEGER,
    publisher       TEXT,
    journal         TEXT,
    pub_type        TEXT CHECK(pub_type IN ('monograph','article','review','encyclopedia','primary_source','critical_edition','edited_volume','translation','dissertation','website')),
    relevance       TEXT CHECK(relevance IN ('PRIMARY','DIRECT','CONTEXTUAL')),
    annotation      TEXT,
    online_url      TEXT,
    access_note     TEXT
);

-- Polymorphic link: any entity (work/image/scholar/term/dispute/event) -> bibliography entry.
CREATE TABLE IF NOT EXISTS scholarly_refs (
    id              INTEGER PRIMARY KEY,
    entity_type     TEXT NOT NULL CHECK(entity_type IN ('work','image','scholar','term','dispute','event','essay')),
    entity_slug     TEXT NOT NULL,
    bib_source_id   TEXT NOT NULL REFERENCES bibliography(source_id),
    page_ref        TEXT,
    note            TEXT
);

-- ============================================================
-- PRACTICE LAYER (PROMPTS.md P-06/P-07/P-10; docs/design/PRACTICES.md)
-- Practice is primary and operable. Friction explains the worldview gap at
-- every step. Scholarly readings that change the mechanics become playable
-- variants rather than footnotes.
-- ============================================================

CREATE TABLE IF NOT EXISTS practices (
    id                  INTEGER PRIMARY KEY,
    slug                TEXT UNIQUE NOT NULL,
    name                TEXT NOT NULL,
    tradition           TEXT,                   -- 'Classical', 'Monastic', 'Renaissance', 'Bruno'
    date_range          TEXT,
    source_text         TEXT,                   -- the work it comes from
    one_line            TEXT NOT NULL,
    what_you_can_do     TEXT NOT NULL,          -- concretely, what the user actually does
    operability         TEXT CHECK(operability IN ('FULLY_OPERABLE','PARTIALLY_OPERABLE','REFERENCE_ONLY')),
    operability_note    TEXT,                   -- WHY it has that grade; what's missing
    worldview_preface   TEXT,                   -- the big gap to state before step 1
    structure_json      TEXT,                   -- e.g. the 24x24 atrium inventory
    sort_order          INTEGER DEFAULT 100,
    source_method       TEXT DEFAULT 'SEED_DATA',
    review_status       TEXT DEFAULT 'DRAFT' CHECK(review_status IN ('DRAFT','REVIEWED','VERIFIED')),
    confidence          TEXT DEFAULT 'MEDIUM' CHECK(confidence IN ('HIGH','MEDIUM','LOW'))
);

CREATE TABLE IF NOT EXISTS practice_steps (
    id              INTEGER PRIMARY KEY,
    practice_slug   TEXT NOT NULL,
    step_number     INTEGER NOT NULL,
    title           TEXT NOT NULL,
    instruction     TEXT NOT NULL,
    attestation     TEXT CHECK(attestation IN ('ATTESTED','RECONSTRUCTED','SPECULATIVE')),
    source_locator  TEXT,                       -- book/chapter/line, so a claim is checkable
    UNIQUE(practice_slug, step_number)
);

-- Every step gets at least one friction note. A step with none is a step
-- nobody has thought hard enough about.
CREATE TABLE IF NOT EXISTS frictions (
    id              INTEGER PRIMARY KEY,
    practice_slug   TEXT NOT NULL,
    step_number     INTEGER,                    -- NULL = applies to the whole practice
    kind            TEXT CHECK(kind IN ('WORLDVIEW','INTERFACE')),
    difficulty      TEXT NOT NULL,              -- what feels wrong to a modern user
    explanation     TEXT NOT NULL               -- why it made sense / what to do about it
);

-- Scholarly readings that change the MECHANICS. If nothing changes
-- mechanically it is commentary, and belongs in the scholarship layer.
CREATE TABLE IF NOT EXISTS practice_variants (
    id                INTEGER PRIMARY KEY,
    practice_slug     TEXT NOT NULL,
    slug              TEXT UNIQUE NOT NULL,
    name              TEXT NOT NULL,
    scholar_slug      TEXT,
    what_changes      TEXT NOT NULL,            -- the mechanical difference
    playable_as       TEXT NOT NULL,            -- what the user does differently
    testability_tier  TEXT CHECK(testability_tier IN ('T1','T2','T3')),
    superseded        INTEGER DEFAULT 0,        -- still playable; see PROMPTS.md P-01/P-07
    notes             TEXT
);

-- Schema version tracking.
CREATE TABLE IF NOT EXISTS schema_version (
    version     INTEGER PRIMARY KEY,
    applied_at  TEXT DEFAULT (datetime('now')),
    description TEXT
);

INSERT OR IGNORE INTO schema_version (version, description)
VALUES (1, 'BRUNOMEMAPP v1: works, images, scholars, dictionary, disputes, biographical_events, essays, app_mode_ideas, bibliography, scholarly_refs');
"""


def main():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA)
    conn.close()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    print(f"Database: {DB_PATH}")
    print(f"Tables ({len(tables)}): {', '.join(tables)}")

    expected = {
        'works', 'images', 'scholars', 'dictionary_terms', 'disputes',
        'biographical_events', 'essays', 'app_mode_ideas', 'bibliography',
        'scholarly_refs', 'schema_version',
        'practices', 'practice_steps', 'frictions', 'practice_variants',
    }
    missing = expected - set(tables)
    if missing:
        print(f"ERROR: Missing tables: {missing}")
        return 1

    print("Schema v1 ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
