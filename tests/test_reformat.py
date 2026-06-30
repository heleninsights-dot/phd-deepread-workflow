#!/usr/bin/env python3
"""
Tests for the final reformat script (reformat.py)
"""

import pytest
import sys
import os
from pathlib import Path

# Add scripts directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

try:
    import reformat
    REFORMAT_AVAILABLE = True
except ImportError as e:
    REFORMAT_AVAILABLE = False
    print(f"⚠ Could not import reformat module: {e}")


@pytest.mark.skipif(not REFORMAT_AVAILABLE, reason="Reformat module not available")
class TestReformatModule:
    """Test basic functionality of the reformat module."""

    def test_import(self):
        """The module exposes its public helpers."""
        assert hasattr(reformat, 'formatted_output_path')
        assert hasattr(reformat, 'create_reformat_prompt')
        assert hasattr(reformat, 'main')

    def test_formatted_output_path(self, tmp_path):
        """Cleaned output is <paper>_formatted.md next to the extraction."""
        extraction_dir = tmp_path / "test_paper"
        extraction_dir.mkdir()
        md = extraction_dir / "test_paper.md"
        md.write_text("# Test\n\nbody")

        files = reformat.find_extracted_files(str(extraction_dir))
        out = reformat.formatted_output_path(files)

        assert out.endswith("test_paper_formatted.md")
        assert str(extraction_dir) in out

    def test_create_reformat_prompt_substitutes_output_path(self):
        """The {output_path} placeholder is replaced and the full text embedded."""
        extracted_text = "experi-\nment results were signifi-\ncant across pages."
        template = "Write the cleaned document to:\n\n```\n{output_path}\n```\n"
        paper_info = {"title": "Test Paper", "first_author": "Smith", "year": "2024"}
        output_path = "markdown_output/test_paper/test_paper_formatted.md"

        prompt = reformat.create_reformat_prompt(
            extracted_text, template, paper_info, output_path
        )

        # Placeholder resolved, no literal {output_path} left in the instructions body
        assert output_path in prompt
        assert "{output_path}" not in prompt
        # Paper info surfaced
        assert "Test Paper" in prompt
        assert "Smith" in prompt
        assert "2024" in prompt
        # Full extracted text embedded (not truncated)
        assert "signifi-\ncant" in prompt

    def test_create_reformat_prompt_handles_missing_info(self):
        """Missing paper metadata falls back to placeholder labels."""
        prompt = reformat.create_reformat_prompt(
            "raw text", "to {output_path}", {}, "out.md"
        )
        assert "Unknown Title" in prompt
        assert "raw text" in prompt
        assert "out.md" in prompt


class TestReformatTemplate:
    """Test that the reformat template carries the required instructions."""

    def test_template_exists(self):
        template_path = (
            Path(__file__).parent.parent / "scripts" / "templates" / "reformat.md"
        )
        assert template_path.exists(), f"Template not found at {template_path}"

    def test_template_has_required_operations(self):
        template_path = (
            Path(__file__).parent.parent / "scripts" / "templates" / "reformat.md"
        )
        content = template_path.read_text(encoding="utf-8").lower()

        # The five core operations the user asked for
        assert "reflow" in content
        assert "dehyphenate" in content
        assert "table" in content
        assert "header" in content or "footer" in content
        assert "callout" in content
        # The output-path placeholder the script fills in
        assert "{output_path}" in template_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
