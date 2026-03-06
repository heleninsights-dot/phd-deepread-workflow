#!/usr/bin/env python3
"""
PhD Deep Read Workflow - Python CLI entry point
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Main entry point for the phd-deepread CLI."""
    # If no arguments, show help
    if len(sys.argv) == 1:
        sys.argv.append("--help")

    # Get the command
    command = sys.argv[1] if len(sys.argv) > 1 else None

    # Map commands to scripts
    script_map = {
        "setup": "setup.sh",
        "extract": "extract.py",
        "generate": "generate.py",
        "canvas": "canvas.py",
"run": "process.py",
        "batch": "batch.sh",
        "verify": "verify.py",
        "guide": "show_guide",
        "help": "show_help",
    }

    # Handle help
    if command in ("--help", "-h", "help"):
        show_help()
        return 0

    # Handle guide
    if command in ("guide", "docs", "documentation"):
        show_guide()
        return 0

    # Check if command exists
    if command not in script_map:
        print(f"Unknown command: {command}")
        show_help()
        return 1

    script_name = script_map[command]

    # Special handling for guide and help
    if script_name == "show_guide":
        show_guide()
        return 0
    elif script_name == "show_help":
        show_help()
        return 0

    # Build script path
    script_dir = Path(__file__).parent
    script_path = script_dir / script_name

    if not script_path.exists():
        print(f"Script not found: {script_path}")
        return 1

    # Prepare arguments
    args = [str(script_path)] + sys.argv[2:]

    # Handle .sh vs .py scripts
    if script_path.suffix == ".sh":
        # Make sure it's executable
        if not os.access(script_path, os.X_OK):
            os.chmod(script_path, 0o755)
        # Run bash script
        result = subprocess.run(args, shell=False)
        return result.returncode
    else:
        # Run Python script
        result = subprocess.run([sys.executable] + args, shell=False)
        return result.returncode

def show_help():
    """Show help message."""
    help_text = """
PhD Deep Read Workflow - Transform academic PDFs into structured literature notes

Usage: phd-deepread <command> [options]

Commands:
  setup       Check dependencies and environment setup
  extract     Extract text/images from PDFs (Text-First decision tree: PyMuPDF + Tesseract OCR)
  generate    Generate structured note prompts from extracted content
  canvas      Create JSON Canvas templates for critical thinking
  run         Run full workflow automation (extract → generate → canvas)
  batch       Batch process multiple PDFs
  verify      Verify output quality and consistency
  guide       Show workflow guide and documentation
  help        Show this help message

Examples:
  phd-deepread setup
  phd-deepread extract paper.pdf -o markdown_output/
  phd-deepread generate markdown_output/paper/
  phd-deepread canvas --title "Paper Title" --authors "Author" --year "2024"
  phd-deepread run paper.pdf
  phd-deepread batch papers/ -o literature_notes/
  phd-deepread guide

For command-specific help: phd-deepread <command> --help
"""
    print(help_text.strip())
def show_guide():
    """Show workflow guide."""
    guide_path = Path(__file__).parent.parent / "docs" / "workflow-guide.md"
    if guide_path.exists():
        with open(guide_path, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("Workflow guide not found. Check docs/workflow-guide.md")

if __name__ == "__main__":
    sys.exit(main())