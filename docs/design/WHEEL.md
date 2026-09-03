# Artifact: THE MEMORY WHEEL

**Type:** artifact (the central one) · **Primary text:** *De umbris idearum* (1582) · **Frames:** Yates, Sturlese, Clucas, Wang, Mertens, Barenstein (6 of 7)

---

## Why this is the first artifact to build

It is the object every frame has an opinion about, the object the field's most famous correction is about, and the only object whose function can be empirically checked. Build it once, properly, and six frames become a configuration rather than six builds.

## What it is

Concentric rotating rings — letters/consonants, vowels, images, planetary figures — which combine to generate syllables, and through syllables, image-encoded material. The rotating-ring mechanism descends from Llull's *Ars Magna*, which Bruno adapted in *De compendiosa architectura* the same year.

## The frame matrix for this artifact

| Frame | Ring geometry | Success criterion | Tier | Renders |
|---|---|---|---|---|
| Yates | **Yates positions** | soul conformed to celestial order | T3 | narration only, no output panel |
| Sturlese | corrected | recall accuracy | T1 | full measurement |
| Barenstein | corrected | recall + low interference | T1 | measurement, esoterica collapsed |
| Clucas | corrected | reordered attention/appetite | T2 | self-report, unscored + relational ladder |
| Wang | corrected | relation survives image removal | T1 partial | scaffold-withdrawal harness |
| Mertens | corrected | interference resistance | T1 partial | distractor harness + protective framing |

**Only the first row has different geometry.** Everything else is one wheel with six readings. The switcher's job is to make that fact impossible to miss.

## The single most important interaction

Switching frames must state what did and did not change:

> *Switched from Sturlese to Clucas. **The wheel has not changed.** What changed is what counts as having used it successfully.*

And going to or from Yates:

> *Switched to Yates. **The planetary ring has moved** — this is the reconstruction Sturlese corrected in 1991. You are operating a historical counterfactual.*

Those two messages carry more of the project's argument than any essay page will.

## The recall harness

One harness, parameterised per frame. Build generic from the start:

| Parameter | Sturlese | Barenstein | Wang | Mertens |
|---|---|---|---|---|
| target material | arbitrary | **confusable** | relational | arbitrary |
| test type | free recall | intrusion errors | post-withdrawal | under distraction |
| control condition | unencoded list | unencoded confusable | image retained | quiet condition |
| primary metric | hit rate | intrusion rate | persistence | degradation delta |

Shared: encoding time, retention curve at spaced intervals, local storage, cross-session and cross-frame comparison.

### Honesty constraints on reporting

- Always show n. Never extrapolate from one session.
- Never present a result as bearing on what Bruno intended — only on what the reconstruction does for this user.
- T1 numbers, T2 verbatim self-report, and T3 narration never share a panel.
- A good result under Sturlese is evidence about *mnemonic efficacy of a reconstruction*, which is a narrower claim than any of the six frames actually makes. Say so in the results panel, every time.

## Data requirements

Currently missing from the seed:

- **Ring position data** for both the Yates and corrected reconstructions, precise enough to render. **This is the single highest-priority corpus verification target in the project** — six frames and the whole switcher depend on it, and it is currently not in the database in any form.
- Full letter/syllable inventory.
- Image inventory per ring (currently 2 wheel-component rows; needs the real set).
- `concept_relations` for Clucas's ladder and Wang's relational material.

**Until ring data is verified, the wheel must be built with the geometry clearly marked `SPECULATIVE_IMPLEMENTATION`.** A plausible-looking wheel with invented positions would be exactly the kind of quiet fabrication the provenance ladder exists to prevent — and it would be very easy to do by accident.

## Build phases

1. Static render, corrected geometry, marked speculative until verified.
2. Rotation + syllable generation.
3. Sturlese recall harness (T1). **First real result.**
4. Frame switcher, Sturlese ↔ Barenstein (shared geometry, different metric).
5. Yates geometry + the ring-comparison animation.
6. Wang scaffold-withdrawal.
7. Clucas relational ladder + T2 prompts. Requires `concept_relations`.
8. Mertens distractor harness.

## Open questions

- Exact ring positions, both reconstructions.
- Does the corrected wheel actually work as a mnemonic for a modern user with no Latin? If not, is that a finding about the reconstruction, about the user, or about the portal's implementation? This is a real risk to the whole T1 spine and should be scoped early with a throwaway prototype before phase 3 is committed to.
- How much Latin/Italian competence does honest operation assume?
