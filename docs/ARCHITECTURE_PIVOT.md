# Architecture Pivot: WitcherPortal Pattern

**Date:** 2026-09-01 (same day as initial scaffold)

## What changed

Session 0 built a heavier Flask/SQLAlchemy-style architecture (`data/schema.sql`, `scripts/build_schema.py`, `scripts/ingest.py` writing directly to a normalized 20-table DB). Ted asked to crib the existing portal pattern instead, to save effort/tokens/context and stay consistent with `WitcherPortal`, `AtalantaClaudiens`, and the other DH portals.

**New pattern (from `C:\Dev\WitcherPortal`), adopted wholesale:**

```
bruno_seed.json          ← hand/LLM-curated content, source of truth for the SITE
scripts/init_db.py        ← idempotent schema (CREATE TABLE IF NOT EXISTS)
scripts/seed_from_json.py ← wipes + reloads seed-sourced rows from bruno_seed.json
scripts/build_site.py     ← reads db/bruno.db, writes static HTML to site/
db/bruno.db                ← generated, not hand-edited
site/                       ← generated static HTML, style.css/script.js edited by hand
corpus/sources/            ← plain-text conversions of PDFs (grep-able research grounding, NOT rendered to site)
scripts/convert_corpus.py  ← PDF/EPUB → corpus/sources/*.md, idempotent, manifest-driven
```

**No frameworks. No build step. Vanilla HTML/CSS/JS on the frontend.** Same as WitcherPortal/AtalantaClaudiens.

## What happened to Session 0's work

- `data/schema.sql`, `scripts/build_schema.py`, `scripts/ingest.py` are **SUPERSEDED**, not deleted. They document a fuller normalized provenance/dispute model (claims↔passages↔interpretations as first-class many-to-many tables) that may be worth reintroducing later if the flat seed-JSON model proves too limiting for the dispute graph or technique reconstructions. Left in place under `data/` and `scripts/` with a superseded note; not run.
- `DESIGN.md` and `BRUNO_PIPELINE.md` describe that heavier architecture — read them as the **long-term/aspirational** design, not the current build target. The current build target is this document + `bruno_seed.json`.

## Why the flat model is enough for now

WitcherPortal's model — every entity is a flat row with `slug`, `summary`, `full_description`, `tags`, `source_method`, `review_status`, `confidence`, plus two polymorphic link tables (`scholarly_refs`, and here `dispute_evidence`) — already satisfies BRUNOMEMAPP's core requirement: **every claim traces to a source, and provenance is visible.** It just does it with fewer tables. The normalized version becomes worth the complexity only once the corpus is large enough that free-text `primary_sources` / `evidence_passages` fields stop being adequate — i.e., once we're doing real FTS5 passage-level citation, not portal cards.

## Two-track content model (mirrors WitcherPortal exactly)

1. **`corpus/`** — raw extracted text from `E:\pdf\renaissance magic\bruno\`. Grep-able research grounding. Not rendered to the site. Used when writing/updating seed entries so claims are source-grounded.
2. **`bruno_seed.json`** — curated cards (works, images, scholars, dictionary, disputes, essays, biographical events, app-mode ideas). This IS the site content.

Ted greps the corpus, writes/updates a seed entry citing what he found, re-runs the three scripts. Same workflow as WitcherPortal's `corpus/sources/*.md` → seed JSON pattern described in that project's CLAUDE.md.

## Domain entities in the new schema (see `scripts/init_db.py`)

- `works` — Bruno's own magical, mnemonic, and poetic works (De umbris idearum through De gli eroici furori), each tagged with `memory_magic_relevance` and `memory_magic_connection`
- `images` — individual mnemonic/magical images and figures Bruno used, as their own addressable cards
- `scholars` — Yates, Clucas, Sturlese, Torchia, Mertens, Wang, Barenstein, Couliano, Gatti, Farinella, Preston, Ostojić, etc.
- `dictionary_terms` — Bruno's vocabulary (memoria, phantasia, simulacrum, signaculum, umbra, vinculum, ...)
- `disputes` — scholarly disagreements, two-position model with evidence on each side
- `biographical_events` — Bruno's life, filtered to events relevant to memory/magic (not a general biography)
- `essays` — long-form connective pieces (e.g., the Plotinus↔Bruno essay already drafted in `brunomem.txt`)
- `app_mode_ideas` — interactive tool / game concepts, including explicitly humorous ones for *Cabala del cavallo pegaseo* and *De gli eroici furori*
- `bibliography` / `scholarly_refs` — same polymorphic citation pattern as WitcherPortal

## Next step

Populate `bruno_seed.json` (this session) with a first real pass at all 21 known Bruno works, initial scholar profiles, the vocabulary list, and app-mode ideas — then run the three scripts and generate the first static site.
