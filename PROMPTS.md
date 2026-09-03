# PROMPTS.md — running record of Ted's intent

**Purpose.** Long sessions get summarised and directives get dropped. This file is the durable record of what Ted actually asked for, verbatim, so no future session has to re-derive intent from code.

**Rules for maintaining this file:**
1. Append every substantive prompt **verbatim**, in order, with date. Do not paraphrase — paraphrase is where intent leaks.
2. Under each, record **DURABLE INTENT** — the standing requirement it creates.
3. Never delete an entry. If something is superseded, mark it `[SUPERSEDED by P-nn]` and keep the text.
4. Read this file at the start of any session on BRUNOMEMAPP, before touching code.
5. Standing requirements are consolidated in §STANDING AT A GLANCE at the bottom — update it when a new one lands.

---

## Session 1 — 2026-09-01

### P-01 — project kickoff

> consult brunomem.txt and create a BRUNOMEMAPP project folder with system files for an agentic coding environment and a pipeline for researching the bruno documents in e:\pdf\renaissance magic\bruno to create some web tools that allow the user to operate Bruno's memory arts and magical memory (according to the interpretations of various scholars even the controversial ones, so for example the Frances Yates talismanic art of memory is fun to play around with even if it might not be the most accurate interpretation, it's a counterfactual magical practice, but we should also let the user do the Clucas and Sturlese versions etc)

**DURABLE INTENT**
- Web tools the user can **operate**, not just read. Operability is the point.
- **Controversial interpretations are explicitly wanted.** Yates's talismanic art is fun *because* it is a counterfactual magical practice. Do not quietly drop superseded readings for being superseded.
- Multiple scholar versions coexist — Yates, Clucas, Sturlese, others.
- Wants an **agentic coding environment**, i.e. system files that make future sessions efficient. (Restated far more sharply at P-09.)
- Path given as `e:\pdf\renaissance magic\bruno` — **this path does not exist**; corrected at P-06 research to `E:\pdf\renaissance magic\Bruno Lull\`.

### P-02 — knowledge portal, memory-magic filtered

> we have a lot of web cards and pages for topics relevant to Bruno and his contexts in our medieval and renaissance magic and alchemy and other esoteric knowledge portals that you could borrow or build on. Create a knowledge portal particularly about Bruno's Memory, Magic, and Images with all dictionary, biographical timeline, historical and scholarly figure summary and primary/secondary document summary cards and pages all tuned to drilling down the rabbit hole of Bruno's so-called "memory magic" (so whatever bruno biographical event or text we choose has to be relevant to the memory magic side of his philosophy and should be written specifically to highlight the connections)

**DURABLE INTENT**
- **Borrow from existing portals** rather than building fresh. (Acted on: WitcherPortal pattern.)
- Required card types: dictionary, biographical timeline, scholar summaries, primary/secondary document summaries.
- **The memory-magic filter is a hard constraint.** Every entity must earn inclusion by an explicit connection to the memory-magic side. Enforced in schema as required `memory_magic_connection` on works, images, biographical events.
- "Drilling down the rabbit hole" — depth and interlinking, not a flat catalogue.

### P-03 — Cabala, Frenzies, humour, and process

> we will also want to study bruno's approach to Kabbalah or "The Cabala of Pegasus" and I want to create some humorous apps or games for exploring this topic. "The Heroic Frenzies" are another huge Bruno topic I'd like to create apps or games around. Make sure we have summaries of all the magical and poetic works and individual images bruno used in our knowledge portal and ask me any questions about how to divide the organization. use python scripting and crib from our existing knowledge portal designs to save effort and tokens and context.

**DURABLE INTENT**
- **Humour is a first-class requirement**, not a garnish. Comic apps/games for the *Cabala del cavallo pegaseo*.
- *De gli eroici furori* gets its own apps/games.
- **All** magical and poetic works summarised, and **individual images** as their own entities.
- **Python scripting; crib from existing portal designs; save effort, tokens, and context.** This is a standing efficiency mandate.
- Ask organisational questions rather than guessing. (Done; answers recorded below.)

### P-04 — model switch

> Switching to the Opus Model to see what capabilities or new approaches and insights it can add to our designs and plans.

**DURABLE INTENT** — invitation to genuinely re-think the design, not merely continue executing. Deeper analysis expected.

### P-05 — per-design proposal docs

> Give me an .md output with proposals for each of our designs like YATES.md CLUCAS.md STURLESE.md CABALA.md FRENZIES.md and all the others

**DURABLE INTENT**
- One `.md` proposal per design, named for the scholar or the work.
- "and all the others" — cover the full set, not a sample.
- Delivered: `docs/design/` — ARCHITECTURE + 7 frames + 6 artifacts + README.

### P-06 — practice-first reframe ★ major

> go back and research the different takes on art of memory and just create separate versions realizing as much of the art of memory practical stuff as possible then adding the scholarly interpretations as a separate writing layer. Be sure that at every step the user is having renaissance worldview and interface difficulties explained.

**DURABLE INTENT** — *inverts the P-05 architecture.*
- **Research the different takes on the art of memory** — not just Bruno; the tradition.
- **Separate operable versions**, realising **as much practical stuff as possible**. Practice is primary.
- **Scholarly interpretation is a separate writing layer**, added over the practice.
- **At every step, explain Renaissance worldview and interface difficulties.** Continuous, per-step, not a preface. This is the friction layer.

### P-07 — scholarly choices stay playable

> any choices that might come up in the scholarly layer will still be "playable" of course (so however one chooses to play with the Yatesian talisman or Sturlese memory tool

**DURABLE INTENT**
- The scholarship layer is **not inert annotation**. Where a scholarly reading changes the mechanics, it becomes a **playable variant** of the practice.
- Yatesian talisman and Sturlese memory tool are both operable. Reinforces P-01.

### P-08 — standing corpus loop

> we should be constantly plugging into our bruno memory magic knowledge portal for close summaries of the texts and rereading the bruno pdf texts directly to make sure we haven't missed anything that would be fun to play with

**DURABLE INTENT**
- **Continuously re-read the primary PDFs**, not once at ingest. Re-reading is an ongoing practice.
- The portal should hold **close summaries** of the texts.
- Explicit mining criterion: **"anything that would be fun to play with."** Read for *playable material*, not just for facts to catalogue.
- Formalised in `docs/WORKING_LOOP.md`.

### P-09 — bake the environment in

> when I say that I mean bake into the system files an efficient system for agentic coding environment to build what I've been asking for in my prompts, including memorizing the prompts so you don't lose track of my intent in a running PROMPTS.md

**DURABLE INTENT**
- System files must encode an **efficient agentic working environment**, not just documentation.
- **This file.** Prompts recorded verbatim so intent survives context loss.
- The environment exists to build *what the prompts asked for* — PROMPTS.md is the spec of record.

### P-10 — progressive revelation of context

> we should have progressive revelation of context so we are only reading the bruno texts we need to when we need to at that stage in the research to game or web dev ideas pipeline

**DURABLE INTENT**
- **Stage-gated corpus reading.** Read only the texts needed, only at the pipeline stage that needs them.
- Implies a **router**: something that says, for this stage and this task, read *these lines* of *these files*.
- Implemented as `scripts/corpus_map.py` → `docs/CORPUS_MAP.md` (line-addressed index) plus the stage table in `docs/WORKING_LOOP.md`.
- Rule that follows: **locate before reading; slice, don't load; record every slice in `HARVEST.md`** so no range is read twice.

### P-11 — reconceive around Llull; ask how to web-dev it

> after understanding Bonne's users guide we may need to reconceive and build on our whole concept of what we're doing making a memory arts app! Ask me any questions you have of how to web dev Bruno's art of memory

**DURABLE INTENT**
- Bonner's *User's Guide* to Llull's Art is a potential **reframe of the whole concept**, not just another source.
- Ted expects the concept to change if the source warrants it. Acting on that is licensed.
- Ask design questions rather than guessing. (Asked; answers below.)
- Outcome: **the soul-state engine becomes the spine**, the mnemonic encoder becomes a subsystem. See `docs/design/ENGINE.md`.

---

## Decisions from direct questions (2026-09-01)

| Question | Ted's answer |
|---|---|
| Depth on Cabala/Frenzies now, or breadth first? | **Breadth first**, revisit later |
| Humour in main site or split off? | **Same site, tone-badged** (current setup) |
| How to fold in the raw PDF corpus? | **Build `convert_corpus.py`** next session — *later overtaken: plain text already existed on disk* |

## Decisions from direct questions (2026-09-02) — the Llull reframe

| Question | Ted's answer |
|---|---|
| What is the app's spine? | **Soul-state engine.** Figure S is load-bearing; the encoder becomes a subsystem |
| Soul-state: tracked or descriptive? | **Real mechanics.** B/C/D, F/G/H, K/L/M, O/P/Q gate what you can do; R is a genuine stuck state |
| What material does the user operate on? | **Both, switchable** — historical questions and own material |
| Latin handling? | **Latin surface, English on hover** |

---

## STANDING AT A GLANCE

Consolidated requirements. Violating one of these is a defect.

1. **Operable, not just readable.** Tools the user runs. (P-01)
2. **Practice first, scholarship as a layer over it.** (P-06)
3. **Every step carries worldview + interface friction notes.** (P-06)
4. **Scholarly disagreements that change mechanics become playable variants.** (P-07)
5. **Superseded readings stay playable** — Yates is fun *because* counterfactual. (P-01, P-07)
6. **Humour is first-class**, tone-badged, in the main site. (P-03, decisions)
7. **Memory-magic filter is hard** — everything earns inclusion by explicit connection. (P-02)
8. **Re-read the primary PDFs continuously, mining for playable material.** (P-08)
9. **Crib from existing portals; Python; save tokens and context.** (P-03)
10. **The soul-state engine is the spine**; the mnemonic encoder is a subsystem. Latin surface, English on hover. Both content modes. (P-11)
11. **Progressive revelation.** Locate before reading; slice, don't load; record slices in HARVEST.md. (P-10)
12. **Never fabricate.** Grade operability honestly; never invent missing steps to make a system look complete. (project + workspace CLAUDE.md)
