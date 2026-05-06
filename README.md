# PhD Deep Read Workflow

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/phd-deepread-workflow.svg)](https://pypi.org/project/phd-deepread-workflow/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-6E56CF)](https://claude.com/claude-code)

> Transform academic PDFs into structured literature notes and critical-thinking canvases for Obsidian, with Claude doing the writing.

---

## Install

**Using Claude Code?** Paste this one line into a Claude Code chat — Claude will install the skill for you:

> Install this skill for me: https://github.com/heleninsights-dot/phd-deepread-workflow

That's it. Claude reads `AGENTS.md` in this repo, runs the install steps, and tells you when it's ready.

After it finishes, drag a PDF into a new Claude Code chat and say *"process this paper with phd-deepread"*.

> Don't have Claude Code yet? [Install it first](https://docs.claude.com/en/docs/claude-code/quickstart) (one command), then come back here.

---

## What you get

Each PDF you process gives you three files:

| Output | What it is |
|--------|-----------|
| `paper.md` | Full text of the PDF, converted to Markdown |
| `paper_literature_note.md` | Structured academic note — summary, critique, wikilinks, Obsidian frontmatter — written by Claude |
| `paper.canvas` | A 9-node critical-thinking canvas, ready to open in Obsidian |

---

## Using the workflow

After install, in a Claude Code chat:

1. **Drag a PDF into the chat** (or paste its file path).
2. **Ask Claude:** *"Process this paper with phd-deepread"*.
3. Claude runs the extraction, writes the literature note, and creates the canvas — all in one go.

You can also be more specific: *"Extract this PDF and just give me the prompt — I'll write the note myself."*

---

## What lives behind the scenes

The skill exposes a small CLI (`phd-deepread`). You don't need to type these — Claude calls them for you — but here they are:

| Command | What it does |
|---------|-------------|
| `setup` | Check that all dependencies are installed |
| `extract <pdf>` | Extract text and images from a PDF |
| `generate <dir>` | Build a literature-note prompt from extracted text |
| `canvas -o <file> [--from-note <md>]` | Create a 9-node canvas; populate from a finished note with `--from-note` |
| `run <pdf>` | Full pipeline: extract → generate prompt → canvas |
| `batch <dir>` | Process all PDFs in a folder |
| `verify <dir>` | Quality-check output files |
| `guide` | Show the workflow guide |

---

## Integration with Obsidian and Zotero

**Obsidian:** Notes use YAML frontmatter and Dataview-compatible callouts. Canvas files open with the Obsidian Canvas plugin. Wikilinks connect to your existing notes.

**Zotero:** Use your Zotero citation key as the `citekey` field in the generated note. Export PDFs from Zotero into your processing folder before running the workflow.

---

## Advanced — manual (pip) install

If you don't use Claude Code, or you want the standalone CLI:

```bash
python3 -m pip install --user phd-deepread-workflow
```

Requires Python 3.10+. For scanned PDFs (image-based), also install Tesseract:

```bash
brew install tesseract          # macOS
sudo apt install tesseract-ocr  # Ubuntu/Debian
```

Then run any of the commands in the table above. The note step prints a prompt you paste into your AI chat tool of choice.

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
