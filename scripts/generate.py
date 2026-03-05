#!/usr/bin/env python3
"""
PhD Deep Read Workflow - Structured Note Generation Script
Prepares extracted PDF content for Claude Code processing with .clauderules template.

This script helps generate structured literature notes by:
1. Reading extracted markdown from Text-First extraction output
2. Loading the .clauderules template
3. Creating a formatted prompt for Claude Code
4. Optionally generating a skeleton note with metadata
"""

import argparse
import json
import sys
from pathlib import Path
import re

def find_extracted_files(extraction_dir):
    """Find markdown and metadata files in extraction directory."""
    extraction_path = Path(extraction_dir)

    if not extraction_path.exists():
        raise FileNotFoundError(f"Extraction directory not found: {extraction_dir}")

    # Look for markdown files (excluding formatted/backup)
    md_files = list(extraction_path.glob("*.md"))
    # Filter out formatted/backup files
    md_files = [f for f in md_files if not f.name.endswith("_formatted.md") and not f.name.endswith(".backup.md")]

    # Look for metadata JSON
    meta_files = list(extraction_path.glob("*_meta.json"))

    # Look for images
    image_files = list(extraction_path.glob("*.jpeg")) + list(extraction_path.glob("*.png"))

    return {
        "directory": extraction_path,
        "markdown": md_files[0] if md_files else None,
        "metadata": meta_files[0] if meta_files else None,
        "images": image_files,
        "has_content": bool(md_files)
    }

def read_template(template_path):
    """Read .clauderules template file."""
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read template: {e}")

def extract_paper_info(metadata_path):
    """Extract paper information from metadata JSON."""
    if not metadata_path or not metadata_path.exists():
        return {}

    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)

        info = {}

        # Extract from metadata if available
        if "title" in meta:
            info["title"] = meta["title"]
        if "authors" in meta and meta["authors"]:
            info["first_author"] = meta["authors"][0]
        if "year" in meta:
            info["year"] = meta["year"]
        if "journal" in meta:
            info["journal"] = meta["journal"]

        return info
    except (json.JSONDecodeError, KeyError) as e:
        print(f"⚠ Could not extract metadata: {e}")
        return {}

def guess_paper_info_from_filename(filename):
    """Attempt to guess paper info from filename."""
    # Common patterns in academic PDF filenames
    name = Path(filename).stem

    # Try to extract year (4-digit number)
    year_match = re.search(r'(19|20)\d{2}', name)
    year = year_match.group() if year_match else "2024"

    # Try to extract first author (text before first punctuation or year)
    author_match = re.match(r'^([A-Za-z]+)', name)
    author = author_match.group(1) if author_match else "Author"

    # Try to extract title (rest of the name)
    # This is very approximate
    title = name.replace(f"{author}", "").replace(f"{year}", "").strip(" -_")

    return {
        "title": title if title else "Unknown Title",
        "first_author": author,
        "year": year,
        "journal": "Unknown Journal"
    }

def create_claude_prompt(extracted_text, template, paper_info):
    """Create a formatted prompt for Claude Code."""
    # Prepare APA citation placeholder
    apa_citation = f"{paper_info.get('first_author', 'Author')} ({paper_info.get('year', 'Year')}). {paper_info.get('title', 'Title')}. *{paper_info.get('journal', 'Journal')}*."

    # Prepare camelCase citekey
    first_author = paper_info.get('first_author', 'Author')
    first_word = paper_info.get('title', 'Title').split()[0] if paper_info.get('title') else 'Paper'
    year = paper_info.get('year', 'Year')
    citekey = f"{first_author}{first_word}{year}"

    # Replace template placeholders with actual info
    prompt_template = f"""# Structured Literature Note Generation

I need you to generate a structured literature note for the following academic paper using the `.clauderules` template.

## Paper Information
- **Title**: {paper_info.get('title', 'Unknown Title')}
- **First Author**: {paper_info.get('first_author', 'Unknown Author')}
- **Year**: {paper_info.get('year', 'Unknown Year')}
- **Journal**: {paper_info.get('journal', 'Unknown Journal')}
- **Citekey**: {citekey}

## Extracted PDF Content
Below is the raw text extracted from the PDF (via Text-First decision tree using PyMuPDF for searchable text + Tesseract OCR fallback):

```markdown
{extracted_text[:5000]}  # Limit to first 5000 chars
```

[Content truncated for brevity. Full text available in extraction directory.]

## Template to Follow
You MUST follow this exact `.clauderules` template:

```yaml
{template}
```

## Instructions
1. Read the extracted PDF content above
2. Apply the `.clauderules` template exactly as shown
3. Fill in all template placeholders with information from the paper
4. Generate a comprehensive literature note in raw Markdown format
5. Include YAML frontmatter, Dataview callouts, and all required sections
6. Use [[Wikilinks]] extensively for key concepts, methods, proteins, etc.
7. Maintain an academic, critical tone throughout

## Output Format
Output ONLY the completed Markdown code block with the structured literature note.

Ready? Begin.
"""

    return prompt_template

def main():
    parser = argparse.ArgumentParser(
        description="Prepare extracted PDF content for structured note generation with Claude Code"
    )
    parser.add_argument("extraction_dir", help="Directory containing extracted PDF content (from marker)")
    parser.add_argument("-t", "--template", default="templates/.clauderules",
                       help="Path to .clauderules template (default: templates/.clauderules)")
    parser.add_argument("-o", "--output", help="Output file for generated prompt (default: print to stdout)")
    parser.add_argument("--skeleton", action="store_true",
                       help="Generate a skeleton note with placeholders instead of a full prompt")

    args = parser.parse_args()

    try:
        # Find extracted files
        files = find_extracted_files(args.extraction_dir)

        if not files["has_content"]:
            print(f"❌ No extracted markdown found in {args.extraction_dir}")
            print("   Make sure you've run the extraction step first.")
            return 1

        print(f"📁 Found extraction directory: {files['directory']}")
        print(f"   Markdown file: {files['markdown'].name if files['markdown'] else 'Not found'}")
        print(f"   Metadata file: {files['metadata'].name if files['metadata'] else 'Not found'}")
        print(f"   Images: {len(files['images'])} files")
        print()

        # Read extracted markdown
        extracted_text = ""
        if files["markdown"]:
            with open(files["markdown"], 'r', encoding='utf-8') as f:
                extracted_text = f.read()
            print(f"📄 Extracted text length: {len(extracted_text)} characters")
        else:
            print("❌ No markdown file found")
            return 1

        # Read template
        template_path = Path(args.template)
        if not template_path.exists():
            # Try relative to script directory
            script_dir = Path(__file__).parent
            template_path = script_dir.parent / "templates" / ".clauderules"

        template = read_template(template_path)
        print(f"📋 Template loaded: {template_path}")
        print()

        # Extract paper info
        paper_info = {}
        if files["metadata"]:
            paper_info = extract_paper_info(files["metadata"])
            if paper_info:
                print("📊 Extracted paper metadata from JSON:")
                for key, value in paper_info.items():
                    print(f"   {key}: {value}")
            else:
                print("⚠ Could not extract metadata from JSON, guessing from filename...")
                paper_info = guess_paper_info_from_filename(files["directory"].name)
        else:
            print("⚠ No metadata JSON, guessing from filename...")
            paper_info = guess_paper_info_from_filename(files["directory"].name)

        print()

        if args.skeleton:
            # Generate skeleton note (placeholder version)
            print("Generating skeleton note with placeholders...")
            # This would create a basic structured note with placeholders
            # For now, just show we'd do it
            print("(Skeleton generation not yet implemented)")
            return 0

        # Create Claude prompt
        prompt = create_claude_prompt(extracted_text, template, paper_info)

        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(prompt)
            print(f"✅ Prompt written to: {output_path}")
            print()
            print("📋 Next steps:")
            print("1. Copy the prompt above")
            print("2. Paste it into a Claude Code conversation")
            print("3. Claude will generate the structured literature note")
            print("4. Save the output to structured_literature_notes/")
        else:
            print("=" * 80)
            print(prompt)
            print("=" * 80)
            print()
            print("📋 Copy the prompt above and paste it into a Claude Code conversation.")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())