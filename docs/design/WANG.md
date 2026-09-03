# Frame: WANG

**Type:** interpretive frame · **Attributed to:** Zheng Wang ("The Role of Iconic Practice in Bruno's Gnoseology," 2022) · **Artifacts:** Wheel, Image Lab, Frenzies

> **Provenance warning.** `LLM_GENERAL_KNOWLEDGE`. See ARCHITECTURE.md §4.

---

## Stance in one line

Bruno's image-making belongs to his theory of knowledge: *phantasia* is not a defective middleman between sense and intellect, and mnemonic practice turns shadows into iconic forms that carry the knower upward.

## The triple

| | |
|---|---|
| **Mechanism** | Inherits Sturlese's corrected wheel unchanged. |
| **Output** | An iconic form / mental schema — something the operator eventually thinks *with* rather than *about*. |
| **Success criterion** | The operator can hold the relation **after the image is removed**. |
| **Testability** | **T1 (partial) — the most surprising result in the project.** |

## The drop-the-scaffold test

This frame sounds like the most abstract of the seven and turns out to be among the most concretely testable, which is worth surfacing to the user as a finding in its own right.

Wang's claim is that the image is an instrument of knowing, not a container. The brief's own Plotinian endpoint states it sharply: *"You no longer need the image. You can see the relation directly."* If that is right, it predicts something checkable:

1. User encodes relational material via the wheel, with images.
2. Trials continue until performance is stable.
3. **The image scaffold is withdrawn.**
4. Re-test the relation without it.
5. Measure persistence, and time-to-independence across items.

A pure-hook model predicts collapse when the hook is removed. Wang's model predicts persistence. **That is a real discriminating prediction, running in a browser.**

Caveats to state in the UI: this tests whether the *reconstructed* practice produces scaffold-independent knowledge in *this* user. It does not establish what Bruno intended, and Wang's own point is that Bruno never gave a transparent account of how the images mediate. Do not let a good result get reported as vindication of a historical thesis.

## Wang's honest complication — keep it

Wang stresses that Bruno never fully explains how his occult images mediate between worlds; the woodcuts have to be read as practical realisations of a larger speculative system whose code has not been cracked. **This is a feature of the frame, not a gap to fill.** The portal should carry it forward as a standing caution against any interface that implies the system is solved. Where the reconstruction has to guess, the guess gets labelled `SPECULATIVE_IMPLEMENTATION`.

## Interactive behaviour

- Corrected wheel geometry; switcher notes the mechanism is unchanged from Sturlese and Clucas.
- Images render with an explicit **schema view**: the image, and separately the relational structure it encodes, toggleable.
- The scaffold-withdrawal harness (above) as a first-class mode, with per-item independence tracking.
- A visible "not fully theorised by Bruno" marker wherever the reconstruction is inferring mediation mechanics.

## Primary texts

- *De imaginum, signorum et idearum compositione* (1591) — the central text for this frame
- *De umbris idearum* — the shadows-into-iconic-forms move
- Wang (2022)

## Disputes

- `esoteric-vs-nonesoteric-interpretation` — Wang sits with the synthetic tendency (with Clucas and Mertens) rather than at either pole
- Bears on `plotinus-vs-aristotle-psychological-source` via the status of *phantasia*

## Build notes

- Reuse Sturlese's recall harness; scaffold-withdrawal is a parameter on it, not a separate build. This is why STURLESE ships first.
- Needs `concept_relations` (see CLUCAS.md) to have relations worth testing independence *of*.

## To verify in corpus

- **Does Wang commit to the strong claim** (image becomes dispensable) or only the weak one (image mediates)? The whole test rests on the strong reading; if Wang only holds the weak one, the test is this project's extrapolation and must be labelled as such rather than attributed to him.
- Wang's actual account of *phantasia*'s positive cognitive role.
- Which specific woodcuts Wang treats as practical realisations — candidates for `images` rows.
