# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- None

### Changed
- None

### Fixed
- None

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