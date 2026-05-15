"""Full pipeline: extract → generate prompt → canvas, all in-process."""

import sys
import json
import argparse
from pathlib import Path

from scripts.extract import extract_pdf
from scripts.generate import main as generate_main
from scripts.canvas import create_canvas_template, main as canvas_main


def run_all(pdf_path, notes_dir="structured_literature_notes"):
    paper_name = Path(pdf_path).stem.strip()
    extraction_folder = f"markdown_output/{paper_name}"
    note_output = f"{notes_dir}/{paper_name}.md"
    canvas_output = f"{notes_dir}/{paper_name}.canvas"

    print(f"--- Starting Full Workflow for: {pdf_path} ---")

    # Step 1: Extract — direct function call, no subprocess
    print("\nStep 1: Extracting PDF...")
    result = extract_pdf(pdf_path)
    if not result.get("success"):
        print(f"❌ Extraction failed: {result.get('error')}")
        return 1
    print(f"✅ Extraction complete — output: {result.get('output_dir')}")

    # Step 2: Generate prompt — invoke main with synthetic argv
    print("\nStep 2: Generating literature-note prompt...")
    saved_argv = sys.argv
    sys.argv = ["generate", extraction_folder, "-o", note_output]
    try:
        ret = generate_main()
        if ret != 0:
            print("❌ Prompt generation failed")
            return ret
    finally:
        sys.argv = saved_argv

    # Step 3: Create canvas — invoke main with synthetic argv
    print("\nStep 3: Creating Visual Canvas...")
    sys.argv = ["canvas", "-o", canvas_output, "--overwrite"]
    try:
        ret = canvas_main()
        if ret != 0:
            print("❌ Canvas creation failed")
            return ret
    finally:
        sys.argv = saved_argv

    print(f"\n--- Workflow Complete! ---")
    print(f"  Literature-note prompt : {note_output}")
    print(f"  Canvas                 : {canvas_output}")
    print()
    print("📋 Next: open the prompt file in Claude Code and ask Claude to write the note,")
    print("   then optionally re-run `phd-deepread canvas --from-note <note.md> -o <canvas>`")
    print("   to populate the canvas from the finished note.")

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run full PhD Deep Read pipeline: extract → generate prompt → canvas"
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "--notes-dir",
        default="structured_literature_notes",
        help="Output directory for notes and canvas (default: structured_literature_notes)",
    )
    args = parser.parse_args()

    sys.exit(run_all(args.pdf_path, notes_dir=args.notes_dir))
