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