"""
harvest_images.py — Extract Bruno's planetary image-courts from the Higgins translation.

Source: Giordano Bruno, *On the Composition of Images, Signs and Ideas*
(= De imaginum, 1591), trans. Dick Higgins. See HARVEST.md H-02.

The gallery is not a flat list of images. It is organised as PLANETARY COURTS:
each deity has a principal image (often charioted) plus a named retinue of
personified attendants. Saturn's attendants are the melancholic afflictions
(Grief, Care, Fear, Doubt, Hunger, Envy, Death, Poverty) -- astrologically
exact. Luna's attendants are split by phase.

Output: data/images_harvested.json

Excerpts are short and attributed; the translation is Higgins's. This file is
research data, not site copy -- keep quoted spans brief downstream.

Usage:  python scripts/harvest_images.py
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS = Path(r"E:\pdf\renaissance magic\Bruno Lull\plain_text_drafts")
SOURCE = ("Giordano Bruno Dick Higgins On the Composition of Images Signs "
          "and Ideas Willis Locker Owens Publishing.txt")
OUT = BASE_DIR / "data" / "images_harvested.json"

# The gallery's extent, established by grep (HARVEST.md H-02).
START, END = 3590, 4935

# A court opens on one of these; everything after belongs to it until the next.
# Trailing \d* absorbs footnote markers ("Images of Saturn1") -- without it a
# word boundary fails against the digit and the court is silently missed.
COURT_RE = re.compile(
    r'^(?:Images? of (?:the )?|The image of |IMAGE OF |THE IMAGE OF )'
    r'(Saturn|Mars|Mercury|Sun or Apollo|Sun|Moon|Venus|Tellus|Pluto|Jove)'
    r'\d*\s*$',
    re.IGNORECASE)
JOVE_RE = re.compile(r"^(THE CHARIOT ON JOVE'S|JOVE'S THRONE|IMAGES THAT COME FROM JOVE)", re.I)
ATTENDANT_HEAD_RE = re.compile(
    r"^(?:([A-Z][A-Za-z'æÆ ]+?)'S ATTENDANTS|ATTENDANTS OF (?:THE )?([A-Z][A-Za-z'æÆ ]+))", re.I)
IMAGE_RE = re.compile(r'^(?:THE )?IMAGE OF ([A-ZÆ][A-Za-zæÆ\' ]+?)\d*\s*$')
FOOTNOTE_TAIL = re.compile(r'\d+\s*$')

COURT_CANON = {
    'saturn': 'Saturn', 'mars': 'Mars', 'mercury': 'Mercury',
    'sun or apollo': 'Sun / Apollo', 'sun': 'Sun / Apollo', 'moon': 'Luna',
    'venus': 'Venus', 'tellus': 'Tellus', 'pluto': 'Pluto', 'jove': 'Jove',
}


def clean(s):
    return FOOTNOTE_TAIL.sub('', s.strip()).strip().rstrip('.,')


def titlecase(s):
    """Title-case without mangling apostrophes ('S -> 's)."""
    return re.sub(r"(?<=[A-Za-z])'S\b", "'s",
                  ' '.join(w.capitalize() if w.isupper() else w for w in s.split()))


def parse_inline(text):
    """
    Pull the comma-separated personifications out of an attendants passage.

    Bruno lists retinues inline as capitalised abstract nouns, often with a
    lower-case qualifier: "nocturnal Silence, starry Crown, silvery Gleam".
    The capitalised head noun is the component; the qualifier is kept with it.
    """
    if not text:
        return []
    # Work from the first list-like run onward; drop a leading clause.
    text = re.sub(r'^[^,]{0,80}?\bstand\b\s*', '', text)
    out, seen = [], set()
    for chunk in re.split(r'[,;]|\. | and ', text):
        c = chunk.strip().rstrip('.').strip()
        # Drop connective lead-ins and OCR replacement chars.
        c = re.sub(r'^(?:Likewise|Also|Then|Next)\b[\s,]*', '', c, flags=re.I)
        c = re.sub(r'^(?:\w+\s+)?stands?\s+next\s+to\s+\w+\s*', '', c, flags=re.I)
        c = re.sub(r'^next\s+to\s+\w+\s*', '', c, flags=re.I)
        c = c.replace('�', '').strip()
        if not (2 < len(c) <= 45):
            continue
        # Require a capitalised head noun that is not a sentence-initial artefact.
        if not re.search(r'\b[A-Z][a-z]{2,}', c):
            continue
        if re.search(r'\b(?:he|she|it|they|there|who|which|from|with|that)\b', c, re.I):
            continue
        # Dangling prepositions left by an upstream clause ("...stand next to
        # Saturn" -> "to Saturn") are not personifications.
        if re.match(r'^(?:to|in|at|of|on|by|the|a|an)\s', c, re.I):
            continue
        c = re.sub(r'\d+$', '', c).strip()
        key = c.lower()
        if key not in seen:
            seen.add(key)
            out.append(c)
    return out[:40]


def excerpt(lines, i, limit=3):
    """First few prose lines after a heading, joined."""
    out = []
    for l in lines[i + 1:i + 12]:
        s = l.strip()
        if not s:
            if out:
                break
            continue
        if IMAGE_RE.match(s) or ATTENDANT_HEAD_RE.match(s) or COURT_RE.match(s):
            break
        out.append(s)
        if len(out) >= limit:
            break
    return ' '.join(out).strip()


def main():
    src = CORPUS / SOURCE
    if not src.exists():
        print(f"ERROR: source not found: {src}")
        return 1

    lines = src.read_text(encoding='utf-8', errors='replace').splitlines()
    seg = lines[START - 1:END]

    courts, cur = [], None
    for i, raw in enumerate(seg):
        s = raw.strip()
        if not s:
            continue
        lineno = START + i

        m = COURT_RE.match(s)
        jove = JOVE_RE.match(s)
        if m or (jove and (cur is None or cur['planet'] != 'Jove')):
            planet = COURT_CANON.get(m.group(1).lower(), m.group(1)) if m else 'Jove'
            if cur and cur['planet'] == planet:
                cur['principal_images'].append(
                    {'heading': clean(s), 'line': lineno, 'excerpt': excerpt(seg, i)})
                continue
            cur = {'planet': planet, 'opens_at_line': lineno,
                   'principal_images': [{'heading': clean(s), 'line': lineno,
                                         'excerpt': excerpt(seg, i)}],
                   'attendant_groups': []}
            courts.append(cur)
            continue

        if cur is None:
            continue

        am = ATTENDANT_HEAD_RE.match(s)
        if am:
            body = excerpt(seg, i, limit=8)
            cur['attendant_groups'].append(
                {'group': clean(s), 'line': lineno, 'attendants': [],
                 'inline_attendants': parse_inline(body),
                 'excerpt': body[:400]})
            continue

        im = IMAGE_RE.match(s)
        if im:
            name = titlecase(clean(im.group(1)))
            # "IMAGE OF POVERTY AND" continues on the next line
            # ("THOSE IMAGES IN EXILE'S DOORS"). Join the dangling conjunction.
            if name.upper().endswith(' AND') and i + 1 < len(seg):
                name = f"{name} {titlecase(clean(seg[i + 1]))}"
            entry = {'name': name, 'line': lineno, 'excerpt': excerpt(seg, i)}
            if cur['attendant_groups']:
                cur['attendant_groups'][-1]['attendants'].append(entry)
            else:
                cur['attendant_groups'].append(
                    {'group': f"{cur['planet']} (ungrouped)", 'line': lineno,
                     'attendants': [entry], 'excerpt': ''})

    payload = {
        'source': {
            'work': 'On the Composition of Images, Signs and Ideas (De imaginum, 1591)',
            'translator': 'Dick Higgins',
            'range': f'lines {START}-{END}',
            'file': SOURCE,
        },
        'structure_note': (
            'Organised as planetary courts: each deity has a principal image '
            '(often charioted) plus a named retinue of personified attendants. '
            "Saturn's retinue is the melancholic afflictions; Luna's is split "
            'by phase (waxing / waning and changing).'
        ),
        'courts': courts,
        'counts': {
            'courts': len(courts),
            'principal_images': sum(len(c['principal_images']) for c in courts),
            'attendant_groups': sum(len(c['attendant_groups']) for c in courts),
            'named_attendants': sum(len(g['attendants'])
                                    for c in courts for g in c['attendant_groups']),
            'inline_attendants': sum(len(g.get('inline_attendants', []))
                                     for c in courts for g in c['attendant_groups']),
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f"Wrote {OUT}")
    for k, v in payload['counts'].items():
        print(f"  {k:20} {v}")
    print()
    for c in courts:
        names = [a['name'] for g in c['attendant_groups'] for a in g['attendants']]
        print(f"  {c['planet']:<14} line {c['opens_at_line']:<5} "
              f"principal={len(c['principal_images'])} "
              f"groups={len(c['attendant_groups'])} named={len(names)}")
        inline = [a for g in c['attendant_groups'] for a in g.get('inline_attendants', [])]
        if names:
            print(f"                 named:  {', '.join(names)}")
        if inline:
            print(f"                 inline: {', '.join(inline[:12])}"
                  + (f" … (+{len(inline)-12})" if len(inline) > 12 else ""))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
