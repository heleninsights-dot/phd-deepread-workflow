# PhD Deep Read Workflow Guide

This guide explains the **PhD Deep Read Workflow**: a pipeline that turns academic PDFs into structured Obsidian literature notes and 9-node critical-thinking canvases.

## Overview

The workflow has four stages:

1. **PDF extraction** — PyMuPDF for searchable text, Tesseract OCR fallback for scanned pages
2. **Note generation** — Claude Code writes the literature note, following the `clauderules.md` template
3. **Canvas creation** — 9-node JSON Canvas, optionally populated from the finished note
4. **Verification** — quality checks against the template

## Stage 1 — Text-First PDF extraction

The extractor pre-scans the PDF with PyMuPDF, then chooses per-page:

```
PDF Input
    ↓
Pre-scan with PyMuPDF
    ↓
Page has ≥100 chars searchable text?
    ├── Yes → PyMuPDF (fast text path)
    └── No  → Tesseract OCR (if installed); else images-only

If 80%+ of pages are searchable → use PyMuPDF for all pages.
```

See `docs/decision-tree.md` for the full algorithm and configurable thresholds.

### Tools

- **PyMuPDF (fitz)** — fast direct text extraction
- **Tesseract OCR** — optional fallback for scanned pages
- **Custom Python script** — `scripts/extract.py`

### Output structure

```
markdown_output/<paper_name>/
├── <paper>.md                 # extracted markdown (text + image refs)
├── <paper>_meta.json          # per-page extraction methods, TOC, metadata
└── _page_*_*.png/.jpeg        # extracted images
```

## Stage 2 — Structured note generation

Claude Code writes the literature note. The template `scripts/templates/clauderules.md` (~230 lines) defines the required structure with an anti-shallow protocol, evidence extraction tables, and validity-mapped critique:

- **YAML frontmatter** — `category`, `tags`, `citekey`, `status`, `dateread`
- **Dataview callouts** — `[!Citation]`, `[!Synthesis]`, `[!Metadata]`, `[!Abstract]`
- **Academic sections** — Research Gap & Hypothesis · Methodology & Evidence · Key Findings · Critical Analysis (Strengths/Limitations/Open Questions) · Connections · Action Items · Summary
- **Wikilinks** — extensive linking of concepts, methods, proteins, diseases

The flow:

1. `phd-deepread generate <extraction_dir> -o <note.md>` writes a prompt file containing the extracted text plus the template instructions.
2. You (or Claude Code) read that prompt and overwrite the file with the finished note.

See `examples/example-output.md` for a complete worked example.

## Stage 3 — Critical-thinking canvas

A 9-node JSON Canvas based on `scripts/templates/critical-thinking.canvas`:

1. **core-argument** — primary claim, logical chain, argument type
2. **assumptions** — explicit, implicit, and most questionable assumption
3. **evidence-assessment** — strongest vs. weakest evidence, critical gaps, replication
4. **alternative-explanations** — competing hypotheses, confounding, reverse causation
5. **methodological-critique** — strongest design choice, most serious limitation, undiscussed gaps
6. **personal-relevance** — direct connections to your work, what you can use now
7. **future-directions** — immediate (1-2yr), medium-term (3-5yr), most important unanswered question
8. **critical-questions-enhanced** — falsifiability, weakest argument, boundary conditions
9. **hypothesis-center** — updated understanding, innovation/evidence/practical potential scores

The canvas can be populated from a finished note via regex section mapping:

```bash
phd-deepread canvas -o paper.canvas --from-note paper.md --overwrite
```

See `examples/example-canvas.canvas`.

## Stage 4 — Verification

```bash
phd-deepread verify markdown_output/<paper>/
```

Checks:
- YAML frontmatter present and well-formed
- Dataview callouts use correct syntax
- Wikilink density (target: 10+ links)
- Canvas has 9 nodes with the expected IDs

## Commands

```bash
phd-deepread doctor                                       # check dependencies
phd-deepread extract paper.pdf                            # PDF → markdown
phd-deepread generate markdown_output/paper/ -o note.md   # build prompt
phd-deepread canvas -o paper.canvas --from-note note.md   # canvas from note
phd-deepread run paper.pdf                                # full pipeline
phd-deepread batch papers/ -o batch_output                # whole folder
phd-deepread verify markdown_output/paper/
```

## Time per paper

| Stage | Time | Notes |
|-------|------|-------|
| Extraction | 10–40 min | depends on page count and OCR needs |
| Note writing | 10–25 min | Claude Code interaction time |
| Canvas | 5–10 min | template-based, light editing |
| Verification | 2–5 min | quick checks |

## Troubleshooting

**Tesseract OCR not installed** (only matters for scanned PDFs)
```bash
brew install tesseract           # macOS
sudo apt install tesseract-ocr   # Ubuntu/Debian
```

**PyMuPDF (fitz) not installed**
```bash
pip install PyMuPDF
```

**Missing images in extraction** — verify the PDF actually contains embedded images; some scanned PDFs do not.

**OCR pages not processed** — install Tesseract (above), check supported languages with `tesseract --list-langs`, and pass `--lang <code>` for non-English PDFs.

## Integration

- **Obsidian** — drop notes into your vault; they work with Dataview and the Canvas plugin out of the box.
- **Zotero** — use Zotero citation keys as the `citekey` field; export PDFs to your processing folder.

## References

- [PyMuPDF docs](https://pymupdf.readthedocs.io/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- Decision-tree details: `docs/decision-tree.md`
- Example note: `examples/example-output.md`
- Example canvas: `examples/example-canvas.canvas`
