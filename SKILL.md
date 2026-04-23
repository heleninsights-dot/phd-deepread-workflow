---
name: phd-deepread
description: "Extracts text and figures from research papers, journal articles, and academic PDFs using PyMuPDF with Tesseract OCR fallback, generates structured Obsidian literature notes with YAML frontmatter and Dataview callouts, and creates 9-node JSON Canvas files for critical analysis. Use when the user wants to process academic PDFs into reading notes, summarize research papers, create literature review notes, extract citations and key findings, or batch-process a collection of papers for an Obsidian vault."
allowed-tools: "Bash, Write, Read, Edit, Glob, Grep, Skill"
---

# PhD Deep Read Workflow

Four-stage pipeline: extract text from academic PDFs → generate structured literature notes → create critical-thinking canvases → verify output quality.

## Commands

### setup

Install and verify dependencies (PyMuPDF, Tesseract OCR, Python 3.10+):

```bash
python scripts/phd_deepread.py setup
```

**Validation**: Confirm `import fitz` succeeds and `tesseract --version` returns a version string.

### extract

Extract text and images from a PDF using the Text-First decision tree. Pre-scans each page with PyMuPDF — pages with ≥100 searchable characters use direct text extraction; others fall back to Tesseract OCR. See [decision-tree.md](docs/decision-tree.md) for the full algorithm.

```bash
python scripts/phd_deepread.py extract paper.pdf --output markdown_output/
```

**Output**: `markdown_output/[PDF_NAME]/` containing `.md`, `_meta.json`, `blocks.json`, and extracted images.

**Validation**: Check `_meta.json` — every page should have `text_extraction_method` set to `pdftext` or `tesseract` and `block_counts.characters > 0`.

### generate

Generate a structured literature note using the clauderules template at `scripts/templates/clauderules.md`. Produces YAML frontmatter (`category`, `tags`, `citekey`, `status`, `dateread`), Dataview callouts (`[!Citation]`, `[!Synthesis]`, `[!Metadata]`, `[!Abstract]`), and academic analysis sections with extensive [[Wikilinks]].

```bash
python scripts/phd_deepread.py generate markdown_output/paper/ --template scripts/templates/clauderules.md
```

**Validation**: Output note must contain valid YAML frontmatter, ≥10 [[Wikilinks]], and all required Dataview callouts.

### canvas

Create a JSON Canvas with 9 interconnected critical-thinking nodes: core-argument, assumptions, evidence-assessment, alternative-explanations, methodological-critique, personal-relevance, future-directions, critical-questions-enhanced, hypothesis-center. See `scripts/templates/critical-thinking.canvas` for the template.

```bash
python scripts/phd_deepread.py canvas --title "Paper Title" --authors "Author" --year "2024"
```

**Validation**: Output `.canvas` must be valid JSON with exactly 9 nodes and connecting edges.

### run

Execute the full pipeline (extract → generate → canvas) for a single PDF:

```bash
python scripts/phd_deepread.py run paper.pdf
```

### batch

Process a directory of PDFs through all stages:

```bash
python scripts/phd_deepread.py batch papers/ --output literature-notes/
```

### verify

Check output quality and consistency against existing corpus patterns:

```bash
python scripts/phd_deepread.py verify structured_notes/
```

## Key Configuration

| Parameter | Default | Effect |
|-----------|---------|--------|
| `--threshold` | 100 | Min characters to consider a page searchable |
| `--percentage` | 0.8 | Fraction of searchable pages before skipping OCR entirely |
| `--lang` | eng | Tesseract OCR language code |
| `--force-ocr` | false | Force OCR on all pages, bypassing the decision tree |

## Setup Requirements

- **Python 3.10+** with virtual environment (`source .venv/bin/activate`)
- **PyMuPDF**: `pip install PyMuPDF`
- **Tesseract OCR** (optional fallback): `brew install tesseract` (macOS) or `sudo apt install tesseract-ocr` (Linux)

## Reference

- [Decision tree architecture](docs/decision-tree.md) — per-page extraction logic and configuration
- [Full workflow guide](docs/workflow-guide.md) — detailed stage descriptions and time estimates
- [Example output note](examples/example-output.md)
- [Example canvas](examples/example-canvas.canvas)
- [Literature note template](scripts/templates/clauderules.md)
- [Critical thinking canvas template](scripts/templates/critical-thinking.canvas)
