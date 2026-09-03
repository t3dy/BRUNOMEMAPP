#!/usr/bin/env python3
"""
SUPERSEDED 2026-09-01 — see docs/ARCHITECTURE_PIVOT.md. Not currently run.
Use scripts/init_db.py + scripts/seed_from_json.py instead (WitcherPortal pattern).

Build and initialize the BRUNOMEMAPP SQLite schema.

Usage:
  python scripts/build_schema.py [--force]

Options:
  --force     Drop existing database and rebuild from scratch
"""

import sqlite3
import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SCHEMA_FILE = DATA_DIR / "schema.sql"
DB_PATH = DATA_DIR / "bruno.db"


def build_schema(force: bool = False):
    """Initialize SQLite schema from schema.sql."""

    # Handle existing database
    if DB_PATH.exists():
        if force:
            print(f"Removing existing database: {DB_PATH}")
            DB_PATH.unlink()
        else:
            print(f"Database already exists: {DB_PATH}")
            print("Use --force to rebuild from scratch")
            return False

    # Read schema
    if not SCHEMA_FILE.exists():
        print(f"ERROR: schema.sql not found at {SCHEMA_FILE}")
        return False

    with open(SCHEMA_FILE, 'r') as f:
        schema = f.read()

    # Create and populate database
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        # Execute schema
        cursor.executescript(schema)
        conn.commit()

        # Verify tables
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = [row[0] for row in cursor.fetchall()]

        print(f"\n✓ Created SQLite database: {DB_PATH}")
        print(f"\nTables created ({len(tables)}):")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  • {table} (0 rows)")

        # Verify FTS5 tables
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name LIKE '%_fts'
            ORDER BY name
        """)
        fts_tables = [row[0] for row in cursor.fetchall()]

        if fts_tables:
            print(f"\nFull-text search tables ({len(fts_tables)}):")
            for table in fts_tables:
                print(f"  • {table}")

        # Verify views
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='view'
            ORDER BY name
        """)
        views = [row[0] for row in cursor.fetchall()]

        if views:
            print(f"\nViews created ({len(views)}):")
            for view in views:
                print(f"  • {view}")

        # Verify indices
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='index' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        indices = [row[0] for row in cursor.fetchall()]

        if indices:
            print(f"\nIndices created ({len(indices)}):")
            for idx in indices:
                print(f"  • {idx}")

        conn.close()
        print(f"\n✓ Schema initialization complete")
        return True

    except sqlite3.Error as e:
        print(f"ERROR: Failed to build schema: {e}")
        return False


def verify_schema():
    """Check that database is properly initialized."""

    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}")
        return False

    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        # Check critical tables
        required_tables = [
            'sources', 'pages', 'passages', 'concepts', 'techniques',
            'scholars', 'claims', 'interpretations', 'disputes', 'experiments'
        ]

        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """)
        existing = [row[0] for row in cursor.fetchall()]

        missing = [t for t in required_tables if t not in existing]

        if missing:
            print(f"ERROR: Missing tables: {missing}")
            conn.close()
            return False

        print(f"✓ Database schema verified")
        print(f"  {len(existing)} tables")

        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"ERROR: Failed to verify schema: {e}")
        return False


if __name__ == '__main__':
    force = '--force' in sys.argv

    print("=" * 60)
    print("BRUNOMEMAPP Schema Builder")
    print("=" * 60)

    success = build_schema(force=force)

    if success:
        verify_schema()
        sys.exit(0)
    else:
        sys.exit(1)
