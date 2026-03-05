# Text-First Decision Tree Architecture

## Overview

The **Text-First Decision Tree** is a custom PDF extraction approach designed to maximize accuracy while minimizing computational cost. Instead of applying heavy OCR to all pages, it intelligently chooses the optimal extraction method per page based on a quick pre-scan.

## Core Philosophy

**"Use the simplest method that works"**
- Most academic PDFs (80%+) have searchable text layers
- OCR is only needed for scanned pages, complex layouts, or tables
- By avoiding unnecessary OCR, we save:
  - CPU/GPU resources
  - Processing time
  - Token usage (OCR text often contains more errors requiring cleanup)

## Decision Tree Flowchart

```mermaid
flowchart TD
    A[PDF Input] --> B{Pre-scan with PyMuPDF<br/>Assess searchable text per page}
    B --> C{Page has >100 chars<br/>searchable text?}
    C -->|Yes| D[Use PyMuPDF (pdftext)<br/>Fast, accurate extraction]
    C -->|No| E{Is Tesseract OCR<br/>available?}
    E -->|Yes| F[Use Tesseract OCR<br/>For scanned/complex pages]
    E -->|No| G[No text extraction<br/>(images only)]

    B --> H{Aggregate: 80%+ pages searchable?}
    H -->|Yes| I[Use PyMuPDF for ALL pages<br/>(Skip OCR entirely)]
    H -->|No| J[Mixed approach<br/>PyMuPDF + Tesseract per page]

    D --> K[Markdown + Images + Metadata]
    F --> K
    G --> K
    I --> K
    J --> K
```

## Detailed Algorithm

### Step 1: Pre-scan Assessment
For each page in the PDF:
1. Open with PyMuPDF (`fitz`)
2. Extract raw text using `page.get_text()`
3. Calculate character count after stripping whitespace
4. **Threshold**: ≥100 characters = "searchable"
5. Record page index as searchable or non-searchable

### Step 2: Aggregate Decision
- Calculate percentage of searchable pages: `searchable_pages / total_pages`
- **Default threshold**: 80% (configurable via `--percentage`)
- If ≥80% pages are searchable: **Use PyMuPDF for all pages**
- Else: **Mixed approach** (PyMuPDF for searchable pages, Tesseract for others)

### Step 3: Per-page Extraction
For each page, based on assessment:
1. **PyMuPDF (pdftext)**: Direct text extraction from PDF text layer
   - Preserves formatting and structure
   - Near-perfect accuracy for searchable PDFs
   - Fast (milliseconds per page)
2. **Tesseract OCR**: Optical character recognition
   - Converts page to 300 DPI image
   - Runs Tesseract OCR with specified language
   - Slower but necessary for scanned content
   - Accuracy depends on image quality and language
3. **None**: If OCR unavailable and page not searchable
   - Only images extracted
   - Placeholder text: "[No text extracted from page X]"

### Step 4: Image Extraction
**Always performed** (regardless of text extraction method):
- Extract all embedded images using PyMuPDF
- Save as PNG files with naming: `_page_{N}_Picture_{M}.png`
- Images are referenced in markdown output

## Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--threshold` | 100 | Minimum characters to consider page searchable |
| `--percentage` | 0.8 | Percentage of pages that must be searchable to use PyMuPDF for all |
| `--lang` | eng | Language code for Tesseract OCR |
| `--force-ocr` | false | Force OCR for all pages (skip decision tree) |
| `--force-text` | false | Force PyMuPDF for all pages (skip OCR) |
| `--no-ocr` | false | Disable OCR entirely (PyMuPDF only) |

## Technical Implementation

### Dependencies
- **PyMuPDF (fitz)**: Python bindings for MuPDF library
- **Tesseract OCR**: Command-line OCR engine (optional)
- **pytesseract**: Python wrapper for Tesseract (optional)
- **PIL/Pillow**: Image processing for OCR

### Key Functions (extract.py)
1. `assess_pdf_searchability()`: Pre-scan PDF, return searchable/non-searchable page indices
2. `extract_with_pymupdf()`: PyMuPDF extraction for specified pages
3. `extract_with_ocr()`: Tesseract OCR extraction for specified pages
4. `combine_extractions()`: Merge results into final markdown and metadata

### Output Metadata
```json
{
  "pdf_filename": "paper.pdf",
  "total_pages": 15,
  "pages": [
    {
      "page_id": 0,
      "text_extraction_method": "pdftext",
      "block_counts": {"characters": 2543, "words": 412, "lines": 45},
      "extracted_text": "...",
      "image_count": 2
    },
    {
      "page_id": 1,
      "text_extraction_method": "tesseract",
      "block_counts": {"characters": 1876, "words": 305, "lines": 32},
      "extracted_text": "...",
      "image_count": 0
    }
  ],
  "extraction_summary": {
    "pdftext_pages": 12,
    "ocr_pages": 3,
    "total_extracted": 15
  }
}
```

## Performance Characteristics

### Best Case (All searchable text)
- **Processing time**: ~0.1 seconds per page
- **Accuracy**: ~100% (direct text extraction)
- **Resource usage**: Minimal CPU

### Worst Case (All OCR required)
- **Processing time**: ~2-5 seconds per page
- **Accuracy**: ~95-99% (depends on image quality)
- **Resource usage**: Moderate CPU, memory for image processing

### Typical Case (80% searchable, 20% OCR)
- **Processing time**: ~0.5 seconds per page average
- **Accuracy**: High overall
- **Resource efficiency**: Optimal balance

## Comparison with Other Approaches

| Approach | Accuracy | Speed | Resource Use | Best For |
|----------|----------|-------|--------------|----------|
| **Text-First Decision Tree** | **High** (mixed) | **Fast** (smart selection) | **Low** (minimal OCR) | Academic PDFs (mostly searchable) |
| Always OCR | Medium | Slow | High | Scanned documents only |
| Always pdftext | **Perfect** (when available) | **Fastest** | **Lowest** | Modern digital PDFs |
| Marker + Surya | High (layout-aware) | Medium | High | Complex layouts, tables |

## Advantages

1. **Efficiency**: Avoids unnecessary OCR for searchable PDFs
2. **Accuracy**: Uses native text extraction when available (perfect)
3. **Flexibility**: Falls back to OCR when needed
4. **Transparency**: Clear metadata about which method used per page
5. **Configurable**: Adjust thresholds for different PDF collections

## Limitations

1. **Page-level granularity**: Cannot switch methods within a page
2. **Simple heuristic**: Based on character count only (could be enhanced)
3. **Tesseract dependency**: Requires separate installation for OCR fallback
4. **Complex layouts**: PyMuPDF may miss text in multi-column layouts (uncommon in academic PDFs)

## Future Enhancements

Potential improvements to the decision tree:
1. **Layout detection**: Check for multi-column layouts, tables
2. **Confidence scoring**: Use text quality metrics beyond character count
3. **Hybrid per-block**: Use OCR for specific blocks within a page
4. **Language detection**: Auto-detect language for OCR
5. **GPU acceleration**: Use GPU-accelerated OCR when available

## References

- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [PhD Deep Read Workflow](workflow-guide.md)