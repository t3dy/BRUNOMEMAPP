# BRUNOMEMAPP Design Architecture

**The master document for the `docs/design/` set.** Every frame doc (YATES, CLUCAS, STURLESE, MERTENS, WANG, BARENSTEIN, COULIANO) and every artifact doc (WHEEL, IMAGELAB, SEALS, CABALA, FRENZIES, VINCULA) inherits the vocabulary defined here.

Status: proposal. Nothing below is implemented yet except where noted.

---

## 1. The problem this architecture solves

The original brief asks for modes where the user can "operate Clucas's Bruno," then "operate Yates's Bruno," then "compare the results." The current `bruno_seed.json` cannot support that. It has `scholars.view_memory`, `scholars.view_magic`, etc. — flat prose fields. Those produce a *card that says what Yates thought*. They do not produce a *system that behaves differently under Yates*.

The gap is that a scholar is a person and a frame is a machine configuration. Conflating them is why "scholar mode" has stayed vague.

---

## 2. A frame is a triple

**FRAME = (MECHANISM, OUTPUT, SUCCESS-CRITERION)**

- **MECHANISM** — what the artifact actually does when operated. Ring positions, combination rules, sequence of steps.
- **OUTPUT** — what the operation produces. A syllable-image pair, a talismanic composite, a bond, an iconic schema.
- **SUCCESS-CRITERION** — how you know it worked. This is the field that does the real work.

Two frames can share a mechanism entirely and still be different frames, because they disagree about what counts as the operation having succeeded.

### The wheel under seven frames

| Frame | Mechanism | Output | Success criterion | Tier |
|---|---|---|---|---|
| **Yates** | rings incl. planetary ring at Yates positions; internalize the composite | talismanic inner image | conformity of the soul to celestial order | T3 |
| **Sturlese/Torchia** | corrected ring positions; consonant + vowel → syllable → image | syllable-image encoding | accurate recall of encoded material | **T1** |
| **Barenstein** | as Sturlese | encoding + regulation schedule | recall accuracy; reduced interference | **T1** |
| **Clucas** | as Sturlese | encoding + a relational path from image toward unity | reordering of the operator's attention and appetite | T2 |
| **Wang** | as Sturlese | an iconic form / mental schema | operator can hold the relation *after the image is removed* | **T1 (partial)** |
| **Mertens** | as Sturlese, plus protective framing | spirit-regulated cognition | resistance to cognitive interference | T1 (partial) |
| **Couliano** | image → attention → desire | a *vinculum* (bond) | change in the bound party's behaviour | T3 (deliberately unbuilt) |

**Read the mechanism column.** Only Yates differs. Everyone post-1991 shares one mechanism and disagrees almost entirely in the success column.

This is the single most useful thing the software can show, and it is a real scholarly point rather than a UI gimmick: *Sturlese's correction settled the mechanism question and left every success-criterion question exactly where it was.* That is why "Yates was refuted" is a bad summary of the field. The matrix makes the bad summary impossible to state.

### Schema consequence

Add a table distinct from `scholars`:

```sql
CREATE TABLE interpretive_frames (
    slug, name,
    scholar_slug,              -- soft FK; a frame is ATTRIBUTED to a scholar, not identical to one
    artifact_slug,             -- which artifact this frame configures
    mechanism_spec,            -- JSON: concrete operational parameters
    output_type,
    success_criterion,
    testability_tier,          -- T1 | T2 | T3
    shares_mechanism_with,     -- JSON array of frame slugs
    divergence_note            -- what exactly separates this from the frames it shares mechanism with
);
```

`shares_mechanism_with` is what lets the UI say: *you just switched from Sturlese to Clucas; the wheel did not change; what changed is what you are now being asked to notice.*

---

## 3. Three tiers of testability

The most interesting property of this project: **one of the contested claims is empirically decidable in a browser, and the rest are not.** That asymmetry should be the spine of the design, not something to paper over.

- **T1 — MEASURABLE IN-APP.** Recall accuracy, retention over intervals, encoding time, scaffold-independence, interference resistance. These are real numbers the app can collect honestly.
- **T2 — SELF-REPORT ONLY.** Attention quality, felt reordering of desire, sense of ascent. The app can record what the user says; it cannot score it.
- **T3 — NOT TESTABLE HERE.** Astral influence, real binding of another person, deification. Describable, operable *as a historical reconstruction*, never scored.

### The design rule that follows

**T1, T2 and T3 results must never share a visual register.**

- T1 gets numbers, charts, comparisons across frames.
- T2 gets the user's own words handed back to them, undigested.
- T3 gets narrated as reconstruction, with no output panel at all.

Violating this is how a scholarly sandbox turns into an occult-simulator that lies about what it knows. The register separation *is* the epistemology, rendered.

### Why this is the strongest available move

If Sturlese and Barenstein are right that the wheel is a combinatorial encoding machine, **then it should work as one, and that is checkable.** A user can encode real material through the reconstructed wheel and the app can measure retention against a control. Nobody has to be taken at their word.

And the silence elsewhere is pedagogically active: the user discovers by using the thing that the mnemonic dispute touches ground truth while the metaphysical dispute does not. That is a better lesson than any essay on the magic/science binary.

**Wang's frame yields the most elegant experiment.** His claim is that the image becomes a schema the operator eventually thinks *with* rather than *about* — and the brief's own Plotinian endpoint is "you no longer need the image." That is a drop-the-scaffold test: after N successful trials, remove the image, re-test the relation. Persistence is measurable. This turns the most abstract-sounding frame into the most concretely testable one, which is a genuinely surprising result and worth surfacing to the user as such.

---

## 4. The provenance ladder

**Verified problem:** all 78 content rows currently carry `source_method = 'SEED_DATA'`. There is no mechanical difference between a claim grounded in a page of Clucas and a claim the model produced from general knowledge. Several `confidence: HIGH` rows are general knowledge.

Replace the flat value with a ladder:

| Value | Meaning | Max confidence |
|---|---|---|
| `LLM_GENERAL_KNOWLEDGE` | Model background knowledge. No locator. **Current state of everything.** | MEDIUM |
| `CORPUS_GROUNDED` | Grep'd from `corpus/sources/*.md` with a locator | HIGH |
| `SOURCE_VERIFIED` | Checked against the actual edition/page | HIGH |
| `USER_AUTHORED` | Ted wrote it | HIGH |

### Enforce it in the build, not in good intentions

`build_site.py` should refuse to emit — or loudly badge — any row with `confidence = HIGH` and `source_method = LLM_GENERAL_KNOWLEDGE`. A lint script (`scripts/validate_seed.py`) should exit non-zero on violations so it can gate a commit.

This is a mechanical guard rather than a promise to be careful, which is the only kind that survives a long session. It also directly serves the anti-fabrication rule in the workspace `CLAUDE.md`: the failure mode being defended against is exactly *quietly laundering a plausible guess into a cited fact*.

**Immediate action when adopted:** bulk-set every existing row to `LLM_GENERAL_KNOWLEDGE`, and demote the current `HIGH` rows to `MEDIUM`. The portal should visibly get less confident the moment this lands. That is correct — it was never that confident; it just wasn't saying so.

---

## 5. Disputes decompose by layer

`disputes.resolution` is currently flat, which lets "Yates vs. Sturlese" read as one settled argument. It is two arguments and only one is settled.

Add `dispute_layer`:

- **PHILOLOGICAL** — about what the text says or the diagram shows. *Can* be settled. (Ring placement: settled against Yates.)
- **INTERPRETIVE** — about what it means or does. Usually open. (Whether the wheel is talismanic in function: open.)
- **HISTORIOGRAPHICAL** — about whether the question is well-posed at all. (Ostojić on the magic/science binary.)

Splitting `yates-vs-sturlese-torchia-planetary-placement` into its philological half (SETTLED) and its interpretive half (ONGOING) is the highest-value single edit available to the current seed. It is the difference between the portal teaching the field's actual shape and teaching a schoolbook simplification.

---

## 6. Two axes: artifacts × frames

**Artifacts** are what you operate. **Frames** are how the operation is read.

|  | Yates | Sturlese | Clucas | Mertens | Wang | Barenstein | Couliano |
|---|---|---|---|---|---|---|---|
| **Wheel** | ● | ● | ● | ● | ● | ● | ○ |
| **Image Lab** | ● | ○ | ● | ● | ● | ○ | ● |
| **Seals** | ● | ○ | ● | ● | ○ | ○ | ● |
| **Vincula** | ○ | ○ | ● | ● | ○ | ○ | ● |
| **Frenzies** | ● | ○ | ● | ● | ● | ○ | ● |
| **Cabala** | — | — | — | — | — | — | — |

● = frame has a documented reading · ○ = no strong documented reading · — = out of scope (see CABALA.md)

**The empty cells are content.** "No scholar in this corpus has a developed reading of the Thirty Seals under Wang's iconic-practice frame" is a research finding, and the UI should say so rather than silently omitting the option. Empty cells are also the natural backlog for corpus work.

---

## 7. Build order

1. **`scripts/validate_seed.py`** + provenance ladder migration. Cheapest, highest integrity payoff, and it makes everything after it trustworthy. Do this first.
2. **Split the Yates/Sturlese dispute** by layer. One seed edit, large conceptual gain.
3. **`interpretive_frames` table** + the wheel's seven frame rows. This is the crux; nothing else in the brief works without it.
4. **WHEEL artifact, Sturlese frame only, with the T1 recall harness.** One frame, real measurement. Proves the empirical spine before multiplying frames.
5. **Add Wang's drop-the-scaffold test** to the same harness. Second frame, near-zero extra machinery, and the most interesting result.
6. **Frame switcher** across the wheel, with the "mechanism unchanged / criterion changed" message.
7. Then artifacts outward: IMAGELAB → FRENZIES → CABALA → SEALS → VINCULA.

Rationale for the order: steps 1–2 are integrity, step 3 is the conceptual keystone, steps 4–5 prove the one thing that makes this project more than a card catalogue. Breadth comes after that spine exists.

---

## 8. Standing constraints

- Never collapse the four layers: PRIMARY SOURCE → SCHOLARLY INTERPRETATION → RECONSTRUCTION → EXPERIMENT → USER CREATION.
- Never present T2 or T3 output in T1's visual register.
- Never let `confidence: HIGH` sit on top of `LLM_GENERAL_KNOWLEDGE`.
- Never silently merge two frames' mechanisms. If they diverge, they render separately.
- Empty matrix cells are shown, not hidden.
- The game layer must not obscure the scholarship layer.

---

## 9. Open questions for corpus verification

Every frame doc ends with a list like this. Consolidated:

- Does Sturlese herself characterise the corrected wheel as "combinatorial-phonetic," or is that a downstream gloss? (Affects STURLESE.md's mechanism spec.)
- Does Clucas anywhere give an operational criterion for "ordering the operations of the soul," or only a descriptive one? (Determines whether Clucas is genuinely T2 or unfalsifiable.)
- Does Wang commit to the strong claim that the image becomes dispensable, or only that it mediates? (The drop-the-scaffold test depends on the strong reading.)
- Does Mertens's "protection from demonic corruption" have a technical mechanism attached, or is it framing?
- Is the Warburg position on Yates's talisman reading published, and where?
