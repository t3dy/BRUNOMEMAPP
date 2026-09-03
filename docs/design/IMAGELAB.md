# Artifact: THE IMAGE LAB

**Type:** artifact · **Primary texts:** *De imaginum, signorum et idearum compositione* (1591), *De umbris idearum* (1582) · **Frames:** Yates, Clucas, Wang, Mertens, Couliano

---

## 1. The shift this artifact has to embody

The most important change in recent Bruno scholarship is from *what does the image represent?* to **what operation is the image designed to perform?** An Image Lab organised around iconography would be building the superseded question into the interface.

So the primary field is not "what this depicts." It is `what_it_does` — already correctly present in the schema, currently populated on 5 rows.

## 2. Composite construction

Bruno's images are composites. The lab needs a **component vocabulary**, not a gallery of finished images:

| Layer | Examples |
|---|---|
| person | mythological figure, type, profession |
| animal | horse, ass, stag |
| object | instrument, attribute |
| action | the verb the figure is caught mid-performing |
| location | locus, architectural position |
| planet | the seven |
| attribute | quality, virtue, vice |
| emotion | the affective charge |
| colour / number / letter / syllable | the combinatorial hooks |
| concept | what the composite is *for* |

The user assembles across layers; the result is a **serialisable data structure**, inspectable as such. Bruno's images are supposed to be intersections of multiplicities — the data structure is not a technical convenience, it is the thing the images actually are.

**This vocabulary is shared with the Cabala engine** (`bruno_attested`), which is why CABALA.md defers to this doc. Build it once.

## 3. Why the images are strange — build for that

Bruno's figures are grotesque, erotic, violent, comic, emotionally overloaded. If memorisation were the goal, plain pictures would serve. The strangeness is functional: it seizes attention (Plotinus: memory follows attention), and it lets one image carry many relations at once — a word, a syllable, a myth, a planet, a moral quality, a position in a hierarchy.

Design consequences:

- The lab must **let composites be strange.** A tasteful component palette would defeat the purpose.
- Every composite should display its **relational load** — how many distinct relations it carries — because that, not prettiness, is the Brunian quality metric.
- Do not render images as pictures only. Render the structure alongside.

## 4. Frames on this artifact

| Frame | The image is |
|---|---|
| **Yates** | a talismanic instrument; planetary components foregrounded (T3, no output) |
| **Clucas** | an instrument for ordering the soul; the relational ladder matters most |
| **Wang** | an iconic form becoming a schema; supports the drop-the-scaffold test |
| **Mertens** | a *simulacrum* regulating cognitive spirits |
| **Couliano** | a bond-former; **reflexive use only** — see COULIANO.md |
| Sturlese / Barenstein | ○ no strong documented reading of image *composition* specifically |

Two empty cells. Per ARCHITECTURE.md §6, show them: the deflationary frames have much to say about the wheel's mechanism and comparatively little about why the images look the way they do. That asymmetry is itself informative about the shape of the field.

## 5. Data requirements

- **Component vocabulary** across all layers, attested. Currently 5 whole-image rows and no components at all. This is the largest single content gap in the project.
- `concept_relations` — shared prerequisite with CLUCAS/WHEEL/FRENZIES.
- Attested composites from *De imaginum* to seed the palette and serve as worked examples.
- Which woodcuts survive, and their rights status, if images are ever displayed rather than described.

## 6. Honesty constraints

- Distinguish **attested components** (Bruno used this) from **plausible components** (fits the system) from **user inventions**. The `reconstruction_level` field already exists; use all four values here rather than the two currently in play.
- A user-built composite is `USER_AUTHORED` and must never render as though it were attested.
- Where Bruno does not specify how a component contributes, say so — Wang's point that the mediation is never fully theorised applies directly.

## 7. Build phases

1. Component vocabulary as data.
2. Assembly UI; serialise composites.
3. Structure view — relational load, component provenance.
4. Frame overlays (what this image *does*, per frame).
5. Feed composites into the wheel as encoding images.
6. Feed the vocabulary into the Cabala engine.

## 8. Open questions

- What is the actual attested component inventory? Needs *De imaginum* from the corpus.
- Does Bruno give composition *rules*, or only examples? Determines whether the lab can validate a composite or merely record it.
- Are the woodcuts reproducible, and under what terms?
