#!/bin/bash
# PhD Deep Read Workflow - Environment Setup Script
# Checks dependencies and provides installation instructions

set -e

echo "🔧 PhD Deep Read Workflow - Environment Setup"
echo "============================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check command availability
check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 is installed"
        return 0
    else
        echo -e "${RED}✗${NC} $1 is NOT installed"
        return 1
    fi
}

# Function to check Python package
check_python_package() {
    if python3 -c "import $1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Python package: $1"
        return 0
    else
        echo -e "${RED}✗${NC} Python package: $1"
        return 1
    fi
}

echo "📦 Checking core dependencies..."

# Check Python
check_command python3 || {
    echo -e "${RED}Python 3 is required but not found.${NC}"
    echo "Install Python 3.10 or later from https://www.python.org/"
    exit 1
}

# Check pip
check_command pip3 || {
    echo -e "${YELLOW}pip3 not found. Trying pip...${NC}"
    if ! check_command pip; then
        echo -e "${RED}pip is required but not found.${NC}"
        echo "Install pip: https://pip.pypa.io/en/stable/installation/"
        exit 1
    fi
}

echo
echo "🔍 Checking workflow tools..."

# Check for PyMuPDF (fitz) - REQUIRED
if check_python_package fitz; then
    echo -e "   PyMuPDF (fitz) is available for pdftext extraction"
else
    echo -e "${YELLOW}PyMuPDF (fitz) is not installed.${NC}"
    echo "Install with: pip install PyMuPDF"
fi

# Check for Tesseract OCR (optional)
check_command tesseract
if check_python_package pytesseract; then
    echo -e "   pytesseract Python package available"
elif check_command tesseract; then
    echo -e "${GREEN}✓${NC} tesseract command available (pytesseract not installed)"
    echo "   Install pytesseract Python package: pip install pytesseract pillow"
else
    echo -e "${YELLOW}⚠ Tesseract OCR not available.${NC}"
    echo "   OCR fallback will be disabled. Install for full functionality:"
    echo "   - Command line: brew install tesseract"
    echo "   - Python package: pip install pytesseract pillow"
fi

echo
echo "🏠 Checking virtual environment..."

# Check if we're in a virtual environment
if [[ -n "$VIRTUAL_ENV" ]]; then
    echo -e "${GREEN}✓${NC} Virtual environment active: $VIRTUAL_ENV"
else
    echo -e "${YELLOW}⚠ Not running in a virtual environment.${NC}"
    echo "Recommended: Use a Python virtual environment to manage dependencies."

    # Check for existing virtual environment in current directory
    if [[ -d ".venv" ]]; then
        echo -e "${GREEN}✓${NC} Found existing virtual environment in current directory."
        echo "Activate with: source .venv/bin/activate"
    else
        echo "Create a new virtual environment:"
        echo "  python3 -m venv .venv"
        echo "  source .venv/bin/activate"
    fi
fi

echo
echo "⚙️ Checking environment variables..."

# Note: ENABLE_EFFICIENT_ATTENTION was for Surya OCR (no longer used)
if [[ -n "$ENABLE_EFFICIENT_ATTENTION" ]]; then
    echo -e "${GREEN}✓${NC} ENABLE_EFFICIENT_ATTENTION=$ENABLE_EFFICIENT_ATTENTION (legacy)"
else
    echo -e "${GREEN}✓${NC} ENABLE_EFFICIENT_ATTENTION not needed for new Text-First workflow"
fi

echo
echo "📁 Checking directory structure..."

# Check for repository files and directories
echo "📁 Checking repository structure..."

# Check for template files
if [[ -f "scripts/templates/clauderules.md" ]]; then
    echo -e "${GREEN}✓${NC} .clauderules template found"
else
    echo -e "${RED}✗${NC} .clauderules template not found in scripts/templates/"
fi

if [[ -f "scripts/templates/critical-thinking.canvas" ]]; then
    echo -e "${GREEN}✓${NC} critical-thinking.canvas template found"
else
    echo -e "${RED}✗${NC} critical-thinking.canvas template not found in scripts/templates/"
fi

# Check for example directory
if [[ -d "examples" ]]; then
    EXAMPLE_COUNT=$(find "examples" -name "*.md" -o -name "*.canvas" -o -name "*.pdf" 2>/dev/null | wc -l)
    echo -e "${GREEN}✓${NC} Examples directory ($EXAMPLE_COUNT example files)"
else
    echo -e "${YELLOW}⚠${NC} Examples directory not found"
fi

# Check for output directories (may not exist yet)
if [[ -d "structured_literature_notes" ]]; then
    NOTE_COUNT=$(find "structured_literature_notes" -name "*.md" 2>/dev/null | wc -l)
    echo -e "${GREEN}✓${NC} Structured notes directory ($NOTE_COUNT notes)"
fi

if [[ -d "markdown_output" ]]; then
    PDF_COUNT=$(find "markdown_output" -type d -mindepth 1 -maxdepth 1 2>/dev/null | wc -l)
    echo -e "${GREEN}✓${NC} Markdown output directory ($PDF_COUNT processed PDFs)"
fi

echo
echo "📋 Summary of Next Steps:"

if ! check_python_package fitz; then
    echo "1. Install PyMuPDF: pip install PyMuPDF"
elif ! check_command tesseract && ! check_python_package pytesseract; then
    echo "1. Optional: Install Tesseract OCR for scanned PDFs"
    echo "   - Command line: brew install tesseract"
    echo "   - Python package: pip install pytesseract pillow"
fi

if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "2. Activate virtual environment"
fi

if [[ -z "$ENABLE_EFFICIENT_ATTENTION" ]]; then
    echo "3. Set environment variable: export ENABLE_EFFICIENT_ATTENTION=0"
fi

echo "4. Test the workflow with: phd-deepread extract --help"
echo
echo "✅ Setup check complete. Run 'phd-deepread guide' for workflow instructions."