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
phd-deepread doctor                       # check dependencies
phd-deepread extract paper.pdf -o markdown_output/
phd-deepread generate markdown_output/paper/
phd-deepread reformat markdown_output/paper/  # prompt to clean extraction → <paper>_formatted.md
phd-deepread canvas --title "Title" --authors "Author" --year "2024"
phd-deepread run paper.pdf              # full pipeline: extract → generate → canvas
phd-deepread batch papers/ -o output/
phd-deepread verify markdown_output/paper/
```

## Architecture

The CLI entry point is `scripts/phd_deepread.py:main()`, which dispatches commands to individual scripts via `subprocess`. Commands map to:

| Command | Script | Role |
|---------|--------|------|
| `doctor` (alias `setup`) | `scripts/doctor.py` | Dependency / first-run check |
| `extract` | `scripts/extract.py` | PDF → Markdown + images |
| `generate` | `scripts/generate.py` | Markdown → Claude prompt (structured literature note) |
| `reformat` | `scripts/reformat.py` | Extracted Markdown → Claude prompt that cleans it into an Obsidian-ready layout |
| `canvas` | `scripts/canvas.py` | → 9-node JSON Canvas file (optionally populated from a finished note via `--from-note`) |
| `run` | `scripts/process.py` | Orchestrates extract → generate prompt → canvas → reformat prompt |
| `verify` | `scripts/verify.py` | Quality checks on output directory |
| `batch` | `scripts/batch.py` | Loop `run` over a folder of PDFs |

### PDF Extraction (`extract.py`)

Uses a **Text-First decision tree**:
1. Pre-scan PDF with PyMuPDF — count pages with >100 chars of extractable text
2. If ≥80% of pages are searchable → extract all with PyMuPDF (fast path)
3. For non-searchable pages → fall back to Tesseract OCR
4. Always extract images via PyMuPDF

Output per paper: `markdown_output/<paper_name>/` containing a `.md` file, `*_meta.json`, and extracted images.

### Note Generation (`generate.py`)

Reads the extracted markdown and loads the **clauderules template** from `scripts/templates/clauderules.md` using `importlib.resources` (reliable in installed packages). It builds a formatted prompt for Claude Code to generate a structured literature note. Does not call any LLM directly — it prepares the prompt and prints it (or writes it to `-o <file>`) for Claude Code to consume.

The clauderules template produces **plain section headings (no emoji) and tight frontmatter** to match the polished Obsidian demo style — see `examples/example-output.md`. `verify.py` matches headings emoji-tolerantly (`strip_heading_emoji`) so older emoji-decorated notes still pass.

### Final Reformat (`reformat.py`)

A **prompt-only polish pass** that mirrors `generate.py`: it reuses `generate.py`'s `find_extracted_files` / `load_template` / `extract_paper_info` helpers, loads `scripts/templates/reformat.md`, embeds the *full* extracted text (not truncated), and emits a prompt asking Claude Code to reflow paragraphs, dehyphenate, rebuild tables, strip page/header artifacts, and collapse back-matter (references, abbreviations, declarations) into foldable Obsidian callouts. Claude Code writes the cleaned copy to `<paper>_formatted.md` inside the extraction directory — the filename the rest of the pipeline already treats as the polished version (`generate.py`/`verify.py` exclude `_formatted.md` from extraction-source globbing). Like `generate.py`, it makes no LLM API calls. In `run`, this is the final, non-fatal step.

### Canvas Creation (`canvas.py`)

Produces a JSON file compatible with Obsidian Canvas plugin. The canvas has 9 fixed nodes (core argument, assumptions, evidence assessment, alternative explanations, methodological critique, personal relevance, future directions, critical questions, hypothesis center) with pre-defined spatial layout and labeled edges connecting nodes in a critical-thinking flow.

### Templates (`scripts/templates/`)

- `clauderules.md` — Instruction-driven template (~230 lines) defining the structured literature note format with anti-shallow protocol, evidence tables, and validity-mapped critique. Loaded via `importlib.resources` in `generate.py`.
- `reformat.md` — Instruction-driven template for the final reformat pass (reflow/dehyphenate/rebuild-tables/strip-artifacts/collapse-back-matter). Loaded via `importlib.resources` in `reformat.py`. Contains an `{output_path}` placeholder the script fills in. Do **not** add triple-backtick fences to this or `clauderules.md` — both are embedded inside a fenced block in the generated prompt, so nested fences would break it.
- `critical-thinking.canvas` — base canvas layout used by `canvas.py`.

These files must stay in `scripts/templates/` and are covered by the `templates/*` `package_data` glob in `pyproject.toml`.

## Key Design Decisions

- **No direct LLM API calls** — the workflow prepares prompts for Claude Code to consume; the CLI itself is dependency-free from any LLM SDK. OpenAI integration was added in v0.2.0 and removed shortly after — do not reintroduce it. The audience is Claude-Code-skill users.
- **`importlib.resources` for templates** — switched from filesystem path heuristics in v0.1.6 after templates failed to load in installed packages. Do not revert to `Path(__file__).parent` for template loading.
- **Tesseract is optional** — the tool degrades gracefully if Tesseract is absent; only scanned PDFs are affected.
- **`config/config.yaml` is documentation-only** — no scripts read this file at runtime. Extraction thresholds and paths are controlled via CLI flags and hardcoded constants in each script.
- **All scripts are Python** — `setup.sh` and `batch.sh` were ported to `doctor.py` and `batch.py` so the CLI works after `pip install` (shell scripts were not in `package_data`).
- **Plugin-install-first** — `/plugin install phd-deepread` is the preferred install path. `AGENTS.md` is the executable spec with two paths: plugin (preferred) and manual skill (fallback). There is no standalone pip-only path — the workflow requires Claude Code and Obsidian to deliver its value (structured notes + critical-thinking canvas).
