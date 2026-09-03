#!/usr/bin/env python3
"""
SUPERSEDED 2026-09-01 — see docs/ARCHITECTURE_PIVOT.md. Not currently run.
Use scripts/convert_corpus.py instead (WitcherPortal pattern: PDF/EPUB -> corpus/sources/*.md,
grep-able research grounding, separate from the seed-JSON-driven site content).

BRUNOMEMAPP Document Ingestion Pipeline

Extracts text, metadata, and figures from PDFs, TXT, DOCX, EPUB.
Generates stable passage IDs and populates sources/pages/passages tables.

Usage:
  python scripts/ingest.py [--source-dir PATH] [--skip-ocr] [--verbose]

Options:
  --source-dir PATH   Directory containing Bruno documents (default: E:\\pdf\\renaissance magic\\bruno)
  --skip-ocr          Skip OCR for image-only PDFs
  --verbose           Print detailed extraction info
"""

import sqlite3
import hashlib
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import re

try:
    import PyPDF2
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "bruno.db"
MANIFEST_PATH = DATA_DIR / "manifest.json"


def hash_file(filepath: Path) -> str:
    """Generate MD5 hash of file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def extract_pdf_text(pdf_path: Path, verbose: bool = False) -> Tuple[str, float, bool]:
    """
    Extract text from PDF.
    Returns (text, ocr_confidence, has_images)
    """

    if not PYPDF_AVAILABLE:
        return "", 0.0, False

    try:
        text = []
        has_images = False
        ocr_confidence = 0.0

        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)

            for page_num, page in enumerate(pdf_reader.pages):
                extracted = page.extract_text()
                if extracted:
                    text.append(f"--- Page {page_num + 1} ---\n{extracted}")
                else:
                    # Page may be image-only
                    has_images = True
                    text.append(f"--- Page {page_num + 1} (image-only, requires OCR) ---")

        if verbose:
            print(f"  Extracted {num_pages} pages from {pdf_path.name}")

        return "\n".join(text), ocr_confidence, has_images

    except Exception as e:
        print(f"  ERROR extracting PDF {pdf_path.name}: {e}")
        return "", 0.0, False


def extract_txt_text(txt_path: Path, verbose: bool = False) -> str:
    """Extract text from plain text file."""

    try:
        with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
            text = f.read()

        if verbose:
            print(f"  Extracted text from {txt_path.name} ({len(text)} chars)")

        return text

    except Exception as e:
        print(f"  ERROR reading {txt_path.name}: {e}")
        return ""


def generate_passages(text: str, source_id: int, page_mapping: Dict[int, int], verbose: bool = False) -> List[Dict]:
    """
    Split extracted text into passages (roughly paragraph-sized chunks).
    Generate stable passage IDs.

    passage_id format: BRUNO-{source_id:04d}/{page}/{chunk:04d}
    """

    passages = []
    passage_counter = 0

    # Split on blank lines (assume paragraphs)
    chunks = re.split(r'\n\n+', text)

    current_page = 1
    lines_on_page = 0

    for chunk_id, chunk in enumerate(chunks):
        chunk = chunk.strip()
        if not chunk:
            continue

        # Estimate page breaks (rough: ~40 lines per page)
        chunk_lines = len(chunk.split('\n'))
        lines_on_page += chunk_lines

        if lines_on_page > 40:
            current_page += 1
            lines_on_page = 0

        stable_id = f"BRUNO-{source_id:04d}/{current_page}/{chunk_id:04d}"

        passages.append({
            'source_id': source_id,
            'page_id': page_mapping.get(current_page, 1),  # Map to actual page
            'passage_type': 'quote',  # default; will be refined later
            'extracted_text': chunk,
            'passage_label': f"p. {current_page}",
            'stable_passage_id': stable_id,
            'language_original': 'unknown',  # will be detected later
            'confidence': 'DIRECTLY_ATTESTED'
        })

        passage_counter += 1

    if verbose:
        print(f"  Generated {passage_counter} passages")

    return passages


def ingest_document(filepath: Path, db_conn: sqlite3.Connection, verbose: bool = False) -> bool:
    """
    Ingest a single document.
    Returns True on success.
    """

    cursor = db_conn.cursor()

    try:
        # Calculate file hash
        file_hash = hash_file(filepath)

        # Check if already ingested
        cursor.execute("SELECT id FROM sources WHERE file_hash = ?", (file_hash,))
        if cursor.fetchone():
            if verbose:
                print(f"  SKIP (already ingested): {filepath.name}")
            return True

        # Determine file type
        suffix = filepath.suffix.lower()
        file_type = {
            '.pdf': 'pdf',
            '.txt': 'txt',
            '.epub': 'epub',
            '.docx': 'docx',
            '.html': 'html'
        }.get(suffix, 'unknown')

        if file_type == 'unknown':
            if verbose:
                print(f"  SKIP (unknown type): {filepath.name}")
            return False

        # Extract text based on file type
        extracted_text = ""
        ocr_confidence = 0.0
        extraction_status = "extracted"
        has_images = False

        if file_type == 'pdf':
            if not PYPDF_AVAILABLE:
                print(f"  ERROR: PyPDF2 not available. Install with: pip install PyPDF2")
                return False

            extracted_text, ocr_confidence, has_images = extract_pdf_text(filepath, verbose=verbose)

            if has_images and not OCR_AVAILABLE:
                extraction_status = "OCR_required"
                if verbose:
                    print(f"  WARN: Image-only pages detected. Install pytesseract for OCR.")

        elif file_type == 'txt':
            extracted_text = extract_txt_text(filepath, verbose=verbose)

        else:
            if verbose:
                print(f"  SKIP (unsupported type for now): {filepath.name} ({file_type})")
            return False

        if not extracted_text:
            if verbose:
                print(f"  WARN: No text extracted from {filepath.name}")
            extraction_status = "failed"

        # Insert source record
        cursor.execute("""
            INSERT INTO sources (filename, file_type, file_hash, file_size, extraction_status, ocr_confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (filepath.name, file_type, file_hash, filepath.stat().st_size, extraction_status, ocr_confidence))

        source_id = cursor.lastrowid

        # Create page records (rough estimate: 1 page per 3000 chars)
        page_count = max(1, len(extracted_text) // 3000)
        page_mapping = {}

        for page_num in range(1, page_count + 1):
            cursor.execute("""
                INSERT INTO pages (source_id, page_number, page_label, extracted_text, ocr_confidence)
                VALUES (?, ?, ?, ?, ?)
            """, (source_id, page_num, f"p. {page_num}", "", ocr_confidence))

            page_id = cursor.lastrowid
            page_mapping[page_num] = page_id

        # Generate and insert passage records
        passages = generate_passages(extracted_text, source_id, page_mapping, verbose=verbose)

        for passage in passages:
            cursor.execute("""
                INSERT INTO passages (
                    source_id, page_id, passage_type, extracted_text, passage_label,
                    stable_passage_id, language_original, confidence
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                passage['source_id'],
                passage['page_id'],
                passage['passage_type'],
                passage['extracted_text'],
                passage['passage_label'],
                passage['stable_passage_id'],
                passage['language_original'],
                passage['confidence']
            ))

        db_conn.commit()

        if verbose:
            print(f"  ✓ Ingested: {filepath.name} (source_id={source_id}, pages={page_count}, passages={len(passages)})")

        return True

    except Exception as e:
        print(f"  ERROR ingesting {filepath.name}: {e}")
        return False


def ingest_directory(source_dir: Path, db_conn: sqlite3.Connection, verbose: bool = False) -> Tuple[int, int]:
    """
    Ingest all documents in a directory.
    Returns (successful, failed) counts.
    """

    successful = 0
    failed = 0

    # Find all supported file types
    supported_extensions = ('*.pdf', '*.txt', '*.epub', '*.docx', '*.html')
    files = []

    for ext in supported_extensions:
        files.extend(source_dir.glob(f'**/{ext}'))
        files.extend(source_dir.glob(f'**/{ext.upper()}'))

    files = sorted(set(files))  # Deduplicate and sort

    if not files:
        print(f"No documents found in {source_dir}")
        return 0, 0

    print(f"\nFound {len(files)} documents to ingest:\n")

    for filepath in files:
        if ingest_document(filepath, db_conn, verbose=verbose):
            successful += 1
        else:
            failed += 1

    return successful, failed


def generate_manifest(db_conn: sqlite3.Connection) -> Dict:
    """Generate machine-readable corpus manifest."""

    cursor = db_conn.cursor()

    cursor.execute("""
        SELECT
            s.id,
            s.filename,
            s.file_type,
            s.extraction_status,
            s.ocr_status,
            COUNT(DISTINCT p.id) as page_count,
            COUNT(DISTINCT pg.id) as passage_count
        FROM sources s
        LEFT JOIN pages p ON s.id = p.source_id
        LEFT JOIN passages pg ON s.id = pg.source_id
        GROUP BY s.id
        ORDER BY s.filename
    """)

    documents = []
    for row in cursor.fetchall():
        documents.append({
            "id": row[0],
            "filename": row[1],
            "file_type": row[2],
            "extraction_status": row[3],
            "ocr_status": row[4],
            "page_count": row[5] or 0,
            "passage_count": row[6] or 0
        })

    manifest = {
        "total_documents": len(documents),
        "documents": documents,
        "generation_timestamp": str(Path(__file__).stat().st_mtime)
    }

    return manifest


def main():
    """Main ingestion pipeline."""

    # Parse arguments
    source_dir = Path("E:\\pdf\\renaissance magic\\bruno")  # default
    skip_ocr = '--skip-ocr' in sys.argv
    verbose = '--verbose' in sys.argv

    for arg in sys.argv[1:]:
        if arg.startswith('--source-dir'):
            source_dir = Path(arg.split('=')[1])

    print("=" * 70)
    print("BRUNOMEMAPP Document Ingestion Pipeline")
    print("=" * 70)

    # Check database
    if not DB_PATH.exists():
        print(f"ERROR: Database not found at {DB_PATH}")
        print("Run: python scripts/build_schema.py")
        return 1

    # Check source directory
    if not source_dir.exists():
        print(f"ERROR: Source directory not found: {source_dir}")
        return 1

    print(f"\nSource directory: {source_dir}")
    print(f"Database: {DB_PATH}")
    print()

    try:
        # Connect to database
        db_conn = sqlite3.connect(str(DB_PATH))

        # Ingest documents
        successful, failed = ingest_directory(source_dir, db_conn, verbose=verbose)

        # Generate manifest
        manifest = generate_manifest(db_conn)

        with open(MANIFEST_PATH, 'w') as f:
            json.dump(manifest, f, indent=2)

        db_conn.close()

        # Summary
        print(f"\n{'=' * 70}")
        print(f"Ingestion Complete")
        print(f"{'=' * 70}")
        print(f"\nSuccessful: {successful}")
        print(f"Failed: {failed}")
        print(f"Manifest: {MANIFEST_PATH}")

        return 0 if failed == 0 else 1

    except Exception as e:
        print(f"ERROR: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
