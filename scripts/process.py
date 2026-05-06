import subprocess
import argparse
from pathlib import Path


def run_all(pdf_path, notes_dir="structured_literature_notes"):
    paper_name = Path(pdf_path).stem.strip()
    extraction_folder = f"markdown_output/{paper_name}"
    note_output = f"{notes_dir}/{paper_name}.md"
    canvas_output = f"{notes_dir}/{paper_name}.canvas"

    print(f"--- Starting Full Workflow for: {pdf_path} ---")

    print("\nStep 1: Extracting PDF...")
    subprocess.run(["phd-deepread", "extract", pdf_path], check=True)

    print("\nStep 2: Generating literature-note prompt...")
    subprocess.run(
        ["phd-deepread", "generate", extraction_folder, "-o", note_output],
        check=True,
    )

    print("\nStep 3: Creating Visual Canvas...")
    subprocess.run(
        ["phd-deepread", "canvas", "-o", canvas_output, "--overwrite"],
        check=True,
    )

    print(f"\n--- Workflow Complete! ---")
    print(f"  Literature-note prompt : {note_output}")
    print(f"  Canvas                 : {canvas_output}")
    print()
    print("📋 Next: open the prompt file in Claude Code and ask Claude to write the note,")
    print("   then optionally re-run `phd-deepread canvas --from-note <note.md> -o <canvas>`")
    print("   to populate the canvas from the finished note.")


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

    run_all(args.pdf_path, notes_dir=args.notes_dir)
