# PRACTICES: the practice-first reframe

**Supersedes the frame-first organisation of ARCHITECTURE.md §2–6.** That design made the scholarly frame the thing you pick, with the artifact configured by it. This inverts that: **the practice is primary and operable; scholarship annotates it; and where scholars disagree about the mechanics, each reading becomes its own playable variant.**

---

## 1. Three layers

```
PRACTICE      the art of memory, realised as concretely as the sources allow.
              Step-by-step. Operable. This is the site.

FRICTION      at every step: what a modern user finds strange, and why it
              made sense. Continuous, not a preface.

SCHOLARSHIP   a separate writing layer over the practice. Where a scholarly
              disagreement changes the mechanics, it becomes a playable
              VARIANT of the practice rather than a footnote about it.
```

The third point is the one that keeps the scholarship from going inert. Yates's talismanic wheel and Sturlese's corrected wheel are not two opinions about one object — they are **two operable variants**, and the user runs both.

## 2. What "realised" means

A practice is `FULLY_OPERABLE` only if a user can sit down and *do* it end to end from what the sources actually specify. Three grades:

| Grade | Meaning |
|---|---|
| `FULLY_OPERABLE` | Every step specified in the source. User can practise it. |
| `PARTIALLY_OPERABLE` | Core specified; gaps marked and filled with labelled reconstruction. |
| `REFERENCE_ONLY` | Source names the technique but does not specify it. Described, not operable. |

**Never silently upgrade a grade by inventing the missing steps.** The seals problem from SEALS.md generalises: a complete-looking system that is substantially our invention is the project's main fabrication risk.

## 3. The friction layer

Two kinds, attached per step:

- **WORLDVIEW** — the step assumes something about mind, cosmos, or value that the user does not share. *Why must the images be violent and obscene? Why are there planets on this? Why does order matter absolutely?*
- **INTERFACE** — the step assumes material conditions the user lacks. *You need a building you've known for years. You need Latin. You need to not be able to look things up.*

This is the layer the brief cares most about and it is the one most portals omit. A user who is told only *what* to do experiences the art as arbitrary ritual. A user told *why it made sense* is doing history.

**Rule: every step gets at least one friction note.** A step with none is a step nobody has thought hard enough about.

## 4. The practice set

Grounding is uneven and must be stated per practice. Corpus check performed 2026-09-01 against `E:\pdf\renaissance magic\Bruno Lull\plain_text_drafts\` (pre-extracted plain text, 30 files).

| Practice | Tradition | Grounding | Grade |
|---|---|---|---|
| `bruno-atrium` | Bruno, *De imaginum* 1591 | **CORPUS** (Higgins trans.) | PARTIALLY ✅ **built** |
| `bruno-lampas-statues` | Bruno, *Lampas* | **CORPUS** (Thirty Statues trans.) | PARTIALLY ✅ **built** |
| `llull-art` | Llull, *Ars* | **CORPUS** (Bonner, *User's Guide*) | PARTIALLY |
| `classical-loci` | *Ad Herennium* c.86 BCE | general knowledge | FULLY ✅ **built** |
| `quintilian-sober` | Quintilian XI.ii | general knowledge | FULLY ✅ **built** |
| `hugh-grid` | Hugh of St Victor | general knowledge | PARTIALLY |
| `aquinas-prudence` | Aquinas / scholastic | general knowledge | PARTIALLY |
| `camillo-theatre` | Camillo, *L'Idea del Theatro* | general knowledge | REFERENCE_ONLY |
| `ramist-tables` | Ramus — the anti-art | general knowledge | FULLY ✅ **built** |

**Not on disk:** Yates *The Art of Memory*, *Ad Herennium*, Quintilian, Carruthers, Camillo, Fludd. Everything in the lower block is `LLM_GENERAL_KNOWLEDGE` and capped at `confidence: MEDIUM` per ARCHITECTURE.md §4.

### Why include the Ramist anti-art

Ramus's dichotomous tables *replace* image-based memory and treat the images as superstitious clutter. Including it as a playable practice gives the user the period's own strongest objection to everything else on the list, in operable form. It also explains why the tradition dies in Protestant Europe. Omitting it would present the art of memory as uncontested in its own time, which it was not.

## 5. The finding that reframes the whole thing

**Bruno's art of memory is not what "memory palace" leads a modern user to expect**, and this should be the first friction note they meet.

The *Lampas* "statues" are not vivid images for recalling a list. They are conceptual organising figures — the Statue of Venus is the topic of *concordance according to will*, subdivided into thirty numbered notions. The system generates and orders **concepts**, closer to rhetorical *inventio* (finding what to say) than to mnemonics (retaining what was said).

A user arriving for shopping-list tricks and meeting the scale of nature has hit a real historical gap, not a failure of the interface. Name it, explain it, and the rest of Bruno becomes legible.

## 6. `bruno-atrium` — worked example, corpus-grounded

From *De imaginum, signorum et idearum compositione* (1591), Bk I Pt 2, chs 3–6, Higgins translation:

- **Atrium form.** Quadrangular. Centre is "the earth and the eye." Four corners = E/W/N/S; four mid-side points also labelled E/W/N/S. → **8 distinct points**, each determining right and left collaterals → **24 positions**.
- **24 atria**, matching "the number of the twenty four elements": altar, basilica, prison, house, colt, fountain, sword, horoscope, fire, yoke, lantern, table, nest, sheepfold, food, four-horse chariot, net, mirror, hot springs, carriage, gate, Pythagorean fork, gift, key of jealousy.
- **Nesting.** The atria names distribute *into* each atrium: in the Atrium of the Altar an altar sits at the eastern corner, a colt at the western, an image at the southern, a sheepfold at the fourth. 24 × 24.
- **Substantive vs adjective places.** Substantive = the angles and spaces themselves. Adjective = what animates the occupant — alive or dead, moving or moved.
- **Adjective inventory for the Altar** is given in full: E angle water flowing / r. plow / l. chain · W angle tree / r. ram / l. banquet · S angle horse / r. anchor / l. chariot · N angle prison / r. giant / l. goat · E side ewer / r. young man / l. amphora · W side oven / r. fork / l. consuming fire · S side smoke / r. fruit / l. stable · N side desk / r. skiff / l. throne.

That is a complete addressing scheme — **576 loci, specified, from the text.** It is the most operable thing in the entire Bruno corpus and the correct first build.

**Textual variant already visible:** the source marks two versions of the atrium diagram, "1591 version" and "Tocco's version." Per §1 that is a playable variant, not a footnote — seeded as `atrium-1591-vs-tocco`.

## 7. Schema

```sql
practices(slug, name, tradition, date_range, source_text, one_line,
          what_you_can_do, operability, worldview_preface,
          structure_json,          -- e.g. the 24×24 atrium inventory
          source_method, confidence)

practice_steps(practice_slug, step_number, title, instruction,
               attestation,        -- ATTESTED | RECONSTRUCTED | SPECULATIVE
               source_locator)

frictions(practice_slug, step_number, kind,   -- WORLDVIEW | INTERFACE
          difficulty, explanation)

practice_variants(practice_slug, slug, name, scholar_slug,
                  what_changes, playable_as, testability_tier)
```

`practice_variants` is where the scholarship layer becomes playable. A variant must state **what changes mechanically** — if nothing changes mechanically it is commentary and belongs in the scholarship layer proper, not here.

## 8. Build order

1. Schema + `practices_seed.json`.
2. `bruno-atrium` fully realised from corpus. **First, because it is the best-grounded and most operable.**
3. `classical-loci` + `quintilian-sober` — the baseline the user needs before Bruno's departure from it is legible.
4. Friction notes across both. Non-optional.
5. `ramist-tables` — the objection.
6. Variants layer: Yates/Sturlese wheel as two playable versions.
7. Remaining practices outward.

## 9. Open questions

- Bonner's *User's Guide* is on disk and is explicitly a practical manual for Llull's Art — likely the second-best grounding available. Not yet read.
- Does Higgins give the adjective inventories for **all 24** atria, or only the Altar? Determines whether `bruno-atrium` is fully or partially operable at scale.
- Is the Higgins translation in copyright? Affects how much can be quoted vs. paraphrased on the site.
- What are the two atrium diagram versions (1591 vs Tocco) and how do they differ?
