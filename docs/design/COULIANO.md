# Frame: COULIANO

**Type:** interpretive frame · **Attributed to:** Ioan P. Couliano (*Eros and Magic in the Renaissance*, 1987) · **Artifacts:** Vincula, Image Lab, Frenzies, Seals

> **Provenance warning.** `LLM_GENERAL_KNOWLEDGE`. See ARCHITECTURE.md §4.

---

## Stance in one line

Magical efficacy is the manipulation of *phantasia*, desire and attention: an image establishes a *vinculum* — a bond — linking operator, imagination, desire, target and action.

## The triple

| | |
|---|---|
| **Mechanism** | Image → attention → desire → bond. Not a wheel operation; this frame lives on the Vincula board. |
| **Output** | A *vinculum*: a specified bond between parties. |
| **Success criterion** | Change in the bound party's behaviour. |
| **Testability** | **T3 — and deliberately left unbuilt. See below.** |

## Why this frame changes the question

Couliano's move is to stop asking whether the magician literally manipulates supernatural forces, and ask instead what is being done to imagination and desire. Because psyche, imagination, spirit and world are continuous in Bruno's own framework, manipulating one can affect the others — so the interpreter is not forced to choose between "mere psychology" and "real magic." The distinction that modern readers want to impose was not Bruno's.

This is the frame with the most direct primary-source warrant in the whole set: *De vinculis in genere* is entirely about this mechanism. Where other frames reconstruct, this one largely reports.

## The ethical design problem, stated plainly

Every other frame targets the operator. **This one targets someone else.** Its success criterion is a change in another person's behaviour, and the historical technique is explicitly a technique of attraction, persuasion and influence.

A tool that helped a user construct and rehearse psychological binding operations aimed at a named real person would be a manipulation aid with a Renaissance skin. The scholarly framing would not make it not that.

### The resolution

- **Model the structure; never operationalise it against a real target.**
- The Vincula board takes **abstract or historical roles** — "the beloved," "the crowd," "the prince" — never a real person the user names, and never contact details, messages, or approach strategies.
- **No output panel. No effectiveness score. No advice.** The board renders the *structure of the bond as Bruno theorised it*, with primary passages attached to each link.
- The banner is fixed: **COULIANO-INSPIRED EXPERIMENTAL MODEL — this reconstructs a historical theory of binding. It does not tell you how to influence anyone.**
- If a user tries to instantiate the board against a specific real individual, the tool declines and says why.

This is a design constraint, not a disclaimer. The refusal to build the "make it work on someone" affordance is what keeps the frame scholarly. And there is a real intellectual gain in the refusal: the structure is the interesting object, and stripping the targeting makes it *more* visible, not less.

## What remains genuinely explorable

- The **anatomy of a bond**: which faculty links to which, what carries the influence (*species*, *spiritus*), where the bond can be broken.
- **Self-directed application** — Couliano's mechanism turned reflexively. What binds *my own* attention, and what does that reveal about my desires? This is honest, is arguably closer to Clucas's ethical reading, and is where the frame overlaps productively with FRENZIES.md.
- **Historical case reading**: take an attested Brunian image and diagram which bonds it was theorised to establish.

## Primary texts

- *De vinculis in genere* (c. 1590–91) — the central text, and the strongest direct warrant of any frame in this set
- *De magia* — the *species* / *spiritus* causal vocabulary the bonds run on
- *De gli eroici furori* — eros and attention, read reflexively
- Couliano (1987)

## Disputes

- Not currently modelled in the seed. Two worth adding:
  - **Couliano vs. Clucas** — is the bond primarily psychological-erotic or ethical-transformative? They are compatible in principle; the emphases differ sharply.
  - **Couliano vs. Yates** — Couliano relocates efficacy from cosmos to psyche without deflating it, which is a third option the esoteric/non-esoteric axis does not capture. This is evidence the seed's single `esoteric-vs-nonesoteric` dispute is too coarse.

## Build notes

- Vincula is a graph artifact, not a wheel — different renderer, different data shape. Schedule it last of the artifacts.
- Needs `concept_relations` (see CLUCAS.md).
- The targeting refusal should live in the artifact's core logic, not in copy that a later refactor can drop.

## To verify in corpus

- Couliano's own framing of the psychological/supernatural relation — is the continuity thesis his, Bruno's, or the portal's gloss?
- Whether *De vinculis* itself sets ethical limits on binding, which would be directly relevant and worth quoting in the banner.
- How Couliano handles the mnemonic works specifically, as opposed to Renaissance magic generally.
