#!/usr/bin/env python3
"""
PhD Deep Read Workflow - dependency check / first-run verification.

Reports the state of every component the workflow needs:
- Python version
- Required Python packages (PyMuPDF, pytesseract, Pillow)
- Tesseract OCR binary (optional — only needed for scanned PDFs)
- Bundled templates (clauderules.md, critical-thinking.canvas)

Exits 0 if everything required is present, 1 otherwise. Optional components
warn but do not fail.
"""

from __future__ import annotations

import importlib
import importlib.resources
import shutil
import subprocess
import sys


GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
NC = "\033[0m"


def ok(msg: str) -> None:
    print(f"{GREEN}✓{NC} {msg}")


def warn(msg: str) -> None:
    print(f"{YELLOW}⚠{NC} {msg}")


def fail(msg: str) -> None:
    print(f"{RED}✗{NC} {msg}")


def check_python() -> bool:
    v = sys.version_info
    if v >= (3, 10):
        ok(f"Python {v.major}.{v.minor}.{v.micro}")
        return True
    fail(f"Python {v.major}.{v.minor}.{v.micro} — need 3.10 or higher")
    print("   Install a newer Python from https://www.python.org/downloads/")
    return False


def check_package(import_name: str, pip_name: str | None = None, required: bool = True) -> bool:
    pip_name = pip_name or import_name
    try:
        importlib.import_module(import_name)
    except ImportError:
        if required:
            fail(f"Python package missing: {import_name}")
            print(f"   Install with: pip install {pip_name}")
        else:
            warn(f"Python package not installed: {import_name} (optional)")
        return False
    ok(f"Python package: {import_name}")
    return True


def check_tesseract_binary() -> bool:
    path = shutil.which("tesseract")
    if not path:
        warn("tesseract binary not found (optional — only needed for scanned PDFs)")
        print("   macOS:        brew install tesseract")
        print("   Ubuntu/Debian: sudo apt install tesseract-ocr")
        return False
    try:
        version_line = subprocess.run(
            ["tesseract", "--version"], capture_output=True, text=True, timeout=5
        ).stdout.splitlines()[0]
    except Exception:
        version_line = path
    ok(f"tesseract: {version_line}")
    return True


def check_template(filename: str) -> bool:
    try:
        importlib.resources.files("scripts.templates").joinpath(filename).read_text(encoding="utf-8")
    except (ImportError, FileNotFoundError, AttributeError):
        fail(f"template missing: {filename}")
        print("   Try: pip install --upgrade phd-deepread-workflow")
        return False
    ok(f"template: {filename}")
    return True


def main() -> int:
    print("PhD Deep Read Workflow — dependency check")
    print("=========================================")
    print()

    print("Core:")
    required_ok = True
    required_ok &= check_python()
    required_ok &= check_package("fitz", "PyMuPDF")
    required_ok &= check_package("pytesseract")
    required_ok &= check_package("PIL", "Pillow")

    print()
    print("Templates:")
    required_ok &= check_template("clauderules.md")
    required_ok &= check_template("critical-thinking.canvas")

    print()
    print("Optional (scanned PDFs):")
    check_tesseract_binary()

    print()
    if required_ok:
        ok("All required dependencies present.")
        print("   Run `phd-deepread guide` for the workflow walkthrough.")
        return 0
    fail("Some required dependencies are missing — see above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
