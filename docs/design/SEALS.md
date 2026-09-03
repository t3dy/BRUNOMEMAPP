# Artifact: THE SEAL LAB

**Type:** artifact · **Primary texts:** *Explicatio triginta sigillorum* (1583), *Sigillus sigillorum* (1583) · **Frames:** Yates, Clucas, Mertens, Couliano

---

## 1. Why the seals matter to the central question

The *Explicatio* presents thirty numbered *sigilli* — structured operations — of which some are plainly mnemonic and some plainly magical, **in the same list, undifferentiated by Bruno.**

That is the hardest single piece of primary evidence for anyone maintaining that Bruno kept memory technique and magical operation apart. He does not sort them. The Seal Lab's job is to let a user encounter that fact directly rather than read about it.

**Design consequence:** do *not* pre-sort the thirty seals into "mnemonic" and "magical" columns. Present them as Bruno presents them — one sequence — and let the frames disagree about which is which. Offer a per-frame classification overlay so the user can watch Yates, Clucas, Barenstein and Mertens draw the line in different places, or decline to draw it.

The disagreement *about where the line falls* is more informative than any single sorting, and it is not currently representable anywhere else in the portal.

## 2. The Seal of Seals

*Sigillus sigillorum* describes a master operation governing the internal senses — common sense, imagination, memory — as one coordinated system.

This is the closest thing in Bruno to an explicit **faculty-control technique**, and it is the primary-source anchor for Mertens's regulatory reading. It also raises the sharpest version of the project's recurring question: **is Bruno's magic ultimately aimed at the world, or at the operator's own cognitive architecture?** The Seal of Seals reads most naturally as the latter, which is why deflationary and synthetic frames can both claim it.

Render it as what it is: a capstone that unifies the thirty, with each of the thirty linked to its role under it.

## 3. Frames

| Frame | Reads the seals as |
|---|---|
| **Yates** | magically operative images; seals as talismanic (T3, no output) |
| **Clucas** | *signacula* — instruments ordering the soul's operations; the pairing with *simulacra* is his title |
| **Mertens** | spirit-regulating technique; **primary frame** for the Seal of Seals |
| **Couliano** | bond-forming operations, reflexive use only |
| Sturlese / Wang / Barenstein | ○ no strong documented reading specific to the seals |

Three empty cells — the largest block in the matrix. Worth stating on the page: **the seals are comparatively under-read** relative to the wheel. That is a genuine finding about the field's attention, and it makes the seals a good target for original corpus work rather than a gap to apologise for.

## 4. Honesty constraints — this artifact needs them most

The brief is explicit that the Seal Lab must distinguish three things, and the seals are where the temptation to blur is strongest because thirty numbered operations *look* like a complete specified system:

- **What Bruno explicitly specifies** — `HISTORICALLY_ATTESTED`
- **What scholars reconstruct** — `SCHOLARLY_RECONSTRUCTION`
- **What this application invents to make it operable** — `SPECULATIVE_IMPLEMENTATION`

Every seal renders with its level visible. Where Bruno names a seal but does not describe its operation, the lab says *"named, not specified"* and offers nothing further. **An interface that quietly filled those gaps would produce a complete-looking thirty-seal system that is substantially this project's invention** — the most likely serious fabrication risk in the whole portal, precisely because it would look so authoritative.

## 5. Data requirements

- The thirty seals: names, and whatever Bruno actually specifies for each. **Currently zero rows.**
- The Seal of Seals operation.
- `dictionary_terms` already has `sigillum` and `signaculum`; needs their relation clarified from source.
- Per-frame classification of each seal (which the frames may not supply — expect gaps).

## 6. Build phases

1. The thirty as data, with attestation level per seal — content-blocked on corpus.
2. Sequence view, unsorted, as Bruno presents them.
3. Per-frame classification overlay.
4. Seal of Seals as capstone, linked to the thirty.
5. Operable reconstruction of individual seals where genuinely specified — and only those.

## 7. Open questions

- How much does Bruno actually specify per seal, versus name? Determines whether this artifact is operable at all or is properly a reference section. **Scope this before committing to build.**
- Relation between the Thirty Seals, the Thirty Intentions (*De umbris*), and the Thirty Statues (*Lampas*). Three thirty-unit systems across two decades — is the recurrence structural or coincidental? Nobody in the seed's scholar set is recorded as addressing it, which may be a gap in the seed rather than the field.
- Is there a critical edition of the *Explicatio*?
