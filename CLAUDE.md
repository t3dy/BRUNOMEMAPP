# Claude Code Instructions — BRUNOMEMAPP

Web tools that let a user **operate** Giordano Bruno's arts of memory, with Renaissance worldview friction explained at every step, and scholarly disagreements exposed as **playable variants**.

---

## START HERE — every session, in this order

1. **`PROMPTS.md`** — Ted's prompts verbatim + the 11 standing requirements. **The spec of record.** Read before touching code.
2. **`docs/WORKING_LOOP.md`** — the S0→S6 pipeline and the progressive-revelation rules.
3. This file — routing.

Then state your goal and enter the loop at the right stage. **Do not open the corpus at S0.**

## Doc routing — load only what your task needs

| Task | Read |
|---|---|
| Any corpus work | `docs/CORPUS_MAP.md` → grep → slice. Never a whole file. |
| What's already been found | `HARVEST.md` |
| Practice / friction design | `docs/design/PRACTICES.md` |
| Frame or artifact design | `docs/design/README.md` → the specific doc |
| Data model, provenance, testability | `docs/design/ARCHITECTURE.md` |
| Site content edits | `bruno_seed.json` → re-run scripts |
| Why the architecture changed | `docs/ARCHITECTURE_PIVOT.md` |

## Corpus — corrected location

**`E:\pdf\renaissance magic\Bruno Lull\`** — the path in earlier drafts (`...\bruno\`) **does not exist**.

- **`plain_text_drafts/`** — 24 pre-extracted `.txt`. Use these; no PDF extraction needed.
- Holdings and gaps: `docs/WORKING_LOOP.md` §Corpus location.
- **Not on disk:** Yates *Art of Memory*, *Ad Herennium*, Quintilian, Carruthers, Camillo, Fludd, Sturlese's critical edition → anything from those is `LLM_GENERAL_KNOWLEDGE`, capped `confidence: MEDIUM`.

```bash
python scripts/corpus_map.py        # regenerate the line-addressed index
```

## Build pipeline

```bash
python scripts/init_db.py           # idempotent schema -> db/bruno.db
python scripts/seed_from_json.py    # bruno_seed.json -> db
python scripts/build_site.py        # db -> site/ (static HTML)
```

After **any** seed edit: `python scripts/seed_from_json.py && python scripts/build_site.py`

Architecture cribbed from `C:\Dev\WitcherPortal` (seed-JSON → SQLite → static site, vanilla CSS/JS, no frameworks, no build step). When unsure of a pattern, look there first.

Superseded and not run: `data/schema.sql`, `scripts/build_schema.py`, `scripts/ingest.py` (marked in-file).

## The three layers

```
PRACTICE      operable, step-by-step, as concrete as the sources allow  ← primary
FRICTION      per-step worldview + interface difficulty, continuous     ← never optional
SCHOLARSHIP   a writing layer over the practice; where a reading changes
              the mechanics it becomes a PLAYABLE VARIANT
```

Superseded readings stay playable. Yates's talismanic wheel is fun *because* it is a counterfactual magical practice.

## Hard rules

- **Never fabricate.** Grade operability honestly (`FULLY_OPERABLE` / `PARTIALLY` / `REFERENCE_ONLY`). Never invent missing steps to make a system look complete — the Thirty Seals are the standing temptation.
- **Memory-magic filter.** Every work, image, and biographical event carries a required explicit connection to the memory-magic question. Nothing is included for being merely Bruno-related.
- **Every practice step gets ≥1 friction note.** A step with none hasn't been thought about.
- **Locate before reading; slice, don't load; log slices in `HARVEST.md`.**
- **Confidence `HIGH` requires corpus grounding.** Currently every row is `SEED_DATA` general knowledge — see `ARCHITECTURE.md` §4 for the provenance ladder that fixes this.
- **Mine for playable material, not facts to file.** Specified inventories are the jackpot.

## Current state (2026-09-02)

- Site builds: **99 pages, 0 broken links.** `site/index.html`, or serve `site/`.
- **27 period plates live** — `scripts/extract_plates.py` → `site/assets/plates/` + `data/plates.json`. Bruno's atrium in both 1591 and Tocco versions, planetary chariots (Jupiter/Saturn/Sol identified by reading the plate), the numeral table, emblems. 9 identified, 18 published by page without a name. 3.9 MB, grayscale-quantized.
- **Scholar quotations live** — `data/quotations.json`, rendered via `quotes_for()` on the gallery, engine and fantastica pages. 14 quotations from Bonner, Mertens, Blum, Llull, Bruno; each carries author, work, corpus locator, and a note on why it is there.
- **The Figures gallery is live** — `site/gallery.html` + `site/diagrams.js`, driven by `data/diagrams.json`. Six interactive SVG figures built from harvested data: Llull A (K16, 120 chords), V (D2/7), X (opposed pairs), S (four inscribed squares), Bruno's atrium (24 atria x 24 positions, switchable), and a combinatorial wheel. Three figures deliberately NOT drawn, with reasons stated on the page.
- **Logica Fantastica is live and playable** — `site/fantastica.html` + `site/fantastica.js`, driven by `data/fantastica.json` plus all three harvested systems. Bruno's side: compose an image (operator→memory, atrium→intellect, court→will) and the triple decides the species. Full dialectic verified E→I→R→E. **`SCHOLARLY_RECONSTRUCTION`, confidence LOW** — components attested, wiring ours.
- **The Art Engine is live and playable** — `site/engine.html` + `site/engine.js`, driven by `data/figure_s.json` and `data/engine_questions.json`. Llull's Figure S as a working state machine; the predestination/free-will dialectic plays end to end, E → I → R → E. **Attribution: Llull's, not Bruno's** (settled, HARVEST H-08).
- **Planetary image-courts live** — `scripts/harvest_images.py` → `data/images_harvested.json` → `site/images/courts.html`. 9 courts, 10 principal images, 239 attendants, extracted from *De imaginum*. Luna's retinue is split by phase.
- **Image alphabet live** — `scripts/harvest_alphabet.py` → `data/alphabet_harvested.json`. 16 simple keys + 7 cluster rows, 136 operators, 13 cross-references. This is the letter→image encoder that makes the atria address space usable for words.
- **Practice layer live** — `practices_seed.json` → 6 practices · 31 steps · 38 friction notes · 1 playable variant. Rendering verified in-browser.
- Portal seed: 21 works · 5 images · 11 scholars · 12 terms · 3 disputes · 9 events · 1 essay · 7 app-mode ideas · 13 bibliography.
- Corpus mapped: 24 files, 2,521 headings → `docs/CORPUS_MAP.md`.
- **Atria extracted from source**: `scripts/harvest_atria.py` → `data/atria_harvested.json`, all 24 atria × 24 positions = 576 loci.
- `docs/design/`: 17 proposal docs. The *frame*/*artifact* docs remain proposals; PRACTICES.md is now partly built.

## The architecture, as of H-08

**Llull computes with letters; Bruno computes with images** (*logica fantastica*, operating in the *spiritus phantasticus* — Mertens/Rossi). That single difference organises everything:

```
ENGINE   Llull's Figure S + dialectic          ← the reasoning machine (built, playable)
           ↓ Bruno swaps letter-variables for images
SUBSTRATE  atria (576 loci) · image alphabet (136 operators) · planetary courts (239 attendants)
```

The encoder is **not** a mnemonic half sitting beside the reasoning half — it is the substrate the reasoning runs on. That is why Bruno had to build an image vocabulary before he could compute with it.

**Built.** All four systems are now one machine, playable at `/fantastica.html`.

**Next, in order of value:**
1. **More questions.** The engine has exactly one (predestination/free will). It is the architecture proving itself; it is not yet a body of content. Bonner's worked examples and Bruno's own dialogues are the source.
2. **Harvest Figures A / T / V / X** (Bonner 227–1600) so the combinatorial half has real material rather than a single scripted dialectic.
3. **H-05** — ch.12's second image layer, position-mapped in prose for a dozen atria (Higgins 2255–2300).
4. **H-06** — the parallel planetary atrium series carrying the months (Higgins ~2839), which may link atria to courts.

**Open threads (HARVEST.md H-05, H-06):** ch.12 gives a *second* image layer position-mapped in prose for a dozen atria (lines 2255–2300) — partially answers H-01's caveat, not yet modelled. And `[X.] ATRIUM OF MERCURY` (line 2839) is a parallel planetary atrium series whose cells carry the **months**, suggesting a second calendrical indexing that may link the atria to the courts. Also unharvested: the 1591-vs-Tocco plate variant.
