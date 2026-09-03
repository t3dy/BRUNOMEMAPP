# Frame: YATES

**Type:** interpretive frame · **Attributed to:** Frances A. Yates (1899–1981) · **Artifacts:** Wheel, Image Lab, Seals, Frenzies

> **Provenance warning.** Every scholarly characterisation in this document is `LLM_GENERAL_KNOWLEDGE` — written from model background knowledge, not from a page-cited reading of Yates. It must be checked against the corpus before any of it reaches the site at `confidence: HIGH`. See ARCHITECTURE.md §4.

---

## Stance in one line

Bruno's mnemonic images are Hermetic-magical instruments; the memory wheel, once internalised, functions as an inner talisman that conforms the operator's soul to celestial order.

## The triple

| | |
|---|---|
| **Mechanism** | Concentric rings including a planetary ring at the positions Yates reconstructed. The operator combines and internalises the composite figure. |
| **Output** | A talismanic inner image — a cosmic structure held in the imagination. |
| **Success criterion** | The operator's soul is brought into conformity with celestial order and receives astral influence. |
| **Testability** | **T3.** Not measurable in-app, by design. |

## Why this frame is indispensable even though its central claim failed

Yates is the reason Bruno's mnemonic writings are a scholarly subject at all. Her general insight — that the art of memory had become something far more ambitious than a technique for remembering speeches — survives the collapse of her specific reconstruction and is presupposed by every frame that followed. A portal that treats Yates as merely refuted would be reproducing the caricature it exists to prevent.

## The known vulnerability

Her reconstruction placed the planetary images incorrectly (per Sturlese 1991, extended by Torchia 1997). Because the talismanic reading depended on *those* positions producing *that* cosmic conformity, the specific mechanism does not survive. See STURLESE.md and `disputes/yates-vs-sturlese-torchia-planetary-placement`.

**The distinction that must stay visible:** the philological claim (where the planets go) is settled against Yates. The interpretive claim (whether Bruno's images do magical work) is not settled by that correction, and Clucas, Mertens and Couliano all continue to answer it affirmatively on other grounds. Yates lost a reconstruction, not the argument that Bruno's memory art is more than mnemonics.

## Interactive behaviour under this frame

- The wheel renders with the **Yates planetary ring positions**, visibly distinct from the corrected ring used by every other frame. This is the *only* frame where the artifact's geometry actually differs — the switcher should say so explicitly.
- A persistent banner: *"This reconstruction is superseded on philological grounds. You are operating it as a historical counterfactual."*
- **No output panel.** The operation is narrated as reconstruction and produces no score, no measurement, no simulated result. T3 discipline. The refusal to produce a number is itself the honest statement of what is and isn't known.
- Offer a one-click **"see the corrected wheel"** toggle so the user can watch the planetary ring move and understand exactly what Sturlese changed.

## Why keep it operable at all

Because it is genuinely fun, historically enormously consequential, and — as the brief puts it — a counterfactual magical practice worth playing with. The design does not need to pretend it is current scholarship in order to let the user run it. It needs to *label* it and refuse to fake its outputs. Those two moves make playing with a superseded reconstruction intellectually respectable rather than misleading.

## Primary texts leaned on

- *De umbris idearum* (1582) — the wheel
- *Cantus Circaeus* (1582) — the explicitly magical framing that most supports this reading
- Yates, *Giordano Bruno and the Hermetic Tradition* (1964); *The Art of Memory* (1966)

`Cantus Circaeus` is the strongest primary card in Yates's hand and the text any de-esotericising frame has to explain. Give it prominence under this frame.

## Disputes this frame is party to

- `yates-vs-sturlese-torchia-planetary-placement` — philological layer, **settled against**
- `esoteric-vs-nonesoteric-interpretation` — interpretive layer, **open**, Yates as the strong-esoteric pole

## Build notes

- Frame row: `mechanism_spec` must carry the Yates ring positions as actual data, not prose, so the wheel can render them.
- This is the only frame with `shares_mechanism_with = []`.
- Ship the side-by-side ring comparison early; it is the clearest single teaching moment in the whole portal.

## To verify in corpus

- Yates's actual ring assignments, precisely enough to render.
- Whether Yates ever qualifies the talismanic claim herself.
- The Warburg Institute's current published position, and where it is stated.
