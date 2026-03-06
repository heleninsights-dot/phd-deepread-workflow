---
name: phd-deepread
description: Guided workflow for processing academic PDFs into structured literature notes using Text-First decision tree (PyMuPDF + Tesseract OCR) and Claude-assisted analysis. Perfect for literature review and note-taking in Obsidian.
tags: [pdf, academic, research, obsidian, workflow]
allowed-tools: [Bash, Write, Read, Edit, Glob, Grep, Skill]
---

# PhD Deep Read Workflow

This skill implements a sophisticated **PhD Deep Read Workflow** that processes academic PDFs into structured literature notes for Obsidian using a hybrid decision-tree approach. The workflow combines:

1. **Text-First PDF Extraction**: Decision-tree using PyMuPDF (fast text extraction) for searchable PDFs and Tesseract OCR fallback for scanned/complex pages
2. **Structured Note Generation**: Template-driven generation of comprehensive academic literature notes
3. **Critical Thinking Canvas**: JSON Canvas files with 9 interconnected nodes for deep critical analysis
4. **Workflow Automation**: Scripts to automate the 4-stage pipeline

## When to Use This Skill

Activate when the user:
- Wants to process academic PDFs into structured literature notes
- Needs to extract text from PDFs with complex layouts or tables
- Wants to generate Obsidian-compatible notes with YAML frontmatter and Dataview callouts
- Needs critical thinking canvases for deep analysis of papers
- Has a collection of PDFs to process in batch

## Commands

The skill provides these main commands:

- `setup`: Setup environment and install required tools (PyMuPDF, Tesseract OCR)
- `extract`: Extract text and images from PDFs using Text-First decision tree (PyMuPDF + Tesseract OCR)
- `generate`: Generate structured literature notes using .clauderules template
- `canvas`: Create JSON Canvas files for critical thinking with 9 interconnected nodes
- `run`: Run full workflow automation (extract → generate → canvas)
- `verify`: Verify output quality and consistency with existing corpus patterns
- `batch`: Batch process directory of PDFs through all stages
- `guide`: Show interactive workflow guide with decision-tree visualization

## Usage Examples

```bash
# Setup environment
phd-deepread setup

# Process a single PDF
phd-deepread extract paper.pdf --output markdown_output/
phd-deepread generate markdown_output/paper/ --template templates/clauderules.md
phd-deepread canvas markdown_output/paper/ --output structured_notes/

# Run full workflow automation
phd-deepread run paper.pdf

# Batch process directory
phd-deepread batch papers/ --output literature-notes/

# Show workflow guide
phd-deepread guide
```

## Workflow Stages

### Stage 1: Text-First PDF Extraction
Text-First decision tree that pre-scans PDF with PyMuPDF, uses direct text extraction for searchable pages (80%+ of academic PDFs), falls back to Tesseract OCR only for scanned/complex pages. Outputs raw markdown with embedded images and metadata JSON.

### Stage 2: Structured Note Generation
Uses the `.clauderules` template with Claude Code assistance to generate comprehensive literature notes with:
- YAML frontmatter with specific fields
- Dataview-compatible callouts (`> [!Synthesis]`, `> [!Metadata]`)
- Academic critical analysis sections
- Extensive [[Wikilinks]] for concepts, methods, proteins
- Personal relevance and action items

### Stage 3: Critical-Thinking Canvas
Creates JSON Canvas files with 9 interconnected nodes for deep critical analysis:
- core-argument, assumptions, evidence-assessment
- alternative-explanations, methodological-critique
- personal-relevance, future-directions
- critical-questions-enhanced, hypothesis-center

### Stage 4: Verification
Quality checks and pattern matching to ensure consistency with existing corpus.

## External Tools Required

The workflow depends on these external tools:

1. **PyMuPDF (fitz)**: Fast text extraction for searchable PDFs (primary method)
2. **Tesseract OCR**: Optical character recognition for scanned/complex pages (optional fallback)
3. **Python 3.10+**: Virtual environment for running the tools
4. **Claude Code**: Template-driven structured note generation
5. **Custom Python scripts**: Implement Text-First decision tree and workflow automation

## Quick Start

1. **Install the skill** (already done if you see this)
2. **Run setup**: `phd-deepread setup` to check/install dependencies
3. **Test with a PDF**: `phd-deepread extract sample.pdf`
4. **Generate notes**: `phd-deepread generate markdown_output/sample/`
5. **Create canvas**: `phd-deepread canvas markdown_output/sample/`

## Troubleshooting

### Common Issues

**Tesseract OCR not installed**: Install with `brew install tesseract` (macOS) or `sudo apt install tesseract-ocr` (Linux)
**PyMuPDF missing**: Install with `pip install PyMuPDF`
**Missing images**: Check `--disable_image_extraction` not set
**OCR pages not processed**: Ensure Tesseract is installed and accessible
**Virtual environment activation**: Ensure you activate the correct Python environment

### Environment Variables

```bash
# Legacy: Disable SDPA for compatibility (no longer required for Tesseract)
export ENABLE_EFFICIENT_ATTENTION=0

# Activate Python virtual environment
source .venv/bin/activate
```

## Related Skills

- [json-canvas](/json-canvas): Create and edit JSON Canvas files
- [obsidian-markdown](/obsidian-markdown): Work with Obsidian Flavored Markdown
- [obsidian-bases](/obsidian-bases): Create Obsidian Bases with views and filters

## References

- Original workflow documentation in `Demo_PhDDeepRead/`
- Decision-tree architecture visualization: `PhD DeepRead_V2.html`
- Workflow demonstration: `2020-Yang_Workflow_Demo_Memo.md`
- Step-by-step instructions: `plan mode.md`

---

**Note**: This skill packages the existing workflow from `Demo_PhDDeepRead` without modifying or including the Python OCR code from `Failed_PhDDeepRead`. It provides guided commands to help users follow the documented hybrid extraction and analysis pipeline.