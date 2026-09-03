# BRUNOMEMAPP Design Architecture

## Overview

BRUNOMEMAPP is a three-tier research laboratory:

1. **Data Layer:** Canonical SQLite database (bruno.db) with FTS5 search, OCR extraction, metadata, provenance tracking
2. **Processing Layer:** Python ingestion pipeline (extraction, parsing, enrichment, schema building)
3. **Interface Layer:** Interactive web tools exposing Bruno's memory/magic through multiple scholarly frameworks

## Key Distinction: The Four Layers

```
PRIMARY SOURCE
    ↓ (extraction + passage ID)
SCHOLARLY INTERPRETATION
    ↓ (parsing claims, identifying disputes, evidence mapping)
RECONSTRUCTION
    ↓ (operationalize techniques, label as HISTORICALLY_ATTESTED / DIRECT / SCHOLARLY / SPECULATIVE)
EXPERIMENT / USER CREATION
    ↓ (interactive tools, scholar-specific modes, counterfactual explorations)
```

**CRITICAL:** These layers never collapse. The UI must always show which layer is which.

## Data Model

### Core Tables

#### sources
- id: source_id (PK)
- filename: original filename
- file_type: pdf | txt | epub | docx | html
- file_hash: MD5/SHA256 (deduplication)
- file_size: bytes
- extraction_status: pending | extracted | OCR_required | failed
- ocr_status: none | pending | completed | failed
- ocr_confidence: float (0–1)
- notes: text

#### authors
- id: author_id (PK)
- name: text
- role: primary | secondary | scholar
- language: it | la | en | de | fr
- active_period: text (e.g., "1548–1600")
- biography_url: reference link
- authority_key: disambiguator (author + dates)

#### works
- id: work_id (PK)
- author_id: FK → authors
- title: text
- subtitle: text
- title_alt: alternative titles (comma-separated)
- work_type: mnemonic_treatise | philosophical_dialogue | magical_text | poetry | correspondence | lost_work | secondary_study
- date_written: year or "1580–1585" or NULL if unknown
- date_published: year or NULL
- language: it | la | en | de | fr | mixed
- is_primary_source: boolean
- notes: text

#### editions
- id: edition_id (PK)
- work_id: FK → works
- edition_type: manuscript | first_printing | critical_edition | modern_translation | scholarly_reprint
- title_edition: text (e.g., "Lagano ed., 1997 with commentary")
- editor: text
- publication_year: year
- publisher: text
- place_published: text
- language_edition: it | la | en | de | fr
- page_count: int
- isbn: text
- url: reference link
- is_canonical: boolean (primary source for this project)
- notes: text

#### pages
- id: page_id (PK)
- source_id: FK → sources
- edition_id: FK → editions (nullable, for when edition is known)
- page_number: int
- page_label: text (e.g., "pp. 45–46" or "sig. A2v")
- extracted_text: text
- ocr_confidence: float
- has_diagram: boolean
- has_figure: boolean
- has_marginal_notes: boolean
- image_filename: filename if saved (e.g., "de_umbris_1582_p45.jpg")
- image_hash: MD5/SHA256
- notes: text

#### passages
- id: passage_id (PK)
- source_id: FK → sources
- page_id: FK → pages
- passage_type: quote | claim | technique_description | diagram_caption | editorial_note
- start_line: int
- end_line: int
- extracted_text: text
- passage_label: text (e.g., "1st memory wheel diagram")
- stable_passage_id: text (BRUNO-SOURCE-ID / PAGE / PASSAGE-ID, globally addressable)
- language_original: it | la | en | de | fr
- language_translated: en (if translation available)
- translated_text: text (if applicable)
- translator: text (if applicable)
- confidence: DIRECTLY_ATTESTED | OCR_UNCERTAIN | EDITORIAL_RECONSTRUCTION
- notes: text

#### concepts
- id: concept_id (PK)
- label: text (English summary)
- label_original: text (Latin/Italian term)
- concept_type: memory_technique | philosophical_principle | magical_operation | psychological_faculty | cosmological_relation | virtue | vice | emotion | celestial | animal | plant | mineral
- definition_bruno: text (how Bruno uses it, extracted from passages)
- definition_scholarly: text (how scholars understand it)
- passages: FK array → passages (many-to-many, which passages mention this concept)
- scholarly_interpretations: FK array (many-to-many, scholars who discuss this)
- notes: text

#### techniques
- id: technique_id (PK)
- name: text (e.g., "The Thirty Intentions of the Shadows")
- technique_type: memory_wheel | image_construction | mnemonic_locus | letter_correspondence | seal_system | philosophical_ascent | attention_discipline | desire_regulation | image_contemplation
- description: text
- reconstruction_level: HISTORICALLY_ATTESTED | DIRECT_RECONSTRUCTION | SCHOLARLY_RECONSTRUCTION | SPECULATIVE_IMPLEMENTATION
- primary_passages: FK array → passages
- procedural_steps: JSON array
  - step: int
  - description: text
  - evidence: passage_id
  - scholarly_source: scholar_id
- scholarly_interpretations: FK array (many-to-many, who explains this technique)
- comparison_with_classical: text (Metrodorus, Simonides, etc.)
- notes: text

#### scholars
- id: scholar_id (PK)
- name: text (e.g., "Frances Yates")
- birth_year: int
- death_year: int
- nationality: text
- primary_affiliation: text
- expertise: text (comma-separated)
- major_bruno_works: JSON array (title, publication year, type)
- interpretation_summary: text (short statement of their Bruno interpretation)
- views: JSON
  - memory: text
  - imagination: text
  - images: text
  - magic: text
  - neoplatonism: text
  - plotinus: text
  - ficino: text
  - natural_magic: text
  - astral_influence: text
  - theurgy: text
  - psychology: text
  - ethics: text
  - mnemonic_wheels: text
  - seals_simulacra: text
  - confidence: CONFIDENT | UNCERTAIN | CONTESTED
- disagreements: FK array (many-to-many with other scholars)
- citations_of_bruno: FK array (which passages do they cite?)
- url: personal/institutional URL
- notes: text

#### claims
- id: claim_id (PK)
- claim_type: source_claim | scholarly_claim | reconstruction_claim | experimental_claim
- claim_text: text
- evidence_passages: FK array → passages (what primary sources support this?)
- scholar_id: FK → scholars (who makes this claim? NULL if source itself)
- confidence: DIRECTLY_SUPPORTED | INFERRED | SPECULATIVE
- disputed_by: FK array → claims (which other claims contradict this?)
- supporting_claims: FK array (which claims support this one?)
- notes: text

#### interpretations
- id: interpretation_id (PK)
- scholar_id: FK → scholars
- object_type: technique | concept | passage | work | image | wheel | seal
- object_id: int (technique_id, concept_id, passage_id, etc.)
- interpretation_text: text
- scholarly_source: text (book/article, page)
- evidence_passages: FK array (passages the scholar cites)
- confidence: CONFIDENT | UNCERTAIN | CONTESTED
- contradicts: FK array → interpretations (which other interpretations does this disagree with?)
- notes: text

#### disputes
- id: dispute_id (PK)
- topic: text (e.g., "Planetary placement in De umbris wheel")
- position_a_scholar: scholar_id
- position_a_text: text
- position_a_evidence: FK array → passages
- position_b_scholar: scholar_id
- position_b_text: text
- position_b_evidence: FK array → passages
- resolution: ONGOING | CONSENSUS | SUPERCEDED | NOT_DIRECTLY_COMPARABLE
- notes: text

#### experiments
- id: experiment_id (PK)
- name: text
- description: text
- experiment_type: memory_wheel_configuration | image_construction | memory_palace_walk | seal_activation | scholar_comparison | psychological_binding
- scholar_mode: YATES | CLUCAS | MERTENS | WANG | BARENSTEIN | COULIANO | UNALIGNED
- configuration_json: JSON (serialized experiment state)
- underlying_techniques: FK array → techniques
- user_notes: text
- timestamp: datetime
- is_public: boolean

#### app_modes
- id: app_mode_id (PK)
- mode_name: text (e.g., "BRUNO MEMORY WHEEL", "IMAGE LAB", "MEMORY PALACE")
- description: text
- scholar_frames: JSON array (which scholars can this mode adopt?)
- core_concepts: FK array → concepts
- core_techniques: FK array → techniques
- underlying_experiments: FK array → experiments
- interactive_elements: JSON array (buttons, controls, visualizations)
- entry_point: text (what does the player do first?)

### Searchability & Indexing

```sql
CREATE VIRTUAL TABLE passages_fts USING fts5(
  passage_id,
  extracted_text,
  passage_type,
  content='passages',
  content_rowid='id'
);

CREATE VIRTUAL TABLE concepts_fts USING fts5(
  concept_id,
  label,
  label_original,
  definition_bruno,
  definition_scholarly,
  content='concepts',
  content_rowid='id'
);
```

## Processing Pipeline

### Stage 1: Extraction (scripts/ingest.py)

```
PDF/TXT/DOCX files
  ↓
Extract text + OCR if needed
  ↓
Identify page boundaries
  ↓
Detect diagrams/figures/marginal notes
  ↓
Generate stable passage IDs (BRUNO-SOURCE-ID/PAGE/PASSAGE-ID)
  ↓
Populate: sources, pages, passages tables
  ↓
Save page images to assets/images/ (if meaningful diagrams)
  ↓
Update manifest.json with extraction status
```

### Stage 2: Schema Build (scripts/build_schema.py)

```
Initialize SQLite with schema.sql
  ↓
Create FTS5 virtual tables
  ↓
Verify table relationships
  ↓
Create indices for common queries
```

### Stage 3: Scholar Parsing (scripts/extract_scholar_profiles.py)

```
For each scholar in corpus:
  Parse their Bruno publications
  ↓
  Extract claims about memory, magic, imagination, etc.
  ↓
  Identify passages they cite
  ↓
  Identify disagreements with other scholars
  ↓
  Populate: scholars, claims, interpretations, disputes tables
```

### Stage 4: Technique Reconstruction (scripts/reconstruct_techniques.py)

```
Search passages for procedural language:
  "first..., then...", "if..., then...", step-by-step descriptions
  ↓
  Extract as technique_id + procedural_steps (JSON)
  ↓
  Label reconstruction_level based on source type + scholar agreement
  ↓
  Populate: techniques table
```

### Stage 5: Vocabulary Extraction (scripts/extract_vocabulary.py)

```
For each key Latin/Italian term:
  Find all passages where it appears
  ↓
  Extract Bruno's usage
  ↓
  Map to English translations
  ↓
  Record scholarly interpretations
  ↓
  Populate: concepts + passages_concepts (many-to-many)
```

## Interactive Tools Architecture

### Frontend Technologies

- **Framework:** Vanilla JS + Vue/React (decide later) or static HTML + data files
- **Visualization:** Three.js (wheels, diagrams), SVG (diagrams, seals), Canvas (memory palace nav)
- **Data delivery:** JSON files + live SQLite queries via API endpoint
- **State persistence:** localStorage for user experiments, IndexedDB for larger state

### API Endpoints (Flask/FastAPI)

```
GET /api/passage/<passage_id>
  → Return passage text, page image, context

GET /api/concept/<concept_id>
  → Return concept definition, passages, scholarly views

GET /api/technique/<technique_id>
  → Return technique description, procedural steps, reconstruction_level

GET /api/scholar/<scholar_id>
  → Return scholar profile, views, disagreements

GET /api/search?q=memoria
  → FTS5 search over passages + concepts

GET /api/compare/<object_type>?objects=technique_1,technique_2&scholars=YATES,CLUCAS
  → Return side-by-side comparison of same object under different scholarly lenses

POST /api/experiment
  → Save user experiment configuration

GET /api/experiment/<experiment_id>
  → Retrieve saved experiment
```

### Tool Prototypes

**1. Memory Wheel**
- Concentric rings: letters, syllables, images, planetary figures, concepts
- Interactive rotation
- Support multiple reconstructions (Yates, Sturlese, Clucas, etc.)
- Show underlying passages for each component
- Allow user to combine elements and generate mnemonic scenes

**2. Image Lab**
- Component picker: person, animal, object, action, location, planet, god, attribute, emotion, color, number, letter, concept
- Real-time image generation (procedural or AI-assisted)
- Store as serializable BrunoImage data structure
- Link to textual descriptions from Bruno's works

**3. Memory Palace**
- Virtual walk-through structure
- Each locus contains: image, word, concept, primary passage, scholarly interpretation, user notes
- Navigation: next/prev locus, jump to index, search
- Mode toggle: YATES (talismanic), CLUCAS (ethical), WANG (iconic practice)

**4. Scholar Mode Switcher**
- Global toggle: BRUNO THROUGH [YATES | CLUCAS | MERTENS | WANG | BARENSTEIN | COULIANO | UNALIGNED]
- When switched, all interpretations, images, technique descriptions update to reflect that scholar's framework
- Show: "this interpretation comes from Scholar X, cites these passages, contested by Scholar Y"

**5. Compare Interface**
- Select object (technique, concept, passage)
- Select scholars (checkboxes)
- Show side-by-side:
  - Primary evidence (Bruno's own words)
  - Scholar A's interpretation
  - Scholar B's interpretation
  - Disagreements flagged
  - User can enter experimental reconstruction under each framework

## Incremental Rollout

**MVP (Phase 1–3):**
- Corpus inventory (BRUNO_CORPUS.md)
- PDF extraction pipeline
- SQLite schema + populated database
- Basic search interface

**Phase 4:**
- Scholar profiles + dispute graph
- Bruno vocabulary glossary
- Technique reconstruction (labeled by confidence)

**Phase 5:**
- Memory Wheel prototype (Yates reconstruction, then expand)
- Scholar mode switching
- "Compare scholars" interface for one technique/concept

**Phase 6:**
- Image Lab
- Memory Palace prototype

**Phase 7+:**
- Remaining modes (Seal Lab, Circle/Cosmos, Vinculum, Plotinian, Heroic Furor)
- Full scholar-specific app variants
- User experiment saving/sharing

## Technical Stack (Provisional)

- **Language:** Python 3.10+
- **PDF extraction:** PyPDF2, pdfplumber, pytesseract (OCR)
- **Data:** SQLite 3.35+ (with FTS5)
- **API:** Flask or FastAPI
- **Frontend:** Vanilla JS + Vue 3 or static HTML (TBD)
- **Visualization:** Three.js, SVG, D3 or Recharts (TBD)
- **Hosting:** Local (development) or Vercel/Netlify (if published)

## File Organization

```
C:\Dev\BRUNOMEMAPP\
├── CLAUDE.md                           ← this project's instructions
├── docs/
│   ├── DESIGN.md                       ← this file (architecture)
│   ├── BRUNO_CORPUS.md                 ← inventory (auto-generated)
│   ├── BRUNO_PIPELINE.md               ← extraction workflow
│   ├── SCHOLARS.md                     ← scholar profiles (auto-generated)
│   ├── VOCABULARY.md                   ← Bruno's terminology glossary
│   └── RESEARCH_QUESTIONS.md           ← open scholarly questions
├── data/
│   ├── schema.sql                      ← SQLite schema definition
│   ├── bruno.db                        ← canonical research database
│   └── manifest.json                   ← corpus inventory (machine-readable)
├── scripts/
│   ├── ingest.py                       ← PDF/text extraction
│   ├── build_schema.py                 ← create SQLite schema
│   ├── extract_scholar_profiles.py     ← parse scholars
│   ├── build_dispute_graph.py          ← identify disagreements
│   ├── extract_vocabulary.py           ← glossary generation
│   ├── reconstruct_techniques.py       ← technique identification
│   └── test_extraction.py              ← QA/testing
├── src/
│   ├── api.py                          ← Flask/FastAPI server
│   ├── models.py                       ← SQLAlchemy ORM models (optional)
│   ├── search.py                       ← FTS5 query handler
│   └── frontend/                       ← web UI (HTML, JS, Vue/React)
│       ├── index.html
│       ├── styles.css
│       ├── app.js
│       └── components/
│           ├── MemoryWheel.js
│           ├── ImageLab.js
│           ├── MemoryPalace.js
│           ├── ScholarComparison.js
│           └── ConceptSearch.js
├── assets/
│   ├── diagrams/                       ← extracted diagram images
│   ├── images/                         ← page images from PDFs
│   └── manuscripts/                    ← reference scholarly articles
└── tests/
    ├── test_ingest.py
    ├── test_schema.py
    └── test_api.py
```

## Research Questions as Living Document

The system must preserve these as actionable UI elements:

1. How magical is Bruno's ars memoriae?
2. Is Bruno's image primarily mnemonic, psychological, metaphysical, magical, or all four?
3. What exactly is a simulacrum? A signaculum? A vinculum?
4. How reliable is Yates's reconstruction? (Sturlese correction forces answer)
5. How does Clucas reinterpret the system through Plotinus?
6. How does Mertens negotiate the memory ↔ magic relationship?
7. How does Wang's "iconic practice" change gnoseology?
8. Does Bruno intend astral influence literally, metaphorically, psychologically, or naturally?
9. Can we transcend the magic/science historiographical binary?

## Next Steps

1. Complete E:\pdf\ audit → BRUNO_CORPUS.md
2. Write BRUNO_PIPELINE.md (details on extraction strategy)
3. Write schema.sql (full SQLite definition)
4. Write scripts/ingest.py (robust PDF extraction)
5. Populate database with real corpus data
6. Build scholar profiles from extracted claims
7. Create first prototype: Memory Wheel with Yates reconstruction + real passages
