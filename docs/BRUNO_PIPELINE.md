# BRUNOMEMAPP Ingestion & Processing Pipeline

## Overview

The pipeline transforms raw Bruno documents (PDFs, texts, scholarly materials) into structured, searchable, citable research data. It maintains clear provenance and supports iterative refinement.

```
Raw Documents (E:\pdf\renaissance magic\bruno\)
    ↓
Document Extraction (scripts/ingest.py)
    ├─ PDF text + OCR
    ├─ TXT/DOCX/EPUB parsing
    ├─ File hashing (deduplication)
    └─ Passage ID generation
    ↓
SQLite Population (sources, pages, passages)
    ↓
Metadata & Biblography Extraction (scripts/extract_metadata.py)
    ├─ Author detection
    ├─ Title/date/edition inference
    ├─ Edition linking
    └─ Scholar identification
    ↓
Scholar Profile Extraction (scripts/extract_scholar_profiles.py)
    ├─ Parse scholarly claims about Bruno
    ├─ Identify evidence passages
    ├─ Build views (memory, magic, imagination, etc.)
    └─ Populate scholars, claims, interpretations tables
    ↓
Technique Reconstruction (scripts/reconstruct_techniques.py)
    ├─ Identify procedural passages
    ├─ Extract steps and evidence
    ├─ Label reconstruction_level
    └─ Populate techniques table
    ↓
Dispute & Disagreement Graph (scripts/build_dispute_graph.py)
    ├─ Parse scholar contradictions
    ├─ Track evidence for each position
    ├─ Model resolution status
    └─ Populate disputes table
    ↓
Vocabulary/Glossary Extraction (scripts/extract_vocabulary.py)
    ├─ Identify key Latin/Italian terms
    ├─ Collect contexts
    ├─ Map translations
    ├─ Record interpretations
    └─ Populate concepts table
    ↓
Full-Text Search Indexing (automatic via FTS5)
    ├─ passages_fts
    ├─ concepts_fts
    └─ claims_fts
    ↓
Web Tools Data Export (scripts/export_for_web.py)
    ├─ JSON for Memory Wheel
    ├─ JSON for Image Lab
    ├─ JSON for Scholar modes
    └─ Serve via API
```

## Phase Descriptions

### Phase 1: Raw Document Ingestion

**Purpose:** Convert files into standardized extracted text with stable IDs.

**Input:** E:\pdf\renaissance magic\bruno\ and related directories (primary and secondary sources)

**Process:**
1. Scan directory recursively for .pdf, .txt, .epub, .docx, .html files
2. For each file:
   - Calculate SHA256 hash (deduplication)
   - Determine file type
   - Extract text (PDFs → PyPDF2, TXTs → direct read, DOCX → python-docx, EPUB → ebooklib)
   - If PDF is image-only, flag for OCR
   - Generate page boundaries (rough: ~3000 chars per page)
   - Split into passages (roughly paragraph-sized)
   - Generate stable passage ID: `BRUNO-{source_id:04d}/{page}/{chunk:04d}`
3. Insert into `sources`, `pages`, `passages` tables

**Output:**
- Populated `sources` table (filename, file_type, file_hash, extraction_status, ocr_confidence)
- Populated `pages` table (page_number, page_label, extracted_text, has_diagram, image_filename)
- Populated `passages` table (extracted_text, stable_passage_id, language_original, confidence)
- `manifest.json` (machine-readable corpus state)

**Script:** `scripts/ingest.py`

**Status indicators:**
- extraction_status: pending | extracted | OCR_required | failed
- ocr_status: none | pending | completed | failed
- confidence: DIRECTLY_ATTESTED | OCR_UNCERTAIN | EDITORIAL_RECONSTRUCTION

### Phase 2: Metadata & Bibliography Extraction

**Purpose:** Enrich documents with edition, author, and date information.

**Process:**
1. For each source, attempt to infer from:
   - Filename patterns (e.g., "De_Umbris_1582.pdf" → date=1582)
   - Title page text extraction
   - Header/footer extraction
   - Embedded metadata (PDF properties)
2. Match against known Bruno editions:
   - De umbris idearum (1582, 1584, etc.)
   - Spaccio della bestia trionfante (1584)
   - Asini cifrati (1585)
   - Imago populi Europae (1585)
   - De imaginum, signorum et idearum compositione (1591)
   - Ars reminiscendi (via Trigone, etc.)
   - Magical texts (Three Books of Occult Philosophy, etc.)
   - Scholarly monographs (Yates, Clucas, etc.)
3. Create or link to existing `editions` records
4. Populate `authors` table
5. Mark `is_primary_source` flag

**Output:**
- Enriched `sources` (edition_id)
- Populated `authors` table
- Populated `editions` table (work_id, editor, publication_year, is_canonical)
- Populated `works` table (author_id, title, work_type, date_published, is_primary_source)

**Script:** `scripts/extract_metadata.py` (TBD)

### Phase 3: Scholar Profile Extraction

**Purpose:** Parse scholarly writings to extract claims about Bruno and build interpretive profiles.

**Process:**
1. For each secondary source (scholarly monograph/article):
   - Extract sections discussing Bruno's memory, magic, imagination
   - Identify explicit claims (e.g., "Bruno's wheel functions as a Hermetic talisman")
   - Locate supporting evidence (citations to Bruno, page refs)
   - Extract scholar's views on:
     - Memory and imagination
     - Images and representation
     - Magic and natural philosophy
     - Neoplatonism and Plotinus
     - Personality (confident, uncertain, speculative)
2. Populate `scholars` table with profile
3. Link claims to passages via `claims_passages`
4. Populate `interpretations` linking scholar → object → interpretation

**Output:**
- Populated `scholars` table (name, views JSON, major_bruno_works)
- Populated `claims` table (scholar_id, claim_text, confidence)
- Populated `interpretations` table (scholar_id, object_type, object_id, interpretation_text)
- Populated `claims_passages` (many-to-many linking claims to evidence)

**Script:** `scripts/extract_scholar_profiles.py` (TBD)

**Confidence levels:**
- CONFIDENT: Scholar explicitly argues position
- UNCERTAIN: Scholar hedges or qualifies
- CONTESTED: Disagreement with other scholars noted

### Phase 4: Technique Reconstruction

**Purpose:** Identify procedural passages and operationalize Bruno's techniques.

**Process:**
1. Search all passages for procedural language:
   - "First..., then...", "If..., then..."
   - Numbered steps
   - Instructions / "how to"
   - Imperative mood
2. For each identified technique:
   - Extract all textual steps
   - Identify evidence source (primary or secondary)
   - Label reconstruction_level:
     - HISTORICALLY_ATTESTED: Bruno explicitly describes
     - DIRECT_RECONSTRUCTION: Straightforward from Bruno's text
     - SCHOLARLY_RECONSTRUCTION: Scholars have reconstructed missing parts
     - SPECULATIVE_IMPLEMENTATION: Educated guess / experimental extension
3. Link to related concepts and interpretations
4. Populate `techniques` table with procedural_steps (JSON)

**Output:**
- Populated `techniques` table (name, reconstruction_level, procedural_steps JSON)
- Populated `techniques_passages` (evidence linking)
- Example techniques:
  - Memory Wheels (Yates / Sturlese / Clucas reconstructions)
  - Image Construction (Couliano)
  - Mnemonic Loci (classical + Bruno)
  - Seal Systems (Sigillus Sigillorum)
  - Contemplative Ascent (Plotinian)

**Script:** `scripts/reconstruct_techniques.py` (TBD)

### Phase 5: Dispute & Disagreement Graph

**Purpose:** Model scholarly disagreements and track evidence for competing interpretations.

**Process:**
1. For each identified dispute (e.g., "Yates vs. Sturlese on planetary placement"):
   - Identify position A and position B
   - Collect evidence passages for each
   - Note resolution status (ONGOING, CONSENSUS, SUPERCEDED, NOT_COMPARABLE)
2. Link disagreeing scholars
3. Track which passages support which position
4. Populate `disputes` and `disputes_passages`

**Output:**
- Populated `disputes` table (topic, position_a_scholar_id, position_b_scholar_id, resolution)
- Populated `disputes_passages` (dispute_id, passage_id, position)
- Example disputes:
  - Planetary images placement in De umbris wheel
  - Whether wheels function as talismans or memory aids
  - Plotinian influence on Bruno's theory

**Script:** `scripts/build_dispute_graph.py` (TBD)

### Phase 6: Vocabulary/Glossary Extraction

**Purpose:** Build a searchable glossary of Bruno's key terms with contexts and interpretations.

**Process:**
1. Identify key Latin/Italian terms:
   - memoria, imaginatio, phantasia, simulacrum, signaculum, umbra, imago, species, etc.
2. For each term:
   - Collect all passages where it appears (with context)
   - Extract Bruno's usage and definition
   - Map to English translations
   - Record scholarly interpretations
   - Note conceptual neighbors
3. Populate `concepts` and `concepts_passages`

**Output:**
- Populated `concepts` table (label, label_original, definition_bruno, definition_scholarly)
- Populated `concepts_passages` (linking concepts to passages)
- FTS5 index for concept search

**Script:** `scripts/extract_vocabulary.py` (TBD)

### Phase 7: Full-Text Search Indexing

**Purpose:** Enable fast, fuzzy search across passages, concepts, and claims.

**Process:**
- SQLite FTS5 automatic indexing via INSERT triggers
- Indices: `passages_fts`, `concepts_fts`, `claims_fts`
- Supports phrase search, AND/OR, NEAR(), prefix matching

**Output:**
- FTS5 virtual tables (automatic)

**Script:** Automatic (no script; triggers in schema.sql)

### Phase 8: Web Tools Data Export

**Purpose:** Export processed data into formats suitable for interactive tools.

**Process:**
1. Export scholar frames (BRUNO THROUGH YATES, etc.) as JSON
2. Export technique reconstructions with evidence
3. Export concept relationships
4. Export dispute graph
5. Generate widget-specific data (Memory Wheel JSON, Image Lab component lists, etc.)
6. Serve via Flask/FastAPI endpoints

**Output:**
- JSON files: `/data/web/memory_wheel.json`, `/data/web/scholars.json`, etc.
- Live API endpoints: `/api/technique/<id>`, `/api/scholar/<id>`, `/api/compare/...`

**Script:** `scripts/export_for_web.py` (TBD)

## Rerunning the Pipeline

**One-time setup:**
```bash
python scripts/build_schema.py           # Creates empty database
python scripts/ingest.py                 # Extracts documents
```

**Iterative refinement (safe to rerun):**
```bash
python scripts/extract_metadata.py       # Updates editions, authors
python scripts/extract_scholar_profiles.py
python scripts/reconstruct_techniques.py
python scripts/build_dispute_graph.py
python scripts/extract_vocabulary.py
python scripts/export_for_web.py
```

**Full rebuild (destructive):**
```bash
python scripts/build_schema.py --force   # Deletes existing database
python scripts/ingest.py                 # Re-extracts all documents
[... rest of pipeline]
```

## Incremental Ingestion

- File hashing prevents duplicate ingestion
- Ingestion log (`ingestion_log` table) tracks progress
- Can safely re-ingest: new documents are added, existing ones skipped

## Data Quality Checkpoints

### OCR Confidence
- PDFs with extracted text: `ocr_confidence = 1.0`
- PDFs with OCR-extracted text: `ocr_confidence = pytesseract confidence (0.0–1.0)`
- Passages flagged as `OCR_UNCERTAIN` when confidence < 0.8

### Passage Confidence
- `DIRECTLY_ATTESTED`: PDFs with direct text extraction
- `OCR_UNCERTAIN`: Passages from OCR with low confidence
- `EDITORIAL_RECONSTRUCTION`: Missing passages inferred from context

### Deduplication
- File-level: SHA256 hash prevents duplicate source ingestion
- Passage-level: Multiple editions of same work detected via edition_id matching

## Archive Structure Assumptions

**Expected layout of E:\pdf\renaissance magic\bruno\:**
```
E:\pdf\renaissance magic\bruno\
├── bruno_primary/                    # Primary sources by Bruno
│   ├── De_Umbris_1582.pdf
│   ├── De_Umbris_1584.pdf
│   ├── Spaccio_1584.pdf
│   ├── Asini_Cifrati_1585.pdf
│   ├── De_Imaginum_1591.pdf
│   └── ...
├── bruno_secondary/                  # Scholarly studies
│   ├── Yates_Art_of_Memory.pdf
│   ├── Clucas_Mnemonics.pdf
│   ├── Mertens_Magic_and_Memory.pdf
│   ├── Wang_Iconic_Practice.pdf
│   ├── Barenstein_Memoria_Regulata.pdf
│   └── ...
└── bruno_manuscripts/                # Transcripts, editions
    ├── Lagano_Critical_Edition/
    └── ...
```

## Troubleshooting

**Issue: "PyPDF2 not available"**
```bash
pip install PyPDF2
```

**Issue: Image-only PDFs (OCR_required)**
```bash
pip install pytesseract pillow
# Also need Tesseract installed (separate binary)
```

**Issue: Malformed PDF**
- Logged in `sources.notes`
- `extraction_status = 'failed'`
- Inspect manually and add notes

**Issue: Duplicate files detected**
- Check `manifest.json` for file_hash matches
- Usually means multiple editions of same work (intentional)
- Separate by creating multiple `editions` records

## Next Steps

1. Verify archive structure in E:\pdf\renaissance magic\bruno\
2. Run: `python scripts/build_schema.py`
3. Run: `python scripts/ingest.py --verbose`
4. Inspect `manifest.json` and `bruno.db` for completeness
5. Run Phase 2 onwards
