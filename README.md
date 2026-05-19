# PhD Deep Read Workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/phd-deepread-workflow.svg)](https://pypi.org/project/phd-deepread-workflow/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-6E56CF)](https://claude.com/claude-code)
[![中文版本](https://img.shields.io/badge/README-%E4%B8%AD%E6%96%87%E7%89%88-green)](README.zh-CN.md)

> Transform academic PDFs into structured literature notes and critical-thinking canvases for Obsidian.

---

> *"The human mind... operates by association. With one item in its grasp, it snaps instantly to the next that is suggested by the association of thoughts."*
> — Vannevar Bush, *As We May Think*, 1945

Bush imagined this in 1945 — a desk where all your reading lives outside its original containers, ready for you to build trails of association through it. That's what this workflow is.

**Step one:** Convert the PDF to Markdown. The knowledge leaves the frozen PDF and becomes something you can return to, search, and connect — today, next month, next year.

**Step two:** Come back anytime and draw out what's relevant now. Connect ideas across papers. Visualize arguments, evidence, and assumptions side by side in an Obsidian canvas. The literature note captures what's there. The canvas lets you see it alongside everything else you know.

---

## Prerequisites

You need both of these:

- **Claude Code** — [download here](https://claude.com/claude-code) if you don't have it yet. This workflow only works inside Claude Code.
- **Obsidian** — [download here](https://obsidian.md). The final output is a JSON canvas file that only renders in Obsidian.

If you just want AI help reading a PDF, you don't need this workflow. Drag the PDF into any AI chat and ask questions directly. This workflow is for people who want structured literature notes and a critical-thinking canvas they can revisit in Obsidian.

---

## Install in 30 seconds

Paste this into Claude Code:

```
Install this skill for me: https://github.com/heleninsights-dot/phd-deepread-workflow
```

Claude Code installs the skill, the Python CLI, and everything else automatically. Done. Drag a PDF into Claude Code and say **"phd-deepread read this paper"**.

### Optional: Tesseract OCR

Only needed if you work with scanned PDFs (image-based, text not selectable):

```bash
brew install tesseract          # macOS
sudo apt install tesseract-ocr  # Ubuntu/Debian
```

---

## Using the workflow

### One paper

Drag a PDF into Claude Code and say:

> **phd-deepread read this paper**

Claude extracts the text, writes a structured literature note, and creates a 9-node critical-thinking canvas — all in one go. Open the `.canvas` file in Obsidian to visualize arguments, evidence, assumptions, and gaps side by side.

You can also ask for specific parts: *"phd-deepread extract this PDF, but just give me the prompt — I'll write the note myself."*

### A folder of papers

Drag a folder into Claude Code and say:

> **phd-deepread read this folder**

Claude batch-processes every PDF inside — extracting text, writing a structured literature note for each one, and creating canvas templates. Already-processed papers are skipped automatically. Works the same as a single paper, just for the whole folder.

---

## What you get

Each PDF you process gives you three files:

| Output | What it is |
|--------|-----------|
| `paper.md` | Full text of the PDF, converted to Markdown |
| `paper_literature_note.md` | Structured academic note — see below for what's extracted |
| `paper.canvas` | A 9-node critical-thinking canvas — **open this in Obsidian** to visualize arguments, evidence, assumptions, and gaps side by side |

### What the literature note extracts

The note doesn't summarize — it pulls out the specific data you need to actually use the paper in your research:

| Category | What you get |
|----------|-------------|
| **Findings** | Every key result with direction, magnitude, p-value, confidence interval, effect size, and source table/figure |
| **Methodology** | Study design, sample sizes with attrition, inclusion/exclusion criteria, every instrument/assay/software named |
| **Critique** | Limitations mapped to validity types (internal, external, construct, statistical), plus limitations the authors don't discuss |
| **Connections** | Extensive [[wikilinks]] to methods, proteins, genes, diseases, concepts — linking the paper to your existing notes |
| **Action items** | Specific, actionable follow-ups you can act on without re-reading the paper |
| **Assessment** | Innovation, evidence strength, and practical potential — each with a concrete justification, not just a score |

---

## CLI reference

Claude Code calls these commands for you — you don't need to type them yourself:

| Command | What it does |
|---------|-------------|
| `doctor` | Check that all dependencies are installed |
| `extract <pdf>` | Extract text and images from a PDF |
| `generate <dir>` | Build a literature-note prompt from extracted text |
| `canvas -o <file> [--from-note <md>]` | Create a 9-node canvas; populate from a finished note with `--from-note` |
| `run <pdf>` | Full pipeline: extract → generate prompt → canvas |
| `batch <dir>` | Process all PDFs in a folder |
| `verify <dir>` | Quality-check output files |

---

## Integration with Obsidian and Zotero

**Obsidian:** Notes use YAML frontmatter and Dataview-compatible callouts. Canvas files open with the Obsidian Canvas plugin. Wikilinks connect to your existing notes.

**Zotero:** Use your Zotero citation key as the `citekey` field in the generated note. Export PDFs from Zotero into your processing folder before running the workflow.

---

## Troubleshooting

**"command not found: phd-deepread"** — your terminal can't see the install location. Open a new terminal window. If still missing, add `~/.local/bin` to your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

**"Tesseract not found"** — only matters for scanned PDFs:

```bash
brew install tesseract          # macOS
sudo apt install tesseract-ocr  # Ubuntu/Debian
```

**"Template not found" after installing** — upgrade to the latest version:

```bash
pip install --upgrade phd-deepread-workflow
```

**Using a virtual environment (cleanest install)**

```bash
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
# or: venv\Scripts\activate   # Windows
pip install phd-deepread-workflow
```

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
