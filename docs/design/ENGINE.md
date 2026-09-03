# ENGINE: the soul-state spine

**Reframes PRACTICES.md, which reframed ARCHITECTURE.md.** Practice stays primary and friction stays continuous; what changes is *what the central instrument is*. Decided 2026-09-02 (PROMPTS.md P-11) after reading Bonner.

---

## 1. Why the frame changed

I had been building toward a mnemonic trainer: type a word, encode it through the image alphabet, place it at an atrium address, walk it back. That is a real thing the sources support — and it is the least distinctive half of Bruno.

Bonner's *User's Guide* makes the other half legible. **Llull's Art is not a mnemonic and never was.** Its worked example is Llull resolving predestination vs. free will through four "figures of X". Its letters are variables: `S in E I N R, with T in X enters the compartment of perfect wisdom.`

And its output is not a retrieved fact. Bonner states the aim plainly: to get **"the S of the user"** — the state of the operator's rational soul — to remember, understand and love the true, and remember, understand and hate the false.

Bruno fuses two traditions:

| | stores | reasons |
|---|---|---|
| **Classical loci-and-images** | atria (address space) + image alphabet (encoder) | — |
| **Lullian Art** | — | figures, combination, dialectic, **soul-state** |

The mnemonic half is the warehouse. The Lullian half is the machine. **The machine is the spine.**

## 1a. ✅ Attribution — SETTLED 2026-09-02. The engine is Llull's.

Before building on this: **Bonner gives no evidence that Bruno took Figure S.**

- Bonner mentions Bruno exactly **twice**, both in the reception chapter. He says Bruno "saw it as a way to explore the connections among his infinity of worlds" — a *cosmological* use of the combinatorics, with no mention of the soul-state.
- Bonner explicitly warns that later users' "aims were different, [and] the use they made of Llull's techniques varied from something vaguely similar to something entirely different."
- Figure S's letter-notation belongs to the **quaternary** phase. Bonner: "In the ternary phase Llull no longer uses letters in the actual discourse of the Art." **Llull himself abandoned it.**

**Therefore:** the soul-state engine is **Llull's, quaternary phase**. Its transmission to Bruno is *not established*. Building it is entirely legitimate and remains the most interesting thing in the corpus — but it must be presented as **Llull's Art, which Bruno inherited combinatorially**, not as Bruno's soul-state machine.

Two concrete consequences for the build:

1. **Labelling.** The engine ships under Llull's name. Any Brunian framing is a claim requiring evidence we do not have.
2. **The Clucas upgrade in §2 below is weaker than it first looks.** Llull's notation shows the *tradition* Bruno drew on had a formal soul-state model. It does not show Bruno used it. Clucas's reading gains a plausible ancestor, not a proof.

### Settled — and it corrects two things I said

**Correction 1.** I claimed last turn that *De compendiosa architectura* was on disk. **It is not.** The Bruno Lull directory holds no copy. The question was settled from the secondaries instead.

**Correction 2.** The verdict confirms the caveat: **Bruno took Llull's combinatorics and *similitudo*-logic, not Figure S.**

- **Blum** (*Giordano Bruno: An Introduction*, corpus line 944): *De compendiosa architectura et complemento artis Lullii* "begins for example in an entirely scholarly manner with the four Aristotelian causes" — Bruno was "eager to translate also this logic to the language of the Aristotelian scholarly philosophy."
- **Mertens** (corpus line 866): what returns in Bruno is "the central idea of this logic through similarities" — the Lullian doctrine that *principia essendi et cognoscendi* are the same, and the ladder of being is climbed and descended through *similitudines*.
- Neither mentions Figure S, the four species, or the soul-state notation.

**The engine therefore ships under Llull's name**, with the attribution stated on the page itself rather than buried in a doc.

## 1b. What Bruno actually did with it — *logica fantastica*

Settling the attribution produced a better architecture than the one it cost.

Mertens names Bruno's version: **"fantastic logic"** — Paolo Rossi's *"La logica fantastica di Giordano Bruno"* — operating in the ***spiritus phantasticus***, whose power *De imaginum compositione* is largely concerned with (Mertens, corpus lines 872, 893, 2439–2494).

**Llull's Art computes with letters. Bruno's computes with images.**

That single difference explains the whole shape of the corpus, and dissolves the "two traditions bolted together" story in §1:

> Bruno needs the atria and the image alphabet **because his logic's operands are phantasms.** Before he can run a Lullian combinatorial argument at all, he must build a systematic image vocabulary and somewhere to put it. The encoder is not the mnemonic half sitting beside the reasoning half — it is the *substrate the reasoning runs on*.

This is the correct frame for the whole project, and it is why the atria (address space), the image alphabet (letter→image), and the planetary courts (component vocabulary) are one machine rather than three exhibits.

## 2. The finding that justifies it

I had filed Clucas's reading — that Bruno's art orders the operations of the soul *including appetite* — as **T2, self-report only, possibly unfalsifiable** (CLUCAS.md). That was wrong, or at least too pessimistic.

**Llull notates it.** Figure S is a formal 4×3 table of the *acts* of memory, intellect and will. Confusion is a named, reachable state. The dialectic is a specified procedure for leaving it. Clucas's "domestication of the soul" has a concrete mechanical **ancestor in the tradition Bruno drew on**, and it can be implemented without inventing anything.

That is the strongest argument for the reframe — but read it against §1a. It shows the tradition had a formal soul-state model; it does **not** show Bruno adopted it. Clucas gains a plausible ancestor, not a proof.

## 3. The state machine (`data/figure_s.json`)

Four species, each a triple of one act per power:

| | memory | intellect | will | |
|---|---|---|---|---|
| **E** | B remembering | C understanding | D loving | **informed acceptance** — goal |
| **I** | F remembering | G understanding | H hating | **informed rejection** — goal |
| **N** | K forgetting | L not knowing | M loving *or* hating | **supposition / credulity** |
| **R** | O remembering-or-forgetting | P understanding-or-not | Q loving-or-hating | **confusion** — stuck |

Llull, in the *AD*: *"By means of E I one formulates in this Art questions, arguments, and solutions… N is the vehicle for suppositions, faith, and belief, whereas R is the vehicle for doubts."*

Two points that matter for design:

- **I is a success state, not a failure.** Rejecting falsehood with full knowledge is as much the aim as accepting truth. A UI that renders I as "wrong" would invert the ethics.
- **R is supposed to happen.** In the worked example the argument *must* jam before it can resolve. Confusion is a stage, not a defeat — the third of four.

### The dialectic

`affirmation (E) → denial (I) → doubt (R) → resolution (E)`

Not a choice between horns: stage 4 re-enters the dignities under further compartments and affirms **both** at a higher level. The contradiction dissolves rather than being decided.

## 4. What this means the app is

**An instrument you operate on a question, which changes your state.**

Core loop:

1. **Pose** a question (historical, or your own).
2. **Combine** — bring figures to bear: dignities (A), oppositions (X), distinctions (T), against your soul-state (S).
3. **The state moves.** Affirming commits you to E; the counter-argument drives you to I; holding both perverts S into R.
4. **Resolve** — find the compartment that affirms both horns, or fail and remain in R.
5. **The mnemonic half stores what you've established** at atrium addresses, so it is recoverable.

The encoder I already built (atria + alphabet, 576 loci, 136 operators) becomes step 5 — a subsystem, not the product.

## 5. Decided constraints (P-11)

- **Soul-state is real mechanics.** B/C/D, F/G/H, K/L/M, O/P/Q are tracked variables that *gate* what you can do. Being stuck in R is a genuine condition you must work out of.
- **Both content modes, switchable.** Historical questions (predestination/free will, virtue/vice) as the grounded default and tutorial; own-material mode for the mnemonic half, where recall is actually measurable.
- **Latin surface, English on hover.** Show *Baptizans*, Figure S, *compartment*; gloss on hover. The letter-variable notation stops working in translation — B must be a B-word.

### The honesty constraint this creates

We are now simulating an operator's inner condition. Two rules:

1. **The state is a model of Llull's notation, not a claim about the user.** The readout says what the *figure* says, never "you are confused."
2. **Keep the tiers separate** (ARCHITECTURE.md §3). That a user reached E in the model is a fact about the model. It is not evidence their soul is ordered. The T1/T2/T3 register rule still holds and matters more here than anywhere else.

## 5a. Built: `site/fantastica.html` — the Art run on images

Bruno's side of §1b, implemented. Each of the three powers of the soul is supplied by one of Bruno's three attested systems, and the triple you compose decides which species of Figure S you land in:

| power | supplied by | present | absent |
|---|---|---|---|
| **memory** | the image alphabet | an operator gives the memory a handle — B/F | K, forgetting |
| **intellect** | the atria | an apt address means you understood where it belongs — C/G | L, not knowing |
| **will** | the planetary courts | the court's register inclines the will — D loving / H hating | M/Q, undecided |

Two rules that fall out of the attested material rather than being invented:

- **Mercury and the Sun do not move the will.** Their retinues are disclosure and illumination (Edition, Prolation, Manifestation, Revelation), so they sharpen the *intellect* — an image from these courts counts as aptly placed even in a poorly chosen atrium, but leaves the will unmoved, and the soul only supposes (N).
- **Luna cannot settle an argument.** Her retinue is split by phase in the source, so the will she produces is undecided: held and understood, but all possibilities open at once — R.

Verified across all five paths (apt+Venus→E, apt+Saturn→I, wrong atrium→N, Mercury→N, Luna→R) and the full dialectic E→I→R→E.

**Status: `SCHOLARLY_RECONSTRUCTION`, confidence `LOW`, stated on the page.** Every component is attested; the wiring is ours. Bruno leaves no worked example of composing a dialectic this way. The page prints its own attested/reconstructed split in two columns so a reader can see exactly where the evidence stops.

## 6. Build order

1. **`figure_s.json` → schema + render.** Show the 4×3 table with the notation, glossed. Cheap, and it teaches the vocabulary the rest depends on.
2. **State machine core.** Four states, twelve individuals, transitions. Pure logic, testable.
3. **The dialectic on one historical question** — predestination vs. free will, worked exactly as Bonner reports it. One question, end to end, is worth more than a general engine with nothing in it.
4. **Figures A / T / X as data.** Needs harvesting (Bonner lines 227–1600).
5. **Combination UI** — bring figures against a question; watch S move.
6. **Wire in the encoder** as the storage step.
7. Own-material mode.

## 7. Open questions

1. **Does *De compendiosa architectura* (1582) keep Figure S?** Highest priority — see §1a. The text is on disk. Until answered, the engine is Llull's.
2. **Quaternary vs ternary.** Answered in part: Figure S's letters are quaternary, and Llull dropped the letter-discourse in the ternary phase. Which phase reached Bruno is still open.
3. The full contents of Figures A, T, V, X — located, not yet read (Bonner 227–1600).
4. Whether `figure_s.json`'s hand-transcription matches Bonner's printed chart.
5. **A bonus thread worth pulling.** Bonner notes Agrippa presented Llull's Art "as an alternative to the rhetorical-mnemonic-logical system of **Ramus**." That is an attested period rivalry between the Art and the Ramist tables — and `ramist-tables` is already a built practice. The engine and that practice are historical opponents, and the portal can stage the argument.
