#!/usr/bin/env python3
"""
Tests for the verification script (verify.py)
"""

import pytest
import sys
import os
import json
import tempfile
from pathlib import Path

# Add scripts directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Try to import the verification module
try:
    import verify
    VERIFY_AVAILABLE = True
except ImportError as e:
    VERIFY_AVAILABLE = False
    print(f"⚠ Could not import verify module: {e}")


@pytest.mark.skipif(not VERIFY_AVAILABLE, reason="Verify module not available")
class TestVerifyModule:
    """Test basic functionality of verify module."""

    def test_import(self):
        """Test that the module imports successfully."""
        import verify
        assert hasattr(verify, 'verify_extraction')
        assert hasattr(verify, 'verify_note')
        assert hasattr(verify, 'verify_canvas')
        assert hasattr(verify, 'verify_all')

    def test_verify_extraction_valid(self, tmp_path):
        """Test verifying a valid extraction directory."""
        extraction_dir = tmp_path / "test_paper"
        extraction_dir.mkdir()

        # Create required files
        (extraction_dir / "test_paper.md").write_text("# Test\n\nContent")
        (extraction_dir / "test_paper_meta.json").write_text(json.dumps({
            "pdf_filename": "test.pdf",
            "total_pages": 1,
            "pages": [{"page_id": 0, "text_extraction_method": "pdftext"}],
            "extraction_summary": {"pdftext_pages": 1, "ocr_pages": 0, "total_extracted": 1}
        }))

        result = verify.verify_extraction(str(extraction_dir))
        assert result["valid"] is True
        assert "markdown_file" in result
        assert "metadata_file" in result

    def test_verify_extraction_missing_files(self, tmp_path):
        """Test verifying extraction directory with missing files."""
        extraction_dir = tmp_path / "empty"
        extraction_dir.mkdir()

        result = verify.verify_extraction(str(extraction_dir))
        assert result["valid"] is False
        assert "errors" in result
        assert len(result["errors"]) > 0

    def test_verify_extraction_invalid_metadata(self, tmp_path):
        """Test verifying extraction with invalid metadata JSON."""
        extraction_dir = tmp_path / "test_paper"
        extraction_dir.mkdir()

        (extraction_dir / "test_paper.md").write_text("# Test")
        (extraction_dir / "test_paper_meta.json").write_text("{ invalid json }")

        result = verify.verify_extraction(str(extraction_dir))
        assert result["valid"] is False
        assert "errors" in result

    def test_verify_note_valid(self, tmp_path):
        """Test verifying a valid structured note."""
        note_file = tmp_path / "note.md"
        note_content = """---
category: literaturenote
tags:
  - #Test
citekey: Test2024
status: read
dateread: 2024-01-01
---

> [!Citation]
> Test

> [!Synthesis]
> **Contribution**:: Test contribution

> [!Metadata]
> **Title**:: Test Paper
> **Year**:: 2024
> **Journal**:: *Test Journal*
> **FirstAuthor**:: Author
> **ItemType**:: journalArticle

> [!Abstract]
> Test abstract

# Notes

## 🚀 Research Gap & Hypothesis

### Problem Context

- **Core Issue**: Test issue
- **Current Knowledge Gap**: Test gap
- **Clinical/Scientific Need**: Test need

### Central Hypothesis

Test hypothesis
"""
        note_file.write_text(note_content)

        result = verify.verify_note(str(note_file))
        assert result["valid"] is True

    def test_verify_note_missing_frontmatter(self, tmp_path):
        """Test verifying note missing YAML frontmatter."""
        note_file = tmp_path / "note.md"
        note_file.write_text("# Just a markdown file\n\nNo frontmatter")

        result = verify.verify_note(str(note_file))
        assert result["valid"] is False
        assert "errors" in result

    def test_verify_note_missing_sections(self, tmp_path):
        """Test verifying note missing required sections."""
        note_file = tmp_path / "note.md"
        note_content = """---
category: literaturenote
citekey: Test
---
# Notes
"""
        note_file.write_text(note_content)

        result = verify.verify_note(str(note_file))
        assert result["valid"] is False
        assert "errors" in result

    def test_verify_canvas_valid(self, tmp_path):
        """Test verifying a valid JSON Canvas file."""
        canvas_file = tmp_path / "canvas.canvas"
        canvas_data = {
            "nodes": [
                {"id": "test", "type": "text", "text": "Test", "x": 0, "y": 0, "width": 100, "height": 100}
            ]
        }
        canvas_file.write_text(json.dumps(canvas_data))

        result = verify.verify_canvas(str(canvas_file))
        assert result["valid"] is True

    def test_verify_canvas_invalid_json(self, tmp_path):
        """Test verifying invalid JSON Canvas."""
        canvas_file = tmp_path / "canvas.canvas"
        canvas_file.write_text("{ invalid json }")

        result = verify.verify_canvas(str(canvas_file))
        assert result["valid"] is False
        assert "errors" in result

    def test_verify_canvas_missing_fields(self, tmp_path):
        """Test verifying canvas missing required fields."""
        canvas_file = tmp_path / "canvas.canvas"
        canvas_data = {"nodes": [{"id": "test"}]}  # Missing required fields
        canvas_file.write_text(json.dumps(canvas_data))

        result = verify.verify_canvas(str(canvas_file))
        assert result["valid"] is False
        assert "errors" in result

    def test_verify_all(self, tmp_path):
        """Test verifying all outputs in a directory."""
        # Create a mock output directory structure
        output_dir = tmp_path / "outputs"
        output_dir.mkdir()

        # Create extraction directory
        extraction_dir = output_dir / "markdown_output" / "test_paper"
        extraction_dir.mkdir(parents=True)
        (extraction_dir / "test_paper.md").write_text("# Test")
        (extraction_dir / "test_paper_meta.json").write_text(json.dumps({
            "pdf_filename": "test.pdf",
            "total_pages": 1,
            "pages": [{"page_id": 0}]
        }))

        # Create note file
        notes_dir = output_dir / "structured_notes"
        notes_dir.mkdir()
        note_content = """---
category: literaturenote
citekey: Test2024
status: read
dateread: 2024-01-01
---

> [!Citation]
> Test

> [!Synthesis]
> **Contribution**:: Test

> [!Metadata]
> **Title**:: Test
> **Year**:: 2024
> **Journal**:: *Test*
> **FirstAuthor**:: Author
> **ItemType**:: journalArticle

> [!Abstract]
> Test

# Notes

## 🚀 Research Gap & Hypothesis

### Problem Context

- **Core Issue**: Test
"""
        (notes_dir / "test_paper.md").write_text(note_content)

        # Create canvas file
        canvas_dir = output_dir / "canvas_templates"
        canvas_dir.mkdir()
        canvas_data = {
            "nodes": [
                {"id": "test", "type": "text", "text": "Test", "x": 0, "y": 0, "width": 100, "height": 100}
            ]
        }
        (canvas_dir / "test_paper.canvas").write_text(json.dumps(canvas_data))

        result = verify.verify_all(str(output_dir))
        assert "extractions" in result
        assert "notes" in result
        assert "canvases" in result


class TestVerificationStandards:
    """Test the verification standards and criteria."""

    def test_extraction_standards(self):
        """Test extraction verification standards."""
        import verify

        # Check that required files are defined
        assert hasattr(verify, 'REQUIRED_EXTRACTION_FILES') or \
               hasattr(verify, 'required_extraction_files')

    def test_note_standards(self):
        """Test note verification standards."""
        import verify

        # Check that required sections are defined
        assert hasattr(verify, 'REQUIRED_NOTE_SECTIONS') or \
               hasattr(verify, 'required_note_sections')

    def test_canvas_standards(self):
        """Test canvas verification standards."""
        import verify

        # Check that required node fields are defined
        assert hasattr(verify, 'REQUIRED_CANVAS_FIELDS') or \
               hasattr(verify, 'required_canvas_fields')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])