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

---

## What you get

When you run this workflow on a PDF, you get three output files:

| Output | What it is |
|--------|-----------|
| `paper.md` | The full text of your PDF, converted to Markdown |
| `paper_literature_note.md` | A structured academic note — with summary, critique, wikilinks, and Obsidian frontmatter — written by Claude |
| `paper.canvas` | A 9-node critical-thinking canvas for deep analysis, ready to open in Obsidian |

---

## Installation

### Step 1 — Install Python (if you don't have it)

`pip` is Python's built-in package installer — it comes with Python automatically. So installing Python is all you need to get pip.

**Check if you already have Python:**
```bash
python3 --version
```

If you see `Python 3.9.x` or higher, skip to Step 2. If not, download it from [python.org](https://www.python.org/downloads/).

---

### Step 2 — Install the workflow

This one command installs the `phd-deepread` CLI and all the PDF/OCR libraries it needs:

```bash
pip install phd-deepread-workflow
```

**What this installs:**
- The `phd-deepread` command you'll type in the terminal
- PyMuPDF — fast PDF text extraction
- pytesseract + Pillow — OCR for scanned PDFs
- The built-in templates for notes and canvases

**What this does NOT install** (because they are not Python packages):
- An AI provider — needed for note generation; set up in Step 3
- Tesseract OCR engine — needed only for scanned PDFs; see Step 4

---

### Step 3 — Set up an AI provider (required for note generation)

The workflow uses AI to read your paper and write the structured literature note. Set up an API key for your chosen provider and export it as an environment variable before running:

```bash
export OPENAI_API_KEY=sk-...        # OpenAI — use with --openai flag
# or
export ANTHROPIC_API_KEY=sk-...     # Anthropic / Claude Code
```

To make it permanent, add the line to your `~/.zshrc` or `~/.bashrc`.

> **For users in China:** OpenAI and Anthropic may not be directly accessible from mainland China. Consider using a domestic provider such as [DeepSeek](https://platform.deepseek.com) — it is OpenAI-compatible. Set `OPENAI_API_KEY` to your DeepSeek key and pass `--model deepseek-chat --base-url https://api.deepseek.com` when running.

---

### Step 4 — Install Tesseract (optional — only for scanned PDFs)

Tesseract reads text from image-based PDFs (e.g. old scanned papers). Skip this if your PDFs come from a journal website — they almost always have selectable text.

**Not sure if you need it?** Open your PDF and try to highlight text. If you can highlight it, you don't need Tesseract.

```bash
brew install tesseract          # macOS
sudo apt install tesseract-ocr  # Ubuntu/Debian
```

---

### Verify everything is ready

```bash
phd-deepread setup
```

---

## Running the workflow

### The simplest way — one command

```bash
# With OpenAI (fully automatic — no copy-pasting)
phd-deepread run paper.pdf --openai

# Without an API key (prints a prompt to paste into Claude Code manually)
phd-deepread run paper.pdf
```

> **Tip for beginners:** Not sure how to type a file path? Drag and drop the PDF from Finder/Explorer directly into the terminal window — it fills in the path for you.

---

### Step by step (if you prefer more control)

**Step 1 — Extract the PDF**

```bash
phd-deepread extract paper.pdf
```

Creates `markdown_output/paper/` with the extracted text and images.

**Step 2 — Generate the literature note**

```bash
# With OpenAI — writes the note directly to a file
phd-deepread generate markdown_output/paper/ --openai -o notes/paper.md

# Without OpenAI — prints a prompt to paste into Claude Code
phd-deepread generate markdown_output/paper/
```

**Step 3 — Create the canvas from the note**

```bash
# With OpenAI — fills all 9 canvas nodes from the note automatically
phd-deepread canvas -o notes/paper.canvas --from-note notes/paper.md --openai

# Without OpenAI — creates a canvas with blank node templates to fill in yourself
phd-deepread canvas --title "Paper Title" --authors "Smith, J." --year "2024" \
  -o notes/paper.canvas
```

---

### Batch process a whole folder of PDFs

```bash
phd-deepread batch papers/ --output literature-notes/
```

> **Tip:** You can drag and drop folders too — type `phd-deepread batch `, drag your PDF folder into the terminal, type ` --output `, drag your output folder, then press Enter.

---

## What to do with the output

After running the workflow, open your output folder. You will find:

```
markdown_output/paper/
├── paper.md                  ← Full extracted text (Markdown)
├── paper_literature_note.md  ← Structured note written by Claude
├── paper.canvas              ← Critical-thinking canvas for Obsidian
├── paper_meta.json           ← Extraction metadata (for reference)
└── _page_*_*.png             ← Any images extracted from the PDF
```

- **Open `.md` files** in Obsidian, Typora, or any Markdown editor
- **Open `.canvas` files** in Obsidian with the Canvas plugin enabled
- **Copy notes into your Obsidian vault** — they are already formatted with YAML frontmatter and Dataview callouts

---

## Troubleshooting

**"command not found: phd-deepread"**
The package installed but your terminal can't find it. Try:
```bash
python3 -m pip install phd-deepread-workflow
python3 -m phd_deepread_workflow
```
Or open a new terminal window after installing.

**"command not found: claude"**
Claude Code isn't installed or not in your PATH. Install it:
```bash
npm install -g @anthropic-ai/claude-code
```
Then open a new terminal window and try again. Alternatively, use `--openai` with an OpenAI API key instead.

**The literature note was not generated**
- With `--openai`: check that `OPENAI_API_KEY` is set (`echo $OPENAI_API_KEY`). If empty, run `export OPENAI_API_KEY=sk-...`
- Without `--openai`: the command prints a prompt — copy it and paste it into a Claude Code session manually.

**"Tesseract not found"**
```bash
brew install tesseract          # macOS
sudo apt install tesseract-ocr  # Ubuntu/Debian
```

**"PyMuPDF missing"**
```bash
pip install PyMuPDF
```

**"Template not found" after installing**
```bash
pip install --upgrade phd-deepread-workflow
```

**Using a virtual environment (recommended for clean installs)**
```bash
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
# or: venv\Scripts\activate   # Windows
pip install phd-deepread-workflow
```

---

## All commands

| Command | What it does |
|---------|-------------|
| `setup` | Check that all dependencies are installed |
| `extract <pdf>` | Extract text and images from a PDF |
| `generate <dir> [--openai]` | Generate literature note — calls OpenAI directly with `--openai`, otherwise prints a prompt |
| `canvas -o <file> [--from-note <md> --openai]` | Create a 9-node canvas; populate from a note automatically with `--openai` |
| `run <pdf> [--openai]` | Full pipeline: extract → generate → canvas |
| `batch <dir>` | Process all PDFs in a folder |
| `verify <dir>` | Quality-check output files |
| `guide` | Show the workflow guide |

---

## Integration with Obsidian and Zotero

**Obsidian:** Notes use YAML frontmatter and Dataview-compatible callouts out of the box. Canvas files open with the Obsidian Canvas plugin. Wikilinks connect to your existing notes.

**Zotero:** Use your Zotero citation key as the `citekey` field in the generated note. Export PDFs from Zotero into your processing folder before running the workflow.

---

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
