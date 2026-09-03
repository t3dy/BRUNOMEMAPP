# BRUNOMEMAPP

### 🜍 **[Open the site → t3dy.github.io/BRUNOMEMAPP](https://t3dy.github.io/BRUNOMEMAPP/)**

A research laboratory and playable reconstruction of the Renaissance arts of memory — Giordano Bruno's image systems, and the Lullian combinatorial Art he inherited them from.

Built from a corpus of primary translations and scholarship. Every claim carries a locator back to the text it came from, and where the evidence stops, the page says so.

---

## What's in it

**Three working instruments**

| | |
|---|---|
| **[The Art Engine](https://t3dy.github.io/BRUNOMEMAPP/engine.html)** | Llull's Figure S as a live state machine. Take the contradiction between predestination and free will through all four figures — affirmation, denial, doubt, resolution — and watch the soul-state move `E → I → R → E`. Confusion is a real, reachable state; escaping it is the point. |
| **[Logica Fantastica](https://t3dy.github.io/BRUNOMEMAPP/fantastica.html)** | The same dialectic run on **images** rather than letters, which is what Bruno's version requires. Compose an image — memory from the alphabet, intellect from the atria, will from the planetary courts — and the triple decides where your soul-state lands. |
| **[The Figures](https://t3dy.github.io/BRUNOMEMAPP/gallery.html)** | Llull's and Bruno's diagrams rebuilt as manipulable SVG: the sixteen dignities as a complete graph (all 120 compartments), virtues and vices as two graphs that never touch, the soul as four inscribed squares, Bruno's atrium with every one of its 576 loci, and a combinatorial wheel you can turn. |

**Six operable practices**, each step-by-step with per-step notes on where the Renaissance worldview and the practical interface diverge from a modern reader's expectations: Bruno's Atria (576 addressable loci), Bruno's Image Alphabet, the Thirty Statues, the classical art of places and agent images, Quintilian's sceptical version, and the Ramist objection to the whole enterprise.

**A knowledge portal** — works, images, scholars, disputes, a timeline, a dictionary, and the planetary image-courts extracted from *De imaginum*.

**Fair-use scholarly quotation.** Short attributed quotations from Bonner, Mertens, Blum, Llull and Bruno appear beside the claims they support, each with a locator so it can be checked, and each with a note on *why* it is there. None is quoted from memory; all were read from the corpus while building the site.

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

## On the diagrams and plates

Two layers, kept distinct.

**[The Plates](https://t3dy.github.io/BRUNOMEMAPP/gallery.html#plates)** — 27 period woodcuts extracted from the corpus: Bruno's atrium in both the 1591 printing and Tocco's redrawing (side by side, so the textual variant is visible), the planetary chariots with their zodiacal houses on the wheels, the numeral table mapping Roman numerals to figures, emblems and lettered geometrical diagrams. Nine are captioned from reading the plate; the other eighteen are published with their source page and *not* named, because inferring their identity from position in the sequence would be a guess.

These are photographic reproductions of woodcuts printed 1585&ndash;1591. The underlying works are long out of copyright and a faithful reproduction of a flat public-domain artwork carries no new authorship. No editorial apparatus &mdash; translation, notes, typography, page design &mdash; is reproduced, and the edition each scan comes from is credited.

**The interactive figures** are **drawn from the harvested data, not photographed**. That is a deliberate choice and not a compromise: a scan of a wheel cannot be turned, and a scan of Figure A cannot tell you which compartment you just formed. It also sidesteps a rights problem — the underlying woodcuts are public domain, but the modern editions that reproduce them are not.

Three figures are **not** drawn, and the gallery says why: Llull's Figure T (vertex terms shredded by text extraction), the *De umbris* memory wheel (neither Bruno's text nor Sturlese's edition is in this corpus, and its ring positions are the field's most contested question), and the *Eroici furori* emblems (pictorial, so they must be reproduced photographically rather than rebuilt). Approximating any of them would produce exactly the plausible-looking invention the rest of the project exists to avoid.

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
