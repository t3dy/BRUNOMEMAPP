# Artifact: THE HEROIC FRENZIES / ACTAEON'S CHAMBER

**Type:** artifact (narrative) · **Primary text:** *De gli eroici furori* (1585) · **Frames:** Clucas, Wang, Mertens, Couliano, Yates

---

## 1. The structural insight

Actaeon is not an illustration attached to the *Furori*. He is the argument, in the only form that can carry it.

The myth's structure is **reflexive**: the hunter becomes the hunted, the seer becomes the seen, and he is destroyed by *his own hounds* — his own faculties, turned on him by what he chose to look at. Bruno picks it because it states the thesis every technical frame is circling: **a sufficiently potent image does not get looked at, it does something to whoever looks.**

That means the interactive cannot be a gallery of symbolic scenes with commentary. If the user's choices do not rebound on them, the artifact has illustrated Actaeon while contradicting him.

## 2. The mechanic: choices rebound

1. The user moves through the chamber choosing **what to contemplate** — an image, a passage, a concept. Choices are logged.
2. Subsequent material is **rendered through those prior choices.** Dwell on Diana and later scenes present themselves in that register; dwell on the hunt and they come differently. The lens is built from the user's own history.
3. After enough choices, **the pack is assembled from the user's own contemplation log** and turned back on them. Their prior focus becomes the thing pursuing and reframing them.
4. The chamber can then show the user what they attended to, and what that pattern selected for.

No supernatural claim is made or needed. The transformation is real in the only sense the app can honestly deliver: **what you chose to dwell on determined what you were subsequently able to see.** That is Actaeon's structure, implemented literally, and it is also — not coincidentally — Plotinus on attention as the thing memory follows.

## 3. Frames on this artifact

| Frame | Reads the chamber as |
|---|---|
| **Clucas** | ethical transformation; the dialogues dramatise what the mnemonic treatises make method. **Primary frame.** |
| **Wang** | iconic practice; contemplation as the operation by which images become knowledge |
| **Mertens** | the heroic spirit; furor as the transformative condition, tied to deification |
| **Couliano** | eros, desire and attention — **turned reflexively on the user, not outward.** See COULIANO.md §"What remains genuinely explorable" |
| **Yates** | the image as cosmic instrument; contemplation as conformity |

Couliano on this artifact is the safe and interesting half of that frame: binding studied on oneself. The Vincula board handles the structure; Actaeon's Chamber is where a user can honestly experience being bound by what they attend to.

## 4. Why Clucas is the primary frame

Clucas's insistence that the *Furori* and *Spaccio* cannot be separated from the technical mnemonic works is what makes this artifact structurally necessary rather than a nice extra. If he is right, then **the wheel and this chamber are one project in two registers** — method and drama — and the portal should cross-link them as such: from a wheel session under the Clucas frame, offer the chamber as the same claim narrated; from the chamber, offer the wheel as the same claim operationalised.

That link is the clearest expression available of the thesis that Bruno's memory art is an ethics.

## 5. The sonnet + gloss reader

The *Furori*'s own structure — sonnet plus Bruno's prose commentary — is already a dual-layer reading interface. Extend it rather than replace it:

- Left: the sonnet. Right: Bruno's own gloss.
- Toggleable third layer: scholarly interpretation, per frame.
- The user can see Bruno interpreting himself, then scholars interpreting that. **Three layers, visibly distinct** — a natural showcase for the four-layer discipline, since the text supplies two of the layers unaided.

## 6. Data requirements

- The sonnet cycle with Bruno's prose commentary — substantial text, needs the corpus.
- Contemplation-object inventory: currently 2 relevant `images` rows (`actaeon-transformed`, `diana-bathing`). Needs the fuller set of *Furori* imagery.
- `concept_relations` for the lens mechanic.
- Per-frame interpretive layers for the reader.

## 7. Honesty constraints

- The rebound mechanic is **the user's own attention history reflected back** — never a claim about transformation of the soul. Present it as what it is; it is interesting enough without inflation.
- T2 discipline: reflections are the user's, handed back unscored.
- Do not let the drama imply the metaphysics is settled. Actaeon is Bruno's image for the claim, not evidence for it.

## 8. Build phases

1. Sonnet + gloss reader (static, high value, needs only text).
2. Contemplation logging.
3. The lens mechanic — prior choices condition later rendering.
4. The pack — user's own log turned back on them.
5. Frame layers on the reader.
6. Cross-links to WHEEL under Clucas.

## 9. Open questions

- Does Bruno's own gloss support the reflexive reading, or is the hunter/hunted symmetry a modern emphasis?
- How does Bruno handle Actaeon's *destruction*? The myth ends badly; a transformation-toward-divine-knowledge reading has to account for the hounds. This is the most interesting unresolved point in the artifact and should be surfaced rather than smoothed.
- Which translation, and are its rights clear?
