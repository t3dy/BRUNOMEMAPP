# BRUNOMEMAPP Next Actions

## STATUS UPDATE (superseding the sessions below — see docs/ARCHITECTURE_PIVOT.md)

The original Flask/SQLAlchemy roadmap below is superseded. Actual current state:

- Architecture pivoted to the WitcherPortal seed-JSON -> SQLite -> static-site pattern.
- `bruno_seed.json` populated with real content: 21 works (full magical + poetic corpus,
  including Cabala del cavallo pegaseo and De gli eroici furori), 5 images, 11 scholars,
  12 dictionary terms, 3 disputes, 9 biographical events (memory/magic-filtered), 1 essay
  (Plotinus <-> Bruno), 7 app-mode ideas (including comedic ones for Cabala), 13 bibliography entries.
- `db/bruno.db` built and seeded. `site/` built: 70 static HTML pages, 0 broken internal links (verified).
- Decisions from 2026-09-01 clarifying questions:
  1. **Breadth first** — next pass expands thinner areas (more images, terms, scholars) across
     the whole corpus rather than going deeper on Cabala/Furori specifically.
  2. **Humor stays in the main site**, tone-badged (gold badge + explicit "why this source
     supports it" grounding) rather than split into a separate section or site.
  3. **`corpus/` + `scripts/convert_corpus.py`** (PDF/text extraction from
     `E:\pdf\renaissance magic\bruno\`, mirroring WitcherPortal's `convert_corpus.py`) is the
     next real build task — not yet started.

### Immediate next session

1. Write `scripts/convert_corpus.py` (manifest-driven, idempotent, PDF/EPUB -> `corpus/sources/*.md`).
2. Run it against `E:\pdf\renaissance magic\bruno\` and see what's actually there.
3. Breadth pass on `bruno_seed.json`: more `images` entries (wheel components from De umbris,
   Sigillus Sigillorum figures, De imaginum examples), more `dictionary_terms`, possibly more
   `scholars` if found in the corpus.
4. Re-run `python scripts/seed_from_json.py && python scripts/build_site.py` after each edit.

### How to view the site right now

This sandbox's Browser-pane networking was cross-wired to another concurrent session during
this build (verified via direct file/link-integrity checks instead — 70/70 pages, 0 broken
links). To view for real: open `C:\Dev\BRUNOMEMAPP\site\index.html` directly in a browser, or
run `python -m http.server` from inside `site/` and open `http://localhost:8000`.

---

## ORIGINAL ROADMAP (superseded, kept for reference)

## Session 0 (Just Completed) ✓

- [x] Create project folder structure
- [x] Write CLAUDE.md (project instructions)
- [x] Write DESIGN.md (architecture + data model)
- [x] Write BRUNO_PIPELINE.md (ingestion workflow)
- [x] Write schema.sql (complete SQLite schema)
- [x] Write scripts/build_schema.py (database initialization)
- [x] Write scripts/ingest.py (document extraction pipeline)
- [x] Write README.md (quick start guide)
- [x] Write docs/PORTAL_INTEGRATION.md (card reuse strategy)
- [x] Write docs/RESEARCH_QUESTIONS.md (open scholarly questions)
- [x] Write requirements.txt (Python dependencies)
- [x] Write .gitignore
- [x] Write docs/CORPUS_AUDIT.md (audit checklist)

**Deliverables:** Core system scaffold, database schema, extraction pipeline, documentation

---

## Session 1 (Next)

### Phase 1: Corpus Inventory & Database Population

#### 1.1 Audit the Archive

**Goal:** Discover what Bruno documents exist in E:\pdf\renaissance magic\bruno\

**Tasks:**
- [ ] Navigate to E:\pdf\renaissance magic\bruno\
- [ ] Explore directory structure (is it flat or organized?)
- [ ] List all files recursively
- [ ] Identify primary vs. secondary sources
- [ ] Note any duplicates or variant editions
- [ ] Fill in docs/CORPUS_AUDIT.md

**Deliverable:** Completed CORPUS_AUDIT.md (at least summary statistics)

#### 1.2 Initialize Database

**Goal:** Create empty SQLite database with schema

**Tasks:**
```bash
cd C:\Dev\BRUNOMEMAPP
python scripts/build_schema.py
```

**Expected output:**
- `data/bruno.db` (empty, but with all tables and indices)
- Console output showing all tables, FTS5 indices, views created

**Deliverable:** Functional database ready for ingestion

#### 1.3 Run Ingestion Pipeline

**Goal:** Extract all documents and populate database

**Tasks:**
```bash
python scripts/ingest.py --verbose
```

**Expected output:**
- `data/manifest.json` (machine-readable corpus inventory)
- Console output showing each file ingested, passage counts, etc.
- `sources`, `pages`, `passages` tables populated

**Troubleshooting:**
- If "PyPDF2 not available": `pip install -r requirements.txt`
- If paths not found: adjust `--source-dir=...`
- If PDFs are image-only: they'll be flagged for OCR in Phase 2

**Deliverable:** Populated database with all documents extracted

#### 1.4 Review Ingestion

**Goal:** Verify extraction quality

**Tasks:**
- [ ] View `data/manifest.json` to see all files + status
- [ ] Query database to spot-check:
  ```sql
  SELECT COUNT(*) FROM sources;                    -- Should match audit count
  SELECT COUNT(*) FROM pages;
  SELECT COUNT(*) FROM passages;
  SELECT * FROM sources WHERE extraction_status = 'failed';  -- Any failures?
  ```
- [ ] Sample a few passages to verify text quality
- [ ] Note any OCR_required PDFs

**Deliverable:** Inventory report, QA notes

### Phase 2: Metadata & Bibliography (Preparatory)

These don't need to run yet, but should be planned.

#### 2.1 Plan metadata extraction

**Goal:** Design how to extract author, title, date, edition from documents

**Deliverable:** Outline for scripts/extract_metadata.py

#### 2.2 Plan scholar profile extraction

**Goal:** Design how to parse scholarly claims

**Deliverable:** Outline for scripts/extract_scholar_profiles.py

---

## Session 2 (Estimated 1-2 weeks)

### Phase 2: Rich Metadata

#### 2.1 Write & run scripts/extract_metadata.py

- Extract/infer: author, title, date, edition
- Link to known editions
- Populate `authors`, `works`, `editions` tables

**Deliverable:** Enriched database with edition metadata

#### 2.2 Generate BRUNO_CORPUS.md

- Auto-generate from database + audit notes
- List all works, editions, language variants
- Note key gaps or duplicates

**Deliverable:** BRUNO_CORPUS.md (canonical inventory)

---

## Session 3 (Estimated 2-3 weeks)

### Phase 3: Scholar Profiles & Claims

#### 3.1 Write & run scripts/extract_scholar_profiles.py

- Parse secondary sources for claims about Bruno
- Extract: memory views, magic views, imagination views, etc.
- Link to passages cited as evidence
- Populate `scholars`, `claims`, `interpretations` tables

**Deliverable:** Scholar profiles with identified claims

#### 3.2 Generate SCHOLARS.md

- Auto-generate scholarly profiles
- List each scholar's views, disagreements, key works

**Deliverable:** SCHOLARS.md

---

## Session 4 (Estimated 2-3 weeks)

### Phase 4: Dispute Graph & Technique Reconstruction

#### 4.1 Write & run scripts/build_dispute_graph.py

- Identify scholarly disagreements
- Model both positions + evidence
- Populate `disputes` table

**Deliverable:** Dispute graph with evidence

#### 4.2 Write & run scripts/reconstruct_techniques.py

- Identify procedural passages
- Extract technique steps
- Label reconstruction confidence
- Populate `techniques` table

**Deliverable:** Technique reconstructions with evidence

#### 4.3 Write & run scripts/extract_vocabulary.py

- Build glossary of key terms (memoria, imagin, etc.)
- Collect contexts and interpretations
- Populate `concepts` table

**Deliverable:** VOCABULARY.md (searchable glossary)

---

## Session 5 (Estimated 1-2 weeks)

### Phase 5: First Interactive Prototype

#### 5.1 Design Memory Wheel prototype

- Decide: React/Vue or vanilla JS?
- Decide: Which scholar reconstruction (Yates? Clucas? Sturlese?)
- Write data export: scripts/export_for_web.py
- Create wheel visualization (SVG or Canvas)

**Deliverable:** Working Memory Wheel prototype with real corpus data

#### 5.2 Build scholar mode switcher

- Add dropdown: "Bruno Through [Scholar]"
- When switched, show that scholar's interpretation
- Display passages supporting each scholar's view

**Deliverable:** Working mode switcher with 2-3 scholar modes

---

## Session 6+ (Longer term)

### Phase 6: Expanded Tools

- Image Lab (construct mnemonic images)
- Memory Palace (walk-through structure)
- Scholar Comparison (side-by-side views)
- Seal Lab (Sigillus Sigillorum)
- Vinculum/Bond mode (Couliano-inspired)
- Plotinian Memory mode
- Heroic Furor mode

### Phase 7: Portal Integration

- Adapt WITCHER PORTAL card templates
- Build biography timeline card
- Build concept cards
- Build work/edition cards
- Build scholar profile cards
- Build dispute cards

### Phase 8: Refinement & Launch

- User testing
- Performance optimization
- Documentation
- Deployment (Vercel? Local?)

---

## Critical Path

**Must-haves before "MVP complete":**

1. ✓ Schema + database (Session 0)
2. ✓ Ingestion pipeline (Session 0-1)
3. Corpus inventory BRUNO_CORPUS.md (Session 2)
4. Scholar profiles SCHOLARS.md (Session 3)
5. Technique reconstructions (Session 4)
6. First Memory Wheel prototype (Session 5)
7. Scholar mode switching (Session 5)

After these 7 items, you have a functional (if minimal) research + interactive system.

---

## Dependency Check

Before starting Session 1, verify:

```bash
# Python 3.10+
python --version

# Required packages
pip install PyPDF2 pdfplumber

# Database
sqlite3 --version   # Should be built-in

# Ready to go!
```

If any missing, run:
```bash
pip install -r requirements.txt
```

---

## Conventions

- All timestamps in UTC
- File hashes: SHA256
- Passage IDs: `BRUNO-{source_id:04d}/{page}/{chunk:04d}`
- Scholar names: Use full name as appears in publications
- Terms: Use original Latin/Italian where possible, English translation in parentheses

---

## Communication Checkpoints

After completing each session, report:

1. **What was completed** (specific deliverables)
2. **What the data looks like** (sample queries, statistics)
3. **What blockers were hit** (if any)
4. **What's next** (preview of Session N+1)

---

## Remember

- Never fabricate Bruno quotes or metadata
- Always link claims back to source passages
- Never blur PRIMARY SOURCE ← → INTERPRETATION boundaries
- Players should always know which layer they're operating in
- Unresolved scholarly questions are features, not bugs

Good luck! This is going to be amazing. 🧠✨
