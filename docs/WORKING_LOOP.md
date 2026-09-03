# WORKING LOOP

**The agentic operating procedure for BRUNOMEMAPP.** Encodes PROMPTS.md P-03 (save tokens/context), P-08 (continuously re-read the texts for playable material), and P-10 (progressive revelation — read only what this stage needs).

Read this before doing corpus work. It is short on purpose.

---

## The pipeline

```
S0 ORIENT   →  S1 LOCATE  →  S2 HARVEST  →  S3 MODEL  →  S4 DESIGN  →  S5 BUILD  →  S6 VERIFY
   no corpus     map+grep     read slices    seed rows    playable      code        prove it
                                                          specs
```

Each stage declares what you may read. **Reading ahead of your stage is the main way this project wastes context.**

| Stage | You may read | You must produce | Never |
|---|---|---|---|
| **S0 ORIENT** | `PROMPTS.md`, `CLAUDE.md`, this file | a stated goal for the session | open the corpus |
| **S1 LOCATE** | `docs/CORPUS_MAP.md`, `grep -n` output | line ranges worth reading | read a whole file |
| **S2 HARVEST** | corpus **slices** at located ranges | `HARVEST.md` entries w/ locators | read >150 lines without cause |
| **S3 MODEL** | your own harvest notes | seed rows (practices, steps, frictions, images) | re-read what HARVEST already captured |
| **S4 DESIGN** | seed + `docs/design/` | playable specs | invent steps the source lacks |
| **S5 BUILD** | design docs + code | scripts, site | change design silently mid-build |
| **S6 VERIFY** | build output | link check, lint, honest report | claim done without checking |

## Progressive revelation rules (P-10)

1. **Locate before reading.** `CORPUS_MAP.md` → `grep -n` → *then* `sed -n 'A,Bp'`. Never open a source to "see what's in it"; the map already tells you.
2. **Slice, don't load.** Sources run 5k–15k lines. Default slice ≤150 lines. A bigger read needs a reason.
3. **Record every slice in `HARVEST.md`** with its locator. A range recorded is a range nobody re-reads.
4. **Read at the stage that needs it.** Don't harvest for the Seal Lab while modelling the atrium.
5. **Re-run `scripts/corpus_map.py`** if the corpus changes. The map is cheap; re-reading is not.

```bash
cd "E:/pdf/renaissance magic/Bruno Lull/plain_text_drafts"
grep -n "atrium" "<file>" | head          # locate
sed -n '1288,1400p' "<file>"              # read the slice
```

## The mining criterion (P-08)

When reading, you are hunting for **playable material**, not facts to file. Ask of every passage:

- Can a user **do** this? (→ a practice step)
- Is there a **specified inventory**? Named places, images, figures, rules. (→ seed data)
- Would a modern user find this **strange**? (→ a friction note — these are as valuable as the mechanics)
- Does it contradict what the portal currently says? (→ a correction, highest priority)

**Specified inventories are the jackpot.** Two found so far, both in *De imaginum*:
- **The atria system** (Bk I Pt 2 ch 3–6, ~line 1257–1400): 24 named atria × 24 positions = 576 addressable loci, with a complete "adjective place" inventory for the Altar. Fully operable.
- **The image gallery** (~line 3616–4930): named images — Grief, Care, Fear, Doubt, Hunger, Envy, Death, Wrath, Cupid, Pluto, Fortune, plus Jove/Mars/Mercury/Apollo sets. Each with a central figure, attendant personifications, and verse. This is the Image Lab's component vocabulary, from source.

Neither was visible from the file list. Both came from map → grep → slice. That is the loop working.

## Standing checks

- **Before designing anything Bruno-specific**, grep the corpus. The portal currently contains general-knowledge claims that the corpus can upgrade or refute (ARCHITECTURE.md §4).
- **Before claiming a practice is operable**, confirm the source specifies every step. Grade honestly (PRACTICES.md §2).
- **After any seed edit**: `python scripts/seed_from_json.py && python scripts/build_site.py`.
- **Never** invent steps to make a system look complete. The Thirty Seals are the standing temptation.

## Corpus location

`E:\pdf\renaissance magic\Bruno Lull\` — **not** `...\bruno\`, which does not exist and was wrong in earlier docs.

- `plain_text_drafts/` — 24 pre-extracted `.txt`. **Use these.** No PDF extraction needed.
- Parent dir — the PDFs/EPUBs themselves.

Key holdings: Higgins trans. *On the Composition of Images* (= *De imaginum*, 1591) · *Thirty Statues* (= *Lampas*) · Sondergard/Sowell *The Cabala of Pegasus* · Blackwell/de Lucca *Cause, Principle and Unity + Essays on Magic* (contains *De magia*, *De vinculis*) · Mertens *Magic and Memory* · Gatti ed. *Philosopher of the Renaissance* (contains Clucas, "Simulacra et Signacula") · Ordine *Philosophy of the Ass* · Bonner *The Art and Logic of Ramon Llull: A User's Guide* + *Doctor Illuminatus*.

**Not on disk:** Yates *The Art of Memory*, *Ad Herennium*, Quintilian, Carruthers, Camillo, Fludd, Sturlese's critical edition. Anything sourced from those is `LLM_GENERAL_KNOWLEDGE`, capped at `confidence: MEDIUM`.
