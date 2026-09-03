# Frame: CLUCAS

**Type:** interpretive frame · **Attributed to:** Stephen Clucas · **Artifacts:** Wheel, Image Lab, Seals, Vincula, Frenzies

> **Provenance warning.** `LLM_GENERAL_KNOWLEDGE`. See ARCHITECTURE.md §4.

---

## Stance in one line

Bruno's mnemonic art is simultaneously logic, ethics and magic: it exists to order all the operations of the soul — intellect *and* appetite — not to store information.

## The triple

| | |
|---|---|
| **Mechanism** | Inherits Sturlese's corrected wheel unchanged. |
| **Output** | An encoding *plus* a traversable relational path from the image toward the unity it participates in. |
| **Success criterion** | Reordering of the operator's attention and appetite. |
| **Testability** | **T2 — self-report only.** With one partial T1 handle; see below. |

## Why this is the most important frame in the portal

It is the one that dissolves the binary the whole project is organised against. Clucas accepts the philological correction and still refuses the conclusion that Bruno was doing "sophisticated ordinary memory training." His formulation — memory art = logic + ethics + magic — makes *magic* mean the efficacy of images and the bonds they establish, rather than astral force transmission. That is what lets the portal hold Yates's insight without Yates's mechanism.

The Plotinian grounding is the load-bearing part: if memory is an active power of soul rather than passive storage (Ennead IV.6), then training memory *is* transforming the soul, and the ethical claim stops being a bolt-on. The essay already in the seed (`plotinus-bruno-memory`) is the long form of this and should be the frame's primary reading.

## The vulnerability worth naming

**If "ordering the operations of the soul" has no operational criterion, this frame is unfalsifiable** — and a portal that scores it anyway would be doing exactly what it forbids. So:

- Under this frame the app **asks** rather than measures. Prompts before and after a session about what the operator noticed themselves attending to, wanting, avoiding.
- Responses are stored and handed back verbatim. Never aggregated into a score. Never charted.
- The frame's own honest self-description appears in the UI: *this criterion is not measurable here; what follows is your report, not a result.*

That is the T2 register from ARCHITECTURE.md §3, and Clucas is its principal test case.

**The partial T1 handle:** Clucas's claim entails that a Brunian image carries *relations* — horse → motion → animal soul → terrestrial life → multiplicity → unity — not just a label. Whether a user can traverse those relations from the image is testable as a structured recall task, distinct from recalling the target word. That does not measure ethical transformation, but it does measure whether the image is functioning relationally rather than as a hook. Worth building; worth labelling precisely as the narrow thing it is.

## Interactive behaviour

- Corrected wheel geometry, identical to Sturlese. Switcher message: **"The wheel has not changed. What you are being asked to notice has."** This single message is the clearest expression of the project's thesis.
- Each generated image exposes a **relational ladder** — the chain from particular image up toward unity — built from `concepts` and their links, with primary passages attached at each rung.
- Pre/post attention-and-appetite prompts (T2, unscored).
- Optional relational-traversal task (partial T1, clearly separated from the T2 material).

## Reading Bruno whole

Clucas insists the mnemonic treatises cannot be separated from *Spaccio* and *Eroici furori* — the Italian dialogues dramatise as narrative what the technical works try to make method. The portal should honour this: under this frame, FRENZIES and the wheel are the same project in two registers, and the UI should cross-link them rather than filing them in separate sections. See FRENZIES.md.

## Primary texts

- *De umbris idearum* — the "higher art ordering the operations of the soul, including appetition" passage is the keystone; **locate and cite it exactly**
- *De imaginum, signorum et idearum compositione* (1591)
- *De gli eroici furori* (1585), *Spaccio* (1584)
- Clucas, "Amorem, artem, magiam, mathesim" (1999); "Simulacra et Signacula" in Gatti ed. (2002)

## Disputes

- `esoteric-vs-nonesoteric-interpretation` — the synthetic pole, against Barenstein
- `plotinus-vs-aristotle-psychological-source` — Clucas as the strong-Plotinus position

## Build notes

- References Sturlese's `mechanism_spec`; does not duplicate it.
- The relational ladder needs `concepts` to be linked to each other, which the current schema does not support. Requires a `concept_relations` table (`from`, `to`, `relation_type`, `evidence_passage`). This is a prerequisite, and it is also what the Memory Palace and Image Lab will need.

## To verify in corpus

- **The exact "operations of the soul / appetition" passage** in *De umbris*. Load-bearing for the whole frame.
- Does Clucas give any operational criterion, or strictly a descriptive one? Determines whether the T2 handling above is generous or merely accurate.
- How far does Clucas actually push the Plotinus claim, versus how far the seed essay pushes it? The essay's final synthesis section is explicitly flagged as going beyond Clucas — keep that flag.
