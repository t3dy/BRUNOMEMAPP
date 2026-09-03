# Frame: STURLESE (with Torchia)

**Type:** interpretive frame · **Attributed to:** Rita Sturlese (crit. ed. 1991), extended by Francesco Torchia (1997) · **Artifacts:** Wheel

> **Provenance warning.** `LLM_GENERAL_KNOWLEDGE`. The mechanism spec below is the single most important thing in this project to verify against the actual critical edition, because five other frames inherit it. See ARCHITECTURE.md §4.

---

## Stance in one line

Once the planetary images are correctly placed, the wheel is a combinatorial engine: consonant–vowel combination generates syllables, syllables attach to memorable images, and the practitioner builds recallable sequences from them.

## The triple

| | |
|---|---|
| **Mechanism** | Corrected ring positions. Consonant + vowel → syllable → attached image → combined into sequences. |
| **Output** | A syllable-image encoding of arbitrary target material. |
| **Success criterion** | Accurate recall of the encoded material. |
| **Testability** | **T1 — measurable.** |

## Why this frame anchors the whole build

**It is the only frame whose success criterion the software can actually check.** Everything in ARCHITECTURE.md §3 rests on that. If the corrected wheel is a working encoding machine, a browser can demonstrate it: encode real material, wait, test recall, compare against a control. No appeal to authority required.

That makes Sturlese the correct first implementation regardless of where one's sympathies lie interpretively. It is the frame that gives the portal a floor of hard results to stand on before it starts handling claims that cannot be scored.

## The mechanism is shared, the reading is not

Five frames — Barenstein, Clucas, Wang, Mertens and by extension most post-1991 work — operate this same mechanism. They diverge only on what the operation is *for*. The frame switcher must make this visible: switching from Sturlese to Clucas does not move a single ring.

This is also the corrective to the common misreading that Sturlese "de-magicked" Bruno. The correction establishes what the wheel *does mechanically*. It is silent on what the doing is for, and Clucas and Mertens fill that silence very differently from Barenstein.

## Interactive behaviour under this frame

- Corrected ring geometry (the default for the portal).
- The wheel is **operable end to end**: pick target material, rotate rings, generate syllable-image pairs, commit the encoding.
- **Full T1 output panel**: encoding time, immediate recall, delayed recall at spaced intervals, comparison against an unencoded control list.
- Results are the user's own data, stored locally, and comparable across sessions and across frames.

## The recall harness (spec sketch)

1. User supplies or picks target material (a word list, a sequence, a set of terms).
2. Wheel generates syllable-image encodings for each item.
3. User commits the pairings.
4. Immediate free-recall test → score.
5. Delayed tests at intervals (1h / 1d / 1w) → retention curve.
6. Control condition: equivalent material memorised without the wheel.
7. Report: raw scores, retention curves, wheel-vs-control delta.

**Honesty constraints.** Report n. Never extrapolate from a single session. Never claim the result generalises beyond this user. State plainly that this tests *the reconstructed mechanism's mnemonic efficacy*, which is a narrower question than "was Bruno right."

## Primary texts

- *De umbris idearum* (1582), in Sturlese's critical edition (1991) — canonical
- *De compendiosa architectura* (1582) — the Lullian rotating-wheel ancestry that makes the combinatorial reading historically natural

## Disputes

- `yates-vs-sturlese-torchia-planetary-placement` — philological, **settled in favour**
- `esoteric-vs-nonesoteric-interpretation` — this frame is often *conscripted* onto Barenstein's side, which may misrepresent Sturlese. Flag as an open question below.

## Build notes

- `mechanism_spec` here is the parent record; Barenstein / Clucas / Wang / Mertens frames should reference it rather than duplicate it, so a correction propagates.
- Build the recall harness generic enough that Wang's drop-the-scaffold variant (see WANG.md) is a parameter, not a rewrite.

## To verify in corpus

- **The actual corrected ring positions**, precisely enough to render. Highest-priority verification target in the project.
- Does Sturlese herself use anything like "combinatorial-phonetic," or is that a downstream gloss this portal would be putting in her mouth?
- Does Sturlese take an interpretive position on magical function at all, or strictly a philological one? If the latter, the "Sturlese frame" is arguably a construct and should be renamed to something like `CORRECTED-WHEEL (Sturlese/Torchia)` to avoid attributing a reading she did not make.
