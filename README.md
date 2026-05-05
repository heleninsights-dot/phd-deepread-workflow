---
feature: thumbnails/external/74a4c4ea2d920c8d9a05a7420946145d.svg
thumbnail: thumbnails/external/74a4c4ea2d920c8d9a05a7420946145d.svg
---
# PhD Deep Read Workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/phd-deepread-workflow.svg)](https://pypi.org/project/phd-deepread-workflow/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-6E56CF)](https://claude.com/claude-code)

> Transform academic PDFs into structured literature notes and critical-thinking canvases for Obsidian using AI-assisted analysis.

## What it does

- **Extracts text and images** from PDFs — uses PyMuPDF for searchable PDFs (fast), falls back to Tesseract OCR only for scanned pages
- **Generates structured literature notes** via a Claude Code prompt built from the `.clauderules` template (YAML frontmatter, Dataview callouts, wikilinks)
- **Creates 9-node critical-thinking canvases** (core argument, assumptions, evidence, methodology, relevance, future directions…) as Obsidian-compatible JSON Canvas files
- **Automates the full pipeline** — one command runs extract → generate → canvas

## Prerequisites

- **Python 3.9+** and `pip`
- **Claude Code** — for note generation (free tier works)
- **Tesseract OCR** — optional, only needed for scanned/image-only PDFs

## Installation

```bash
pip install phd-deepread-workflow
```

Then install Tesseract OCR (the engine that reads image-based text):

```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt install tesseract-ocr
```

> **Not sure if you need Tesseract?**
> Most PDFs downloaded from journal websites are "searchable" — you can highlight and copy text in them. Those work without Tesseract.
> Older scanned papers (e.g., a 1990s article photographed and saved as PDF) are image-only — Tesseract is needed for those.
> **When in doubt, install Tesseract anyway** — it's a one-line command and won't cause any harm. After installing, run `phd-deepread setup` to confirm everything is ready.

## Quick Start

### One command — full pipeline

```bash
phd-deepread run paper.pdf
```

This runs extract → generate → canvas automatically and prints the Claude Code prompt for note generation.

### Step by step

```bash
# 1. Extract text and images from PDF
phd-deepread extract paper.pdf --output markdown_output/

# 2. Build and print the Claude Code prompt for note generation
phd-deepread generate markdown_output/paper/

# 3. Create the critical-thinking canvas
phd-deepread canvas --title "Paper Title" --authors "Smith, J." --year "2024" \
  -o structured_notes/SmithPaper2024-CriticalThinking.canvas
```

### Batch process a folder of PDFs

```bash
phd-deepread batch papers/ --output literature-notes/
```

Or drag-and-drop in terminal: type `phd-deepread batch `, drag your PDF folder, type ` --output `, drag your Obsidian output folder, press Enter.

## Commands

| Command | What it does |
|---------|-------------|
| `setup` | Check and install dependencies |
| `extract <pdf>` | Extract text + images from a PDF |
| `generate <dir>` | Build the Claude Code prompt for note generation |
| `canvas` | Create a 9-node critical-thinking canvas |
| `run <pdf>` | Full pipeline: extract → generate → canvas |
| `batch <dir>` | Process all PDFs in a directory |
| `verify <dir>` | Quality-check output for format consistency |
| `guide` | Show interactive workflow guide |

## Detailed Usage

### Extraction options

```bash
phd-deepread extract paper.pdf \
  --output markdown_output/ \
  --threshold 100 \      # Min chars to count a page as searchable (default: 100)
  --percentage 0.8 \     # Use PyMuPDF if ≥80% of pages are searchable (default: 0.8)
  --lang eng \           # OCR language (default: eng)
  --force-ocr \          # Force OCR for every page
  --force-text \         # Force PyMuPDF for every page (skip OCR)
  --no-ocr               # Disable OCR entirely
```

Output per paper:

```
markdown_output/paper/
├── paper.md            # Extracted text with embedded image references
├── paper_meta.json     # Metadata and extraction method per page
└── _page_*_*.png       # Extracted images
```

### Note generation

```bash
phd-deepread generate markdown_output/paper/
```

Prints a formatted prompt. Paste it into Claude Code — Claude produces a structured note with:
- YAML frontmatter (`citekey`, `tags`, `status`, `dateread`)
- Dataview callouts (`[!Citation]`, `[!Synthesis]`, `[!Abstract]`)
- Academic analysis sections with wikilinks

### Canvas creation

```bash
phd-deepread canvas \
  --title "Paper Title" \
  --authors "Smith, J., Doe, A." \
  --year "2024" \
  -o structured_notes/SmithPaper2024-CriticalThinking.canvas
```

Creates 9 interconnected nodes: core-argument, assumptions, evidence-assessment, alternative-explanations, methodological-critique, personal-relevance, future-directions, critical-questions-enhanced, hypothesis-center.

Open in Obsidian with the Canvas plugin and fill in each node.

### Verification

```bash
phd-deepread verify literature-notes/
```

## Troubleshooting

**Tesseract not found:**
```bash
brew install tesseract          # macOS
sudo apt install tesseract-ocr  # Ubuntu/Debian
pip install pytesseract pillow
```

**PyMuPDF missing:**
```bash
pip install PyMuPDF
```

**Template not found after `pip install`:**
Upgrade to the latest version which uses `importlib.resources` for reliable template loading:
```bash
pip install --upgrade phd-deepread-workflow
```

**Virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
pip install phd-deepread-workflow
```

## Integration

### Obsidian
- Notes are ready for Dataview queries out of the box
- Canvas files open directly with the Obsidian Canvas plugin
- Wikilinks connect to existing or future notes

### Zotero
- Use Zotero citation keys as `citekey` in the generated frontmatter
- Export PDFs from Zotero to your processing folder

## Examples

See the `examples/` directory:
- `example-output.md` — complete structured literature note
- `example-canvas.canvas` — 9-node critical-thinking canvas

## Testing

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
pytest -m "not slow"   # skip slow integration tests
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit and push, then open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT — see [LICENSE](LICENSE).

## Support

- Issues: [GitHub Issues](https://github.com/heleninsights-dot/phd-deepread-workflow/issues)
- Email: [heleninsights@gmail.com](mailto:heleninsights@gmail.com)

---

<div align="center">
  <p>Made with love for the academic community</p>
  <p>If this workflow helps your research, consider giving it a star on GitHub!</p>
</div>
