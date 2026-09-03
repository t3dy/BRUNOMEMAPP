"""
seed_from_json.py — Load bruno_seed.json into the BRUNOMEMAPP SQLite DB.

Idempotent: wipes and re-inserts all rows in seed-covered tables on each run.
Mirrors WitcherPortal's seed_from_json.py pattern exactly.
"""

import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "bruno.db"
SEED_PATH = BASE_DIR / "bruno_seed.json"
PRACTICES_PATH = BASE_DIR / "practices_seed.json"


def jsonarr(v):
    """Serialize a Python list/dict to JSON; pass through None / strings unchanged."""
    if v is None:
        return None
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False)
    return v


def main():
    if not SEED_PATH.exists():
        print(f"ERROR: seed file not found: {SEED_PATH}")
        return 1

    with open(SEED_PATH, encoding='utf-8') as f:
        seed = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for table in [
        'scholarly_refs', 'bibliography', 'app_mode_ideas', 'essays',
        'biographical_events', 'disputes', 'dictionary_terms', 'scholars',
        'images', 'works',
        'practice_variants', 'frictions', 'practice_steps', 'practices',
    ]:
        cur.execute(f"DELETE FROM {table}")

    # ---- works ----
    for w in seed.get('works', []):
        cur.execute("""
            INSERT INTO works (
                slug, title_original, title_english, work_type, language,
                date_written, date_published, place_published, summary,
                memory_magic_connection, memory_magic_relevance, key_editions,
                notable_content, tags, source_method, review_status, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            w['slug'], w['title_original'], w.get('title_english'), w.get('work_type'),
            w.get('language'), w.get('date_written'), w.get('date_published'),
            w.get('place_published'), w['summary'], w['memory_magic_connection'],
            w.get('memory_magic_relevance', 'SUPPORTING'), jsonarr(w.get('key_editions')),
            w.get('notable_content'), jsonarr(w.get('tags')),
            'SEED_DATA', 'DRAFT', w.get('confidence', 'MEDIUM'),
        ))

    # ---- images ----
    for i in seed.get('images', []):
        cur.execute("""
            INSERT INTO images (
                slug, name, work_slug, image_role, description, what_it_does,
                reconstruction_level, scholarly_interpretation, image_filename,
                tags, source_method, review_status, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            i['slug'], i['name'], i.get('work_slug'), i.get('image_role'),
            i['description'], i.get('what_it_does'), i.get('reconstruction_level'),
            i.get('scholarly_interpretation'), i.get('image_filename'),
            jsonarr(i.get('tags')), 'SEED_DATA', 'DRAFT', i.get('confidence', 'MEDIUM'),
        ))

    # ---- scholars ----
    for s in seed.get('scholars', []):
        cur.execute("""
            INSERT INTO scholars (
                slug, name, birth_year, death_year, affiliation, interpretation_summary,
                view_memory, view_imagination, view_images, view_magic, view_neoplatonism,
                view_plotinus, view_ficino, view_mnemonic_wheels, view_seals_simulacra,
                major_bruno_works, tags, source_method, review_status, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s['slug'], s['name'], s.get('birth_year'), s.get('death_year'),
            s.get('affiliation'), s['interpretation_summary'], s.get('view_memory'),
            s.get('view_imagination'), s.get('view_images'), s.get('view_magic'),
            s.get('view_neoplatonism'), s.get('view_plotinus'), s.get('view_ficino'),
            s.get('view_mnemonic_wheels'), s.get('view_seals_simulacra'),
            jsonarr(s.get('major_bruno_works')), jsonarr(s.get('tags')),
            'SEED_DATA', 'DRAFT', s.get('confidence', 'MEDIUM'),
        ))

    # ---- dictionary_terms ----
    for t in seed.get('dictionary_terms', []):
        cur.execute("""
            INSERT INTO dictionary_terms (
                slug, term_original, language, short_definition, bruno_usage,
                scholarly_interpretation, related_terms, tags, source_method, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            t['slug'], t['term_original'], t.get('language'), t['short_definition'],
            t.get('bruno_usage'), t.get('scholarly_interpretation'),
            jsonarr(t.get('related_terms')), jsonarr(t.get('tags')),
            'SEED_DATA', t.get('confidence', 'MEDIUM'),
        ))

    # ---- disputes ----
    for d in seed.get('disputes', []):
        cur.execute("""
            INSERT INTO disputes (
                slug, topic, position_a_scholar_slug, position_a_text,
                position_b_scholar_slug, position_b_text, resolution, resolution_note,
                tags, source_method, review_status, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            d['slug'], d['topic'], d.get('position_a_scholar_slug'), d.get('position_a_text'),
            d.get('position_b_scholar_slug'), d.get('position_b_text'), d.get('resolution'),
            d.get('resolution_note'), jsonarr(d.get('tags')),
            'SEED_DATA', 'DRAFT', d.get('confidence', 'MEDIUM'),
        ))

    # ---- biographical_events ----
    for e in seed.get('biographical_events', []):
        cur.execute("""
            INSERT INTO biographical_events (
                slug, title, year, place, summary, memory_magic_connection,
                related_work_slugs, tags, source_method, review_status, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            e['slug'], e['title'], e.get('year'), e.get('place'), e['summary'],
            e['memory_magic_connection'], jsonarr(e.get('related_work_slugs')),
            jsonarr(e.get('tags')), 'SEED_DATA', 'DRAFT', e.get('confidence', 'MEDIUM'),
        ))

    # ---- essays ----
    for e in seed.get('essays', []):
        cur.execute("""
            INSERT INTO essays (
                slug, title, subtitle, summary, body, related_entities,
                source_method, review_status, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            e['slug'], e['title'], e.get('subtitle'), e.get('summary'),
            e['body'], jsonarr(e.get('related_entities')),
            'SEED_DATA', 'DRAFT', e.get('confidence', 'MEDIUM'),
        ))

    # ---- app_mode_ideas ----
    for a in seed.get('app_mode_ideas', []):
        cur.execute("""
            INSERT INTO app_mode_ideas (
                slug, name, mode_category, based_on_work_slugs, scholar_frames, tone,
                description, why_this_source_supports_it, status, tags,
                source_method, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            a['slug'], a['name'], a.get('mode_category'), jsonarr(a.get('based_on_work_slugs')),
            jsonarr(a.get('scholar_frames')), a.get('tone'), a['description'],
            a.get('why_this_source_supports_it'), a.get('status', 'IDEA'),
            jsonarr(a.get('tags')), 'SEED_DATA', a.get('confidence', 'MEDIUM'),
        ))

    # ---- bibliography ----
    for b in seed.get('bibliography', []):
        cur.execute("""
            INSERT INTO bibliography (
                source_id, author, title, year, publisher, journal, pub_type,
                relevance, annotation, online_url, access_note
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            b['source_id'], b['author'], b['title'], b.get('year'),
            b.get('publisher'), b.get('journal'), b.get('pub_type'),
            b.get('relevance'), b.get('annotation'), b.get('online_url'), b.get('access_note'),
        ))

    # ---- scholarly_refs ----
    for s in seed.get('scholarly_refs', []):
        cur.execute("""
            INSERT INTO scholarly_refs (entity_type, entity_slug, bib_source_id, page_ref, note)
            VALUES (?, ?, ?, ?, ?)
        """, (s['entity_type'], s['entity_slug'], s['bib_source_id'], s.get('page_ref'), s.get('note')))

    # ---- practices (docs/design/PRACTICES.md) ----
    if PRACTICES_PATH.exists():
        with open(PRACTICES_PATH, encoding='utf-8') as f:
            pseed = json.load(f)

        for p in pseed.get('practices', []):
            # A practice may point at a harvested structure file (e.g. the
            # 24x24 atria) rather than inlining it. Embed it at load time so
            # the harvested JSON stays the single canonical copy.
            structure = p.get('structure_json')
            src = p.get('structure_source')
            if src:
                src_path = BASE_DIR / src
                if src_path.exists():
                    structure = src_path.read_text(encoding='utf-8')
                else:
                    print(f"  WARNING: {p['slug']} structure_source missing: {src}")

            cur.execute("""
                INSERT INTO practices (
                    slug, name, tradition, date_range, source_text, one_line,
                    what_you_can_do, operability, operability_note,
                    worldview_preface, structure_json, sort_order,
                    source_method, review_status, confidence
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p['slug'], p['name'], p.get('tradition'), p.get('date_range'),
                p.get('source_text'), p['one_line'], p['what_you_can_do'],
                p.get('operability'), p.get('operability_note'),
                p.get('worldview_preface'), structure, p.get('sort_order', 100),
                p.get('source_method', 'SEED_DATA'), 'DRAFT',
                p.get('confidence', 'MEDIUM'),
            ))

            for s in p.get('steps', []):
                cur.execute("""
                    INSERT INTO practice_steps (
                        practice_slug, step_number, title, instruction,
                        attestation, source_locator
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (p['slug'], s['step_number'], s['title'], s['instruction'],
                      s.get('attestation'), s.get('source_locator')))

            for fr in p.get('frictions', []):
                cur.execute("""
                    INSERT INTO frictions (
                        practice_slug, step_number, kind, difficulty, explanation
                    ) VALUES (?, ?, ?, ?, ?)
                """, (p['slug'], fr.get('step_number'), fr['kind'],
                      fr['difficulty'], fr['explanation']))

            for v in p.get('variants', []):
                cur.execute("""
                    INSERT INTO practice_variants (
                        practice_slug, slug, name, scholar_slug, what_changes,
                        playable_as, testability_tier, superseded, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (p['slug'], v['slug'], v['name'], v.get('scholar_slug'),
                      v['what_changes'], v['playable_as'],
                      v.get('testability_tier'), v.get('superseded', 0),
                      v.get('notes')))

        # Enforce the standing rule: every step carries >=1 friction note.
        bare = cur.execute("""
            SELECT s.practice_slug, s.step_number FROM practice_steps s
            LEFT JOIN frictions f
              ON f.practice_slug = s.practice_slug
             AND f.step_number = s.step_number
            WHERE f.id IS NULL
            ORDER BY s.practice_slug, s.step_number
        """).fetchall()
        if bare:
            print("  WARNING: steps with no friction note "
                  "(docs/design/PRACTICES.md §3 requires >=1):")
            for slug, n in bare:
                print(f"    {slug} step {n}")

    conn.commit()

    print(f"Seeded from {SEED_PATH.name}:")
    for table in [
        'works', 'images', 'scholars', 'dictionary_terms', 'disputes',
        'biographical_events', 'essays', 'app_mode_ideas', 'bibliography', 'scholarly_refs',
        'practices', 'practice_steps', 'frictions', 'practice_variants',
    ]:
        n = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table:25s}  {n:4d}")

    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
