"""
build_site.py — Generate the static HTML site from the BRUNOMEMAPP SQLite DB.

Reads db/bruno.db; writes:
    site/index.html
    site/works/index.html          + site/works/<slug>.html
    site/images/index.html         + site/images/<slug>.html
    site/scholars/index.html       + site/scholars/<slug>.html
    site/disputes/index.html       + site/disputes/<slug>.html
    site/timeline/index.html       + site/timeline/<slug>.html   (biographical_events)
    site/essays/index.html         + site/essays/<slug>.html
    site/ideas/index.html          + site/ideas/<slug>.html      (app_mode_ideas)
    site/dictionary.html
    site/bibliography.html
    site/research-questions.html
    site/about.html
    site/search.html  + site/search-index.json
    site/style.css and site/script.js are NOT regenerated — edit those by hand.

Cribbed structurally from C:\\Dev\\WitcherPortal\\scripts\\build_site.py.
"""

import json
import sqlite3
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import md as _md

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "bruno.db"
SITE_DIR = BASE_DIR / "site"

NAV_ITEMS = [
    ('Home',        'index.html'),
    ('Engine',      'engine.html'),
    ('Fantastica',  'fantastica.html'),
    ('Practices',   'practices/index.html'),
    ('Designs',     'designs.html'),
    ('Works',       'works/index.html'),
    ('Images',      'images/index.html'),
    ('Scholars',    'scholars/index.html'),
    ('Disputes',    'disputes/index.html'),
    ('Timeline',    'timeline/index.html'),
    ('Dictionary',  'dictionary.html'),
    ('Essays',      'essays/index.html'),
    ('App Ideas',   'ideas/index.html'),
    ('Bibliography','bibliography.html'),
    ('Open Questions', 'research-questions.html'),
    ('Search',      'search.html'),
    ('About',       'about.html'),
]


def esc(s):
    if s is None:
        return ''
    return html.escape(str(s), quote=True)


def jparse(v):
    if not v:
        return []
    try:
        return json.loads(v)
    except (json.JSONDecodeError, TypeError):
        return []


def nav_html(active='', depth=0):
    prefix = '../' * depth
    links = []
    for label, href in NAV_ITEMS:
        cls = ' class="active"' if label == active else ''
        links.append(f'<a href="{prefix}{href}"{cls}>{label}</a>')
    return '\n            '.join(links)


def page_shell(title, body, active_nav='', depth=0, subtitle=None):
    prefix = '../' * depth
    sub = subtitle or 'A research laboratory for Giordano Bruno&rsquo;s memory, magic, and images'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(title)} — BRUNOMEMAPP</title>
    <link rel="stylesheet" href="{prefix}style.css">
</head>
<body>
    <header>
        <div class="header-content">
            <h1>BRUNOMEMAPP</h1>
            <div class="subtitle">{sub}</div>
            <div class="attribution">Primary source → scholarly interpretation → reconstruction → experiment. The layers are never collapsed.</div>
            <nav class="site-nav">
            {nav_html(active_nav, depth)}
            </nav>
        </div>
    </header>
    <main class="page-content">
{body}
    </main>
    <footer>
        <p>BRUNOMEMAPP &middot; scholarly and educational use &middot; a research sandbox, not a settled account of Giordano Bruno&rsquo;s work.</p>
    </footer>
    <script src="{prefix}script.js"></script>
</body>
</html>
"""


def confidence_badge(c):
    if not c:
        return ''
    cls = {'HIGH': 'confidence-high', 'MEDIUM': 'confidence-medium', 'LOW': 'confidence-low'}.get(c, 'confidence-medium')
    return f'<span class="badge {cls}" title="Confidence">{esc(c)}</span>'


def review_badge(r):
    if not r:
        return ''
    cls = {'DRAFT': 'review-draft', 'REVIEWED': 'review-reviewed', 'VERIFIED': 'review-verified'}.get(r, 'review-draft')
    return f'<span class="badge {cls}" title="Review status">{esc(r)}</span>'


def relevance_badge(rel):
    if not rel:
        return ''
    cls = f"badge-relevance-{rel.lower()}"
    return f'<span class="badge {cls}" title="Memory/magic relevance">{esc(rel)}</span>'


def tone_badge(t):
    if not t:
        return ''
    cls = f"badge-tone-{t.lower()}"
    return f'<span class="badge {cls}">{esc(t)}</span>'


def resolution_badge(r):
    if not r:
        return ''
    cls = f"badge-resolution-{r.lower().replace('_', '-')}"
    return f'<span class="badge {cls}">{esc(r.replace("_", " "))}</span>'


def tag_list(tags_json):
    tags = jparse(tags_json)
    if not tags:
        return ''
    return '<div class="tags">' + ''.join(f'<span class="tag">{esc(t)}</span>' for t in tags) + '</div>'


def render_paragraphs(text):
    if not text:
        return ''
    paras = [p.strip() for p in text.split('\n\n') if p.strip()]
    return '\n'.join(f'<p>{esc(p)}</p>' for p in paras) if paras else f'<p>{esc(text)}</p>'


def provenance_line(source_method, review_status, confidence):
    return f'<p class="provenance">{esc(source_method)} &middot; {review_badge(review_status)} {confidence_badge(confidence)}</p>'


def fetch_scholarly_refs(cur, entity_type, slug):
    return cur.execute("""
        SELECT b.author, b.title, b.year, b.source_id, sr.page_ref, sr.note
        FROM scholarly_refs sr
        JOIN bibliography b ON sr.bib_source_id = b.source_id
        WHERE sr.entity_type = ? AND sr.entity_slug = ?
        ORDER BY b.year, b.author
    """, (entity_type, slug)).fetchall()


def refs_block(cur, entity_type, slug):
    refs = fetch_scholarly_refs(cur, entity_type, slug)
    if not refs:
        return ''
    items = []
    for author, title, year, source_id, page_ref, note in refs:
        yr = f' ({year})' if year else ''
        pg = f', {esc(page_ref)}' if page_ref else ''
        nt = f'<div class="ref-note">{esc(note)}</div>' if note else ''
        items.append(f'<li class="ref-item">{esc(author)}{yr}. <em>{esc(title)}</em>{pg}{nt}</li>')
    return f'<h3>Scholarly References</h3><ul class="ref-list">{"".join(items)}</ul>'


# ============================================================
# HOME
# ============================================================

def render_home(cur):
    counts = {}
    for table in ['works', 'images', 'scholars', 'dictionary_terms', 'disputes',
                  'biographical_events', 'essays', 'app_mode_ideas', 'bibliography',
                  'practices']:
        counts[table] = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

    body = f"""
        <div class="hero">
            <p class="lead">A digital-humanities laboratory for Giordano Bruno&rsquo;s art of memory, theory of images,
            and magical philosophy. Bruno&rsquo;s own words become structured data; scholars&rsquo; interpretations
            (Yates, Sturlese, Clucas, Mertens, Wang, Couliano, Barenstein, and others) sit alongside them, in explicit
            disagreement where they disagree. Everything traces back to a source.</p>
        </div>

        <div class="layer-strip">
            <span class="layer">PRIMARY SOURCE</span><span class="arrow">&rarr;</span>
            <span class="layer">SCHOLARLY INTERPRETATION</span><span class="arrow">&rarr;</span>
            <span class="layer">RECONSTRUCTION</span><span class="arrow">&rarr;</span>
            <span class="layer">EXPERIMENT</span>
        </div>

        <div class="stats">
            <div class="stat-card"><span class="stat-number">{counts['practices']}</span><span class="stat-label">Practices</span></div>
            <div class="stat-card"><span class="stat-number">{counts['works']}</span><span class="stat-label">Works</span></div>
            <div class="stat-card"><span class="stat-number">{counts['images']}</span><span class="stat-label">Images</span></div>
            <div class="stat-card"><span class="stat-number">{counts['scholars']}</span><span class="stat-label">Scholars</span></div>
            <div class="stat-card"><span class="stat-number">{counts['disputes']}</span><span class="stat-label">Disputes</span></div>
            <div class="stat-card"><span class="stat-number">{counts['dictionary_terms']}</span><span class="stat-label">Dictionary terms</span></div>
            <div class="stat-card"><span class="stat-number">{counts['bibliography']}</span><span class="stat-label">Bibliography</span></div>
        </div>

        <section class="home-grid">
            <div class="home-card featured">
                <h2><a href="engine.html">The Art Engine</a></h2>
                <p>Llull&rsquo;s Figure S as a working state machine. Take the contradiction between
                predestination and free will through all four figures &mdash; affirmation, denial,
                doubt, resolution &mdash; and watch the state of the soul move E &rarr; I &rarr; R &rarr; E.
                Confusion is a real, reachable state, and escaping it is the point.</p>
            </div>
            <div class="home-card featured">
                <h2><a href="fantastica.html">Logica Fantastica</a></h2>
                <p>The same dialectic, run on <em>images</em> instead of letters &mdash; which is what
                Bruno&rsquo;s version requires. Compose one from the image alphabet, the atria and the
                planetary courts; the triple you build decides where your soul-state lands.
                A labelled reconstruction.</p>
            </div>
            <div class="home-card">
                <h2><a href="designs.html">Design Documents</a></h2>
                <p>The working record: 17 documents arguing what this project should be, including
                the places where a later reading overturned an earlier decision.</p>
            </div>
            <div class="home-card">
                <h2><a href="practices/index.html">Practices</a></h2>
                <p>{counts['practices']} arts of memory realised step by step so you can run them — Bruno's 576-locus atria, the classical art of places and agent images, Quintilian's sceptical version, Bruno's conceptual Statues, and the Ramist objection to the whole enterprise. Every step explains where the Renaissance worldview parts company with yours.</p>
            </div>
            <div class="home-card">
                <h2><a href="works/index.html">Works</a></h2>
                <p>{counts['works']} of Bruno&rsquo;s mnemonic treatises, magical texts, and Italian/Latin poetic-philosophical works — De umbris idearum through De gli eroici furori — each tagged with exactly how it bears on memory and magic.</p>
            </div>
            <div class="home-card">
                <h2><a href="images/index.html">Images</a></h2>
                <p>{counts['images']} individual mnemonic and magical images Bruno used, as their own addressable cards: what each does, not just what it depicts.</p>
            </div>
            <div class="home-card">
                <h2><a href="scholars/index.html">Scholars</a></h2>
                <p>{counts['scholars']} profiles — Yates, Sturlese, Torchia, Clucas, Mertens, Wang, Barenstein, Couliano, Gatti, Farinella/Preston, Ostojić — with their specific views and disagreements.</p>
            </div>
            <div class="home-card">
                <h2><a href="disputes/index.html">Disputes</a></h2>
                <p>{counts['disputes']} scholarly disagreements laid out as two positions with evidence, not resolved on the page.</p>
            </div>
            <div class="home-card">
                <h2><a href="timeline/index.html">Timeline</a></h2>
                <p>Bruno&rsquo;s biography, filtered to events that bear specifically on his memory/magic system — not a general life story.</p>
            </div>
            <div class="home-card">
                <h2><a href="dictionary.html">Dictionary</a></h2>
                <p>{counts['dictionary_terms']} key terms — memoria, phantasia, simulacrum, signaculum, umbra, vinculum — with Bruno&rsquo;s usage and scholarly interpretation side by side.</p>
            </div>
            <div class="home-card">
                <h2><a href="essays/index.html">Essays</a></h2>
                <p>Long-form pieces connecting Bruno to his intellectual background — starting with Plotinus on memory as an active power of soul.</p>
            </div>
            <div class="home-card">
                <h2><a href="ideas/index.html">App-Mode Ideas</a></h2>
                <p>Interactive tool and game concepts grounded in specific works — including explicitly comic modes for the Cabala del cavallo pegaseo and serious ones for the Eroici furori.</p>
            </div>
        </section>

        <p class="provenance-note">
            <strong>Provenance.</strong> Every entry carries <code>source_method</code>, <code>review_status</code>, and <code>confidence</code> fields.
            Current content is <code>SEED_DATA</code> at <code>DRAFT</code> status — grounded in the cited scholarship but not yet
            line-verified against the primary-source corpus in <code>corpus/</code>. Treat claims as a research starting point, not settled fact.
        </p>
    """
    return page_shell('Home', body, active_nav='Home', depth=0)


# ============================================================
# THE ART ENGINE  (docs/design/ENGINE.md)
# Llull's Figure S as a working state machine. NOT Bruno's -- see ENGINE.md §1a.
# ============================================================

def render_engine():
    fig_path = BASE_DIR / 'data' / 'figure_s.json'
    q_path = BASE_DIR / 'data' / 'engine_questions.json'
    if not (fig_path.exists() and q_path.exists()):
        return None
    fig_raw = fig_path.read_text(encoding='utf-8')
    q_raw = q_path.read_text(encoding='utf-8')
    fig = json.loads(fig_raw)
    q = json.loads(q_raw)
    attrib = q.get('attribution', {})
    prov = fig.get('_provenance', {})

    body = f"""
        <h1 class="section-title">The Art Engine</h1>
        <p class="section-intro">{esc(fig.get('what_this_is',''))}</p>

        <div class="attribution-banner">
            <span class="label">Whose art is this?</span>
            <p><strong>{esc(attrib.get('engine_is',''))}</strong> — not Bruno's.
            {esc(attrib.get('why_labelled_this_way',''))}</p>
            <p class="attrib-bruno"><strong>Bruno's version:</strong>
            {esc(attrib.get('brunos_version',''))}</p>
        </div>

        <div class="engine-aim">
            <span class="label">The aim of the Art</span>
            <p>{esc(fig.get('aim_of_the_art',''))}</p>
        </div>

        <div class="engine-layout">
            <div class="engine-figure">
                <h3>Figura S</h3>
                <div id="state-readout" class="state-readout"></div>
                <div id="figure-s-mount"></div>
                <p class="caveat-line">The readout reports the state of the <em>figure</em>,
                never of the reader. Reaching E in the model is a fact about the model.</p>
            </div>
            <div class="engine-work">
                <h3>{esc(q['questions'][0]['title'])}
                    <span class="stage-en">{esc(q['questions'][0]['title_en'])}</span></h3>
                <p class="stage-prompt">{esc(q['questions'][0]['prompt'])}</p>
                <div id="stage-mount"></div>
                <div id="outcome-mount"></div>
            </div>
        </div>

        <p class="provenance-note">
            <strong>Provenance.</strong> Figure S transcribed from {esc(prov.get('source',''))},
            {esc(prov.get('locator',''))}. The dialectic follows Bonner's report of Llull's worked
            example (ACIV, MOG I, vii, 9–10: 441–2). Both are
            <code>{esc(prov.get('method',''))}</code> — the chart is a grid mangled into an ASCII
            column by text extraction and could not be parsed reliably. Verify against the printed
            chart before treating as authoritative.
        </p>

        <script type="application/json" id="figure-s-data">{fig_raw}</script>
        <script type="application/json" id="engine-data">{q_raw}</script>
        <script src="engine.js"></script>
    """
    return page_shell('The Art Engine', body, active_nav='Engine', depth=0,
                      subtitle="Llull's Figure S, as a working instrument")


DESIGN_GROUPS = [
    ("Start here", ["README", "ENGINE", "PRACTICES", "ARCHITECTURE"]),
    ("Interpretive frames", ["YATES", "STURLESE", "CLUCAS", "MERTENS", "WANG",
                             "BARENSTEIN", "COULIANO"]),
    ("Artifacts", ["WHEEL", "IMAGELAB", "SEALS", "CABALA", "FRENZIES", "VINCULA"]),
]


def _design_docs():
    d = BASE_DIR / 'docs' / 'design'
    if not d.exists():
        return []
    return sorted(d.glob('*.md'))


def _design_slug(stem):
    return 'design-' + stem.lower()


def render_design_index():
    docs = {f.stem: f for f in _design_docs()}
    if not docs:
        return None
    seen, sections = set(), []
    for title, names in DESIGN_GROUPS:
        cards = []
        for nm in names:
            f = docs.get(nm)
            if not f:
                continue
            seen.add(nm)
            text = f.read_text(encoding='utf-8')
            lines_ = text.splitlines()[1:]
            first = next((l.strip() for l in lines_
                          if l.strip() and not l.startswith('#')), '')
            first = re.sub(r'[*`\[\]]|\(.*?\)', '', first)[:230]
            cards.append(
                f'<a class="entity-card" href="{_design_slug(nm)}.html">'
                f'<div class="entity-card-head"><h3>{esc(nm)}.md</h3></div>'
                f'<p>{esc(first)}…</p></a>')
        if cards:
            sections.append(f'<h3 class="alpha-sub">{esc(title)}</h3>'
                            f'<div class="entity-grid">{"".join(cards)}</div>')
    extra = [n for n in docs if n not in seen]
    if extra:
        cards = ''.join(
            f'<a class="entity-card" href="{_design_slug(n)}.html">'
            f'<div class="entity-card-head"><h3>{esc(n)}.md</h3></div></a>'
            for n in sorted(extra))
        sections.append('<h3 class="alpha-sub">Other</h3>'
                        f'<div class="entity-grid">{cards}</div>')

    body = f"""
        <h1 class="section-title">Design Documents</h1>
        <p class="section-intro">The working design record: what this project decided, why, and
        where the evidence stops. These are proposals and arguments, not user documentation —
        including the places where a later reading overturned an earlier decision.</p>
        <div class="layer-strip">
            <span class="layer">PRACTICE</span><span class="arrow">+</span>
            <span class="layer">FRICTION</span><span class="arrow">+</span>
            <span class="layer">SCHOLARSHIP as playable variants</span>
        </div>
        {"".join(sections)}
    """
    return page_shell('Design Documents', body, active_nav='Designs', depth=0)


def render_design_doc(path):
    text = path.read_text(encoding='utf-8')
    body = f"""
        <div class="entity-nav"><a href="designs.html">&larr; All design documents</a></div>
        <article class="doc-body">{_md.render(text)}</article>
        <p class="provenance-note">Source: <code>docs/design/{esc(path.name)}</code> in the
        repository. Design documents are working records and may be superseded by later ones.</p>
    """
    return page_shell(path.stem, body, active_nav='Designs', depth=0,
                      subtitle='Design record')


def render_fantastica():
    """Bruno's side of the engine: the Art run on images. ENGINE.md §1b."""
    paths = {
        'fantastica-data': BASE_DIR / 'data' / 'fantastica.json',
        'figure-s-data':   BASE_DIR / 'data' / 'figure_s.json',
        'alphabet-data':   BASE_DIR / 'data' / 'alphabet_harvested.json',
        'atria-data':      BASE_DIR / 'data' / 'atria_harvested.json',
        'courts-data':     BASE_DIR / 'data' / 'images_harvested.json',
    }
    if not all(p.exists() for p in paths.values()):
        return None
    raw = {k: p.read_text(encoding='utf-8') for k, p in paths.items()}
    fa = json.loads(raw['fantastica-data'])
    prov = fa.get('_provenance', {})
    q = fa['question']

    attested = ''.join(f'<li>{esc(x)}</li>' for x in prov.get('what_is_attested', []))
    reconstructed = ''.join(f'<li>{esc(x)}</li>' for x in prov.get('what_is_reconstructed', []))
    powers = ''.join(
        f'<div class="power-card"><h4>{esc(p["power"])}</h4>'
        f'<div class="power-source">from {esc(p["supplied_by"])}</div>'
        f'<p>{esc(p["rule"])}</p></div>'
        for p in fa.get('power_sources', []))

    scripts = ''.join(
        f'<script type="application/json" id="{k}">{v}</script>' for k, v in raw.items())

    body = f"""
        <h1 class="section-title">Logica Fantastica</h1>
        <p class="section-intro">Llull's Art computes with letters. Bruno's computes with
        <em>images</em>, held in the <em>spiritus phantasticus</em> — which is why he had to build an
        image vocabulary before he could reason with it. Here the same dialectic runs on images
        composed from Bruno's own three systems.</p>

        <div class="attribution-banner recon">
            <span class="label">Scholarly reconstruction</span>
            <p>{esc(prov.get('why_it_is_defensible',''))}</p>
            <div class="recon-cols">
                <div><h4>Attested</h4><ul class="recon-list">{attested}</ul></div>
                <div><h4>Reconstructed by this project</h4><ul class="recon-list">{reconstructed}</ul></div>
            </div>
        </div>

        <h3 class="alpha-sub">One power, one system</h3>
        <p>{esc(fa.get('how_composition_works',''))}</p>
        <div class="power-grid">{powers}</div>

        <div class="engine-layout">
            <div class="engine-figure">
                <h3>Figura S</h3>
                <div id="fantastica-figure"></div>
                <p class="caveat-line">The readout reports the state of the <em>figure</em>, never of the reader.</p>
            </div>
            <div class="engine-work">
                <h3>{esc(q['title'])} <span class="stage-en">{esc(q['title_en'])}</span></h3>
                <p class="stage-prompt">{esc(q['prompt'])}</p>
                <div id="fantastica-stage"></div>
                <div id="fantastica-outcome"></div>
            </div>
        </div>

        <p class="provenance-note">
            <strong>Status: <code>{esc(prov.get('status',''))}</code>, confidence
            <code>{esc(prov.get('confidence',''))}</code>.</strong>
            Every component is drawn from the corpus; the wiring between them is not.
            Compare <a href="engine.html">the Art Engine</a>, which is Llull's attested version.
        </p>

        {scripts}
        <script src="fantastica.js"></script>
    """
    return page_shell('Logica Fantastica', body, active_nav='Fantastica', depth=0,
                      subtitle="The Art run on images, as Bruno's version requires")


# ============================================================
# PRACTICES  (primary layer — see docs/design/PRACTICES.md)
# ============================================================

def operability_badge(op):
    if not op:
        return ''
    cls = {'FULLY_OPERABLE': 'op-full', 'PARTIALLY_OPERABLE': 'op-partial',
           'REFERENCE_ONLY': 'op-ref'}.get(op, 'op-ref')
    return f'<span class="badge {cls}">{esc(op.replace("_", " ").lower())}</span>'


def attestation_badge(a):
    if not a:
        return ''
    cls = {'ATTESTED': 'att-attested', 'RECONSTRUCTED': 'att-reconstructed',
           'SPECULATIVE': 'att-speculative'}.get(a, 'att-speculative')
    return f'<span class="badge {cls}">{esc(a.lower())}</span>'


def grounding_badge(sm):
    if sm == 'CORPUS_GROUNDED':
        return '<span class="badge grounding-corpus">corpus-grounded</span>'
    if sm == 'LLM_GENERAL_KNOWLEDGE':
        return '<span class="badge grounding-general">general knowledge</span>'
    return f'<span class="badge grounding-general">{esc(sm)}</span>'


def render_practices_index(cur):
    rows = cur.execute("""
        SELECT slug, name, tradition, date_range, one_line, what_you_can_do,
               operability, source_method, confidence
        FROM practices ORDER BY sort_order, name
    """).fetchall()

    cards = []
    for slug, name, trad, dates, one_line, can_do, op, sm, conf in rows:
        cards.append(f"""
            <a class="entity-card practice-card" href="{esc(slug)}.html">
                <div class="entity-card-head">
                    <h3>{esc(name)}</h3>
                    {operability_badge(op)}
                </div>
                <div class="badge badge-cat">{esc(trad)}</div>
                <span class="badge badge-date">{esc(dates)}</span>
                {grounding_badge(sm)}
                <p>{esc(one_line)}</p>
                <p class="connection-line">{esc(can_do)}</p>
            </a>""")

    body = f"""
        <h1 class="section-title">Practices</h1>
        <p class="section-intro">The arts of memory, realised as concretely as the sources allow — step by step, so you can actually run them. Every step carries notes on where the Renaissance worldview and the practical interface diverge from what you expect. Scholarly readings that change the mechanics appear as playable variants, not footnotes.</p>
        <div class="layer-strip">
            <span class="layer">PRACTICE</span><span class="arrow">+</span>
            <span class="layer">FRICTION at every step</span><span class="arrow">+</span>
            <span class="layer">SCHOLARSHIP as playable variants</span>
        </div>
        <div class="entity-grid">{''.join(cards)}</div>
        <p class="provenance-note">
            <strong>Operability is graded honestly.</strong> <em>Fully operable</em> means every step is
            specified in the source. <em>Partially operable</em> means the core is specified and the gaps
            are marked. Steps we extended beyond the source are labelled <em>reconstructed</em>.
            Missing steps are never invented to make a system look complete.
        </p>
    """
    return page_shell('Practices', body, active_nav='Practices', depth=1)


def render_atrium_structure(structure_json):
    """Render the harvested 24x24 atria inventory, if present."""
    if not structure_json:
        return ''
    try:
        d = json.loads(structure_json)
    except (json.JSONDecodeError, TypeError):
        return ''
    atria = d.get('transcribed') or []
    if not atria:
        return ''

    form = d.get('atrium_form', {})
    rows = []
    for a in atria:
        att = a.get('position_mapping_attestation', '')
        pos = ', '.join(a.get('positions', [])[:8])
        rows.append(
            f'<tr><td>{a.get("number")}</td>'
            f'<td><strong>{esc(a.get("centre",""))}</strong></td>'
            f'<td>{attestation_badge(att)}</td>'
            f'<td class="pos-cells">{esc(pos)}…</td></tr>'
        )

    return f"""
        <h3>The Address Space</h3>
        <p>{esc(form.get('note',''))} Twenty-four atria × twenty-four positions =
        <strong>576 addressable loci</strong>, extracted from the source by
        <code>scripts/harvest_atria.py</code>.</p>
        <p class="caveat-line">{esc(d.get('caveat',''))}</p>
        <div class="table-scroll">
        <table class="atria-table">
            <thead><tr><th>#</th><th>Atrium</th><th>Position mapping</th><th>First positions</th></tr></thead>
            <tbody>{''.join(rows)}</tbody>
        </table>
        </div>
    """


def render_alphabet_structure(structure_json):
    """Render the harvested letter/cluster -> operator table, if present."""
    if not structure_json:
        return ''
    try:
        d = json.loads(structure_json)
    except (json.JSONDecodeError, TypeError):
        return ''
    if 'simple_keys' not in d:
        return ''

    def rows(keys):
        out = []
        for r in keys:
            cells = []
            for e in r['entries']:
                if e['kind'] == 'CROSS_REFERENCE':
                    cells.append(
                        f'<span class="op op-xref" title="{esc(e["note"])}">'
                        f'{esc(e["form"])} <em>as</em> {esc(e["use_image_of"])}</span>')
                else:
                    g = f' <span class="op-gloss">{esc(e["gloss"])}</span>' if e.get('gloss') else ''
                    sus = ' op-suspect' if e.get('ocr_suspect') else ''
                    t = ' title="Damaged or abbreviated in the source"' if e.get('ocr_suspect') else ''
                    cells.append(f'<span class="op{sus}"{t}>{esc(e["form"])}{g}</span>')
            out.append(f'<tr><th class="alpha-key">{esc(r["key"])}</th>'
                       f'<td><div class="op-row">{"".join(cells)}</div></td></tr>')
        return ''.join(out)

    c = d.get('counts', {})
    return f"""
        <h3>The Lookup Table</h3>
        <p>{esc(d.get('how_it_works',''))}</p>
        <p class="caveat-line">{esc(d.get('cross_reference_note',''))}</p>
        <h4 class="alpha-sub">Simple letters</h4>
        <div class="table-scroll"><table class="alpha-table"><tbody>{rows(d['simple_keys'])}</tbody></table></div>
        <h4 class="alpha-sub">Consonant clusters</h4>
        <div class="table-scroll"><table class="alpha-table"><tbody>{rows(d['cluster_keys'])}</tbody></table></div>
        <p class="caveat-line">{esc(d.get('caveat',''))}
        {c.get('operators',0)} operators · {c.get('cross_references',0)} cross-references ·
        {c.get('ocr_suspect',0)} flagged as damaged. Extracted by
        <code>scripts/harvest_alphabet.py</code>.</p>
    """


def render_practice_detail(cur, row):
    (slug, name, trad, dates, source_text, one_line, can_do, op, op_note,
     preface, structure, sm, rs, conf) = row

    steps = cur.execute("""
        SELECT step_number, title, instruction, attestation, source_locator
        FROM practice_steps WHERE practice_slug = ? ORDER BY step_number
    """, (slug,)).fetchall()

    frictions = cur.execute("""
        SELECT step_number, kind, difficulty, explanation
        FROM frictions WHERE practice_slug = ? ORDER BY step_number, kind
    """, (slug,)).fetchall()

    fr_by_step = {}
    for n, kind, diff, expl in frictions:
        fr_by_step.setdefault(n, []).append((kind, diff, expl))

    def friction_html(items):
        out = []
        for kind, diff, expl in items:
            cls = 'friction-worldview' if kind == 'WORLDVIEW' else 'friction-interface'
            label = 'Worldview' if kind == 'WORLDVIEW' else 'Interface'
            out.append(f"""
                <div class="friction {cls}">
                    <span class="friction-label">{label}</span>
                    <p class="friction-difficulty">“{esc(diff)}”</p>
                    <p class="friction-explanation">{esc(expl)}</p>
                </div>""")
        return ''.join(out)

    step_html = []
    for n, title, instr, att, loc in steps:
        step_html.append(f"""
            <li class="step">
                <div class="step-head">
                    <span class="step-num">{n}</span>
                    <h3>{esc(title)}</h3>
                    {attestation_badge(att)}
                </div>
                <p class="step-instruction">{esc(instr)}</p>
                {f'<p class="step-locator">{esc(loc)}</p>' if loc else ''}
                {friction_html(fr_by_step.get(n, []))}
            </li>""")

    general = friction_html(fr_by_step.get(None, []))

    variants = cur.execute("""
        SELECT name, scholar_slug, what_changes, playable_as, testability_tier,
               superseded, notes
        FROM practice_variants WHERE practice_slug = ?
    """, (slug,)).fetchall()

    var_html = ''
    if variants:
        items = []
        for vname, vsch, changes, playable, tier, sup, notes in variants:
            sch = ''
            if vsch:
                r = cur.execute("SELECT name FROM scholars WHERE slug = ?", (vsch,)).fetchone()
                if r:
                    sch = f' — <a href="../scholars/{esc(vsch)}.html">{esc(r[0])}</a>'
            supmark = ('<span class="badge att-reconstructed">superseded, still playable</span>'
                       if sup else '')
            items.append(f"""
                <div class="variant">
                    <h4>{esc(vname)}{sch} {supmark}</h4>
                    <p><strong>What changes:</strong> {esc(changes)}</p>
                    <p><strong>Playable as:</strong> {esc(playable)}</p>
                    {f'<p class="ref-note">{esc(notes)}</p>' if notes else ''}
                </div>""")
        var_html = f"""
            <h3>Playable Variants</h3>
            <p class="section-body">Scholarly readings that change the mechanics. A reading that
            changes nothing mechanically is commentary, and lives in the scholarship layer instead.</p>
            {''.join(items)}
        """

    body = f"""
        <div class="entity-nav"><a href="index.html">&larr; All Practices</a></div>
        <div class="entity-detail practice-detail">
            <div class="entity-header">
                <h1>{esc(name)}</h1>
                <div class="entity-meta">
                    <span class="badge badge-cat">{esc(trad)}</span>
                    <span class="badge badge-date">{esc(dates)}</span>
                    {operability_badge(op)}
                    {grounding_badge(sm)}
                    {confidence_badge(conf)}
                </div>
                <p class="region">{esc(source_text)}</p>
            </div>

            <p class="lead">{esc(one_line)}</p>

            <div class="connection-callout">
                <span class="label">What you can actually do</span>
                {esc(can_do)}
            </div>

            {f'''<div class="worldview-preface">
                <span class="label">Before you start</span>
                <p>{esc(preface)}</p>
            </div>''' if preface else ''}

            {f'<h3>Operability</h3><p>{esc(op_note)}</p>' if op_note else ''}
            {general}

            <h3>The Practice</h3>
            <ol class="steps">{''.join(step_html)}</ol>

            {render_atrium_structure(structure)}
            {render_alphabet_structure(structure)}
            {var_html}

            <div class="entity-footer">
                {provenance_line(sm, rs, conf)}
            </div>
        </div>
    """
    return page_shell(name, body, active_nav='Practices', depth=1)


# ============================================================
# WORKS
# ============================================================

def render_works_index(cur):
    rows = cur.execute("""
        SELECT slug, title_original, title_english, work_type, date_written,
               summary, memory_magic_connection, memory_magic_relevance, confidence
        FROM works ORDER BY
            CASE memory_magic_relevance WHEN 'CENTRAL' THEN 0 WHEN 'MAJOR' THEN 1 WHEN 'SUPPORTING' THEN 2 ELSE 3 END,
            date_written
    """).fetchall()

    cards = []
    for slug, orig, eng, wtype, date, summary, conn, rel, conf in rows:
        title = f'{esc(orig)}' + (f' <span style="color:var(--text-muted); font-weight:400;">({esc(eng)})</span>' if eng else '')
        cards.append(f"""
            <a class="entity-card" href="{esc(slug)}.html">
                <div class="entity-card-head">
                    <h3>{title}</h3>
                    {relevance_badge(rel)}
                </div>
                <div class="badge badge-cat">{esc(wtype)}</div> <span class="badge badge-date">{esc(date)}</span>
                <p>{esc(summary)}</p>
                <p class="connection-line">{esc(conn[:160])}{'…' if conn and len(conn) > 160 else ''}</p>
            </a>""")

    body = f"""
        <h1 class="section-title">Works</h1>
        <p class="section-intro">Bruno&rsquo;s mnemonic treatises, magical texts, and poetic/philosophical dialogues — including the full magical and poetic corpus, from De umbris idearum to De gli eroici furori. Sorted by how central each work is to the memory/magic project.</p>
        <div class="entity-grid">{''.join(cards)}</div>
    """
    return page_shell('Works', body, active_nav='Works', depth=1)


def render_work_detail(cur, row):
    (id_, slug, orig, eng, wtype, lang, dw, dp, place, summary, conn, rel,
     key_ed, notable, tags, sm, rs, cf) = row

    editions = jparse(key_ed)
    ed_html = ''
    if editions:
        items = ''.join(f'<li class="ref-item">{esc(e.get("editor",""))} ({esc(e.get("year",""))}) — {esc(e.get("note",""))}</li>' for e in editions)
        ed_html = f'<h3>Key Editions</h3><ul class="ref-list">{items}</ul>'

    images = cur.execute("SELECT slug, name FROM images WHERE work_slug = ?", (slug,)).fetchall()
    img_html = ''
    if images:
        items = ''.join(f'<li class="ref-item"><a href="../images/{esc(s)}.html">{esc(n)}</a></li>' for s, n in images)
        img_html = f'<h3>Images From This Work</h3><ul class="ref-list">{items}</ul>'

    body = f"""
        <div class="entity-nav"><a href="index.html">&larr; All Works</a></div>
        <div class="entity-detail">
            <div class="entity-header">
                <h1>{esc(orig)}</h1>
                <div class="title-original">{esc(eng) if eng else ''}</div>
                <div class="entity-meta">
                    <span class="badge badge-cat">{esc(wtype)}</span>
                    <span class="badge badge-date">{esc(dw)}</span>
                    {relevance_badge(rel)}
                    {confidence_badge(cf)}
                </div>
                <p class="region">{esc(lang)} &middot; published {esc(dp) if dp else 'n/a'}{' in ' + esc(place) if place else ''}</p>
            </div>

            <div class="summary"><p>{esc(summary)}</p></div>

            <div class="connection-callout">
                <span class="label">Memory / Magic Connection</span>
                {esc(conn)}
            </div>

            {section_notable(notable)}
            {ed_html}
            {img_html}
            {refs_block(cur, 'work', slug)}

            <div class="entity-footer">
                {tag_list(tags)}
                {provenance_line(sm, rs, cf)}
            </div>
        </div>
    """
    return page_shell(orig, body, active_nav='Works', depth=1)


def section_notable(notable):
    if not notable:
        return ''
    return f'<h3>Notable Content</h3><p>{esc(notable)}</p>'


# ============================================================
# IMAGES
# ============================================================

def render_image_courts():
    """
    Bruno's planetary image-courts, from data/images_harvested.json
    (scripts/harvest_images.py). See HARVEST.md H-02.
    """
    path = BASE_DIR / 'data' / 'images_harvested.json'
    if not path.exists():
        return None
    d = json.loads(path.read_text(encoding='utf-8'))
    src = d.get('source', {})

    blocks = []
    for c in d.get('courts', []):
        principals = ''.join(
            f'<div class="court-principal"><h4>{esc(p["heading"])}</h4>'
            f'<p class="court-excerpt">{esc(p["excerpt"][:180])}…</p>'
            f'<p class="step-locator">line {p["line"]}</p></div>'
            for p in c.get('principal_images', []))

        groups = []
        for g in c.get('attendant_groups', []):
            named = ''.join(
                f'<li class="ref-item"><strong>{esc(a["name"])}</strong> '
                f'<span class="ref-note">— {esc(a["excerpt"][:140])}…</span></li>'
                for a in g.get('attendants', []))
            inline = ''.join(f'<span class="attendant">{esc(x)}</span>'
                             for x in g.get('inline_attendants', []))
            groups.append(f"""
                <div class="court-group">
                    <h4>{esc(g['group'])} <span class="step-locator">line {g['line']}</span></h4>
                    {f'<div class="attendant-cloud">{inline}</div>' if inline else ''}
                    {f'<ul class="ref-list">{named}</ul>' if named else ''}
                </div>""")

        n_named = sum(len(g.get('attendants', [])) for g in c.get('attendant_groups', []))
        n_inline = sum(len(g.get('inline_attendants', [])) for g in c.get('attendant_groups', []))
        blocks.append(f"""
            <section class="court" id="court-{esc(c['planet'].split()[0].lower())}">
                <h3 class="court-title">{esc(c['planet'])}</h3>
                <p class="court-meta">opens at line {c['opens_at_line']} ·
                   {len(c.get('principal_images', []))} principal ·
                   {n_named} named attendants · {n_inline} in retinue lists</p>
                {principals}
                {''.join(groups)}
            </section>""")

    toc = ' · '.join(
        f'<a href="#court-{esc(c["planet"].split()[0].lower())}">{esc(c["planet"])}</a>'
        for c in d.get('courts', []))

    counts = d.get('counts', {})
    body = f"""
        <div class="entity-nav"><a href="index.html">&larr; Images</a></div>
        <h1 class="section-title">The Planetary Image-Courts</h1>
        <p class="section-intro">{esc(d.get('structure_note',''))}</p>
        <div class="layer-strip">{toc}</div>
        <p class="provenance-note">
            <strong>{counts.get('courts',0)} courts · {counts.get('principal_images',0)} principal images ·
            {counts.get('inline_attendants',0)} attendants.</strong>
            Extracted from {esc(src.get('work',''))}, trans. {esc(src.get('translator',''))},
            {esc(src.get('range',''))}, by <code>scripts/harvest_images.py</code>.
            <strong>Rights:</strong> the Higgins translation is in copyright. Reproduced here are
            short attributed excerpts for scholarly comment, plus structural inventories (names,
            positions, retinue lists) which are data rather than expression. Consult the published
            translation for the full text. Retinue lists are parsed from running prose, so
            occasional fragments survive.
        </p>
        {''.join(blocks)}
    """
    return page_shell('Planetary Image-Courts', body, active_nav='Images', depth=1)


def render_images_index(cur):
    rows = cur.execute("""
        SELECT slug, name, work_slug, image_role, description, reconstruction_level, confidence
        FROM images ORDER BY name
    """).fetchall()

    cards = []
    for slug, name, work_slug, role, desc, recon, conf in rows:
        cards.append(f"""
            <a class="entity-card" href="{esc(slug)}.html">
                <div class="entity-card-head">
                    <h3>{esc(name)}</h3>
                    {confidence_badge(conf)}
                </div>
                <div class="badge badge-cat">{esc(role)}</div>
                <p>{esc(desc)}</p>
            </a>""")

    body = f"""
        <h1 class="section-title">Images</h1>
        <p class="section-intro">Individual mnemonic and magical images Bruno used, addressed as their own cards — what each does operationally, alongside what it depicts, and how reconstructed vs. historically attested each reading is.</p>
        <div class="home-card" style="margin-bottom:1.5rem;">
            <h2><a href="courts.html">The Planetary Image-Courts &rarr;</a></h2>
            <p>Bruno&rsquo;s image gallery is not a flat list. It is organised as planetary courts — each deity
            with a principal image and a named retinue. Saturn&rsquo;s attendants are the melancholic afflictions;
            Luna&rsquo;s are split by phase. 241 attendants, extracted from <em>De imaginum</em>.</p>
        </div>
        <div class="entity-grid">{''.join(cards)}</div>
    """
    return page_shell('Images', body, active_nav='Images', depth=1)


def render_image_detail(cur, row):
    (id_, slug, name, work_slug, role, desc, what_it_does, recon, sch_interp, img_file, tags, sm, rs, cf) = row

    work_link = ''
    if work_slug:
        w = cur.execute("SELECT title_original FROM works WHERE slug = ?", (work_slug,)).fetchone()
        if w:
            work_link = f'<p class="region">From <a href="../works/{esc(work_slug)}.html">{esc(w[0])}</a></p>'

    recon_html = f'<h3>Reconstruction Level</h3><p><span class="badge badge-cat">{esc(recon)}</span></p>' if recon else ''
    interp_html = f'<h3>Scholarly Interpretation</h3><p>{esc(sch_interp)}</p>' if sch_interp else ''

    body = f"""
        <div class="entity-nav"><a href="index.html">&larr; All Images</a></div>
        <div class="entity-detail">
            <div class="entity-header">
                <h1>{esc(name)}</h1>
                <div class="entity-meta"><span class="badge badge-cat">{esc(role)}</span>{confidence_badge(cf)}</div>
                {work_link}
            </div>
            <div class="summary"><p>{esc(desc)}</p></div>
            {f'<div class="connection-callout"><span class="label">What It Does</span>{esc(what_it_does)}</div>' if what_it_does else ''}
            {recon_html}
            {interp_html}
            {refs_block(cur, 'image', slug)}
            <div class="entity-footer">
                {tag_list(tags)}
                {provenance_line(sm, rs, cf)}
            </div>
        </div>
    """
    return page_shell(name, body, active_nav='Images', depth=1)


# ============================================================
# SCHOLARS
# ============================================================

def render_scholars_index(cur):
    rows = cur.execute("""
        SELECT slug, name, birth_year, death_year, interpretation_summary, confidence
        FROM scholars ORDER BY birth_year IS NULL, birth_year, name
    """).fetchall()

    cards = []
    for slug, name, by, dy, summ, conf in rows:
        dates = f'{by or "?"}–{dy or "?"}' if (by or dy) else ''
        cards.append(f"""
            <a class="entity-card" href="{esc(slug)}.html">
                <div class="entity-card-head">
                    <h3>{esc(name)}</h3>
                    {confidence_badge(conf)}
                </div>
                <div class="badge badge-date">{esc(dates)}</div>
                <p>{esc(summ)}</p>
            </a>""")

    body = f"""
        <h1 class="section-title">Scholars</h1>
        <p class="section-intro">Interpreters of Bruno&rsquo;s memory and magic. Each profile is a position within the field, not a settled biography — cross-reference with Disputes for where they explicitly disagree.</p>
        <div class="entity-grid">{''.join(cards)}</div>
    """
    return page_shell('Scholars', body, active_nav='Scholars', depth=1)


def render_scholar_detail(cur, row):
    (id_, slug, name, by, dy, affil, interp_summ, v_mem, v_imag, v_img, v_magic,
     v_neo, v_plot, v_fic, v_wheel, v_seal, major_works, tags, sm, rs, cf) = row

    views = [
        ('Memory', v_mem), ('Imagination', v_imag), ('Images', v_img), ('Magic', v_magic),
        ('Neoplatonism', v_neo), ('Plotinus', v_plot), ('Ficino', v_fic),
        ('Mnemonic Wheels', v_wheel), ('Seals / Simulacra', v_seal),
    ]
    views_html = ''.join(f'<h3>{esc(k)}</h3><p>{esc(v)}</p>' for k, v in views if v)

    works = jparse(major_works)
    works_html = ''
    if works:
        items = ''.join(f'<li class="ref-item">{esc(w.get("title",""))} ({esc(w.get("year",""))})</li>' for w in works)
        works_html = f'<h3>Major Bruno Works</h3><ul class="ref-list">{items}</ul>'

    disputes = cur.execute("""
        SELECT slug, topic FROM disputes
        WHERE position_a_scholar_slug = ? OR position_b_scholar_slug = ?
    """, (slug, slug)).fetchall()
    disp_html = ''
    if disputes:
        items = ''.join(f'<li class="ref-item"><a href="../disputes/{esc(s)}.html">{esc(t)}</a></li>' for s, t in disputes)
        disp_html = f'<h3>Involved In These Disputes</h3><ul class="ref-list">{items}</ul>'

    dates = f'{by or "?"}–{dy or "?"}' if (by or dy) else ''

    body = f"""
        <div class="entity-nav"><a href="index.html">&larr; All Scholars</a></div>
        <div class="entity-detail">
            <div class="entity-header">
                <h1>{esc(name)}</h1>
                <div class="entity-meta"><span class="badge badge-date">{esc(dates)}</span>{confidence_badge(cf)}</div>
                <p class="region">{esc(affil) if affil else ''}</p>
            </div>
            <div class="connection-callout">
                <span class="label">Interpretation Summary</span>
                {esc(interp_summ)}
            </div>
            {views_html}
            {works_html}
            {disp_html}
            {refs_block(cur, 'scholar', slug)}
            <div class="entity-footer">
                {tag_list(tags)}
                {provenance_line(sm, rs, cf)}
            </div>
        </div>
    """
    return page_shell(name, body, active_nav='Scholars', depth=1)


# ============================================================
# DISPUTES
# ============================================================

def render_disputes_index(cur):
    rows = cur.execute("SELECT slug, topic, resolution, confidence FROM disputes ORDER BY topic").fetchall()
    cards = []
    for slug, topic, res, conf in rows:
        cards.append(f"""
            <a class="entity-card" href="{esc(slug)}.html">
                <div class="entity-card-head">
                    <h3>{esc(topic)}</h3>
                    {confidence_badge(conf)}
                </div>
                {resolution_badge(res)}
            </a>""")
    body = f"""
        <h1 class="section-title">Disputes</h1>
        <p class="section-intro">Scholarly disagreements about Bruno&rsquo;s memory and magic, presented as two positions with evidence. Resolution status reflects the state of the field, not this project&rsquo;s judgment.</p>
        <div class="entity-grid">{''.join(cards)}</div>
    """
    return page_shell('Disputes', body, active_nav='Disputes', depth=1)


def render_dispute_detail(cur, row):
    (id_, slug, topic, a_slug, a_text, b_slug, b_text, resolution, res_note, tags, sm, rs, cf) = row

    def scholar_name(s):
        if not s:
            return None
        r = cur.execute("SELECT name FROM scholars WHERE slug = ?", (s,)).fetchone()
        return r[0] if r else s

    a_name = scholar_name(a_slug)
    b_name = scholar_name(b_slug)
    a_link = f'<a href="../scholars/{esc(a_slug)}.html">{esc(a_name)}</a>' if a_slug else 'Position A'
    b_link = f'<a href="../scholars/{esc(b_slug)}.html">{esc(b_name)}</a>' if b_slug else 'Position B'

    body = f"""
        <div class="entity-nav"><a href="index.html">&larr; All Disputes</a></div>
        <div class="entity-detail">
            <div class="entity-header">
                <h1>{esc(topic)}</h1>
                <div class="entity-meta">{resolution_badge(resolution)}{confidence_badge(cf)}</div>
            </div>

            <div class="dispute-positions">
                <div class="dispute-position position-a">
                    <h4>{a_link}</h4>
                    <p>{esc(a_text)}</p>
                </div>
                <div class="dispute-position position-b">
                    <h4>{b_link}</h4>
                    <p>{esc(b_text)}</p>
                </div>
            </div>

            {f'<h3>Resolution Note</h3><p>{esc(res_note)}</p>' if res_note else ''}
            {refs_block(cur, 'dispute', slug)}

            <div class="entity-footer">
                {tag_list(tags)}
                {provenance_line(sm, rs, cf)}
            </div>
        </div>
    """
    return page_shell(topic, body, active_nav='Disputes', depth=1)


# ============================================================
# TIMELINE (biographical_events)
# ============================================================

def render_timeline_index(cur):
    rows = cur.execute("SELECT slug, title, year, summary, confidence FROM biographical_events ORDER BY year").fetchall()
    items = []
    for slug, title, year, summary, conf in rows:
        items.append(f"""
            <a class="timeline-item" href="{esc(slug)}.html">
                <div class="timeline-date">{esc(year)}</div>
                <div class="timeline-body">
                    <h3>{esc(title)}</h3>
                    <p>{esc(summary)}</p>
                    <div class="timeline-meta">{confidence_badge(conf)}</div>
                </div>
            </a>""")
    body = f"""
        <h1 class="section-title">Timeline</h1>
        <p class="section-intro">Bruno&rsquo;s life, filtered to events that bear specifically on his memory and magic system — not a general biography. Every entry states explicitly why it matters to that story.</p>
        <div class="timeline">{''.join(items)}</div>
    """
    return page_shell('Timeline', body, active_nav='Timeline', depth=1)


def render_event_detail(cur, row):
    (id_, slug, title, year, place, summary, conn, related, tags, sm, rs, cf) = row

    related_slugs = jparse(related)
    related_html = ''
    if related_slugs:
        items = []
        for ws in related_slugs:
            w = cur.execute("SELECT title_original FROM works WHERE slug = ?", (ws,)).fetchone()
            if w:
                items.append(f'<li class="ref-item"><a href="../works/{esc(ws)}.html">{esc(w[0])}</a></li>')
        if items:
            related_html = f'<h3>Related Works</h3><ul class="ref-list">{"".join(items)}</ul>'

    body = f"""
        <div class="entity-nav"><a href="index.html">&larr; Timeline</a></div>
        <div class="entity-detail">
            <div class="entity-header">
                <h1>{esc(title)}</h1>
                <div class="entity-meta"><span class="badge badge-date">{esc(year)}</span>{confidence_badge(cf)}</div>
                <p class="region">{esc(place) if place else ''}</p>
            </div>
            <div class="summary"><p>{esc(summary)}</p></div>
            <div class="connection-callout">
                <span class="label">Memory / Magic Connection</span>
                {esc(conn)}
            </div>
            {related_html}
            {refs_block(cur, 'event', slug)}
            <div class="entity-footer">
                {tag_list(tags)}
                {provenance_line(sm, rs, cf)}
            </div>
        </div>
    """
    return page_shell(title, body, active_nav='Timeline', depth=1)


# ============================================================
# DICTIONARY (single page)
# ============================================================

def render_dictionary(cur):
    rows = cur.execute("""
        SELECT term_original, language, short_definition, bruno_usage,
               scholarly_interpretation, confidence
        FROM dictionary_terms ORDER BY term_original
    """).fetchall()

    entries = []
    for term, lang, short_def, usage, interp, conf in rows:
        extra = ''
        if usage:
            extra += f'<p class="dict-long"><strong>Bruno&rsquo;s usage:</strong> {esc(usage)}</p>'
        if interp:
            extra += f'<p class="dict-long"><strong>Scholarly interpretation:</strong> {esc(interp)}</p>'
        entries.append(f"""
            <div class="dict-entry">
                <h3>{esc(term)}</h3>
                <div class="dict-meta">{esc(lang)} {confidence_badge(conf)}</div>
                <p class="dict-short">{esc(short_def)}</p>
                {extra}
            </div>""")

    body = f"""
        <h1 class="section-title">Dictionary</h1>
        <p class="section-intro">Bruno&rsquo;s key vocabulary — memoria, phantasia, simulacrum, signaculum, umbra, vinculum, and more — with his own usage and scholarly interpretation held apart.</p>
        <div class="dict-list">{''.join(entries)}</div>
    """
    return page_shell('Dictionary', body, active_nav='Dictionary', depth=0)


# ============================================================
# ESSAYS
# ============================================================

def render_essays_index(cur):
    rows = cur.execute("SELECT slug, title, subtitle, summary, confidence FROM essays ORDER BY title").fetchall()
    cards = []
    for slug, title, subtitle, summary, conf in rows:
        cards.append(f"""
            <a class="essay-card" href="{esc(slug)}.html">
                <h3>{esc(title)}</h3>
                <div class="essay-subtitle">{esc(subtitle) if subtitle else ''}</div>
                <p>{esc(summary) if summary else ''}</p>
            </a>""")
    body = f"""
        <h1 class="section-title">Essays</h1>
        <p class="section-intro">Long-form pieces threading multiple works, scholars, and concepts together.</p>
        <div class="essay-list">{''.join(cards)}</div>
    """
    return page_shell('Essays', body, active_nav='Essays', depth=1)


def render_essay_detail(cur, row):
    (id_, slug, title, subtitle, summary, body_text, related, sm, rs, cf) = row

    paras = render_paragraphs(body_text)

    related_items = jparse(related)
    related_html = ''
    if related_items:
        link_map = {'scholar': '../scholars/', 'work': '../works/', 'image': '../images/', 'term': None, 'dispute': '../disputes/'}
        items = []
        for r in related_items:
            rtype, rslug, rlabel = r.get('type'), r.get('slug'), r.get('label')
            prefix = link_map.get(rtype)
            if prefix:
                items.append(f'<li><span class="related-type">{esc(rtype)}</span> — <a href="{prefix}{esc(rslug)}.html">{esc(rlabel)}</a></li>')
            elif rtype == 'term':
                items.append(f'<li><span class="related-type">term</span> — <a href="../dictionary.html">{esc(rlabel)}</a></li>')
            else:
                items.append(f'<li><span class="related-type">{esc(rtype)}</span> — {esc(rlabel)}</li>')
        related_html = f'<div class="related-entities"><h3>Related</h3><ul>{"".join(items)}</ul></div>'

    body = f"""
        <div class="entity-nav"><a href="index.html">&larr; All Essays</a></div>
        <article class="essay">
            <h1 class="section-title">{esc(title)}</h1>
            {f'<p class="essay-subtitle">{esc(subtitle)}</p>' if subtitle else ''}
            {f'<div class="essay-summary">{esc(summary)}</div>' if summary else ''}
            <div class="essay-body">{paras}</div>
            {related_html}
            <div class="entity-footer">{provenance_line(sm, rs, cf)}</div>
        </article>
    """
    return page_shell(title, body, active_nav='Essays', depth=1)


# ============================================================
# APP-MODE IDEAS
# ============================================================

def render_ideas_index(cur):
    rows = cur.execute("""
        SELECT slug, name, mode_category, tone, description, status, confidence
        FROM app_mode_ideas ORDER BY
            CASE tone WHEN 'COMEDIC' THEN 0 WHEN 'SATIRICAL' THEN 1 WHEN 'PLAYFUL' THEN 2 ELSE 3 END, name
    """).fetchall()
    cards = []
    for slug, name, cat, tone, desc, status, conf in rows:
        tone_cls = f"tone-{tone.lower()}" if tone else ''
        cards.append(f"""
            <div class="mode-card {tone_cls}">
                <div class="entity-card-head">
                    <h3><a href="{esc(slug)}.html">{esc(name)}</a></h3>
                    {tone_badge(tone)}
                </div>
                <div class="badge badge-cat">{esc(cat)}</div>
                <span class="mode-status">{esc(status)}</span>
                <p>{esc(desc)}</p>
            </div>""")
    body = f"""
        <h1 class="section-title">App-Mode Ideas</h1>
        <p class="section-intro">Interactive tool and game concepts, grounded in specific works — serious modes (Vinculum/Bond, Seal Lab, Actaeon&rsquo;s Chamber) alongside explicitly comic ones for the Cabala del cavallo pegaseo, licensed by Bruno&rsquo;s own use of satire.</p>
        {''.join(cards)}
    """
    return page_shell('App-Mode Ideas', body, active_nav='App Ideas', depth=1)


def render_idea_detail(cur, row):
    (id_, slug, name, cat, based_on, frames, tone, desc, why, status, tags, sm, cf) = row

    based_on_slugs = jparse(based_on)
    based_html = ''
    if based_on_slugs:
        items = []
        for ws in based_on_slugs:
            w = cur.execute("SELECT title_original FROM works WHERE slug = ?", (ws,)).fetchone()
            if w:
                items.append(f'<li class="ref-item"><a href="../works/{esc(ws)}.html">{esc(w[0])}</a></li>')
        if items:
            based_html = f'<h3>Based On</h3><ul class="ref-list">{"".join(items)}</ul>'

    frame_slugs = jparse(frames)
    frames_html = ''
    if frame_slugs:
        items = []
        for fs in frame_slugs:
            s = cur.execute("SELECT name FROM scholars WHERE slug = ?", (fs,)).fetchone()
            if s:
                items.append(f'<li class="ref-item"><a href="../scholars/{esc(fs)}.html">{esc(s[0])}</a></li>')
        if items:
            frames_html = f'<h3>Scholar Frames</h3><ul class="ref-list">{"".join(items)}</ul>'

    body = f"""
        <div class="entity-nav"><a href="index.html">&larr; All Ideas</a></div>
        <div class="entity-detail">
            <div class="entity-header">
                <h1>{esc(name)}</h1>
                <div class="entity-meta">
                    <span class="badge badge-cat">{esc(cat)}</span>
                    {tone_badge(tone)}
                    <span class="mode-status">{esc(status)}</span>
                    {confidence_badge(cf)}
                </div>
            </div>
            <div class="summary"><p>{esc(desc)}</p></div>
            {f'<div class="mode-grounding"><strong>Why this source supports it:</strong> {esc(why)}</div>' if why else ''}
            {based_html}
            {frames_html}
            <div class="entity-footer">
                {tag_list(tags)}
                {provenance_line(sm, 'DRAFT', cf)}
            </div>
        </div>
    """
    return page_shell(name, body, active_nav='App Ideas', depth=1)


# ============================================================
# BIBLIOGRAPHY (single page)
# ============================================================

def render_bibliography(cur):
    rows = cur.execute("""
        SELECT author, title, year, pub_type, relevance, annotation, online_url
        FROM bibliography ORDER BY year, author
    """).fetchall()
    entries = []
    for r in rows:
        author, title, year, ptype, rel, annot, url = r
        rel_cls = f"badge-{rel.lower()}" if rel else ''
        entries.append(f"""
            <div class="bib-entry">
                <h3>{esc(author)} ({esc(year) if year else 'n.d.'})</h3>
                <div class="bib-meta"><span class="badge {rel_cls}">{esc(rel)}</span> {esc(ptype)}</div>
                <p class="bib-annotation"><em>{esc(title)}</em>{'. ' + esc(annot) if annot else ''}</p>
            </div>""")
    body = f"""
        <h1 class="section-title">Bibliography</h1>
        <p class="section-intro">Primary and secondary sources cited throughout this project.</p>
        <div class="bib-list">{''.join(entries)}</div>
    """
    return page_shell('Bibliography', body, active_nav='Bibliography', depth=0)


# ============================================================
# RESEARCH QUESTIONS (static content page)
# ============================================================

def render_research_questions():
    body = """
        <h1 class="section-title">Open Research Questions</h1>
        <p class="section-intro">These stay visible, not resolved. See docs/RESEARCH_QUESTIONS.md for the full discussion.</p>
        <div class="entity-detail">
            <h3>Core Questions</h3>
            <p>How magical is Bruno&rsquo;s ars memoriae? What exactly does an image do? How should Plotinus be understood as background to Bruno? Is Bruno&rsquo;s image primarily mnemonic, psychological, metaphysical, magical, or all four? What is the relationship between phantasia and intellect? What does Bruno mean by &ldquo;shadow&rdquo;? What is a simulacrum, a signaculum, a vinculum? What is the role of desire? How does mnemonic discipline transform the soul? How reliable is Yates&rsquo;s reconstruction? Can we transcend the magic/science historiographical binary?</p>
            <h3>How These Are Used</h3>
            <p>Each question links to relevant works, scholars, and disputes elsewhere in this portal rather than being answered here. Explore Disputes and Scholars to see the live disagreement.</p>
        </div>
    """
    return page_shell('Open Questions', body, active_nav='Open Questions', depth=0)


# ============================================================
# ABOUT (static)
# ============================================================

def render_about():
    body = """
        <h1 class="section-title">About</h1>
        <div class="entity-detail">
            <p>BRUNOMEMAPP is a digital-humanities laboratory for studying and experimenting with Giordano Bruno&rsquo;s
            memory, imagination, magic, and philosophy. Bruno&rsquo;s primary texts and the scholarly interpretations of
            those texts become structured data that can generate interactive experimental tools — while keeping
            historical evidence, scholarly interpretation, reconstruction, and playful experimentation clearly distinct.</p>
            <h3>Architecture</h3>
            <p>SQLite source of truth (<code>db/bruno.db</code>), populated from a hand/LLM-curated seed
            (<code>bruno_seed.json</code>), rendered to this static site by Python scripts. No frameworks, no build step.
            Raw source-document extraction lives separately in <code>corpus/</code> and is not rendered to the site —
            it exists to ground and check the seed content. Pattern cribbed from WitcherPortal / AtalantaClaudiens.</p>
            <h3>Provenance discipline</h3>
            <p>Every entity carries <code>source_method</code>, <code>review_status</code>, and <code>confidence</code>.
            Works, images, and biographical events additionally carry a required, explicit statement of how they connect
            to memory/magic specifically — nothing is included just because it&rsquo;s &ldquo;about Bruno.&rdquo;</p>
        </div>
    """
    return page_shell('About', body, active_nav='About', depth=0)


# ============================================================
# SEARCH INDEX
# ============================================================

def build_search_index(cur):
    index = []
    for slug, title, summary in cur.execute("SELECT slug, name, one_line FROM practices"):
        index.append({'type': 'practice', 'title': title, 'summary': summary,
                      'href': f'practices/{slug}.html'})
    for slug, title, summary in cur.execute("SELECT slug, title_original, summary FROM works"):
        index.append({'type': 'work', 'title': title, 'summary': summary, 'href': f'works/{slug}.html'})
    for f in _design_docs():
        index.append({'type': 'design', 'title': f'{f.stem}.md',
                      'summary': 'Design document',
                      'href': f'{_design_slug(f.stem)}.html'})
    index.append({'type': 'engine', 'title': 'Logica Fantastica',
                  'summary': "The Art run on images -- Bruno's version",
                  'href': 'fantastica.html'})
    index.append({'type': 'engine', 'title': 'The Art Engine',
                  'summary': "Llull's Figure S as a working state machine",
                  'href': 'engine.html'})
    cp = BASE_DIR / 'data' / 'images_harvested.json'
    if cp.exists():
        for c in json.loads(cp.read_text(encoding='utf-8')).get('courts', []):
            index.append({'type': 'image-court', 'title': f"{c['planet']} — image-court",
                          'summary': 'Principal image and retinue from De imaginum',
                          'href': 'images/courts.html'})
    for slug, title, summary in cur.execute("SELECT slug, name, description FROM images"):
        index.append({'type': 'image', 'title': title, 'summary': summary, 'href': f'images/{slug}.html'})
    for slug, title, summary in cur.execute("SELECT slug, name, interpretation_summary FROM scholars"):
        index.append({'type': 'scholar', 'title': title, 'summary': summary, 'href': f'scholars/{slug}.html'})
    for slug, title in cur.execute("SELECT slug, topic FROM disputes"):
        index.append({'type': 'dispute', 'title': title, 'summary': None, 'href': f'disputes/{slug}.html'})
    for slug, title, summary in cur.execute("SELECT slug, title, summary FROM biographical_events"):
        index.append({'type': 'timeline', 'title': title, 'summary': summary, 'href': f'timeline/{slug}.html'})
    for slug, title, summary in cur.execute("SELECT slug, term_original, short_definition FROM dictionary_terms"):
        index.append({'type': 'term', 'title': title, 'summary': summary, 'href': f'dictionary.html'})
    for slug, title, summary in cur.execute("SELECT slug, title, summary FROM essays"):
        index.append({'type': 'essay', 'title': title, 'summary': summary, 'href': f'essays/{slug}.html'})
    for slug, title, summary in cur.execute("SELECT slug, name, description FROM app_mode_ideas"):
        index.append({'type': 'idea', 'title': title, 'summary': summary, 'href': f'ideas/{slug}.html'})
    return index


def render_search():
    body = """
        <h1 class="section-title">Search</h1>
        <input id="search-input" type="text" placeholder="Search works, images, scholars, disputes, timeline, dictionary, essays, ideas…" autofocus>
        <div id="search-results"><p class="section-intro">Type to search.</p></div>
    """
    return page_shell('Search', body, active_nav='Search', depth=0)


# ============================================================
# MAIN
# ============================================================

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    write(SITE_DIR / 'index.html', render_home(cur))

    # Practices (primary layer)
    write(SITE_DIR / 'practices' / 'index.html', render_practices_index(cur))
    for row in cur.execute("""
        SELECT slug, name, tradition, date_range, source_text, one_line,
               what_you_can_do, operability, operability_note, worldview_preface,
               structure_json, source_method, review_status, confidence
        FROM practices
    """).fetchall():
        write(SITE_DIR / 'practices' / f'{row[0]}.html', render_practice_detail(cur, row))

    # Works
    write(SITE_DIR / 'works' / 'index.html', render_works_index(cur))
    for row in cur.execute("""
        SELECT id, slug, title_original, title_english, work_type, language, date_written,
               date_published, place_published, summary, memory_magic_connection,
               memory_magic_relevance, key_editions, notable_content, tags,
               source_method, review_status, confidence
        FROM works
    """).fetchall():
        write(SITE_DIR / 'works' / f'{row[1]}.html', render_work_detail(cur, row))

    # Images
    write(SITE_DIR / 'images' / 'index.html', render_images_index(cur))
    courts_page = render_image_courts()
    if courts_page:
        write(SITE_DIR / 'images' / 'courts.html', courts_page)
    for row in cur.execute("""
        SELECT id, slug, name, work_slug, image_role, description, what_it_does,
               reconstruction_level, scholarly_interpretation, image_filename, tags,
               source_method, review_status, confidence
        FROM images
    """).fetchall():
        write(SITE_DIR / 'images' / f'{row[1]}.html', render_image_detail(cur, row))

    # Scholars
    write(SITE_DIR / 'scholars' / 'index.html', render_scholars_index(cur))
    for row in cur.execute("""
        SELECT id, slug, name, birth_year, death_year, affiliation, interpretation_summary,
               view_memory, view_imagination, view_images, view_magic, view_neoplatonism,
               view_plotinus, view_ficino, view_mnemonic_wheels, view_seals_simulacra,
               major_bruno_works, tags, source_method, review_status, confidence
        FROM scholars
    """).fetchall():
        write(SITE_DIR / 'scholars' / f'{row[1]}.html', render_scholar_detail(cur, row))

    # Disputes
    write(SITE_DIR / 'disputes' / 'index.html', render_disputes_index(cur))
    for row in cur.execute("""
        SELECT id, slug, topic, position_a_scholar_slug, position_a_text,
               position_b_scholar_slug, position_b_text, resolution, resolution_note,
               tags, source_method, review_status, confidence
        FROM disputes
    """).fetchall():
        write(SITE_DIR / 'disputes' / f'{row[1]}.html', render_dispute_detail(cur, row))

    # Timeline
    write(SITE_DIR / 'timeline' / 'index.html', render_timeline_index(cur))
    for row in cur.execute("""
        SELECT id, slug, title, year, place, summary, memory_magic_connection,
               related_work_slugs, tags, source_method, review_status, confidence
        FROM biographical_events
    """).fetchall():
        write(SITE_DIR / 'timeline' / f'{row[1]}.html', render_event_detail(cur, row))

    # Essays
    write(SITE_DIR / 'essays' / 'index.html', render_essays_index(cur))
    for row in cur.execute("""
        SELECT id, slug, title, subtitle, summary, body, related_entities,
               source_method, review_status, confidence
        FROM essays
    """).fetchall():
        write(SITE_DIR / 'essays' / f'{row[1]}.html', render_essay_detail(cur, row))

    # App-mode ideas
    write(SITE_DIR / 'ideas' / 'index.html', render_ideas_index(cur))
    for row in cur.execute("""
        SELECT id, slug, name, mode_category, based_on_work_slugs, scholar_frames, tone,
               description, why_this_source_supports_it, status, tags, source_method, confidence
        FROM app_mode_ideas
    """).fetchall():
        write(SITE_DIR / 'ideas' / f'{row[1]}.html', render_idea_detail(cur, row))

    # Single pages
    engine_page = render_engine()
    if engine_page:
        write(SITE_DIR / 'engine.html', engine_page)
    di = render_design_index()
    if di:
        write(SITE_DIR / 'designs.html', di)
        for f in _design_docs():
            write(SITE_DIR / f'{_design_slug(f.stem)}.html', render_design_doc(f))
    fa_page = render_fantastica()
    if fa_page:
        write(SITE_DIR / 'fantastica.html', fa_page)
    write(SITE_DIR / 'dictionary.html', render_dictionary(cur))
    write(SITE_DIR / 'bibliography.html', render_bibliography(cur))
    write(SITE_DIR / 'research-questions.html', render_research_questions())
    write(SITE_DIR / 'about.html', render_about())
    write(SITE_DIR / 'search.html', render_search())
    write(SITE_DIR / 'search-index.json', json.dumps(build_search_index(cur), ensure_ascii=False))

    conn.close()

    print(f"Site built at {SITE_DIR}")
    n_pages = sum(1 for _ in SITE_DIR.rglob('*.html'))
    print(f"  {n_pages} HTML pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
