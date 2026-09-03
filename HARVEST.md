# HARVEST.md — playable material found in the corpus

**Purpose (PROMPTS.md P-08).** A running record of what re-reading the primary texts turned up that is *fun to play with*. Every entry carries a locator so nobody re-reads the same range.

**How to add an entry:** follow `docs/WORKING_LOOP.md` S1→S2. Locate with `CORPUS_MAP.md` + `grep -n`, read the slice, record it here with file + line range. Then model it into the seed at S3.

**Status key:** `FOUND` (recorded, not yet modelled) · `MODELLED` (in the seed) · `BUILT` (operable on the site)

---

## Ranges read so far

| File | Lines | What's there | Status |
|---|---|---|---|
| `thirty statues…txt` | 1–60 | Prologue; species of investigation | FOUND |
| `thirty statues…txt` | 4078–4130 | Statue of Venus | **BUILT** |
| `thirty statues…txt` | 4671–4760 | Applications; Scale of Nature (30 degrees) | **BUILT** |
| `…Higgins On the Composition of Images…txt` | 1257–1400 | **Atria system** — form, 24 names, adjective places | **BUILT** |
| `…Higgins…txt` | 3590–4935 | **Planetary image-courts** — 9 courts, 239 attendants | **BUILT** |
| `…Higgins…txt` | 1373–1997 | All 24 atrium diagrams (12 plates × 2) | **BUILT** |
| `…Higgins…txt` | 2255–2300 | Ch.12 sensible images (centre/E/W/S/N per atrium) | FOUND |
| `…Higgins…txt` | 2311–2341 | **Image alphabet** — operator catalogue + clusters | **BUILT** |
| `…Higgins…txt` | 2800–2845 | Second, planetary atrium series (months + maritime) | FOUND |
| `Anthony Bonner…User s Guide…txt` | 1579–1680 | **Figure S** — the soul-state table | **MODELLED** |
| `Anthony Bonner…User s Guide…txt` | 1866–1935 | **The dialectic** — worked example, 4 figures of X | **MODELLED** |
| `Anthony Bonner…User s Guide…txt` | 2846–2856 | Bonner on the aim of the Art | **BUILT** |
| `…Blum…An Introduction…txt` | 885–952 | Bruno recasts Llull in Aristotelian terms | **BUILT** |
| `…Mertens Magic And Memory…txt` | 866–893 | *logica fantastica*; similitudo-logic | **BUILT** |

---

## H-01 · The Atria system ★★★ — fully operable loci architecture

**Source:** Higgins trans., *On the Composition of Images, Signs and Ideas* (*De imaginum*, 1591), Bk I Pt 2 chs 3–6 · lines **1257–1400**

**What it is.** A complete, specified memory-place architecture — not a reconstruction.

- **Atrium form.** Quadrangular; centre is "the earth and the eye." Four corners E/W/N/S; four mid-side points also E/W/N/S → **8 points**, each with right + left collaterals → **24 positions**.
- **24 atria**, "after the number of the twenty four elements": altar, basilica, prison, house, colt, fountain, sword, horoscope, fire, yoke, lantern, table, nest, sheepfold, food, four-horse chariot, net, mirror, hot springs, carriage, gate, Pythagorean fork, gift, key of jealousy.
- **Nesting.** Atria names distribute *into* each atrium (altar at the Altar's east corner, colt at its west, image at its south, sheepfold at the fourth) → **24 × 24 = 576 addressable loci**.
- **Substantive vs adjective places.** Substantive = the angles/spaces themselves. Adjective = what animates the occupant (alive/dead, moving/moved) — "so that it brings an image or form to life."
- **Full adjective inventory for the Altar:** E angle water flowing / r. plow / l. chain · W angle tree / r. ram / l. banquet · S angle horse / r. anchor / l. chariot · N angle prison / r. giant / l. goat · E side ewer / r. young man / l. amphora · W side oven / r. fork / l. consuming fire · S side smoke / r. fruit / l. stable · N side desk / r. skiff / l. throne.
- **Diagram transcription** (line ~1367) lists: Palm, Bath, Water, Anchor, Breastplate, Plow, Chariot, Amphora, Chain, Stable, Desk, Fruit, Skiff, **ALTAR** (centre), Smoke, Throne, Prison, Oven, Tree, Jar, Sword, Globe, Stool, Fire, Banquet, Pool.

**Why it's playable.** A user can be given a real address space and place real content in it. This is the single most operable thing found in the Bruno corpus.

**Variant already visible:** the text marks **two** atrium diagrams — "1591 version" and "Tocco's version." Per P-07 that is a playable variant, not a footnote.

**Operability settled → all 24 atria transcribed.**

> ⚠️ **Correction (2026-09-02).** An earlier pass here recorded "12 of 24 transcribed — only the odd-numbered ones." **That was wrong.** Higgins *heads* only the 12 odd-numbered atria, but each plate transcribes **two**: the headed one and the following even-numbered one, unheaded. Caught by extracting the cells rather than trusting the headings. Logged per WORKING_LOOP §Standing checks — contradicting what the portal says is the highest-priority find.

Each plate is 52 lines and holds 50 diagram cells = **two atria of 25 cells each** (24 positions + centre). Centres are ALL-CAPS and reproduce the ch.4 canonical list exactly, in order — an independent cross-check on both the list and the extraction.

| plate | line | headed (odd) | unheaded (even) |
|---|---:|---|---|
| I | 1373 | ALTAR | BASILICA |
| III | 1425 | PRISON | HOUSE |
| V | 1477 | COLT | FOUNTAIN |
| VII | 1529 | SWORD | HOROSCOPE |
| IX | 1581 | FIRE | YOKE |
| XI | 1633 | LANTERN | TABLE |
| XIII | 1685 | NEST | SHEEPFOLD |
| XV | 1737 | FOOD | FOUR HORSE CHARIOT |
| XVII | 1789 | NET | MIRROR |
| XIX | 1841 | HOT SPRINGS | CARRIAGE |
| XXI | 1893 | GATE | PYTHAGORAS' FORK |
| XXIII | 1945 | *(gift — caps marker absent)* | KEY OF JEALOUSY |

**Extracted:** `scripts/harvest_atria.py` → `data/atria_harvested.json`. 24 atria × 24 positions = **576 loci**.

**The distinction that must survive into the build.** *Inventory* is `ATTESTED` for all 24. *Position mapping* is `ATTESTED` only for the **Altar**, where ch.6 gives position→item in prose (E angle water / r. plow / l. chain …). For atria 2–24 the cell order is a 2-D plate flattened into a text column, so the mapping is `RECONSTRUCTED` and may not be geometrically faithful. Do not render atria 2–24 as though their positions were certain.

Also spotted: `[X.] ATRIUM OF MERCURY` at line 2839 — a *different* atrium series (planetary?) not in the 24-element list. Unresolved; worth a look.

---

## H-02 · The planetary image-courts ★★★ — Image Lab vocabulary from source  ·  **BUILT**

**Source:** Higgins trans. · lines **3590–4935** · extracted by `scripts/harvest_images.py` → `data/images_harvested.json`

> ⚠️ **Correction (2026-09-02).** An earlier pass called this "a gallery of named images." **It is not a flat list.** It is organised as **planetary courts**: each deity has a principal image (often charioted) plus a named retinue of personified attendants. Missing that structure would have produced a shapeless bag of images instead of a system.

**9 courts** — Jove, Saturn, Mars, Mercury, Sun/Apollo, Luna, Venus, Tellus, Pluto — with **10 principal images** and **239 attendants**.

**The retinues are astrologically exact**, which is the finding that makes this usable:

| Court | Retinue |
|---|---|
| **Saturn** | old Antiquity, defective Decrepitude, Weariness, Lassitude, Slowness, Exhaustion, Maceration, Decay, Disease… plus named images: Grief, Care, Fear, Doubt, Hunger, Envy, Death, Orcus, Poverty — **the melancholic afflictions** |
| **Mercury** | Edition, Prolation, Nudation, Detection, Vulgation, Signification, Manifestation, Dissemination, Revelation — **disclosure and speech** |
| **Venus** | Sweet Unanimity, peaceful Agreement, gentle Will, Union of Hearts, Joy of the Breast, concordant Conformity — **concord** |
| **Tellus** | Conception, Gestation, Fertility, Generation, Birth, Nursing, Feeding, Cherishing — **generation** |
| **Luna** | split **by phase**: base retinue (nocturnal Silence, starry Crown, silvery Gleam, rosy Calm, tawny Pallor); *waxing* (Growth, Amplification, Swelling, Maturing — 34 items); *waning and changing* |

**Why it's playable.** This is Bruno's own attested component vocabulary, not an invented palette — exactly the layered structure IMAGELAB.md specifies. Two mechanics fall straight out:

1. **Pick a planet, get its retinue.** The court is a themed component set with a coherent affective register.
2. **Luna changes with phase.** A practice whose available components depend on the state of the moon is Bruno's own design, not a bolt-on.

It is also prime friction material: a modern user asking why an image needs a planetary attribution meets a correspondence cosmology in which Saturn *is* melancholy, and the retinue is the argument.

**Rendered:** `site/images/courts.html`.

**Caveat carried into the site.** Retinue lists are parsed from running prose, so occasional fragments survive the extraction. Excerpts are brief and attributed (Higgins translation).

---

## H-03 · Bruno's art of memory is not "memory palace" ★★ — the key friction  ·  **BUILT**

**Source:** `thirty statues…txt` lines 4078–4130, 4671–4760

**What it is.** The *Lampas* "statues" are **not** vivid images for recalling a list. The Statue of Venus is the *topic* of concordance-according-to-will, subdivided into thirty numbered notions (aptitude, facility, compliance, complacence, delectation, adoption, consensus…). The accompanying "Scale of Nature" is a 30-degree metaphysical ladder from vacuum/shadow/matter/atom upward.

**Why it matters.** The system generates and orders **concepts** — closer to rhetorical *inventio* (finding what to say) than to mnemonics (retaining what was said). A user arriving for shopping-list tricks meets the scale of nature instead.

**This is the first friction note the user should ever see** (PRACTICES.md §5). It is a genuine historical gap, not an interface failure, and naming it early makes the rest of Bruno legible.

---

## H-04 · The image alphabet ★★★ — the letter→image encoder  ·  **BUILT**

**Source:** Higgins trans., Bk I Pt 2 chs 12–13 · lines **2311–2341** · extracted by `scripts/harvest_alphabet.py` → `data/alphabet_harvested.json`

**The missing piece.** The atria give an address space; this gives something to store in it. Every initial letter and consonant cluster carries a small cast of Latin **agent-nouns** — "operators", people named by what they do.

- **16 simple keys** (B, C, D, F, G, H, I, L, M, N, P, Q, R, S, T, V), ~5 operators each: B → *Baptizans* (one baptizing), *Bellator* (warrior), *Bibliopola* (bookseller), *Boarius* (cattle-dealer), *Buccinator* (trumpeter).
- **7 cluster rows** (Bl/Br, Cl/Cr, Fl/Fr, Gl/Gr, Pl/Pr, Sc/St/Str, Tr).
- **136 operators, 13 cross-references, 8 damaged cells** flagged rather than repaired.

**Two findings worth keeping.**

1. **The alphabet is a workforce.** Not objects, not animals — occupations. A trumpeter arrives already blowing a trumpet; a gravedigger already digging. A trade is the most compact way to specify a person *plus* an action *plus* its props, and an image must act to hold attention. This is the affective-shock principle of the classical *imagines agentes*, systematised into a lookup table.
2. **Cross-references reveal the system encodes sound, not spelling.** `*Ble as Ple` means Ble borrows Ple's image. Bruno spends one image on two phonetically close clusters, accepting ambiguity for a smaller set to memorise — a trade a machine would refuse and a practitioner will happily make.

**Honest edge.** Ch.13 closes: each operator "receives the six differences which are sought in the six double triangles of the minor chambers." The six are **not enumerated here**, so the inflection step is `RECONSTRUCTED` and the practice runs at a sixth of its stated capacity. Joining the alphabet to the atria is likewise obvious but unstated — also marked.

**Rendered:** `site/practices/bruno-image-alphabet.html`.

---

## H-05 · Chapter 12's second image layer — position-mapped, many atria  ·  FOUND

**Source:** Higgins trans., Bk I Pt 2 ch 12 · lines **2255–2300**

"An explication of the sensible images, first by the action of other accompanying things." For each atrium in turn it gives **centre / east / west / south / north**: *"in the first atrium in the centre, someone removing or setting free; in the east, a drunkard; in the west, an ibis; in the south, a barrier; in the north, the sign of ubiquity."* Runs I–XIII+, with some entries noting "south and north are vacant."

**Why this matters.** It is a *second* image layer over the atria, and it is **position-specified in prose for a dozen atria**, not just the Altar. It partially answers the caveat in H-01 — though only for 5 of the 24 positions. Not yet modelled.

---

## H-06 · A second, planetary atrium series — unresolved  ·  FOUND

**Source:** Higgins trans. · line **2839**, `[X.] ATRIUM OF MERCURY`

Numbered X, but atrium 10 in the 24-element list is *yoke*, so this is a **parallel series keyed to planets rather than to the alphabet**. Its cells mix maritime imagery (Arion, Scylla, Charybdis, Sirens, Triton, Proteus) with the **months** (June through December).

This is where the atria and the planetary courts (H-02) may join. Unresolved and worth pursuing — it suggests the address space has a second, calendrical indexing.

---

## H-07 · Figure S and the aim of the Art ★★★★ — **the reframe**  ·  MODELLED

**Source:** Bonner, *The Art and Logic of Ramon Llull: A User's Guide* · lines **1579–1680, 1866–1935, 2846–2856** → `data/figure_s.json`, `docs/design/ENGINE.md`

**Llull's Art is not a mnemonic.** Bonner's worked example is Llull resolving *predestination vs. free will* in four "figures of X". Letters are variables: `S in E I N R, with T in X enters the compartment of perfect wisdom.`

**And its output is a change in the operator.** Bonner on the aim: to get *"the S of the user"* to remember, understand and love the true, and remember, understand and hate the false — the remaining states being unreliable belief (N) or confusion (R).

**Figure S**, a 4×3 table of the *acts* of memory/intellect/will (Bonner: "dynamic and combinatory"):

| | memory | intellect | will | |
|---|---|---|---|---|
| **E** | B remembering | C understanding | D loving | informed acceptance — goal |
| **I** | F remembering | G understanding | H hating | informed rejection — **also a goal** |
| **N** | K forgetting | L not knowing | M loving *or* hating | supposition / credulity |
| **R** | O | P | Q | **confusion — stuck state** |

**The dialectic:** affirmation (E) → denial (I) → doubt (R) → resolution (E). Stage 4 does not pick a horn; it re-enters the dignities and affirms both at a higher level.

**Why this reframes the project.** I had filed Clucas's "ordering the operations of the soul, including appetite" as **T2 — self-report, possibly unfalsifiable** (CLUCAS.md). Llull *notates* it. Confusion is named and reachable; the escape is a specified procedure. Clucas's reading has a concrete mechanical ancestor, and it can be built without inventing anything. That turns the most interesting scholarly claim in the project from describable into operable.

**Caveat on the data.** `figure_s.json` is `HAND_TRANSCRIBED` — Bonner's chart is a 4×3 grid mangled into an ASCII column by the extraction and cannot be parsed reliably. Flagged in the file; verify against the printed chart.

**RESOLVED 2026-09-02 → see H-08.** Bruno did *not* take Figure S. The engine ships as Llull's.

---

## H-08 · Whose art is it? ★★★★ — attribution settled  ·  **BUILT**

**Sources:** Blum, *Giordano Bruno: An Introduction* lines 885–952 · Mertens, *Magic and Memory* lines 866–893

**Verdict: Bruno took Llull's combinatorics and *similitudo*-logic, not Figure S.**

- Blum: *De compendiosa architectura et complemento artis Lullii* "begins… in an entirely scholarly manner with the four Aristotelian causes"; Bruno was "eager to translate also this logic to the language of the Aristotelian scholarly philosophy."
- Mertens: what returns in Bruno is "logic through similarities" — *principia essendi et cognoscendi* the same, the ladder of being climbed and descended through *similitudines*.
- Neither mentions the four species or the soul-state notation. Bonner mentions Bruno only twice, for the cosmological use.

**Correction:** I claimed *De compendiosa architectura* was on disk. **It is not** — no copy in the corpus. Settled from secondaries instead.

**The better find.** Mertens names Bruno's own version: **"fantastic logic"** (Rossi, *"La logica fantastica di Giordano Bruno"*), operating in the ***spiritus phantasticus***.

**Llull computes with letters; Bruno computes with images.** That is why Bruno must first build an image vocabulary — the atria, the alphabet, the courts are not a separate mnemonic half but **the substrate his logic runs on**. This reframes the whole corpus as one machine rather than three exhibits.

**Built as `site/fantastica.html`** — memory from the alphabet, intellect from the atria, will from the courts. See ENGINE.md §5a.

---

## Queue — located but not yet read

| Target | Where to look | Why |
|---|---|---|
| Ch.12 sensible images (H-05) | Higgins 2255–2300 | second image layer, position-mapped |
| Second atrium series (H-06) | Higgins ~2700–2900 | may link atria to planetary courts |
| *De vinculis* text | Blackwell/de Lucca *Essays on Magic* | VINCULA.md is currently unsourced |
| *De magia* taxonomy | same | MERTENS frame mechanism |
| Figures A, T, V, X contents | Bonner 227–1600 | the combinable material |
| Quaternary vs ternary phase | Bonner, later chapters | which version of the Art to implement |
| Clucas, "Simulacra et Signacula" | Gatti ed. *Philosopher of the Renaissance* | upgrades CLUCAS.md off general knowledge |
| Mertens on memory/magic unity | Mertens *Magic and Memory* | upgrades MERTENS.md |
| Ass / asinine vocabulary | Sondergard/Sowell *Cabala*; Ordine *Philosophy of the Ass* | CABALA.md needs the attested comic register |
| De umbris wheel ring positions | **not on disk** — Sturlese ed. absent | blocks WHEEL.md; may be unresolvable locally |
