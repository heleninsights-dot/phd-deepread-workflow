import subprocess
import sys
import argparse
from pathlib import Path


def run_all(pdf_path, openai=False, model="gpt-4o", base_url=None,
            notes_dir="structured_literature_notes"):
    paper_name = Path(pdf_path).stem.strip()
    extraction_folder = f"markdown_output/{paper_name}"
    note_output = f"{notes_dir}/{paper_name}.md"
    canvas_output = f"{notes_dir}/{paper_name}.canvas"

    print(f"--- Starting Full Workflow for: {pdf_path} ---")

    # 1. Extract
    print("\nStep 1: Extracting PDF...")
    subprocess.run(["phd-deepread", "extract", pdf_path], check=True)

    # 2. Generate literature note
    print("\nStep 2: Generating Literature Note...")
    gen_cmd = ["phd-deepread", "generate", extraction_folder, "-o", note_output]
    if openai:
        gen_cmd += ["--openai", "--model", model]
        if base_url:
            gen_cmd += ["--base-url", base_url]
    subprocess.run(gen_cmd, check=True)

    # 3. Create canvas
    print("\nStep 3: Creating Visual Canvas...")
    canvas_cmd = ["phd-deepread", "canvas", "-o", canvas_output, "--overwrite"]
    if openai:
        canvas_cmd += ["--from-note", note_output, "--openai", "--model", model]
        if base_url:
            canvas_cmd += ["--base-url", base_url]
    subprocess.run(canvas_cmd, check=True)

    print(f"\n--- Workflow Complete! ---")
    print(f"  Literature note : {note_output}")
    print(f"  Canvas          : {canvas_output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run full PhD Deep Read pipeline: extract → generate → canvas"
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument("--openai", action="store_true",
                        help="Use an OpenAI-compatible API to generate note and populate canvas "
                             "(requires OPENAI_API_KEY)")
    parser.add_argument("--model", default="gpt-4o",
                        help="Model name (default: gpt-4o). Use e.g. deepseek-chat for DeepSeek.")
    parser.add_argument("--base-url", dest="base_url", default=None,
                        help="API base URL for non-OpenAI providers (e.g. https://api.deepseek.com). "
                             "Can also be set via OPENAI_BASE_URL env var.")
    parser.add_argument("--notes-dir", default="structured_literature_notes",
                        help="Output directory for notes and canvas (default: structured_literature_notes)")
    args = parser.parse_args()

    run_all(args.pdf_path, openai=args.openai, model=args.model,
            base_url=args.base_url, notes_dir=args.notes_dir)
