# Artifact: THE CABALA ENGINE

**Type:** artifact (comedic) · **Primary text:** *Cabala del cavallo pegaseo con l'aggiunta dell'Asino cillenico* (1585) · **Frames:** none — see §3

---

## 1. The design insight this artifact turns on

**The satire generator and the serious combinatorial engine should be the same code path.**

Bruno's joke in the *Cabala* is not that he invented a silly method. It is that he ran **his own real method** — letter manipulation, etymological combination, mythological layering, numerological inflation — on deliberately absurd material, and it produced cosmic-sounding results anyway. The Ass becomes a vehicle of divine wisdom by exactly the procedure that makes anything else one.

So the implementation is:

```
one combinatorial engine
  ├── vocabulary: bruno_attested   → serious mnemonic/philosophical output
  └── vocabulary: asinine_register → the Cabala's satire
```

Same rules. Same traversal. Different dictionary loaded. Nothing else differs.

This is cheaper to build than two tools, and it *is the argument*. A user who swaps the vocabulary and watches identical machinery produce solemn philosophy and then sacred donkeys has understood Bruno's satire better than any explanatory paragraph could manage.

## 2. The killer feature

**Run one input through both vocabularies simultaneously, side by side.**

The user supplies a term. The left column elaborates it through Bruno's attested philosophical register; the right column elaborates it through the asinine register. The procedures are visibly identical — same steps, same combination rules, highlighted in parallel.

The realisation that lands: *the method does not know which one it is doing.* That is precisely Bruno's satirical thesis about learned exegesis, delivered as an interaction rather than a claim.

This supersedes the seed's existing `cabala-vs-furori-tone-toggle` idea, which compared two *works*. Comparing two *vocabularies through one engine* is sharper, and it is the same build.

## 3. Why this artifact has no frame column

None of the seven interpretive frames has a reading of the *Cabala*'s combinatorial satire — they are all concerned with the mnemonic-magical corpus. The artifact matrix row is empty by design.

Per ARCHITECTURE.md §6, **empty cells are content.** The page should say plainly: *no scholar in this corpus has developed a reading of the Cabala as a comment on Bruno's own mnemonic method. The parallel drawn here is this project's, not theirs.* That keeps a genuinely useful idea from being laundered into attributed scholarship — and flags a real gap someone could go fill.

## 4. Honesty constraints — the ones that matter here

The *Cabala* satirises Kabbalistic exegesis. A generator producing mock-Kabbalistic readings needs care that the seed's current entry does not yet specify:

- **The target is learned pretension and the exegetical method's capacity to prove anything — not Judaism, and not Jewish mysticism as a tradition.** The framing copy must be explicit. Bruno's own satire is aimed at pretentious interpretation; a modern tool that reads as mockery of a living religious tradition would be a different and worse thing.
- The asinine vocabulary should draw on **Bruno's actual comic register** — the Ass, Pegasus, Cyllene, his mock-etymologies — not on invented pseudo-Hebrew. The joke is Bruno's; do not extend it into territory he did not occupy.
- Real Kabbalistic technique (gematria, notarikon, temurah) may be **described historically** where Bruno engages it, but the generator should not present itself as performing them.
- A short standing note: *this is a satirical instrument, reconstructing a 1585 parody. It is not an account of Kabbalah.*

These are constraints on framing and vocabulary, not reasons to soften the comedy. The *Cabala* is genuinely funny and its target is genuinely worth satirising.

## 5. The Ass Oracle

The seed's second idea, kept, with one addition: **every oracular pronouncement should be able to reveal the serious doctrine it parodies.** Toggle a response and see the Brunian move it inverts, with a citation.

That turns a joke generator into a teaching instrument without dulling the joke — the reveal is funnier when you can see what it was aimed at.

## 6. Data requirements

- `asinine_register` vocabulary — Bruno's attested comic terms from the *Cabala*. **Currently one `images` row** (`the-ass-pegasean-cyllenic`). Needs the real set, which means the corpus.
- `bruno_attested` vocabulary — shared with the Image Lab; see IMAGELAB.md.
- Combination rules — shared with the wheel; see WHEEL.md.
- Attested passages for the oracle's reveal function.

**Dependency note:** this artifact needs the same engine as WHEEL and the same vocabulary structure as IMAGELAB. Build those first and the Cabala engine is mostly configuration. Building it standalone would duplicate both.

## 7. Build phases

1. Vocabulary tables (`bruno_attested`, `asinine_register`) as data, not code.
2. Single combinatorial engine, vocabulary-parameterised.
3. Side-by-side dual-vocabulary view — the killer feature.
4. Ass Oracle with doctrine-reveal.
5. Cross-link to FRENZIES for the tonal-range comparison.

## 8. Open questions

- What *is* the attested comic vocabulary of the *Cabala*, precisely? Needs the text.
- Does Bruno's satirical method actually mirror his serious one step for step, or is that this project's tidy overstatement? **The whole artifact rests on this.** It is a genuinely checkable claim and should be checked before the side-by-side view is built, because if the methods diverge, the parallel view teaches something false.
- Is there scholarship on the *Cabala* as reflexive commentary on Bruno's own method? If it exists, the empty frame row above closes.
