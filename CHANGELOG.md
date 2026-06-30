# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Claude Code Plugin support** — `.claude-plugin/` with `plugin.json` and `marketplace.json` for `/plugin marketplace add` and `/plugin install` workflow
- **Manual skill install files** — `skills/deepread/SKILL.md` for users who prefer manual skill install over plugin
- **Chinese README** — `README.zh-CN.md` translation for Chinese-speaking researchers (linked from main README)
- **Prerequisites section** — both AGENTS.md and README now explicitly check for Claude Code + Obsidian before install; AGENTS.md tells users who only want AI help reading a PDF they don't need this tool
- **Bush epigraph** — README opens with the Vannevar Bush "As We May Think" quote placing the workflow in the tradition of associative trails
- **Output expectations table** — README now includes a structured table showing exactly what the literature note extracts (findings with stats, methodology details, critique mapped to validity types, wikilinks, action items, scored assessment)
- **Anti-Shallow Protocol** — clauderules template now enforces concrete output with banned phrases, mandatory practices (numbers over adjectives, named entities, verbatim quoting, noting absent data), minimum 25 wikilinks, and 3-bullet-per-section minimums
- **Three-phase task structure** — clauderules now splits work into EXTRACTION → ANALYSIS → OUTPUT phases so Claude collects all concrete data before writing
- **ANALYSIS phase** — new middle phase in clauderules requiring explicit critical evaluation of evidence support, assumptions, alternative explanations, and validity threats before writing the note
- **Wikilink count warning** — verify.py now alerts when wikilink count is below 15, recommending 25+ for dense concept linking
- **Canvas node derivation** — `populate_nodes_from_note()` now derives assumptions and alternative-explanations nodes from populated content when they are not directly mappable from the note
- **Canvas truncation** — long sections (>800 chars) are now truncated in canvas nodes with a pointer to the full literature note

### Changed
- **Repositioned as Claude Code skill** — removed the standalone-pip focus; install flow now leads with `/plugin install` and manual skill install
- **Removed OpenAI integration** — `--openai`, `--model`, `--base-url` flags removed from generate, canvas, and run commands; workflow returns to Claude-Code-native model (Claude does the writing)
- **AGENTS.md rewritten** — restructured as executable spec with prerequisites check, two install paths (30-second plugin → manual fallback), and end-to-end value statement
- **README rewritten** — prerequisite callout, simplified dual install paths, Bush epigraph, output structure table, CLI reference table
- **clauderules template overhauled** (~224 lines changed) — replaced generic placeholders with specific extraction requirements (sample sizes, instruments, p-values, CIs, effect sizes), added explicit role definition, and mandated concrete data over adjectives
- **Canvas nodes rewritten** — all 9 node templates upgraded from generic numbered placeholders to focused annotation prompts (e.g. "The single piece of evidence that carries the most weight, with numbers", "Which assumption, if wrong, would most damage the conclusions?")
- **Canvas section mapping expanded** — `populate_nodes_from_note()` now maps Problem Context, Study Characteristics, Open Questions, Integration, and Final Assessment sections from the updated note structure
- **generate.py prompt sharpened** — emphasizes evidence-density and explicit data extraction from the paper text
- **Hypothesis center node** — replaced Innovation/Plausibility/Evidence scores with Innovation/Evidence Strength/Practical Potential to better serve research decision-making
- **verify.py** — added wikilink count warning threshold (below 15)
- **AGENTS.md install paths** — renamed from "Install path A / B" to "30 seconds (fastest)" and "Paste one line (just as easy)" for clearer user guidance
- **SKILL.md** — synced with plugin metadata to reference phd-deepread.read

### Fixed
- Canvas next-steps message now guides users to "review and refine" prompts rather than "fill in" from scratch (nodes now contain annotation prompts, not blanks)
- Section map in `populate_nodes_from_note()` now uses proper word-boundary regex to avoid partial section name matches

---

## [0.2.2] - 2026-06-30

### Added
- **`reformat` command** — a final polish pass that emits a prompt asking Claude Code to clean the raw extraction into an Obsidian-ready layout: reflow paragraphs, dehyphenate words split across line breaks, rebuild tables from the raw text, strip page/header/footer artifacts, and collapse back-matter (references, abbreviations, declarations) into foldable callouts. Like `generate`, it makes no LLM API calls — it writes the cleaned copy to `<paper>_formatted.md`. `run` now emits this prompt automatically as its final step.
- **`scripts/templates/reformat.md`** — instruction template for the reformat pass (loaded via `importlib.resources`).
- **`strip_heading_emoji()` in verify.py** — section checks now match headings with or without a leading emoji, so older emoji-decorated notes still verify.

### Changed
- **Clean structured-note style** — the clauderules template now produces plain section headings (no emoji) and tight frontmatter (no blank lines between fields, two-space-indented tag list), matching the polished Obsidian demo layout. `examples/example-output.md` and the verify/generate heading lists were updated to match.

---

## [0.2.0] - 2026-05-05

### Added
- **OpenAI-compatible API integration** — `generate` and `canvas` commands now accept `--openai`, `--model`, and `--base-url` flags to call any OpenAI-compatible API directly (OpenAI, DeepSeek, etc.) without copy-pasting prompts
- `--from-note` flag on `canvas` command — populates all 9 canvas nodes from a generated literature note automatically
- `--base-url` flag on `generate`, `canvas`, and `run` — redirects API calls to non-OpenAI providers; also reads `OPENAI_BASE_URL` env var (e.g. `https://api.deepseek.com` for users in China)
- `run` command now accepts `--openai`, `--model`, `--base-url`, and `--notes-dir` flags for a fully automated end-to-end pipeline
- `extract_pdf()` public function in `extract.py` for programmatic use
- `verify_extraction()`, `verify_note()`, `verify_canvas()`, `verify_all()` public functions in `verify.py` returning structured result dicts
- `REQUIRED_EXTRACTION_FILES`, `REQUIRED_NOTE_SECTIONS`, `REQUIRED_CANVAS_FIELDS` constants in `verify.py`

### Changed
- `check_dependencies()` in `extract.py` now returns a dict `{'pdftext': bool, 'tesseract': bool}` instead of a plain bool
- `run` pipeline saves notes to `structured_literature_notes/` and wires canvas generation directly from the note
- README installation section rewritten to clarify the layering: Python → pip install → AI provider → Tesseract
- Help text and README updated with API key setup instructions and non-OpenAI provider examples (including DeepSeek for China)

### Fixed
- Python comment `# Limit to first 5000 chars` was being sent literally inside API prompts
- "Copy the prompt above" message was shown even when the prompt had been written to a file
- `"run": "process.py"` indentation error in CLI dispatcher
- `assess_pdf_searchability()` now raises on invalid or empty PDFs instead of silently returning empty lists
- 17 pre-existing test failures in `test_extract.py` and `test_verify.py` (missing public functions and incorrect return types)

## [0.1.6] - 2026-03-06

### Added
- None

### Changed
- Updated template loading to use importlib.resources for reliable package resource access
- Improved packaging configuration for explicit template inclusion

### Deprecated
- None

### Removed
- None

### Fixed
- Fixed template not found error in installed packages using importlib.resources
- Added filesystem fallback for source development mode
- Updated test paths to reflect scripts/templates/ location

## [0.1.5] - 2026-03-06

### Added
- None

### Changed
- Moved templates folder into scripts directory for better path resolution
- Updated template loading logic to use absolute paths relative to script location
- Updated README batch process section with human-readable instructions

### Deprecated
- None

### Removed
- None

### Fixed
- Updated packaging configuration (MANIFEST.in, pyproject.toml) to include scripts/templates/

## [0.1.4] - 2026-03-06

### Added
- None

### Changed
- None

### Deprecated
- None

### Removed
- None

### Fixed
- Renamed `.clauderules` dotfile to `clauderules.md` to prevent packaging exclusion
- Updated all Python code, configuration, and tests to reference new template filename
- Ensured templates folder is explicitly included in package data

## [0.1.3] - 2026-03-06

### Added
- None

### Changed
- None

### Deprecated
- None

### Removed
- None

### Fixed
- Fixed template path resolution in generate command to use importlib.resources for locating `.clauderules` template in installed package
- Updated canvas.py to also use resource-aware template loading (critical-thinking.canvas)

## [0.1.2] - 2026-03-06

### Added
- None

### Changed
- None

### Deprecated
- None

### Removed
- None

### Fixed
- Fixed missing .clauderules template in installed package by updating MANIFEST.in and pyproject.toml to include dot files in templates/ directory

## [0.1.1] - 2026-03-05

### Added
- New "run" command for full workflow automation (extract → generate → canvas)
- `process.py` script implementing the automated pipeline
- GitHub issue and pull request templates
- Comprehensive GitHub repository setup documentation

### Changed
- Updated all repository URLs to use consistent GitHub username (`heleninsights-dot`)
- Fixed version consistency between `pyproject.toml` and `scripts/__init__.py`
- Enhanced CLI help text to include "run" command
- Improved installation instructions in README.md

### Deprecated
- None

### Removed
- None

### Fixed
- None

## [0.1.0] - 2026-03-03

### Added
- First public release
- Core workflow functionality:
  - `extract`: PDF extraction with Text-First decision tree
  - `generate`: Structured note generation with Claude Code
  - `canvas`: Critical-thinking canvas creation
  - `verify`: Quality verification
  - `batch`: Batch processing
  - `setup`: Environment setup
  - `guide`: Workflow documentation

### Technical Details
- Python 3.10+ compatibility
- MIT License
- PyMuPDF for fast text extraction
- Tesseract OCR fallback for scanned pages
- JSON Canvas format for Obsidian
- Modular command-line interface
- Virtual environment support

---

## Versioning Scheme

- **Major version**: Breaking changes to API or workflow structure
- **Minor version**: New features and enhancements
- **Patch version**: Bug fixes and minor improvements

## How to Update

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on contributing changes and updating the changelog.