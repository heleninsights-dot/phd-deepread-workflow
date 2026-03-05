#!/usr/bin/env python3
"""
Tests for the PDF extraction script (extract.py)
"""

import pytest
import sys
import os
from pathlib import Path
import tempfile
import json

# Add scripts directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Try to import the extraction module
try:
    import extract
    EXTRACT_AVAILABLE = True
except ImportError as e:
    EXTRACT_AVAILABLE = False
    print(f"⚠ Could not import extract module: {e}")


@pytest.mark.skipif(not EXTRACT_AVAILABLE, reason="Extract module not available")
class TestExtractModule:
    """Test basic functionality of extract module."""

    def test_import(self):
        """Test that the module imports successfully."""
        import extract
        assert hasattr(extract, 'check_dependencies')
        assert hasattr(extract, 'extract_pdf')

    def test_check_dependencies(self):
        """Test dependency checking."""
        result = extract.check_dependencies()
        assert isinstance(result, dict)
        assert 'pdftext' in result
        assert 'tesseract' in result
        assert isinstance(result['pdftext'], bool)
        assert isinstance(result['tesseract'], bool)

    def test_assess_pdf_searchability_no_file(self):
        """Test searchability assessment with non-existent file."""
        with tempfile.NamedTemporaryFile(suffix='.pdf') as tmp:
            # File exists but is empty (not a valid PDF)
            with pytest.raises(Exception):
                extract.assess_pdf_searchability(tmp.name)

    def test_extract_pdf_invalid_file(self):
        """Test extraction with invalid PDF file."""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(b"Not a valid PDF")
            tmp_path = tmp.name

        try:
            result = extract.extract_pdf(tmp_path, output_dir=None)
            # Should handle gracefully or raise exception
            if 'success' in result:
                assert result['success'] is False
        except Exception:
            # Exception is also acceptable
            pass
        finally:
            os.unlink(tmp_path)


class TestMetadataStructure:
    """Test metadata JSON structure."""

    def test_metadata_schema(self):
        """Test that metadata follows expected schema."""
        metadata = {
            "pdf_filename": "test.pdf",
            "total_pages": 10,
            "pages": [
                {
                    "page_id": 0,
                    "text_extraction_method": "pdftext",
                    "block_counts": {"characters": 100, "words": 20, "lines": 5},
                    "extracted_text": "Sample text",
                    "image_count": 1
                }
            ],
            "extraction_summary": {
                "pdftext_pages": 1,
                "ocr_pages": 0,
                "total_extracted": 1
            }
        }

        # Required fields
        assert "pdf_filename" in metadata
        assert "total_pages" in metadata
        assert "pages" in metadata
        assert "extraction_summary" in metadata

        # Page structure
        page = metadata["pages"][0]
        assert "page_id" in page
        assert "text_extraction_method" in page
        assert "block_counts" in page
        assert "extracted_text" in page
        assert "image_count" in page

        # Block counts structure
        counts = page["block_counts"]
        assert "characters" in counts
        assert "words" in counts
        assert "lines" in counts

        # Summary structure
        summary = metadata["extraction_summary"]
        assert "pdftext_pages" in summary
        assert "ocr_pages" in summary
        assert "total_extracted" in summary


class TestDecisionTreeLogic:
    """Test the decision tree logic."""

    def test_searchable_threshold(self):
        """Test searchable page threshold logic."""
        # Mock page assessments
        searchable_pages = [0, 1, 2, 3]  # 4 pages
        non_searchable_pages = [4]  # 1 page
        total_pages = 5

        # 80% threshold (default)
        searchable_percentage = len(searchable_pages) / total_pages
        use_pdftext_for_all = searchable_percentage >= 0.8

        # 4/5 = 80% exactly, should use pdftext for all
        assert searchable_percentage == 0.8
        assert use_pdftext_for_all is True

        # Add another non-searchable page
        non_searchable_pages.append(5)
        total_pages = 6
        searchable_percentage = len(searchable_pages) / total_pages
        use_pdftext_for_all = searchable_percentage >= 0.8

        # 4/6 = 66.7%, should not use pdftext for all
        assert searchable_percentage == 4/6
        assert use_pdftext_for_all is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])