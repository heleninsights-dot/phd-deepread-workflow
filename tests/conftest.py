"""
Pytest configuration and fixtures for PhD Deep Read tests.
"""

import pytest
import tempfile
import json
from pathlib import Path
import sys
import os

# Add scripts directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


@pytest.fixture
def tmp_extraction_dir():
    """Create a temporary extraction directory with sample files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        dir_path = Path(tmpdir) / "test_paper"
        dir_path.mkdir()

        # Create markdown file
        md_file = dir_path / "test_paper.md"
        md_file.write_text("# Test Paper\n\nThis is a test paper with some content.")

        # Create metadata file
        meta_file = dir_path / "test_paper_meta.json"
        metadata = {
            "pdf_filename": "test_paper.pdf",
            "total_pages": 5,
            "pages": [
                {
                    "page_id": 0,
                    "text_extraction_method": "pdftext",
                    "block_counts": {"characters": 1500, "words": 250, "lines": 30},
                    "extracted_text": "Abstract\n\nThis is the abstract.",
                    "image_count": 2
                },
                {
                    "page_id": 1,
                    "text_extraction_method": "pdftext",
                    "block_counts": {"characters": 2000, "words": 350, "lines": 45},
                    "extracted_text": "Introduction\n\nThis is the introduction.",
                    "image_count": 1
                }
            ],
            "extraction_summary": {
                "pdftext_pages": 5,
                "ocr_pages": 0,
                "total_extracted": 5
            }
        }
        meta_file.write_text(json.dumps(metadata))

        # Create a dummy image file
        img_file = dir_path / "_page_0_Picture_0.png"
        img_file.write_bytes(b"fake image data")

        yield str(dir_path)


@pytest.fixture
def tmp_note_file():
    """Create a temporary structured note file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        note_content = """---
category: literaturenote
tags:
  - #Test
  - #Example
citekey: Test2024
status: read
dateread: 2024-01-01
---

> [!Citation]
> Author, A. (2024). Test Paper Title. *Test Journal*.

> [!Synthesis]
> **Contribution**:: This paper demonstrates a test.
> **Related**:: [[Test Concept]], [[Another Concept]]

> [!Metadata]
> **Title**:: Test Paper Title
> **Year**:: 2024
> **Journal**:: *Test Journal*
> **FirstAuthor**:: Author
> **ItemType**:: journalArticle

> [!Abstract]
> This is a test abstract summarizing the paper.

# Notes

## 🚀 Research Gap & Hypothesis

### Problem Context

- **Core Issue**: The core issue being addressed
- **Current Knowledge Gap**: What is missing in the literature
- **Clinical/Scientific Need**: Why this is important

### Central Hypothesis

The central hypothesis of the paper.

## 🔬 Methodology & Evidence Base

### Study Characteristics

- **Type**: Experimental study
- **Scope**: Test scope description

### Key Techniques Evaluated

- **[[Test Technique]]**: How it was applied
- **[[Another Technique]]**: How it was applied

## 📊 Key Mechanisms & Findings

### Mechanism 1

1. **Concept**: Description of concept
2. **Findings**:
   - Key result 1
   - Key result 2

### Mechanism 2

1. **Concept**: Description of concept
2. **Findings**:
   - Key result 1

## 🎯 Critical Analysis

### Strengths

1. **Strength 1**: Description
2. **Strength 2**: Description

### Limitations

1. **Limitation 1**: Description
2. **Limitation 2**: Description

### Open Questions

1. **Question 1**?
2. **Question 2**?

## 🔗 Connections & Integration

### Practical Implementation

- **Protocols**: Test protocols
- **Tools**: [[Test Tool]]

### Personal Relevance

- **Research Interests**: How this fits
- **Application**: Potential use cases

## 📋 Action Items & Next Steps

- [ ] Investigate question 1
- [ ] Test practical application
- [ ] Address knowledge gap

## 🏁 Summary & Conclusion

> **Key Takeaway**: One sentence powerful summary.

### Final Assessment

- **Innovation**: Medium
- **Evidence**: High
- **Clinical Potential**: Low
"""
        f.write(note_content)
        f.flush()
        yield f.name
        os.unlink(f.name)


@pytest.fixture
def tmp_canvas_file():
    """Create a temporary JSON Canvas file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.canvas', delete=False) as f:
        canvas_data = {
            "nodes": [
                {
                    "id": "core-argument",
                    "type": "text",
                    "text": "# Core Argument Structure\n\n**Primary Claim:** Test claim",
                    "x": -1320,
                    "y": -960,
                    "width": 700,
                    "height": 410,
                    "color": "2"
                },
                {
                    "id": "assumptions",
                    "type": "text",
                    "text": "# Key Assumptions\n\n**Explicit Assumptions:**\n1. Test assumption",
                    "x": -1320,
                    "y": -400,
                    "width": 700,
                    "height": 600,
                    "color": "3"
                }
            ]
        }
        json.dump(canvas_data, f)
        f.flush()
        yield f.name
        os.unlink(f.name)


@pytest.fixture
def sample_paper_info():
    """Return sample paper information."""
    return {
        "title": "Test Paper Title",
        "first_author": "Test Author",
        "year": "2024",
        "journal": "Test Journal"
    }


@pytest.fixture
def sample_template():
    """Return a sample template."""
    return """---
category: literaturenote
tags:
  - #{{Field}}
citekey: {{camelCase: FirstAuthor+FirstWordOfTitle+Year}}
status: read
dateread: {{Current Date YYYY-MM-DD}}
---

> [!Citation]
> {{Full APA Style Citation}}

> [!Synthesis]
> **Contribution**:: {{Contribution}}
> **Related**:: [[{{Concept1}}]], [[{{Concept2}}]]

> [!Metadata]
> **Title**:: {{Title}}
> **Year**:: {{Year}}
> **Journal**:: *{{Journal}}*
> **FirstAuthor**:: {{FirstAuthor}}
> **ItemType**:: journalArticle

> [!Abstract]
> {{Abstract}}

# Notes

## 🚀 Research Gap & Hypothesis

### Problem Context

- **Core Issue**: {{Core Issue}}
- **Current Knowledge Gap**: {{Knowledge Gap}}
- **Clinical/Scientific Need**: {{Need}}

### Central Hypothesis

{{Hypothesis}}
"""