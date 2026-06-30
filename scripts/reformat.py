#!/usr/bin/env python3
"""
PhD Deep Read Workflow - Final Reformat Script

Prepares a prompt that asks Claude Code to reformat the raw extracted markdown
into a clean, Obsidian-ready layout (reflow paragraphs, dehyphenate, rebuild
tables, strip page/header artifacts, collapse back-matter into foldable
callouts).

Like generate.py, this script makes NO LLM API calls -- it builds a prompt and
prints it (or writes it to -o <file>) for Claude Code to consume. The cleaned
document is written by Claude Code to <paper>_formatted.md inside the extraction
directory, which the rest of the pipeline already treats as the polished copy.
"""

import argparse
import sys
from pathlib import Path

# Reuse the extraction-discovery and template-loading helpers from generate.py.
# Package import works when imported as scripts.reformat (e.g. from process.py);
# the bare import works when this file is run directly as a script (scripts/ on
# sys.path[0]).
try:
    from scripts.generate import (
        find_extracted_files,
        load_template,
        extract_paper_info,
        guess_paper_info_from_filename,
    )
except ImportError:
    from generate import (
        find_extracted_files,
        load_template,
        extract_paper_info,
        guess_paper_info_from_filename,
    )


def formatted_output_path(files):
    """Where Claude Code should write the cleaned markdown: <paper>_formatted.md."""
    markdown = files["markdown"]
    if markdown is not None:
        return str(markdown.with_name(f"{markdown.stem}_formatted.md"))
    # No markdown yet -- fall back to the directory name.
    directory = files["directory"]
    return str(directory / f"{directory.name}_formatted.md")


def create_reformat_prompt(extracted_text, template, paper_info, output_path):
    """Create a formatted reformat prompt for Claude Code."""
    # The template carries the reformat instructions and an {output_path} slot.
    instructions = template.replace("{output_path}", output_path)

    title = paper_info.get("title", "Unknown Title")
    first_author = paper_info.get("first_author", "Unknown Author")
    year = paper_info.get("year", "Unknown Year")

    return f"""# Final Reformat: Clean the Extracted Markdown

I need you to reformat the raw, machine-extracted text of an academic paper into
a clean, Obsidian-ready Markdown document. Follow ALL instructions below. This is
a layout pass only -- preserve the author's words and numbers exactly.

## Paper Information
- **Title**: {title}
- **First Author**: {first_author}
- **Year**: {year}

## Reformat Instructions
{instructions}

## Raw Extracted Content
Below is the full text extracted from the PDF (PyMuPDF for searchable text +
Tesseract OCR fallback). Reformat this content:

```markdown
{extracted_text}
```

Ready? Reformat the content above and write the result to `{output_path}`.
"""


def main():
    parser = argparse.ArgumentParser(
        description="Prepare a reformat prompt that cleans extracted markdown into "
        "an Obsidian-ready layout (for Claude Code to execute)"
    )
    parser.add_argument(
        "extraction_dir",
        help="Directory containing extracted PDF content (from `extract`)",
    )
    parser.add_argument(
        "-t",
        "--template",
        default="templates/reformat.md",
        help="Path to the reformat template relative to script directory "
        "(default: templates/reformat.md)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file for the generated prompt (default: print to stdout)",
    )

    args = parser.parse_args()

    try:
        files = find_extracted_files(args.extraction_dir)

        if not files["has_content"]:
            print(f"❌ No extracted markdown found in {args.extraction_dir}")
            print("   Make sure you've run the extraction step first.")
            return 1

        print(f"📁 Found extraction directory: {files['directory']}")
        print(f"   Markdown file: {files['markdown'].name}")
        print()

        with open(files["markdown"], "r", encoding="utf-8") as f:
            extracted_text = f.read()
        print(f"📄 Extracted text length: {len(extracted_text)} characters")

        template, template_source = load_template(args.template)
        print(f"📋 Template loaded: {template_source}")

        if files["metadata"]:
            paper_info = extract_paper_info(files["metadata"])
        else:
            paper_info = {}
        if not paper_info:
            paper_info = guess_paper_info_from_filename(files["directory"].name)
        print()

        cleaned_path = formatted_output_path(files)
        prompt = create_reformat_prompt(
            extracted_text, template, paper_info, cleaned_path
        )

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(prompt)
            print(f"✅ Reformat prompt written to: {output_path}")
            print()
            print("📋 Next steps:")
            print(f"1. Open {output_path} and copy the prompt")
            print("2. Paste it into a Claude Code conversation")
            print(f"3. Claude writes the cleaned note to {cleaned_path}")
        else:
            print("=" * 80)
            print(prompt)
            print("=" * 80)
            print()
            print("📋 Copy the prompt above into a Claude Code conversation.")
            print(f"   Claude will write the cleaned note to {cleaned_path}")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
