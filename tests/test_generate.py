#!/usr/bin/env python3
"""
Tests for the structured note generation script (generate.py)
"""

import pytest
import sys
import os
import json
import tempfile
from pathlib import Path

# Add scripts directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Try to import the generation module
try:
    import generate
    GENERATE_AVAILABLE = True
except ImportError as e:
    GENERATE_AVAILABLE = False
    print(f"⚠ Could not import generate module: {e}")


@pytest.mark.skipif(not GENERATE_AVAILABLE, reason="Generate module not available")
class TestGenerateModule:
    """Test basic functionality of generate module."""

    def test_import(self):
        """Test that the module imports successfully."""
        import generate
        assert hasattr(generate, 'find_extracted_files')
        assert hasattr(generate, 'read_template')
        assert hasattr(generate, 'extract_paper_info')
        assert hasattr(generate, 'create_claude_prompt')

    def test_find_extracted_files(self, tmp_path):
        """Test finding extracted files in a directory."""
        # Create a mock extraction directory
        extraction_dir = tmp_path / "test_paper"
        extraction_dir.mkdir()

        # Create mock files
        (extraction_dir / "test_paper.md").write_text("# Test Paper\n\nContent")
        (extraction_dir / "test_paper_meta.json").write_text('{"title": "Test"}')
        (extraction_dir / "_page_0_Picture_0.png").write_bytes(b"fake image data")

        files = generate.find_extracted_files(str(extraction_dir))

        assert files["directory"] == extraction_dir
        assert files["markdown"].name == "test_paper.md"
        assert files["metadata"].name == "test_paper_meta.json"
        assert len(files["images"]) == 1
        assert files["has_content"] is True

    def test_find_extracted_files_no_markdown(self, tmp_path):
        """Test finding extracted files when no markdown exists."""
        extraction_dir = tmp_path / "empty"
        extraction_dir.mkdir()

        files = generate.find_extracted_files(str(extraction_dir))
        assert files["has_content"] is False
        assert files["markdown"] is None

    def test_read_template(self, tmp_path):
        """Test reading template file."""
        template_file = tmp_path / "test_template.txt"
        template_content = "# Test Template\n\n{{placeholder}}"
        template_file.write_text(template_content)

        result = generate.read_template(str(template_file))
        assert result == template_content

    def test_read_template_nonexistent(self):
        """Test reading non-existent template file."""
        with pytest.raises(RuntimeError):
            generate.read_template("/nonexistent/path/template.txt")

    def test_extract_paper_info(self, tmp_path):
        """Test extracting paper info from metadata JSON."""
        metadata_file = tmp_path / "metadata.json"
        metadata = {
            "title": "Test Paper Title",
            "authors": ["First Author", "Second Author"],
            "year": 2024,
            "journal": "Test Journal"
        }
        metadata_file.write_text(json.dumps(metadata))

        info = generate.extract_paper_info(metadata_file)

        assert info["title"] == "Test Paper Title"
        assert info["first_author"] == "First Author"
        assert info["year"] == 2024
        assert info["journal"] == "Test Journal"

    def test_extract_paper_info_missing_fields(self, tmp_path):
        """Test extracting paper info with missing fields."""
        metadata_file = tmp_path / "metadata.json"
        metadata = {"title": "Test"}
        metadata_file.write_text(json.dumps(metadata))

        info = generate.extract_paper_info(metadata_file)
        assert info["title"] == "Test"
        assert "first_author" not in info
        assert "year" not in info
        assert "journal" not in info

    def test_extract_paper_info_invalid_json(self, tmp_path):
        """Test extracting paper info from invalid JSON."""
        metadata_file = tmp_path / "metadata.json"
        metadata_file.write_text("{ invalid json }")

        info = generate.extract_paper_info(metadata_file)
        assert info == {}  # Should return empty dict on error

    def test_guess_paper_info_from_filename(self):
        """Test guessing paper info from filename."""
        filename = "Smith2024_QuantumComputing_PhysRevLett.pdf"
        info = generate.guess_paper_info_from_filename(filename)

        assert info["first_author"] == "Smith"
        assert info["year"] == "2024"
        assert "QuantumComputing" in info["title"]
        assert info["journal"] == "Unknown Journal"

    def test_create_claude_prompt(self):
        """Test creating Claude prompt."""
        extracted_text = "# Test Paper\n\nThis is a test paper."
        template = "category: literaturenote\n\n---\n\n{{content}}"
        paper_info = {
            "title": "Test Paper",
            "first_author": "Author",
            "year": "2024",
            "journal": "Test Journal"
        }

        prompt = generate.create_claude_prompt(extracted_text, template, paper_info)

        # Check that all paper info appears in prompt
        assert "Test Paper" in prompt
        assert "Author" in prompt
        assert "2024" in prompt
        assert "Test Journal" in prompt

        # Check that template appears
        assert "category: literaturenote" in prompt

        # Check that extracted text appears (truncated)
        assert "Test Paper" in prompt


class TestTemplateStructure:
    """Test that the .clauderules template has required structure."""

    def test_template_exists(self):
        """Test that the template file exists."""
        template_path = Path(__file__).parent.parent / "templates" / "clauderules.md"
        assert template_path.exists(), f"Template not found at {template_path}"

    def test_template_structure(self):
        """Test that template has required sections."""
        template_path = Path(__file__).parent.parent / "templates" / "clauderules.md"
        template_content = template_path.read_text()

        # Required YAML frontmatter markers
        assert "category: literaturenote" in template_content
        assert "tags:" in template_content
        assert "citekey:" in template_content
        assert "status:" in template_content
        assert "dateread:" in template_content

        # Required Dataview callouts
        assert "> [!Citation]" in template_content
        assert "> [!Synthesis]" in template_content
        assert "> [!Metadata]" in template_content
        assert "> [!Abstract]" in template_content

        # Required sections
        assert "# Notes" in template_content
        assert "## 🚀 Research Gap & Hypothesis" in template_content
        assert "## 🔬 Methodology & Evidence Base" in template_content
        assert "## 📊 Key Mechanisms & Findings" in template_content
        assert "## 🎯 Critical Analysis" in template_content
        assert "## 🔗 Connections & Integration" in template_content
        assert "## 📋 Action Items & Next Steps" in template_content
        assert "## 🏁 Summary & Conclusion" in template_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])