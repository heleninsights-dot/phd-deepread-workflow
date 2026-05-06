#!/usr/bin/env python3
"""
PhD Deep Read Workflow - Batch processing.

Runs the workflow over every PDF in a folder. By default each PDF is extracted
and a literature-note prompt is written. Optionally also creates a 9-node
canvas template per paper.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_step(cmd: list[str]) -> bool:
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def find_extraction_subdir(extract_dir: Path, pdf_stem: str) -> Path | None:
    candidates = [d for d in extract_dir.iterdir() if d.is_dir() and pdf_stem in d.name]
    return candidates[0] if candidates else None


def read_meta(extract_subdir: Path) -> dict:
    meta_files = list(extract_subdir.glob("*_meta.json"))
    if not meta_files:
        return {}
    try:
        return json.loads(meta_files[0].read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Batch-process every PDF in a folder through phd-deepread."
    )
    parser.add_argument("input_dir", help="Directory containing PDF files")
    parser.add_argument("-o", "--output", default="batch_output",
                        help="Output directory (default: batch_output)")
    parser.add_argument("--extract-only", action="store_true",
                        help="Only run PDF extraction; skip prompt and canvas")
    parser.add_argument("--create-canvases", action="store_true",
                        help="Also create a 9-node canvas template for each paper")
    parser.add_argument("--no-skip", action="store_true",
                        help="Reprocess PDFs even if output already exists")
    parser.add_argument("-p", "--page-range",
                        help='Page range, e.g. "0,5" for first 6 pages')
    parser.add_argument("--lang", default="eng", help="OCR language (default: eng)")

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.is_dir():
        print(f"Error: input directory not found: {input_dir}", file=sys.stderr)
        return 1

    pdfs = sorted(input_dir.glob("*.pdf"))
    if not pdfs:
        print(f"Error: no PDF files found in {input_dir}", file=sys.stderr)
        return 1

    output_dir = Path(args.output)
    extract_dir = output_dir / "markdown_output"
    prompt_dir = output_dir / "generation_prompts"
    canvas_dir = output_dir / "canvas_templates"
    for d in (extract_dir, prompt_dir, canvas_dir):
        d.mkdir(parents=True, exist_ok=True)

    print("PhD Deep Read — batch processing")
    print(f"  Input  : {input_dir}")
    print(f"  Output : {output_dir}")
    print(f"  PDFs   : {len(pdfs)}")
    print()

    counts = {"extract": 0, "prompt": 0, "canvas": 0}
    skip = not args.no_skip

    for pdf in pdfs:
        stem = pdf.stem
        print(f"--- {stem} ---")

        extract_cmd = ["phd-deepread", "extract", str(pdf), "-o", str(extract_dir),
                       "--lang", args.lang]
        if args.page_range:
            extract_cmd += ["-p", args.page_range]
        if not run_step(extract_cmd):
            print(f"  ✗ extraction failed for {stem}")
            continue
        counts["extract"] += 1

        subdir = find_extraction_subdir(extract_dir, stem)
        if not subdir:
            print(f"  ⚠ extraction subdir not found for {stem}")
            continue

        if args.extract_only:
            continue

        prompt_file = prompt_dir / f"{stem}_prompt.txt"
        if prompt_file.exists() and skip:
            print(f"  ⤳ prompt exists, skipping ({prompt_file.name})")
        else:
            if run_step(["phd-deepread", "generate", str(subdir), "-o", str(prompt_file)]):
                counts["prompt"] += 1
            else:
                print(f"  ✗ prompt generation failed for {stem}")

        if args.create_canvases:
            canvas_file = canvas_dir / f"{stem}-CriticalThinking.canvas"
            if canvas_file.exists() and skip:
                print(f"  ⤳ canvas exists, skipping ({canvas_file.name})")
            else:
                meta = read_meta(subdir)
                canvas_cmd = ["phd-deepread", "canvas", "-o", str(canvas_file), "--overwrite"]
                if meta.get("title"):
                    canvas_cmd += ["--title", meta["title"]]
                if meta.get("authors"):
                    authors = meta["authors"]
                    if isinstance(authors, list) and authors:
                        canvas_cmd += ["--authors", str(authors[0])]
                    elif isinstance(authors, str):
                        canvas_cmd += ["--authors", authors]
                if meta.get("year"):
                    canvas_cmd += ["--year", str(meta["year"])]
                if run_step(canvas_cmd):
                    counts["canvas"] += 1
                else:
                    print(f"  ✗ canvas creation failed for {stem}")

    print()
    print("Summary")
    print(f"  extracted : {counts['extract']}/{len(pdfs)}")
    if not args.extract_only:
        print(f"  prompts   : {counts['prompt']}/{len(pdfs)}")
    if args.create_canvases:
        print(f"  canvases  : {counts['canvas']}/{len(pdfs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
