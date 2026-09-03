# Artifact: THE VINCULA BOARD

**Type:** artifact (structural, non-operational by design) · **Primary text:** *De vinculis in genere* (c. 1590–91) · **Frames:** Couliano (primary), Clucas, Mertens

---

## 1. What it is

A graph interface for the *vinculum* — the bond. Nodes are the parties and faculties Bruno's theory implicates: operator, image, attention, imagination, desire, emotion, *spiritus*, *species*, target, action. Edges are the links between them. The board renders the **anatomy of a bond as Bruno theorised it**.

Unlike every other artifact, this one is deliberately not operable toward its historical purpose. See §3.

## 2. Why it earns a place

*De vinculis in genere* is the most direct primary-source warrant of any frame in the portal. Where the wheel requires reconstruction and the seals require guesswork, this text is explicitly *about* the mechanism it describes. Couliano's reading is close to reportage.

It also supplies something no other artifact does: the **causal vocabulary** — *species*, *spiritus*, *vinculum* — by which Bruno's images were supposed to actually do anything. Without it, "magic" in the memory art has no stated mechanism. The board is where that vocabulary becomes inspectable.

## 3. The constraint that defines the build

Every other artifact targets the operator. This one, historically, targets someone else — and its success criterion is a change in another person's behaviour.

**A tool that helped a user construct and rehearse binding operations against a real named person would be a manipulation aid with a Renaissance skin.** Scholarly framing would not change what it was.

So:

- Nodes take **abstract or historical roles** — "the beloved," "the crowd," "the prince." Never a real named individual.
- **No output panel. No effectiveness score. No strategy, messaging, or approach advice.**
- If a user tries to instantiate the board against a specific real person, the tool declines and explains why.
- Fixed banner: **COULIANO-INSPIRED EXPERIMENTAL MODEL — this reconstructs a historical theory of binding. It does not tell you how to influence anyone.**

This is core logic, not copy — a later refactor must not be able to drop it.

**And the constraint is intellectually productive, not merely defensive.** Stripping the targeting leaves the structure, and the structure is the interesting object. The board is *more* legible as a theory of how imagination, desire and attention interlock when it is not also trying to be a procedure.

## 4. What is genuinely explorable

- **Bond anatomy.** Which faculty links to which; what carries influence; where a bond can be broken. All with primary passages attached per edge.
- **Reflexive mode — the strongest use.** Turn the mechanism on oneself: what binds *my* attention, and what does that pattern reveal about what I want? Honest, non-manipulative, and it converges with Clucas's ethical reading and with FRENZIES.md's rebound mechanic. This should be the default entry point.
- **Historical case reading.** Take an attested Brunian image and diagram the bonds it was theorised to establish. Pure scholarship, no operation.

## 5. Frames

| Frame | Reads the bond as |
|---|---|
| **Couliano** | psychological binding via *phantasia*, desire, attention. **Primary.** |
| **Clucas** | the "magic" third of logic+ethics+magic — efficacy of images and the bonds they establish |
| **Mertens** | continuous with spirit-regulation; bonds as forces acting on cognition |
| Yates / Sturlese / Wang / Barenstein | ○ no strong documented reading of the *vincula* |

The Couliano/Clucas overlap here is worth surfacing: both treat image-efficacy as real and non-astral, but Couliano's is erotic-psychological and Clucas's ethical-transformative. Whether these are the same claim in different registers is an open question the seed does not yet model — see COULIANO.md §Disputes.

## 6. Data requirements

- Bond taxonomy from *De vinculis*: kinds of bond, parties, faculties. **Currently zero rows.**
- `concept_relations` — shared prerequisite.
- `dictionary_terms` has `vinculum`, `spiritus`, `species`; needs their interrelation from source.
- Attested passages per edge.

## 7. Build phases

Scheduled **last** among artifacts. It is a graph renderer rather than a wheel variant, so it shares no machinery with WHEEL/IMAGELAB/CABALA, and the ethical design work deserves the benefit of the patterns established by everything before it.

1. Bond taxonomy as data — content-blocked on corpus.
2. Static anatomy view with passages per edge.
3. Reflexive mode (default entry).
4. Historical case reader.
5. Frame overlays.

## 8. Open questions

- **Does *De vinculis* itself set ethical limits on binding?** If Bruno does, quoting him in the banner would be far better than the portal's own disclaimer — his constraint, not ours.
- Is the psyche/world continuity thesis Couliano's, Bruno's, or this project's gloss?
- How does Couliano treat the mnemonic works specifically, as against Renaissance magic generally?
