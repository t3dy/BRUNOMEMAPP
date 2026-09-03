# Portal Integration Strategy

BRUNOMEMAPP can leverage existing card templates, components, and styling from your other knowledge portals and game systems.

## Existing Portal Systems to Borrow From

### WITCHER PORTAL

**Location:** C:\Dev\WitcherPortal\  
**Relevant components:**
- Knowledge card design (biography, concept, source)
- Timeline visualization (biographical events → scholarly disputes)
- Tag/theme system (demonology, witchcraft, history, scholarship)
- Search + faceted filtering
- Citation/provenance UI patterns
- Dark academic aesthetic (excellent for Bruno's era)

**What to adapt:**
- Biography timeline cards (Bruno's life → memory philosophy connections)
- Concept cards with scholarly interpretation layers
- Source summary cards (work → editions → passages)

### TurkaGame & IslamicateOccultPortal

**Location:** C:\Dev\TurkaGame\, C:\Dev\IslamicateOccultPortal\  
**Relevant components:**
- Historical figure biographical cards
- Manuscript/edition sourcing workflows
- Scholar attribution and citation chains
- Occult concept relationship graphs
- Multi-language source support (Latin ↔ Italian ↔ English)

**What to adapt:**
- Biographical timeline of Bruno with memory-specific milestones
- Edition/manuscript relationship diagrams
- Occult scholarship card design
- Citation graph visualization

### 3dprintlab

**Location:** C:\Dev\3dprintlab\`  
**Relevant components:**
- Provenance tracking UI
- Source → reconstruction → visualization pipeline
- Multiple "interpretation modes" (different scholar views)
- Interactive mode switcher

**What to adapt:**
- Provenance panel ("Why is this here?" + source citations)
- Multi-mode visualization switcher (YATES MODE ↔ CLUCAS MODE)
- Confidence labeling system (HISTORICALLY_ATTESTED vs. SPECULATIVE)

### AlchemyBoardGame

**Location:** C:\Dev\AlchemyBoardGame\`  
**Relevant components:**
- Interactive game-like interface for esoteric content
- Real-time simulation of alchemical/magical operations
- Next.js full-stack framework
- Procedural state management

**What to adapt:**
- If building interactive tools: game-like interaction patterns
- State serialization for saving experiments
- Real-time visualization of technique execution

## Card Template Architecture

### Bruno Biography Card

**Reuse:** WITCHER PORTAL biography template  
**Customize:** Filter events to ONLY those relevant to memory/magic development

```html
<card class="bruno-biography">
  <header>Giordano Bruno</header>
  <section class="timeline">
    <event year="1548">
      Born in Nola (location significance for memory palace practice)
    </event>
    <event year="1571">
      Joins Dominican order (memory discipline in monastic training)
    </event>
    <event year="1575">
      Composes first memory works
    </event>
    <!-- etc: filter to memory/magic milestones only -->
  </section>
  <footer class="scholarship">
    <scholar-interpretation scholar="Clucas">
      Connection to Plotinian philosophy of soul
    </scholar-interpretation>
  </footer>
</card>
```

**Memory-focused fields:**
- Memory training events (monastic, composition dates)
- Travel to intellectual centers (access to manuscript traditions)
- Publication dates of mnemonic treatises
- Documented use of memory techniques (if any)
- Philosophical developments affecting memory theory

### Concept Card

**Reuse:** WITCHER PORTAL concept template  
**Customize:** Multiple scholarly interpretation layers

```html
<card class="bruno-concept">
  <header>Simulacrum</header>
  <section class="definition">
    <def-bruno>
      Bruno's usage: simulacrum as...
      (extracted from passages)
    </def-bruno>
    <def-scholarly>
      Scholars understand simulacrum as...
    </def-scholarly>
  </section>
  <section class="interpretations">
    <interpretation scholar="YATES">
      Magical image participating in cosmic forces...
    </interpretation>
    <interpretation scholar="CLUCAS">
      Simulacrum as instrument for ordering soul...
    </interpretation>
    <interpretation scholar="BARENSTEIN">
      Technical mnemonic device...
    </interpretation>
  </section>
  <section class="passages">
    <passage-link stable-id="BRUNO-0001/45/0003">
      De umbris idearum, p. 45
    </passage-link>
  </section>
</card>
```

### Source/Work Card

**Reuse:** Adapted from IslamicateOccultPortal manuscript card  
**Customize:** Bruno's mnemonic treatises

```html
<card class="bruno-work">
  <header>De umbris idearum</header>
  <section class="metadata">
    <work-type>Primary: Mnemonic Treatise</work-type>
    <author>Giordano Bruno</author>
    <date-written>1582</date-written>
  </section>
  <section class="editions">
    <edition year="1582" title="First printing (Paris)">
      → Link to Yates reconstruction
    </edition>
    <edition year="1584" title="Second edition">
      → Variations from first
    </edition>
    <edition year="1991" title="Sturlese critical edition">
      → Modern scholarly reconstruction
    </edition>
  </section>
  <section class="scholarly-focus">
    <focus scholar="YATES">
      Hermetic wheel as magical computer
    </focus>
    <focus scholar="STURLESE">
      Corrected planetary placement
    </focus>
    <focus scholar="CLUCAS">
      Ethical + logical + magical integration
    </focus>
  </section>
</card>
```

### Scholar Profile Card

**Reuse:** TurkaGame scholar biographies  
**Customize:** Bruno scholarship focus

```html
<card class="bruno-scholar">
  <header>Stephen Clucas</header>
  <section class="biography">
    Birth, affiliation, major works on Bruno
  </section>
  <section class="bruno-interpretation">
    <position>Memory art = logic + ethics + magic</position>
    <key-claim>
      Bruno's system orders the operations of the soul, not merely stores information.
      (Cite: "Amorem, artem, magiam, mathesim")
    </key-claim>
    <views>
      <memory-view>...</memory-view>
      <magic-view>...</magic-view>
      <imagination-view>...</imagination-view>
    </views>
  </section>
  <section class="disagreements">
    <disagree-with scholar="YATES">
      Rejects talismanic interpretation of wheel...
    </disagree-with>
    <agrees-with scholar="PLOTINUS">
      Uses Neoplatonic psychology...
    </agrees-with>
  </section>
</card>
```

### Dispute/Disagreement Card

**Reuse:** Adapted from WITCHER PORTAL disagreement chains  
**Customize:** Scholarly disputes about Bruno

```html
<card class="bruno-dispute">
  <header>Where do the planetary images belong in De umbris?</header>
  <section class="position-a">
    <scholar>Frances Yates</scholar>
    <claim>Planets placed at [positions A, B, C]</claim>
    <evidence>
      <passage stable-id="BRUNO-0001/67/0001">
        De umbris, p. 67 (Yates's interpretation)
      </passage>
    </evidence>
    <consequence>
      Wheel functions as magical talisman transmitting astral forces
    </consequence>
  </section>
  <section class="position-b">
    <scholar>Rita Sturlese</scholar>
    <claim>Planets actually placed at [positions X, Y, Z]</claim>
    <evidence>
      <source>
        Sturlese critical edition (1991), notes
      </source>
    </evidence>
    <consequence>
      Wheel is primarily combinatorial phonetic machine, not talisman
    </consequence>
  </section>
  <section class="resolution">
    Status: CONSENSUS (Warburg Institute accepts Sturlese correction)
    But: Clucas argues both miss the point (ethical + logical + magical integration)
  </section>
</card>
```

## File Organization for Cards

```
src/frontend/
├── components/
│   ├── cards/
│   │   ├── BrunoCard.vue              ← Base card component
│   │   ├── BiographyCard.vue          ← Bruno's life
│   │   ├── ConceptCard.vue            ← Concepts (simulacrum, memoria, etc.)
│   │   ├── WorkCard.vue               ← De umbris, other treatises
│   │   ├── ScholarCard.vue            ← Scholar profiles
│   │   ├── DisputeCard.vue            ← Disagreements
│   │   ├── TechniqueCard.vue          ← Memory wheels, techniques
│   │   ├── PassageCard.vue            ← Primary source quotes
│   │   └── InterpreterCard.vue        ← Scholar's interpretation of object
│   ├── layouts/
│   │   ├── PortalLayout.vue           ← Reuse from WITCHER
│   │   └── TimelineLayout.vue
│   └── panels/
│       ├── ProvenancePanel.vue        ← "Why is this here?" (from 3dprintlab)
│       ├── ScholarModeToggle.vue      ← BRUNO THROUGH [YATES|CLUCAS|...]
│       └── ComparisonPanel.vue        ← Side-by-side scholar views
└── styles/
    ├── bruno-theme.css                ← Customize WITCHER theme
    ├── dark-academic.css              ← Bruno-specific aesthetic
    └── _cards.css
```

## Styling Approach

**Base:** Dark academic aesthetic from WITCHER PORTAL  
**Customize for Bruno:**
- Color scheme: Alchemical (gold, copper, mercury, sulfur)
- Typography: Serif for primary sources (period feel), sans-serif for scholarship
- Diagram aesthetic: Renaissance astronomical instruments, memory wheels
- Interactive elements: Click-to-reveal interpretations, smooth mode switching

## API Endpoints (Reuse Pattern from 3dprintlab)

```
GET /api/bruno/biography
  → Returns Bruno timeline with memory milestones

GET /api/bruno/concept/<concept_id>
  → Returns concept card with all scholarly interpretations

GET /api/bruno/work/<work_id>
  → Returns work card with editions + scholarly focus

GET /api/bruno/scholar/<scholar_id>
  → Returns scholar profile

GET /api/bruno/dispute/<dispute_id>
  → Returns dispute card with both positions + evidence

GET /api/bruno/search?q=memoria
  → FTS5 search over passages + concepts

GET /api/bruno/compare/<object_type>/<object_id>?scholars=YATES,CLUCAS
  → Returns side-by-side comparison of object under different lenses
```

## Implementation Priority

1. **MVP (Quick reuse):**
   - Adapt WITCHER biography card for Bruno timeline
   - Adapt concept card template
   - Adapt scholar profile template
   - Adapt dispute card for scholarly disagreements

2. **Phase 2:**
   - Create work/edition cards (adapted from IslamicateOccultPortal)
   - Build technique cards (novel)
   - Build passage cards (novel)

3. **Phase 3+:**
   - Integrate interactive modes (BRUNO THROUGH [SCHOLAR])
   - Build comparison interface
   - Attach to Memory Wheel + other interactive tools

## Avoid

- Don't duplicate card code; instead, fork and modify
- Don't create new styling language; extend WITCHER theme
- Don't build new search/filter system; reuse portal architecture

## Success Metric

By Phase 4, a user can:
1. Click on any concept and see how Yates, Clucas, Mertens, and Wang interpret it differently
2. Click on any technique and see evidence from primary sources + scholarly reconstructions
3. Click "Why is this here?" and trace back to evidence passages
4. Read Bruno's biography with memory/magic milestones highlighted
5. Compare scholar positions on any disputed question

All using components borrowed and adapted from your existing portals.
