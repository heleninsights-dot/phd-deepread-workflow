#!/usr/bin/env python3
"""
PhD Deep Read Workflow - Verification Script
Checks output quality and consistency with existing corpus patterns.
"""

import argparse
import json
import sys
from pathlib import Path
import re

# Public constants used by tests and external callers
REQUIRED_EXTRACTION_FILES = ["*.md", "*_meta.json"]
REQUIRED_NOTE_SECTIONS = [
    "## Research Gap & Hypothesis",
    "## Methodology & Evidence Base",
    "## Key Mechanisms & Findings",
    "## Critical Analysis",
    "## Connections & Integration",
    "## Action Items & Next Steps",
    "## Summary & Conclusion",
]
REQUIRED_CANVAS_FIELDS = ["id", "type", "text", "x", "y", "width", "height"]

# Matches a leading decorative emoji on a heading, e.g. "## 🚀 Title" -> "## Title".
# Lets section checks accept both the current plain headings and older emoji-decorated notes.
_HEADING_EMOJI = re.compile(r"^(#{1,6})\s+[^\w\s#]+\s+", re.MULTILINE)


def strip_heading_emoji(content):
    """Remove a leading emoji from each Markdown heading so plain-text matching works."""
    return _HEADING_EMOJI.sub(r"\1 ", content)


def verify_extraction(extract_dir):
    """Verify an extraction directory. Returns a result dict."""
    extract_path = Path(extract_dir)
    errors = []
    result = {"valid": False, "errors": errors}

    if not extract_path.exists():
        errors.append(f"Directory not found: {extract_dir}")
        return result

    md_files = [f for f in extract_path.glob("*.md")
                if not f.name.endswith("_formatted.md") and not f.name.endswith(".backup.md")]
    meta_files = list(extract_path.glob("*_meta.json"))

    if not md_files:
        errors.append("No markdown file found")
    else:
        result["markdown_file"] = md_files[0].name

    if not meta_files:
        errors.append("No metadata JSON found")
    else:
        try:
            with open(meta_files[0], "r", encoding="utf-8") as f:
                json.load(f)
            result["metadata_file"] = meta_files[0].name
        except json.JSONDecodeError as e:
            errors.append(f"Invalid metadata JSON: {e}")

    result["valid"] = len(errors) == 0
    return result


def verify_note(note_path):
    """Verify a structured literature note. Returns a result dict."""
    path = Path(note_path)
    errors = []
    result = {"valid": False, "errors": errors}

    if not path.exists():
        errors.append(f"File not found: {note_path}")
        return result

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        errors.append(f"Could not read file: {e}")
        return result

    if not (content.startswith("---\n") and "\n---\n" in content[4:]):
        errors.append("Missing YAML frontmatter")

    for callout in ("> [!Citation]", "> [!Synthesis]", "> [!Metadata]", "> [!Abstract]"):
        if callout not in content:
            errors.append(f"Missing callout: {callout}")

    result["valid"] = len(errors) == 0
    return result


def verify_canvas(canvas_path):
    """Verify a JSON Canvas file. Returns a result dict."""
    path = Path(canvas_path)
    errors = []
    result = {"valid": False, "errors": errors}

    if not path.exists():
        errors.append(f"File not found: {canvas_path}")
        return result

    try:
        with open(path, "r", encoding="utf-8") as f:
            canvas = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {e}")
        return result

    if "nodes" not in canvas or not isinstance(canvas.get("nodes"), list):
        errors.append("Missing or invalid 'nodes' array")
        return result

    for node in canvas["nodes"]:
        missing = [k for k in ("id", "type", "x", "y", "width", "height") if k not in node]
        if missing:
            errors.append(f"Node missing fields: {missing}")
            break

    result["valid"] = len(errors) == 0
    return result


def verify_all(output_dir):
    """Verify all outputs found under output_dir. Returns a summary dict."""
    base = Path(output_dir)
    summary = {"extractions": [], "notes": [], "canvases": []}

    for extraction_dir in (base / "markdown_output").glob("*") if (base / "markdown_output").exists() else []:
        if extraction_dir.is_dir():
            summary["extractions"].append(verify_extraction(str(extraction_dir)))

    for note_file in base.rglob("*.md"):
        summary["notes"].append(verify_note(str(note_file)))

    for canvas_file in base.rglob("*.canvas"):
        summary["canvases"].append(verify_canvas(str(canvas_file)))

    return summary


def check_extraction_directory(extract_dir):
    """Verify structure and content of extraction directory."""
    print(f"🔍 Checking extraction directory: {extract_dir}")

    extract_path = Path(extract_dir)
    if not extract_path.exists():
        print(f"❌ Directory does not exist: {extract_dir}")
        return False

    checks = {
        "has_markdown": False,
        "has_metadata": False,
        "has_images": False,
        "metadata_valid": False,
        "extraction_methods": {}
    }

    # Check for markdown file
    md_files = list(extract_path.glob("*.md"))
    md_files = [f for f in md_files if not f.name.endswith("_formatted.md") and not f.name.endswith(".backup.md")]

    if md_files:
        checks["has_markdown"] = True
        md_size = md_files[0].stat().st_size
        print(f"  ✓ Markdown file: {md_files[0].name} ({md_size} bytes)")
    else:
        print(f"  ❌ No markdown file found (excluding formatted/backup)")

    # Check for metadata JSON
    meta_files = list(extract_path.glob("*_meta.json"))
    if meta_files:
        checks["has_metadata"] = True
        try:
            with open(meta_files[0], 'r', encoding='utf-8') as f:
                meta = json.load(f)

            # Check for extraction methods
            if "pages" in meta:
                pdftext_count = sum(1 for p in meta["pages"]
                                  if p.get("text_extraction_method") == "pdftext")
                tesseract_count = sum(1 for p in meta["pages"]
                                if p.get("text_extraction_method") == "tesseract")
                none_count = sum(1 for p in meta["pages"]
                                if p.get("text_extraction_method") == "none")
                checks["extraction_methods"] = {"pdftext": pdftext_count, "tesseract": tesseract_count, "none": none_count}
                print(f"  ✓ Extraction methods: pdftext={pdftext_count}, tesseract={tesseract_count}, none={none_count}")

            # Check for table of contents
            if "toc" in meta and meta["toc"]:
                print(f"  ✓ Table of contents: {len(meta['toc'])} entries")

            checks["metadata_valid"] = True
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  ❌ Metadata invalid: {e}")
    else:
        print(f"  ❌ No metadata JSON found")

    # Check for images
    image_files = list(extract_path.glob("*.jpeg")) + list(extract_path.glob("*.png"))
    if image_files:
        checks["has_images"] = True
        print(f"  ✓ Extracted images: {len(image_files)} files")
    else:
        print(f"  ⚠ No images extracted (may be normal if PDF has no images)")

    # Overall assessment
    if checks["has_markdown"] and checks["has_metadata"] and checks["metadata_valid"]:
        print(f"✅ Extraction directory looks good")
        return True
    else:
        print(f"❌ Extraction directory has issues")
        return False

def check_structured_note(note_path):
    """Verify structure of a generated literature note."""
    print(f"📝 Checking structured note: {note_path}")

    note_path = Path(note_path)
    if not note_path.exists():
        print(f"❌ Note file does not exist: {note_path}")
        return False

    try:
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()

        checks = {
            "has_frontmatter": False,
            "has_citation": False,
            "has_synthesis": False,
            "has_metadata": False,
            "has_abstract": False,
            "has_wikilinks": False,
            "has_sections": False
        }

        # Check for YAML frontmatter
        if content.startswith('---\n'):
            end_frontmatter = content.find('\n---\n', 4)
            if end_frontmatter != -1:
                checks["has_frontmatter"] = True
                print(f"  ✓ YAML frontmatter present")

        # Check for Dataview callouts
        if '> [!Citation]' in content:
            checks["has_citation"] = True
            print(f"  ✓ Citation callout present")

        if '> [!Synthesis]' in content:
            checks["has_synthesis"] = True
            print(f"  ✓ Synthesis callout present")

        if '> [!Metadata]' in content:
            checks["has_metadata"] = True
            print(f"  ✓ Metadata callout present")

        if '> [!Abstract]' in content:
            checks["has_abstract"] = True
            print(f"  ✓ Abstract callout present")

        # Check for wikilinks
        wikilink_count = len(re.findall(r'\[\[[^\]]+\]\]', content))
        if wikilink_count > 0:
            checks["has_wikilinks"] = True
            print(f"  ✓ Wikilinks: {wikilink_count} found")
            if wikilink_count < 15:
                print(f"  ⚠ Wikilink count is low ({wikilink_count}); recommend 25+ for dense concept linking")

        # Check for major sections (tolerant of older emoji-decorated headings)
        normalized = strip_heading_emoji(content)
        present_sections = []
        for section in REQUIRED_NOTE_SECTIONS:
            if section in normalized:
                present_sections.append(section)

        if len(present_sections) >= 5:  # Most sections should be present
            checks["has_sections"] = True
            print(f"  ✓ Academic sections: {len(present_sections)}/7 present")

        # Overall assessment
        required_checks = ['has_frontmatter', 'has_citation', 'has_synthesis', 'has_metadata', 'has_abstract']
        passed = sum(checks[check] for check in required_checks)

        if passed >= 4:  # At least 4 of 5 required checks
            print(f"✅ Structured note looks good")
            return True
        else:
            print(f"❌ Structured note missing required elements")
            return False

    except Exception as e:
        print(f"❌ Error reading note: {e}")
        return False

def check_canvas_file(canvas_path):
    """Verify structure of a JSON Canvas file."""
    print(f"🎨 Checking canvas file: {canvas_path}")

    canvas_path = Path(canvas_path)
    if not canvas_path.exists():
        print(f"❌ Canvas file does not exist: {canvas_path}")
        return False

    try:
        with open(canvas_path, 'r', encoding='utf-8') as f:
            canvas = json.load(f)

        checks = {
            "has_nodes": False,
            "has_edges": False,
            "node_count": 0,
            "edge_count": 0
        }

        if "nodes" in canvas and isinstance(canvas["nodes"], list):
            checks["has_nodes"] = True
            checks["node_count"] = len(canvas["nodes"])
            print(f"  ✓ Nodes: {checks['node_count']}")

        if "edges" in canvas and isinstance(canvas["edges"], list):
            checks["has_edges"] = True
            checks["edge_count"] = len(canvas["edges"])
            print(f"  ✓ Edges: {checks['edge_count']}")

        # Check for critical-thinking nodes
        if checks["node_count"] >= 9:
            print(f"  ✓ Has sufficient nodes for critical thinking")

        if checks["has_nodes"] and checks["has_edges"] and checks["node_count"] >= 5:
            print(f"✅ Canvas file looks good")
            return True
        else:
            print(f"❌ Canvas file missing required structure")
            return False

    except (json.JSONDecodeError, KeyError) as e:
        print(f"❌ Error reading canvas: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Verify output quality and consistency of PhD Deep Read workflow"
    )
    parser.add_argument("--extract", help="Check extraction directory")
    parser.add_argument("--note", help="Check structured literature note")
    parser.add_argument("--canvas", help="Check JSON Canvas file")
    parser.add_argument("--all", action="store_true", help="Check all outputs in a directory")

    args = parser.parse_args()

    if not any([args.extract, args.note, args.canvas, args.all]):
        print("No verification targets specified.")
        print("Use --extract, --note, --canvas, or --all")
        return 1

    success = True

    if args.extract:
        if not check_extraction_directory(args.extract):
            success = False

    if args.note:
        if not check_structured_note(args.note):
            success = False

    if args.canvas:
        if not check_canvas_file(args.canvas):
            success = False

    if args.all:
        # Check all outputs in a directory
        print("⚠ --all flag not yet implemented")
        print("Check individual outputs with --extract, --note, --canvas")

    if success:
        print("\n✅ All checks passed!")
        return 0
    else:
        print("\n❌ Some checks failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())