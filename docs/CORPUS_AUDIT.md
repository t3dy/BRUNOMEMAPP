# BRUNO CORPUS AUDIT

**Status:** IN PROGRESS  
**Last Updated:** 2026-09-01  
**Archive Location:** E:\pdf\renaissance magic\bruno\

## Overview

This document tracks the results of auditing the Bruno documents archive. The goal is to:

1. Inventory all documents (PDF, TXT, DOCX, EPUB)
2. Identify file types and condition (OCR needed? duplicates?)
3. Categorize as PRIMARY (Bruno's writings) or SECONDARY (scholarship)
4. Extract metadata (author, title, date, edition)
5. Identify key works and their variants
6. Flag extraction issues

This audit feeds into BRUNO_CORPUS.md (the canonical inventory) and guides ingestion strategy.

## Archive Structure (Observed)

```
E:\pdf\renaissance magic\bruno\
├── [Primary Sources - Bruno's Own Works]
│   ├── [To be audited]
│
├── [Secondary Sources - Scholarship]
│   ├── [To be audited]
│
└── [Related Materials]
    ├── [To be audited]
```

## Document Categories

### Primary Sources (Bruno's Writings)

These are works by Giordano Bruno himself (original publications, critical editions, translations).

#### Mnemonic Treatises (Central to BRUNOMEMAPP)

**De umbris idearum (On the Shadows of Ideas)**
- Foundational memory work
- Published 1582 (Paris)
- Second edition 1584
- Critical modern editions: Sturlese (1991)
- Status: [TO AUDIT]
- Files found: [ ]
- Extraction status: [ ]
- Notes:

**Trigone (On the Trinity)**
- Contains discussion of memory art
- Publication details: [TO AUDIT]
- Status: [ ]

**Cantus Circaeus (Circe's Incantation)**
- Memory and magical imagery
- Publication details: [TO AUDIT]
- Status: [ ]

**Ars reminiscendi (Art of Remembering)**
- Via Trigone; separate tradition
- Publication details: [TO AUDIT]
- Status: [ ]

**De imaginum, signorum et idearum compositione**
- On images, signs, and ideas
- Published 1591 (Frankfurt)
- Central to image + magic questions
- Status: [TO AUDIT]
- Files found: [ ]
- Extraction status: [ ]

**Sigillus Sigillorum (Seal of Seals)**
- Magical seals and sigils
- Publication details: [TO AUDIT]
- Status: [ ]

#### Philosophical Dialogues (Italian works)

**Spaccio della bestia trionfante (The Expulsion of the Triumphant Beast)**
- Published 1584
- Contains ethical + magical themes
- Related to memory transformation
- Status: [TO AUDIT]

**Asini Cifrati (The Cipher Asses)**
- Publication details: [TO AUDIT]

**Eroici furori (Heroic Frenzies)**
- On Actaeon, desire, contemplation
- Published 1585–1586
- Relates to imagination + transformation
- Status: [TO AUDIT]

#### Other Primary Sources

[List to be completed during audit]

### Secondary Sources (Scholarship)

These are scholarly works ABOUT Bruno, his memory, and his magic.

#### Major Monographs

**Yates, Frances A.** *Giordano Bruno and the Hermetic Tradition*
- Foundational (though controversial)
- Status: [TO AUDIT - CRITICAL]

Yates, Frances A.** *The Art of Memory*
- Essential context for Renaissance memory traditions
- Status: [TO AUDIT - CRITICAL]

**Clucas, Stephen** (editor) *'Simulacra et Signacula: Memory, Magic and Metaphysics in Brunian Mnemonics'* (in *Giordano Bruno: Philosopher of the Renaissance*)
- Modern reconstruction emphasizing ethics + logic + magic
- Status: [TO AUDIT - CRITICAL]

**Mertens, Manuel.** *Magic and Memory in Giordano Bruno: The Art of a Heroic Spirit*
- Recent intervention on memory + magic + spirit integration
- Status: [TO AUDIT - CRITICAL]

**Couliano, Ioan P.** *Eros and Magic in the Renaissance*
- Psychological + magical interpretation
- Status: [TO AUDIT]

**Sturlese, Rita** (editor). *Critical edition of De umbris idearum*
- Corrects Yates's planetary placement
- Status: [TO AUDIT - CRITICAL]

**Gatti, Hilary.** *Giordano Bruno and Renaissance Science*
- Broader philosophical context
- Status: [TO AUDIT]

**Wang, Zheng.** *"The Role of Iconic Practice in Bruno's Gnoseology"* (article)
- Contemporary scholarship on images as knowledge
- Status: [TO AUDIT]

**Barenstein, Julián.** *"Memoria regulata: hacia una interpretación no esotérica del De umbris idearum"* (article)
- De-esotericizing position
- Status: [TO AUDIT]

#### Articles & Book Chapters

[To be catalogued during audit]

#### Secondary Literature on Related Topics

- Ficino and Neoplatonism
- Renaissance memory traditions (Matteo Ricci, etc.)
- Renaissance magic (Agrippa, etc.)
- Plotinus and memory
- [Others to be identified]

## Audit Checklist

For each document found:

- [ ] **Filename:** Record exact filename
- [ ] **File type:** PDF | TXT | DOCX | EPUB | HTML | Other
- [ ] **File size:** Bytes / pages (rough estimate)
- [ ] **Category:** Primary (Bruno) | Secondary (Scholarship) | Related
- [ ] **Title:** Extract actual title from document
- [ ] **Author:** Who wrote it?
- [ ] **Date written/published:** When?
- [ ] **Edition:** If known (first printing, critical edition, translation, etc.)
- [ ] **Language:** Original language (Latin, Italian, English, German, French)
- [ ] **Extraction test:** Can text be extracted from PDF? If not, note "image-only, needs OCR"
- [ ] **Condition:** Complete | Fragment | Damaged | Multiple editions present
- [ ] **Notes:** Any observations (missing pages, poor quality scan, etc.)

## Summary Statistics

**To be filled in after audit:**

- Total documents found: [ ]
- Primary sources: [ ]
- Secondary sources: [ ]
- Related materials: [ ]

### By File Type

- PDFs: [ ]
- TXT files: [ ]
- DOCX files: [ ]
- EPUB files: [ ]
- HTML files: [ ]
- Other: [ ]

### By Extraction Status

- Extractable (text PDFs): [ ]
- Image-only (requires OCR): [ ]
- Corrupted/unreadable: [ ]

### Critical Works (Must Have)

- [ ] De umbris idearum (at least one edition)
- [ ] Yates' *Giordano Bruno and the Hermetic Tradition*
- [ ] Sturlese critical edition of De umbris
- [ ] Clucas studies
- [ ] Mertens *Magic and Memory*

### Gaps Identified

[To be filled during audit]

---

## Next Steps After Audit

1. Generate BRUNO_CORPUS.md from this audit
2. Run `python scripts/ingest.py --verbose` to extract all documents
3. Review `manifest.json` for any extraction failures
4. Address OCR for image-only PDFs (if desired)
5. Begin Phase 2 (metadata extraction)

---

## Instructions for Auditing

1. Navigate to E:\pdf\renaissance magic\bruno\
2. For each file, fill in the checklist above
3. Note any patterns (e.g., multiple editions of De umbris)
4. Flag any duplicates or suspicious files
5. Count total documents and categorize
6. Save this file with updates
7. Proceed to Phase 1 ingestion

**Time estimate:** 1-2 hours for complete inventory

**Current progress:** 0%
