# Design Proposals

Proposal set for BRUNOMEMAPP's interactive layer. **Nothing here is implemented.** These are design documents to argue with, not a build log.

**Read [ARCHITECTURE.md](ARCHITECTURE.md) first** — every other document inherits its vocabulary (frames as triples, testability tiers, the provenance ladder, the artifact×frame matrix).

## Frames — how an operation is read

| Doc | Stance | Testability |
|---|---|---|
| [YATES.md](YATES.md) | wheel as inner talisman; Hermetic-magical | T3 |
| [STURLESE.md](STURLESE.md) | corrected wheel as combinatorial encoder | **T1** |
| [CLUCAS.md](CLUCAS.md) | logic + ethics + magic; ordering the soul | T2 (+partial T1) |
| [WANG.md](WANG.md) | iconic practice; image becomes schema | **T1 partial** |
| [MERTENS.md](MERTENS.md) | spirit-regulation; memory and magic as one | T1 partial |
| [BARENSTEIN.md](BARENSTEIN.md) | *memoria regulata*; non-esoteric | **T1** |
| [COULIANO.md](COULIANO.md) | *vinculum*; psychological binding | T3 (deliberately unbuilt) |

## Artifacts — what you operate

| Doc | Primary text | Frames |
|---|---|---|
| [WHEEL.md](WHEEL.md) | *De umbris idearum* | 6 of 7 |
| [IMAGELAB.md](IMAGELAB.md) | *De imaginum* | 5 |
| [SEALS.md](SEALS.md) | *Explicatio* / *Sigillus sigillorum* | 4 |
| [CABALA.md](CABALA.md) | *Cabala del cavallo pegaseo* | none — by design |
| [FRENZIES.md](FRENZIES.md) | *De gli eroici furori* | 5 |
| [VINCULA.md](VINCULA.md) | *De vinculis in genere* | 3 |

## The three ideas that carry the set

1. **A frame is (mechanism, output, success-criterion).** Only Yates has a different mechanism; every post-1991 frame shares one wheel and disagrees about what success means. That is why Sturlese's correction settled the philology and left the interpretation untouched — and the software can show it.
2. **One contested claim is empirically decidable in a browser.** The mnemonic claim is measurable; the metaphysical ones are not. Keeping those in separate visual registers is the whole epistemology, rendered.
3. **Provenance must be mechanically enforced.** All 78 current content rows are `SEED_DATA` — model general knowledge — and some carry `confidence: HIGH`. A build-time lint should make that combination impossible.

## Status

All scholarly characterisations in these documents are `LLM_GENERAL_KNOWLEDGE`, written from model background knowledge rather than a page-cited reading of the corpus. Each document ends with a **To verify in corpus** section. The highest-priority item across the whole set: **the actual ring positions of both wheel reconstructions**, which six frames depend on.
