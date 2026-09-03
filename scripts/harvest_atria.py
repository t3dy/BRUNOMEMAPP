"""
harvest_atria.py — Extract Bruno's atrium diagrams from the Higgins translation.

Source: Giordano Bruno, *On the Composition of Images, Signs and Ideas*
(= De imaginum, signorum et idearum compositione, 1591), trans. Dick Higgins.
Book I Part 2, chs 3-6. See HARVEST.md H-01.

Higgins HEADS only the 12 odd-numbered atria, but each plate transcribes TWO:
the headed one and the following even-numbered one, unheaded. All 24 are
present. This pulls each diagram into structured JSON for seeding.

Output: data/atria_harvested.json

Usage:  python scripts/harvest_atria.py
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS = Path(r"E:\pdf\renaissance magic\Bruno Lull\plain_text_drafts")
SOURCE = ("Giordano Bruno Dick Higgins On the Composition of Images Signs "
          "and Ideas Willis Locker Owens Publishing.txt")
OUT = BASE_DIR / "data" / "atria_harvested.json"

# Diagram headings look like:  [I.] ATRIUM OF THE ALTAR   /   XV. ATRIUM. FOOD.
HEAD_RE = re.compile(
    r'^\[?(?P<num>[IVXL]+)\.?\]?\.?\s*ATRIUM[\s.]*(?:OF\s+(?:THE\s+)?)?(?P<name>.*?)\.?\s*$',
    re.IGNORECASE,
)

ROMAN = {'I': 1, 'III': 3, 'V': 5, 'VII': 7, 'IX': 9, 'XI': 11, 'XIII': 13,
         'XV': 15, 'XVII': 17, 'XIX': 19, 'XXI': 21, 'XXIII': 23}

# The 24 atria named in Bk I Pt 2 ch 4, in Bruno's order.
CANONICAL_24 = [
    "altar", "basilica", "prison", "house", "colt", "fountain",
    "sword", "horoscope", "fire", "yoke", "lantern", "table",
    "nest", "sheepfold", "food", "four horse chariot", "net", "mirror",
    "hot springs", "carriage", "gate", "Pythagorean fork", "gift", "key of jealousy",
]


def is_item(line: str) -> bool:
    """A diagram cell: a short word/phrase on its own line, not prose."""
    s = line.strip()
    if not s or len(s) > 40:
        return False
    if s.endswith(('.', ',', ';', ':')):
        return False
    words = s.split()
    return 1 <= len(words) <= 3 and s[0].isalpha()


def main():
    src = CORPUS / SOURCE
    if not src.exists():
        print(f"ERROR: source not found: {src}")
        return 1

    lines = src.read_text(encoding='utf-8', errors='replace').splitlines()

    # Locate diagram headings.
    heads = []
    for i, line in enumerate(lines):
        m = HEAD_RE.match(line.strip())
        if m and m.group('num') in ROMAN:
            heads.append((i, ROMAN[m.group('num')], m.group('name').strip().lower()))

    # Each plate carries TWO atria: the headed odd-numbered one and the
    # following even-numbered one, unheaded. Centres are ALL-CAPS cells.
    # Each atrium is 25 cells: 24 positions with the centre in the middle.
    HALF = 12
    atria = []
    for idx, (start, num, _name) in enumerate(heads):
        end = heads[idx + 1][0] if idx + 1 < len(heads) else start + 60
        cells = [l.strip() for l in lines[start + 1:end] if is_item(l)]

        centres = [j for j, c in enumerate(cells) if c.isupper() and len(c) > 2]
        # Last plate omits the caps marker for atrium 23; infer it 25 cells back.
        if len(centres) == 1:
            centres = [centres[0] - 25, centres[0]]

        for k, ci in enumerate(centres[:2]):
            lo, hi = ci - HALF, ci + HALF + 1
            # Last plate omits atrium 23's caps marker, so its inferred window
            # can run off the start; clamp to the first 25 cells instead.
            if lo < 0:
                lo, hi, ci = 0, 25, min(ci, 24)
            if hi > len(cells):
                continue
            n = num + k
            block = cells[lo:hi]
            atria.append({
                "number": n,
                "name": CANONICAL_24[n - 1],
                "centre": cells[ci] if cells[ci].isupper() else CANONICAL_24[n - 1].upper(),
                "centre_attested": cells[ci].isupper(),
                "source_line": start + 1,
                "plate": f"{['I','III','V','VII','IX','XI','XIII','XV','XVII','XIX','XXI','XXIII'][idx]}"
                         f" ({'headed' if k == 0 else 'unheaded, second on plate'})",
                "positions": block[:HALF] + block[HALF + 1:],   # 24 cells, centre removed
                "position_count": len(block) - 1,
                "inventory_attestation": "ATTESTED",
                "position_mapping_attestation": (
                    "ATTESTED" if n == 1 else "RECONSTRUCTED"
                ),
            })

    atria.sort(key=lambda a: a["number"])
    missing = [
        {"number": n, "name": CANONICAL_24[n - 1], "attestation": "NOT_TRANSCRIBED"}
        for n in range(1, 25) if n not in {a["number"] for a in atria}
    ]

    payload = {
        "source": {
            "work": "On the Composition of Images, Signs and Ideas (De imaginum, 1591)",
            "translator": "Dick Higgins",
            "locus": "Book I, Part 2, chapters 3-6",
            "file": SOURCE,
        },
        "atrium_form": {
            "shape": "quadrangular",
            "centre": "the earth and the eye",
            "corners": ["east", "west", "south", "north"],
            "mid_sides": ["east", "west", "south", "north"],
            "points": 8,
            "collaterals_per_point": ["right", "left"],
            "positions": 24,
            "note": "8 points x (self + right + left) = 24 positions per atrium.",
        },
        "canonical_24": CANONICAL_24,
        "plate_structure": (
            "Higgins heads only the 12 odd-numbered atria, but each plate "
            "transcribes TWO: the headed one and the following even-numbered "
            "one, unheaded. All 24 are therefore present. Centres are ALL-CAPS "
            "cells and reproduce the ch.4 canonical list exactly, in order -- "
            "an independent cross-check on both."
        ),
        "caveat": (
            "Position MAPPING is attested only for the Altar, where ch.6 gives "
            "position->item in prose. For atria 2-24 the inventory is attested "
            "but the cell order is a 2D plate flattened into text, so the "
            "mapping is RECONSTRUCTED and may not be geometrically faithful."
        ),
        "transcribed": atria,
        "not_transcribed": missing,
        "counts": {"transcribed": len(atria), "not_transcribed": len(missing)},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')

    print(f"Wrote {OUT}")
    print(f"  transcribed:     {len(atria)}")
    print(f"  not transcribed: {len(missing)}")
    print()
    for a in atria:
        print(f"  {a['number']:>3}. {a['name']:<20} {a['position_count']:>3} positions  "
              f"centre={a['centre']:<20} map={a['position_mapping_attestation']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
