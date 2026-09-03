"""
extract_plates.py — Extract the period woodcuts and diagrams from the corpus PDFs.

WHY THIS IS OK, AND WHERE THE LINE IS
-------------------------------------
The images extracted here are photographic reproductions of woodcuts printed in
1585-1591. The underlying works are centuries out of copyright, and a faithful
reproduction of a flat public-domain artwork adds no new authorship. What IS in
copyright in these volumes is the editorial apparatus -- translation, notes,
typography, page design -- and none of that is taken.

So: period woodcuts and diagrams, yes. Pages of modern text, modern redrawings,
and typeset apparatus, no. The curated list below is explicit about which is
which, and anything not visually identified is labelled as unidentified rather
than given a plausible caption.

Output: site/assets/plates/*.png  +  data/plates.json

Usage:  python scripts/extract_plates.py
"""

import json
from pathlib import Path

import fitz

BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS = Path(r"E:\pdf\renaissance magic\Bruno Lull")
OUT_IMG = BASE_DIR / "site" / "assets" / "plates"
OUT_JSON = BASE_DIR / "data" / "plates.json"

HIGGINS = ("Giordano Bruno Dick Higgins On the Composition of Images Signs "
           "and Ideas Willis Locker Owens Publishing.pdf")
ESSAYS = ("Bruno Giordano_ Gatti Hilary_ Bruno Giordano Essays on Giordano "
          "Bruno Princeton University Press.pdf")

# Curated selection. `id` is set only where the figure has been visually
# identified; otherwise the plate is published with an honest label.
PLATES = [
    # --- Bruno's memory architecture -------------------------------------
    dict(src=HIGGINS, page=56, idx=0, slug="atrium-altar",
         title="The Atrium of the Altar",
         caption="Bruno's atrium as printed: a circle enclosing a square, with "
                 "ALTA/RIS at an eight-spoked hub, letter-groups at the four "
                 "corners and lozenges at the mid-sides. This is the figure the "
                 "interactive atrium above reconstructs.",
         work="De imaginum, signorum et idearum compositione (1591)",
         identified=True, group="architecture", links="#bruno-atrium-figure"),
    dict(src=HIGGINS, page=56, idx=1, slug="atrium-variant",
         title="The atrium, second version",
         caption="The companion plate. Higgins prints two versions of the atrium "
                 "diagram — the 1591 printing and Tocco's — which is the textual "
                 "variant seeded as a playable alternative.",
         work="De imaginum (1591); cf. Tocco's edition",
         identified=True, group="architecture"),
    dict(src=HIGGINS, page=73, idx=0, slug="field-of-asterisks",
         title="Bounded field with markers",
         caption="A ruled rectangle with asterisk markers at the margins and five "
                 "within. One of the schematic place-figures of the first book.",
         work="De imaginum (1591)", identified=True, group="architecture"),
    dict(src=HIGGINS, page=157, idx=0, slug="numeral-table",
         title="The numeral table",
         caption="Roman numerals mapped to figures: X a boy, XX a youth, XXX a "
                 "girl, L an old man, LX the ugly, LXX the beautiful, C the great, "
                 "CX the blind, D the foolish — and I a column, II a little fork, "
                 "III a tripod, IV a seat, V a serpent, VI a noose. A number "
                 "alphabet to set beside the letter alphabet.",
         work="De imaginum (1591)", identified=True, group="architecture",
         links="practices/bruno-image-alphabet.html"),

    # --- the planetary chariots ------------------------------------------
    dict(src=HIGGINS, page=107, idx=0, slug="iupiter",
         title="IVPITER", caption="Jupiter enthroned in his chariot, drawn by "
                 "eagles, sceptre in hand; his zodiacal houses ride on the wheels.",
         work="De imaginum (1591)", identified=True, group="chariots",
         links="images/courts.html#court-jove"),
    dict(src=HIGGINS, page=115, idx=0, slug="saturnus",
         title="SATVRNVS", caption="Saturn with the scythe, drawn by dragons, "
                 "Capricorn and Aquarius on the wheels. His retinue in the text is "
                 "the melancholic afflictions — Grief, Care, Decay, Death.",
         work="De imaginum (1591)", identified=True, group="chariots",
         links="images/courts.html#court-saturn"),
    dict(src=HIGGINS, page=135, idx=0, slug="sol",
         title="SOL", caption="The Sun crowned and radiant, horse-drawn, with Leo "
                 "on the wheel.",
         work="De imaginum (1591)", identified=True, group="chariots",
         links="images/courts.html#court-sun"),
    # Same series, not individually identified — published by page, not named.
    *[dict(src=HIGGINS, page=p, idx=0, slug=f"chariot-p{p}",
           title=f"Chariot plate, p. {p}",
           caption="From the same series of deity chariots. Not visually "
                   "identified here, so it is not given a name — the text's order "
                   "of courts runs Jove, Saturn, Mars, Mercury, Sol, Luna, Venus, "
                   "Tellus, Pluto, but inferring from position alone would be a "
                   "guess.",
           work="De imaginum (1591)", identified=False, group="chariots")
      for p in (118, 126, 139, 145, 167, 168, 170, 173, 175)],

    # --- emblems ----------------------------------------------------------
    dict(src=ESSAYS, page=120, idx=0, slug="serpent-medallion",
         title="Serpent medallion", invert=True,
         caption="A serpent coiled within a bordered roundel, with foliate corner "
                 "ornaments. An emblematic figure of the kind Bruno's seal and "
                 "image treatises turn on.",
         work="Reproduced in Gatti (ed.), Essays on Giordano Bruno",
         identified=True, group="emblems"),
    dict(src=ESSAYS, page=83, idx=0, slug="geometric-figure", invert=True,
         title="Lettered geometrical figure",
         caption="Intersecting circles with lettered points (A, B, E, G, H, I, K, "
                 "L, M, N, O) and chords drawn between them — the style of "
                 "demonstration Bruno's geometrical and cosmological works use.",
         work="Reproduced in Gatti (ed.), Essays on Giordano Bruno",
         identified=True, group="emblems"),
    *[dict(src=ESSAYS, page=p, idx=0, slug=f"emblem-p{p}", invert=True,
           title=f"Figure, Essays p. {p}",
           caption="A further figure from the same plate section. Not visually "
                   "identified, and therefore not captioned beyond its source.",
           work="Reproduced in Gatti (ed.), Essays on Giordano Bruno",
           identified=False, group="emblems")
      for p in (66, 67, 68, 73, 79, 82, 117, 121, 124)],
]


def looks_inverted(pix):
    """Cheap check: sample the border; a mostly-dark frame means a negative."""
    try:
        w, h = pix.width, pix.height
        pts = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
               (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]
        vals = []
        for x, y in pts:
            p = pix.pixel(x, y)
            vals.append(sum(p[:3]) / 3 if isinstance(p, (tuple, list)) else p)
        return (sum(vals) / len(vals)) < 110
    except Exception:
        return False


def main():
    OUT_IMG.mkdir(parents=True, exist_ok=True)
    docs, out, missing = {}, [], 0

    for spec in PLATES:
        src = CORPUS / spec["src"]
        if not src.exists():
            print(f"  MISSING source: {spec['src'][:50]}")
            missing += 1
            continue
        if spec["src"] not in docs:
            docs[spec["src"]] = fitz.open(str(src))
        d = docs[spec["src"]]

        imgs = [im for im in d[spec["page"] - 1].get_images(full=True)
                if im[2] >= 300 and im[3] >= 300]
        if spec["idx"] >= len(imgs):
            print(f"  no image {spec['idx']} on p.{spec['page']} ({spec['slug']})")
            missing += 1
            continue

        im = imgs[spec["idx"]]
        pix = fitz.Pixmap(d, im[0])
        if pix.n - pix.alpha >= 4:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        if spec.get("invert") or looks_inverted(pix):
            pix.invert_irect()
        fn = OUT_IMG / f"{spec['slug']}.png"
        pix.save(str(fn))

        out.append({
            "slug": spec["slug"], "file": f"assets/plates/{spec['slug']}.png",
            "title": spec["title"], "caption": spec["caption"],
            "work": spec["work"], "group": spec["group"],
            "identified": spec["identified"],
            "links": spec.get("links"),
            "source_page": spec["page"],
            "source_edition": spec["src"].split(" - ")[0][:80],
            "width": im[2], "height": im[3],
            "size_kb": round(fn.stat().st_size / 1024),
        })
        print(f"  {spec['slug']:22} p.{spec['page']:<4} {im[2]}x{im[3]:<5} "
              f"{'identified' if spec['identified'] else 'unidentified'}")

    for d in docs.values():
        d.close()

    payload = {
        "_provenance": {
            "method": "EXTRACTED_FROM_CORPUS_PDFS",
            "rights": (
                "These are photographic reproductions of woodcuts printed in "
                "1585-1591. The underlying works are long out of copyright and a "
                "faithful reproduction of a flat public-domain artwork carries no "
                "new authorship. No editorial apparatus -- translation, notes, "
                "typography, page design -- is reproduced. The edition each scan "
                "comes from is credited."),
            "identification": (
                "Plates marked identified were read directly and captioned from "
                "what they show. The rest are published with their source page and "
                "no name: the order of courts in the text would let one guess, and "
                "guessing is what this project does not do."),
        },
        "plates": out,
        "counts": {
            "total": len(out),
            "identified": sum(1 for p in out if p["identified"]),
            "unidentified": sum(1 for p in out if not p["identified"]),
        },
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False),
                        encoding="utf-8")
    print(f"\nWrote {OUT_JSON}")
    print(f"  plates: {len(out)}  identified: {payload['counts']['identified']}  "
          f"missing: {missing}")
    print(f"  images: {OUT_IMG}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
