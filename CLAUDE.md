# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install
pip install -r requirements.txt          # core deps (PyMuPDF, pytesseract, Pillow)
pip install -r requirements-dev.txt      # dev deps (pytest, black, flake8, mypy)
brew install tesseract                   # required OCR engine (macOS)

# Test
make test                                # run all tests
pytest tests/test_canvas.py -v          # run single test file
pytest -m "not slow"                    # skip slow tests (markers: slow, integration)
make test-cov                           # with coverage report

# Code quality
make lint                               # flake8
make format                             # black + isort
make type-check                         # mypy
make check                              # all of the above + test

# Build & publish
make build                              # creates dist/
make publish-test                       # upload to TestPyPI
make publish                            # upload to PyPI

# Run the CLI locally
phd-deepread extract paper.pdf -o markdown_output/
phd-deepread generate markdown_output/paper/
phd-deepread canvas --title "Title" --authors "Author" --year "2024"
phd-deepread run paper.pdf              # full pipeline: extract → generate → canvas
phd-deepread batch papers/ -o output/
phd-deepread verify markdown_output/paper/
```

## Architecture

The CLI entry point is `scripts/phd_deepread.py:main()`, which dispatches commands to individual scripts via `subprocess`. Commands map to:

| Command | Script | Role |
|---------|--------|------|
| `extract` | `scripts/extract.py` | PDF → Markdown + images |
| `generate` | `scripts/generate.py` | Markdown → Claude prompt + skeleton note |
| `canvas` | `scripts/canvas.py` | → 9-node JSON Canvas file |
| `run` | `scripts/process.py` | Orchestrates extract → generate → canvas |
| `verify` | `scripts/verify.py` | Quality checks on output directory |
| `batch` | `scripts/batch.sh` | Loop `run` over a folder of PDFs |

### PDF Extraction (`extract.py`)

Uses a **Text-First decision tree**:
1. Pre-scan PDF with PyMuPDF — count pages with >100 chars of extractable text
2. If ≥80% of pages are searchable → extract all with PyMuPDF (fast path)
3. For non-searchable pages → fall back to Tesseract OCR
4. Always extract images via PyMuPDF

Output per paper: `markdown_output/<paper_name>/` containing a `.md` file, `*_meta.json`, and extracted images.

### Note Generation (`generate.py`)

Reads the extracted markdown and loads the **clauderules template** from `scripts/templates/clauderules.md` using `importlib.resources` (reliable in installed packages). It builds a formatted prompt for Claude Code to generate a structured literature note. Does not call Claude directly — it prepares the prompt and prints it for the user to run in Claude Code. The `--skeleton` flag exists in the CLI but generation is not yet implemented.

### Canvas Creation (`canvas.py`)

Produces a JSON file compatible with Obsidian Canvas plugin. The canvas has 9 fixed nodes (core argument, assumptions, evidence assessment, alternative explanations, methodological critique, personal relevance, future directions, critical questions, hypothesis center) with pre-defined spatial layout and wikilink-style connections.

### Templates (`scripts/templates/`)

- `clauderules.md` — 175+ line template defining the structured literature note format (YAML frontmatter, Dataview callouts, academic sections, wikilinks). Loaded via `importlib.resources` in `generate.py`.
- `critical-thinking.canvas` — base canvas layout used by `canvas.py`.

Both files must stay in `scripts/templates/` and are declared as `package_data` in `pyproject.toml`.

## Key Design Decisions

- **No direct Claude API calls** — the workflow prepares prompts for the user to run manually in Claude Code. This is intentional: it keeps the tool dependency-free from the Anthropic SDK.
- **`importlib.resources` for templates** — switched from filesystem path heuristics in v0.1.6 after templates failed to load in installed packages. Do not revert to `Path(__file__).parent` for template loading.
- **Tesseract is optional** — the tool degrades gracefully if Tesseract is absent; only scanned PDFs are affected.
- **`config/config.yaml` is documentation-only** — no scripts read this file at runtime. Extraction thresholds and paths are controlled via CLI flags and hardcoded constants in each script.
- **`ENABLE_EFFICIENT_ATTENTION=0`** — set this env var if using Surya OCR to avoid CUDA SDPA errors on CPU.
