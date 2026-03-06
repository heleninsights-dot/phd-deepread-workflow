# PhD Deep Read Workflow Guide

This guide explains the **PhD Deep Read Workflow**, a sophisticated pipeline for processing academic PDFs into structured literature notes and critical-thinking canvases for Obsidian.

## Overview

The workflow transforms raw PDFs into comprehensive academic notes through four stages:

1. **Hybrid PDF Extraction** (pdftext + Surya OCR)
2. **Structured Note Generation** (Claude Code with `.clauderules` template)
3. **Critical-Thinking Canvas Creation** (9-node JSON Canvas)
4. **Verification & Integration** (Quality checks and pattern matching)

## Stage 1: Text-First PDF Extraction

### Decision-Tree Architecture

The extraction uses a **Text-First Decision Tree** that prioritizes speed and accuracy:

```
PDF Input
    ↓
Pre-scan with PyMuPDF (fast)
    ↓
Assess searchable text per page
    ├── If page has ≥100 chars searchable text → Use PyMuPDF (pdftext)
    ├── If page lacks searchable text → Use Tesseract OCR (if available)
    └── If 80%+ pages searchable → Use PyMuPDF for ALL pages
```

**Key Features:**
- **Text-First approach**: Uses direct text extraction whenever possible (80%+ of academic PDFs)
- **Smart OCR fallback**: Only uses Tesseract OCR for scanned/complex pages
- **Image extraction** for figures and tables
- **Metadata generation** with extraction method tracking per page
- **Configurable thresholds**: Adjust searchability criteria for different PDF types

### Tools Used
- **PyMuPDF (fitz)**: Fast text extraction for searchable PDFs
- **Tesseract OCR**: Optical character recognition for scanned/complex pages (optional)
- **Custom Python script**: Implements the Text-First decision tree (no external orchestrator)

### Environment Requirements
```bash
# Python 3.10+ virtual environment
source .venv/bin/activate

# Optional: Disable SDPA for compatibility (legacy for Surya)
export ENABLE_EFFICIENT_ATTENTION=0
```

### Output Structure
```
markdown_output/[PDF_NAME]/
├── [PDF_NAME].md              # Raw markdown with embedded images
├── [PDF_NAME]_meta.json       # Metadata, TOC, extraction methods per page
├── blocks.json                # Block-level segmentation data
└── _page_*_*.jpeg/.png        # Extracted images
```

## Stage 2: Structured Note Generation

### The `.clauderules` Template

A comprehensive 175+ line template that ensures consistent academic note structure:

- **YAML Frontmatter**: `category`, `tags`, `citekey`, `status`, `dateread`
- **Dataview Callouts**: `[!Citation]`, `[!Synthesis]`, `[!Metadata]`, `[!Abstract]`
- **Academic Sections**:
  - Research Gap & Hypothesis
  - Methodology & Evidence Base
  - Key Mechanisms & Findings
  - Critical Analysis (Strengths/Limitations/Open Questions)
  - Connections & Integration
  - Action Items & Next Steps
  - Summary & Conclusion
- **Wikilinks**: Extensive linking of concepts, methods, proteins, diseases

### Generation Process

1. **Read extracted markdown** from Stage 1 output
2. **Apply `.clauderules` template** with Claude Code assistance
3. **Fill template** with critical analysis of the paper
4. **Generate structured note** in raw Markdown format
5. **Save to** `structured_literature_notes/[Citekey].md`

### Example Output
See `examples/example-output.md` for a complete example.

## Stage 3: Critical-Thinking Canvas Creation

### 9-Node Canvas Structure

Based on the `ValverdePhotobiomodulation2022-CriticalThinking.canvas` template:

1. **core-argument**: Primary claim and logical chain
2. **assumptions**: Explicit, implicit, and questionable assumptions
3. **evidence-assessment**: Strength of evidence (strong/moderate/weak)
4. **alternative-explanations**: Competing hypotheses and confounding factors
5. **methodological-critique**: Study design limitations and measurement issues
6. **personal-relevance**: Connections to research interests and existing work
7. **future-directions**: Immediate, medium-term, and long-term research goals
8. **critical-questions-enhanced**: Hypothesis testing, mechanism, implementation questions
9. **hypothesis-center**: Central hypothesis re-examined with innovation/plausibility/evidence scores

### Layout
Nodes are spatially arranged with connecting edges to facilitate visual critical thinking.

### Example Canvas
See `examples/example-canvas.canvas` for the complete JSON structure.

## Stage 4: Verification & Integration

### Quality Checks

1. **Format verification**: Ensure note follows `.clauderules` template exactly
2. **Wikilink density**: 10+ relevant concept links
3. **Dataview compatibility**: Proper YAML frontmatter and callout syntax
4. **Canvas structure**: 9 nodes with appropriate connections
5. **Pattern matching**: Consistency with existing corpus of processed papers

### Integration with Obsidian

- Notes are ready for use in Obsidian with Dataview plugin
- Canvases work with Obsidian Canvas plugin
- All wikilinks connect to existing or future notes

## Workflow Commands

The skill provides these commands:

```bash
# Setup environment
phd-deepread setup

# Single PDF processing
phd-deepread extract paper.pdf --output markdown_output/
phd-deepread generate markdown_output/paper/ --template templates/clauderules.md
phd-deepread canvas markdown_output/paper/ --output structured_notes/

# Batch processing
phd-deepread batch papers/ --output literature-notes/

# Interactive guide
phd-deepread guide
```

## Time Estimates

| Stage | Time per Paper | Notes |
|-------|----------------|-------|
| Extraction | 10-40 minutes | Depends on PDF complexity, pages, OCR needs |
| Note Generation | 10-25 minutes | Claude Code interaction time |
| Canvas Creation | 5-10 minutes | Template-based, quick editing |
| Verification | 2-5 minutes | Quick quality checks |

**Total**: 27-80 minutes per paper

## Troubleshooting

### Common Issues

**Tesseract OCR not installed**
```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt install tesseract-ocr

# Python package
pip install pytesseract pillow
```

**PyMuPDF (fitz) not installed**
```bash
pip install PyMuPDF
```

**Missing images in extraction**
- Check `--disable_image_extraction` not set
- Verify PDF contains extractable images

**Virtual environment activation**
```bash
source .venv/bin/activate
```

**OCR pages not processed**
- Install Tesseract OCR (see above)
- Check language support: `tesseract --list-langs`
- Use `--lang` parameter for non-English PDFs

## Advanced Usage

### Custom Templates
- Modify `templates/clauderules.md` for different academic fields
- Create custom canvas templates with different node structures
- Adjust extraction parameters for specific PDF types

### Batch Processing
- Use `batch.sh` for processing multiple PDFs overnight
- Combine with cron jobs for automated processing
- Generate progress reports and summaries

### Integration with Zotero
- Use Zotero's citation keys as `citekey` in frontmatter
- Export PDFs from Zotero to processing directory
- Import generated notes back into Zotero as linked files

## References

- Original workflow documentation: `Demo_PhDDeepRead/`
- Decision-tree architecture: `decision-tree.md`
- Decision-tree visualization: `PhD DeepRead_V2.html`
- Workflow demonstration: `2020-Yang_Workflow_Demo_Memo.md`
- Step-by-step instructions: `plan mode.md`

## Getting Help

Use `phd-deepread guide` for interactive guidance or refer to this document.

For issues with external tools, consult their respective documentation:
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [Tesseract OCR GitHub](https://github.com/tesseract-ocr/tesseract)