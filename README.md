# BRUNOMEMAPP

### 🜍 **[Open the site → t3dy.github.io/BRUNOMEMAPP](https://t3dy.github.io/BRUNOMEMAPP/)**

A research laboratory and playable reconstruction of the Renaissance arts of memory — Giordano Bruno's image systems, and the Lullian combinatorial Art he inherited them from.

Built from a corpus of primary translations and scholarship. Every claim carries a locator back to the text it came from, and where the evidence stops, the page says so.

---

## What's in it

**Two working instruments**

| | |
|---|---|
| **[The Art Engine](https://t3dy.github.io/BRUNOMEMAPP/engine.html)** | Llull's Figure S as a live state machine. Take the contradiction between predestination and free will through all four figures — affirmation, denial, doubt, resolution — and watch the soul-state move `E → I → R → E`. Confusion is a real, reachable state; escaping it is the point. |
| **[Logica Fantastica](https://t3dy.github.io/BRUNOMEMAPP/fantastica.html)** | The same dialectic run on **images** rather than letters, which is what Bruno's version requires. Compose an image — memory from the alphabet, intellect from the atria, will from the planetary courts — and the triple decides where your soul-state lands. |

**Six operable practices**, each step-by-step with per-step notes on where the Renaissance worldview and the practical interface diverge from a modern reader's expectations: Bruno's Atria (576 addressable loci), Bruno's Image Alphabet, the Thirty Statues, the classical art of places and agent images, Quintilian's sceptical version, and the Ramist objection to the whole enterprise.

**A knowledge portal** — works, images, scholars, disputes, a timeline, a dictionary, and the planetary image-courts extracted from *De imaginum*.

**[17 design documents](https://t3dy.github.io/BRUNOMEMAPP/designs.html)** — the working record of what this project decided and why, including where a later reading overturned an earlier one.

## Three findings worth the visit

**Bruno's art of memory is not a memory palace.** The *Lampas* "statues" are conceptual organising figures — the Statue of Venus is the *topic* of concordance-according-to-will, subdivided into thirty notions. The system generates and orders **concepts**: closer to rhetorical *inventio* (finding what to say) than to mnemonics (retaining what was said).

**Llull computes with letters; Bruno computes with images.** Bruno's version is a *logica fantastica* operating in the *spiritus phantasticus*. That single difference explains why he had to build an image vocabulary — the atria, the alphabet, the courts — before he could reason with it at all. They are not a mnemonic half bolted onto a reasoning half; they are the substrate the reasoning runs on.

**The image alphabet is a workforce.** Every letter carries a small cast of Latin agent-nouns — *Baptizans* (one baptizing), *Bellator* (warrior), *Bibliopola* (bookseller). Not objects but occupations, because a trade specifies a person *plus* an action *plus* its props, and an image must act to hold attention.

## Honesty machinery

The project's main risk is producing a complete-looking system that is substantially its own invention. Countermeasures, all visible on the site:

- **Operability is graded.** `FULLY_OPERABLE` (every step in the source) · `PARTIALLY_OPERABLE` (core specified, gaps marked) · `REFERENCE_ONLY` (named but not specified). Missing steps are never invented to fill a grade.
- **Attestation per step.** `ATTESTED` · `RECONSTRUCTED` · `SPECULATIVE`, with a source locator.
- **Grounding per record.** `CORPUS_GROUNDED` vs `LLM_GENERAL_KNOWLEDGE`; the latter is capped at medium confidence.
- **Damaged source cells are flagged, not repaired.** Eight garbled entries in the image alphabet are marked and excluded from play rather than silently guessed at.
- **Reconstructions state their own limits.** Logica Fantastica prints its attested/reconstructed split in two columns.
- **Every practice step carries at least one friction note** — enforced by a check in the seed loader.

Corrections made during the build are recorded rather than overwritten. Two examples: all 24 atria are transcribed, not 12 (the plates carry two each, and only the odd ones are headed); and the soul-state engine is **Llull's, not Bruno's** — Bruno took the combinatorics and the *similitudo*-logic, not Figure S.

## Rights

Excerpts from in-copyright translations (Dick Higgins's *On the Composition of Images*; Anthony Bonner's *The Art and Logic of Ramon Llull*) appear as short attributed quotations for scholarly comment, alongside structural inventories — names, positions, retinue lists — which are data rather than expression. Consult the published editions for the full texts. The source corpus itself is not redistributed here.

## Build

No frameworks, no build step, no runtime dependencies. Python 3 and a browser.

```bash
python scripts/init_db.py         # idempotent schema -> db/bruno.db
python scripts/seed_from_json.py  # seed JSON -> database
python scripts/build_site.py      # database -> site/ (static HTML)
```

Then open `site/index.html`, or serve the folder:

```bash
python -m http.server --directory site 8000
```

### Corpus harvesters

These read a local corpus of plain-text sources (not included) and emit structured JSON:

```bash
python scripts/corpus_map.py       # line-addressed index of the corpus
python scripts/harvest_atria.py    # 24 atria x 24 positions = 576 loci
python scripts/harvest_alphabet.py # 16 letter-keys + 7 cluster rows
python scripts/harvest_images.py   # 9 planetary courts, 239 attendants
```

## Repository layout

```
site/                 built static site (deployed to GitHub Pages)
scripts/              build pipeline and corpus harvesters
data/                 harvested JSON: atria, alphabet, courts, Figure S
docs/design/          17 design documents
docs/WORKING_LOOP.md  the agentic working procedure
PROMPTS.md            the running record of project intent
HARVEST.md            what re-reading the sources turned up, with locators
CLAUDE.md             entry point and routing for coding sessions
```

## Documentation

- **[docs/design/README.md](docs/design/README.md)** — index of the design set; start with `ENGINE.md`
- **[docs/design/ENGINE.md](docs/design/ENGINE.md)** — the soul-state engine and the Llull/Bruno attribution
- **[docs/design/PRACTICES.md](docs/design/PRACTICES.md)** — the practice/friction/scholarship layering
- **[docs/design/ARCHITECTURE.md](docs/design/ARCHITECTURE.md)** — data model, provenance ladder, testability tiers
- **[docs/WORKING_LOOP.md](docs/WORKING_LOOP.md)** — progressive-revelation rules for corpus work
- **[HARVEST.md](HARVEST.md)** — findings with source line ranges

## Status

A research sandbox, not a settled account of Bruno's work. The engine currently carries one worked question; the architecture is proven, the body of content is not yet built out.
