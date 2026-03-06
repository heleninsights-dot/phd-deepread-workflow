# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of PhD Deep Read Workflow
- Text-First PDF extraction decision tree (PyMuPDF + Tesseract OCR)
- Structured note generation with `.clauderules` template
- Critical-thinking canvas creation with 9 interconnected nodes
- Batch processing for multiple PDFs
- Quality verification and consistency checks
- Comprehensive documentation and examples
- Claude Code skill integration
- Test suite for core functionality
- Configuration system with YAML config file
- Installation script and Makefile

### Changed
- None (initial release)

### Deprecated
- None (initial release)

### Removed
- None (initial release)

### Fixed
- None (initial release)

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