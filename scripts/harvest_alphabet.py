"""
harvest_alphabet.py — Extract Bruno's image-alphabet from the Higgins translation.

Source: Giordano Bruno, *On the Composition of Images, Signs and Ideas*
(= De imaginum, 1591), Bk I Pt 2 chs 12-13, trans. Dick Higgins.
See HARVEST.md H-04.

Two tables, and together they are the letter/syllable -> image encoder that
makes the atria address space actually usable for words:

  SIMPLE   one initial letter -> ~5 Latin agent-nouns ("operators"):
           B -> Baptizans (one baptizing), Bellator (warrior),
                Bibliopola (bookseller), Boarius (cattle-dealer),
                Buccinator (trumpeter)

  CLUSTER  consonant clusters (Bl, Br, Cl, Cr, Fl, Fr, Gl, Gr, Pl, Pr,
           Sc, St, Str, Tr), some of which CROSS-REFER rather than carry
           their own image: "*Ble as Ple" = for Ble, use Ple's image.

Output: data/alphabet_harvested.json

Usage:  python scripts/harvest_alphabet.py
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS = Path(r"E:\pdf\renaissance magic\Bruno Lull\plain_text_drafts")
SOURCE = ("Giordano Bruno Dick Higgins On the Composition of Images Signs "
          "and Ideas Willis Locker Owens Publishing.txt")
OUT = BASE_DIR / "data" / "alphabet_harvested.json"

SIMPLE_RANGE = (2311, 2326)    # Baptizans … Vulneratus
CLUSTER_RANGE = (2333, 2340)   # Blactearius … Trutinans

# A cross-reference cell: "*Ble as Ple" -> use Ple's image for Ble.
XREF_RE = re.compile(r'^\*?([A-Z][a-z]{1,5})\s+as\s+([A-Z][a-z]{1,5})$')

# Glosses for the operators that a modern reader cannot be expected to know.
# Only where reasonably certain; unglossed entries are left unglossed rather
# than guessed at.
GLOSS = {
    'Baptizans': 'one baptizing', 'Bellator': 'warrior', 'Bibliopola': 'bookseller',
    'Boarius': 'cattle-dealer', 'Buccinator': 'trumpeter', 'Caupona': 'innkeeper',
    'Cerdo': 'cobbler / artisan', 'Circulator': 'street-performer', 'Colonus': 'farmer',
    'Custos': 'guard', 'Danista': 'money-lender', 'Delirus': 'madman',
    'Domitor': 'tamer', 'Dux': 'leader', 'Famulator': 'servant', 'Figulus': 'potter',
    'Fossor': 'digger', 'Fur': 'thief', 'Geometra': 'geometer', 'Gulosus': 'glutton',
    'Herbarius': 'herbalist', 'Histrio': 'actor', 'Hospes': 'host / guest',
    'Iaculator': 'javelin-thrower', 'Ieiunans': 'one fasting', 'Incantans': 'one enchanting',
    'Iocans': 'jester', 'Lector': 'reader', 'Luxuriosus': 'voluptuary',
    'Medicus': 'physician', 'Miles': 'soldier', 'Musicus': 'musician',
    'Nauta': 'sailor', 'Nutrix': 'nurse', 'Pastor': 'shepherd', 'Pictor': 'painter',
    'Puerpera': 'woman in childbirth', 'Raptor': 'ravisher', 'Rector': 'ruler',
    'Rusticus': 'peasant', 'Saltator': 'dancer', 'Sepultor': 'gravedigger',
    'Sigillator': 'sealer', 'Tinctor': 'dyer', 'Tonsor': 'barber',
    'Venator': 'hunter', 'Vitrarius': 'glassmaker', 'Gladiator': 'gladiator',
    'Clericus': 'cleric', 'Claviger': 'key-bearer', 'Scenicus': 'stage-player',
    'Statuarius': 'sculptor', 'Prudens': 'prudent one', 'Precans': 'one praying',
}

# Entries where the extraction is visibly damaged or abbreviated in the source.
SUSPECT = {'Go', 'Licto', 'Digladiat', 'Frondes spar.', 'Quumulatus',
           'Trophoearius', 'Blactearius', 'Glomer'}


def cells(line):
    """Split a table row into cells. Cross-refs contain spaces, so protect them."""
    line = line.strip()
    if not line:
        return []
    # Protect "*X as Y" before splitting on whitespace.
    line = re.sub(r'\*?([A-Z][a-z]{1,5})\s+as\s+([A-Z][a-z]{1,5})', r'\1~as~\2', line)
    line = re.sub(r'(Frondes)\s+(spar\.)', r'\1~\2', line)
    out = []
    for tok in line.split():
        t = tok.replace('~as~', ' as ').replace('~', ' ').strip('*').strip()
        if t:
            out.append(t)
    return out


def entry(tok):
    m = XREF_RE.match(tok)
    if m:
        return {'form': m.group(1), 'kind': 'CROSS_REFERENCE',
                'use_image_of': m.group(2),
                'note': f"For {m.group(1)}, use the image assigned to {m.group(2)}."}
    e = {'form': tok, 'kind': 'OPERATOR'}
    if tok in GLOSS:
        e['gloss'] = GLOSS[tok]
    if tok in SUSPECT:
        e['ocr_suspect'] = True
    return e


def main():
    src = CORPUS / SOURCE
    if not src.exists():
        print(f"ERROR: source not found: {src}")
        return 1
    lines = src.read_text(encoding='utf-8', errors='replace').splitlines()

    def rows(rng):
        return [(n, lines[n - 1]) for n in range(rng[0], rng[1] + 1)
                if lines[n - 1].strip() and lines[n - 1].strip() != '*']

    simple, cluster = [], []
    for n, raw in rows(SIMPLE_RANGE):
        cs = cells(raw)
        if not cs:
            continue
        simple.append({'key': cs[0][0].upper(), 'line': n,
                       'entries': [entry(c) for c in cs]})

    for n, raw in rows(CLUSTER_RANGE):
        cs = cells(raw)
        if not cs:
            continue
        key = re.match(r'^([A-Z][a-z]?)', cs[0])
        cluster.append({'key': key.group(1) if key else cs[0][:2], 'line': n,
                        'entries': [entry(c) for c in cs]})

    # Merge continuation rows (a row whose key repeats the previous one).
    merged = []
    for row in cluster:
        if merged and row['key'][0] == merged[-1]['key'][0] and len(row['entries']) < 5:
            merged[-1]['entries'].extend(row['entries'])
        else:
            merged.append(row)
    cluster = merged

    n_ops = sum(1 for r in simple + cluster for e in r['entries'] if e['kind'] == 'OPERATOR')
    n_x = sum(1 for r in simple + cluster for e in r['entries'] if e['kind'] == 'CROSS_REFERENCE')
    n_susp = sum(1 for r in simple + cluster for e in r['entries'] if e.get('ocr_suspect'))

    payload = {
        'source': {
            'work': 'On the Composition of Images, Signs and Ideas (De imaginum, 1591)',
            'translator': 'Dick Higgins',
            'locus': 'Book I, Part 2, chapters 12-13',
            'lines': {'simple': list(SIMPLE_RANGE), 'cluster': list(CLUSTER_RANGE)},
            'file': SOURCE,
        },
        'how_it_works': (
            'Each initial letter or consonant cluster carries a small set of Latin '
            'agent-nouns -- "operators", people defined by what they do. To encode a '
            'word, take its opening letter or cluster and use one of that key\'s '
            'operators as the image. Chapter 13 adds that each operator "receives the '
            'six differences which are sought in the six double triangles of the minor '
            'chambers", so a single operator can be inflected six ways.'
        ),
        'cross_reference_note': (
            'Asterisked cells are cross-references, not images: "*Ble as Ple" means '
            'the syllable Ble borrows the image assigned to Ple. Bruno economises by '
            'sharing images between phonetically close clusters.'
        ),
        'caveat': (
            'A handful of cells are damaged or abbreviated in the source text and are '
            'flagged ocr_suspect (e.g. "Go", "Licto", "Frondes spar."). Glosses are '
            'given only where reasonably certain; the rest are left unglossed rather '
            'than guessed.'
        ),
        'simple_keys': simple,
        'cluster_keys': cluster,
        'counts': {
            'simple_keys': len(simple), 'cluster_keys': len(cluster),
            'operators': n_ops, 'cross_references': n_x, 'ocr_suspect': n_susp,
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f"Wrote {OUT}")
    for k, v in payload['counts'].items():
        print(f"  {k:18} {v}")
    print()
    for r in simple:
        forms = ', '.join(e['form'] for e in r['entries'])
        print(f"  {r['key']:<4} {forms}")
    print()
    for r in cluster:
        forms = ', '.join(
            f"{e['form']} as {e['use_image_of']}" if e['kind'] == 'CROSS_REFERENCE' else e['form']
            for e in r['entries'])
        print(f"  {r['key']:<4} {forms[:110]}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
