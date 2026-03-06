"""
PhD Deep Read Workflow - Python scripts package

This package contains the core scripts for the PhD Deep Read Workflow:
- extract.py: PDF extraction with Text-First decision tree
- generate.py: Structured note generation
- canvas.py: Critical-thinking canvas creation
- verify.py: Quality verification
- phd_deepread.py: CLI entry point
"""

__version__ = "0.1.2"
__author__ = "Helen Insights"
__email__ = "heleninsights@gmail.com"

# Export main functions for easier imports
from .phd_deepread import main as cli_main
from .extract import main as extract_main
from .generate import main as generate_main
from .canvas import main as canvas_main
from .verify import main as verify_main

__all__ = [
    "cli_main",
    "extract_main",
    "generate_main",
    "canvas_main",
    "verify_main",
    "__version__",
    "__author__",
    "__email__",
]