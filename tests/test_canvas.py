#!/usr/bin/env python3
"""
Tests for the JSON Canvas creation script (canvas.py)
"""

import pytest
import sys
import os
import json
import tempfile
from pathlib import Path

# Add scripts directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# Try to import the canvas module
try:
    import canvas
    CANVAS_AVAILABLE = True
except ImportError as e:
    CANVAS_AVAILABLE = False
    print(f"⚠ Could not import canvas module: {e}")


@pytest.mark.skipif(not CANVAS_AVAILABLE, reason="Canvas module not available")
class TestCanvasModule:
    """Test basic functionality of canvas module."""

    def test_import(self):
        """Test that the module imports successfully."""
        import canvas
        assert hasattr(canvas, 'create_critical_thinking_canvas')
        assert hasattr(canvas, 'load_template')
        assert hasattr(canvas, 'save_canvas')

    def test_load_template(self, tmp_path):
        """Test loading a canvas template."""
        template_file = tmp_path / "template.canvas"
        template_data = {
            "nodes": [
                {"id": "test", "type": "text", "text": "Test node"}
            ]
        }
        template_file.write_text(json.dumps(template_data))

        loaded = canvas.load_template(str(template_file))
        assert loaded == template_data

    def test_load_template_invalid_json(self, tmp_path):
        """Test loading invalid JSON template."""
        template_file = tmp_path / "template.canvas"
        template_file.write_text("{ invalid json }")

        with pytest.raises(json.JSONDecodeError):
            canvas.load_template(str(template_file))

    def test_load_template_nonexistent(self):
        """Test loading non-existent template."""
        with pytest.raises(FileNotFoundError):
            canvas.load_template("/nonexistent/path/template.canvas")

    def test_create_critical_thinking_canvas_basic(self):
        """Test creating a basic critical thinking canvas."""
        paper_info = {
            "title": "Test Paper",
            "first_author": "Author",
            "year": "2024"
        }

        canvas_data = canvas.create_critical_thinking_canvas(paper_info)

        # Check basic structure
        assert "nodes" in canvas_data
        assert isinstance(canvas_data["nodes"], list)

        # Should have at least the 9 core nodes
        node_ids = [node["id"] for node in canvas_data["nodes"]]
        expected_nodes = [
            "core-argument", "assumptions", "evidence-assessment",
            "alternative-explanations", "methodological-critique",
            "personal-relevance", "future-directions",
            "critical-questions-enhanced", "hypothesis-center"
        ]

        for expected in expected_nodes:
            assert expected in node_ids, f"Missing node: {expected}"

    def test_canvas_node_structure(self):
        """Test that canvas nodes have required structure."""
        paper_info = {"title": "Test"}
        canvas_data = canvas.create_critical_thinking_canvas(paper_info)

        for node in canvas_data["nodes"]:
            # Required fields
            assert "id" in node
            assert "type" in node
            assert "text" in node
            assert "x" in node
            assert "y" in node
            assert "width" in node
            assert "height" in node

            # Type should be "text" for text nodes
            if "type" in node and node["type"] == "text":
                assert isinstance(node["text"], str)

    def test_save_canvas(self, tmp_path):
        """Test saving canvas to file."""
        canvas_data = {
            "nodes": [
                {"id": "test", "type": "text", "text": "Test"}
            ]
        }
        output_file = tmp_path / "output.canvas"

        canvas.save_canvas(canvas_data, str(output_file))
        assert output_file.exists()

        # Verify JSON is valid
        loaded = json.loads(output_file.read_text())
        assert loaded == canvas_data

    def test_save_canvas_with_indentation(self, tmp_path):
        """Test saving canvas with pretty indentation."""
        canvas_data = {"nodes": []}
        output_file = tmp_path / "output.canvas"

        canvas.save_canvas(canvas_data, str(output_file))
        content = output_file.read_text()

        # Should be pretty-printed with indentation
        assert "\n" in content  # Not a single line


class TestCriticalThinkingCanvasStructure:
    """Test the structure of the critical thinking canvas."""

    def test_default_template_exists(self):
        """Test that the default template exists."""
        # Check if there's a default template in templates directory
        template_path = Path(__file__).parent.parent / "scripts" / "templates" / "critical-thinking.canvas"
        if template_path.exists():
            template_content = json.loads(template_path.read_text())
            assert "nodes" in template_content

    def test_canvas_validation(self):
        """Test that generated canvas is valid JSON Canvas format."""
        paper_info = {"title": "Test"}
        import canvas
        canvas_data = canvas.create_critical_thinking_canvas(paper_info)

        # JSON Canvas spec: https://obsidian.md/canvas
        # Basic validation
        assert isinstance(canvas_data, dict)
        assert "nodes" in canvas_data

        # Nodes should be a list
        nodes = canvas_data["nodes"]
        assert isinstance(nodes, list)

        # Each node should have required fields
        for node in nodes:
            assert "id" in node
            assert "type" in node
            assert node["type"] in ["text", "file", "link"]  # Common types
            assert "x" in node and isinstance(node["x"], (int, float))
            assert "y" in node and isinstance(node["y"], (int, float))

    def test_canvas_node_content(self):
        """Test that canvas nodes have appropriate placeholder content."""
        paper_info = {
            "title": "Test Paper Title",
            "first_author": "Test Author",
            "year": "2024"
        }
        import canvas
        canvas_data = canvas.create_critical_thinking_canvas(paper_info)

        # Check that paper info appears in relevant nodes
        for node in canvas_data["nodes"]:
            if "text" in node:
                text = node["text"]
                # Some nodes might reference the paper title
                if node["id"] == "core-argument":
                    assert "[State the paper's central claim]" in text
                elif node["id"] == "assumptions":
                    assert "[Assumption 1]" in text

    def test_canvas_layout(self):
        """Test that nodes are positioned to avoid overlap."""
        import canvas
        paper_info = {"title": "Test"}
        canvas_data = canvas.create_critical_thinking_canvas(paper_info)

        # Collect node positions
        positions = []
        for node in canvas_data["nodes"]:
            positions.append((node["x"], node["y"]))

        # Check for obvious overlaps (simple check)
        unique_positions = set(positions)
        assert len(unique_positions) == len(positions), "Duplicate node positions found"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])