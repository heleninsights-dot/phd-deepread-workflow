#!/bin/bash
# PhD Deep Read Workflow - Installation script

set -e

echo "🎓 PhD Deep Read Workflow - Installation"
echo "========================================"
echo

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "   Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Python $PYTHON_VERSION detected"

# Check if we're in a virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠ Not running in a virtual environment."
    read -p "   Create virtual environment in .venv? [Y/n] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z "$REPLY" ]]; then
        python3 -m venv .venv
        echo "✓ Virtual environment created at .venv"
        echo "   Activate with: source .venv/bin/activate"
        # Activate for rest of script
        source .venv/bin/activate
    fi
else
    echo "✓ Virtual environment detected: $VIRTUAL_ENV"
fi

# Install Python dependencies
echo
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for Tesseract OCR
echo
echo "🔍 Checking for Tesseract OCR (optional but recommended)..."
if command -v tesseract &> /dev/null; then
    TESSERACT_VERSION=$(tesseract --version 2>/dev/null | head -1 | cut -d' ' -f2)
    echo "✓ Tesseract OCR detected: version $TESSERACT_VERSION"
    echo "  Installing Python wrapper..."
    pip install pytesseract pillow
else
    echo "⚠ Tesseract OCR not found."
    echo "   OCR fallback will not be available for scanned PDFs."
    echo "   Install with:"
    echo "     macOS: brew install tesseract"
    echo "     Ubuntu/Debian: sudo apt install tesseract-ocr"
    echo "     Windows: https://github.com/UB-Mannheim/tesseract/wiki"
fi

# Make scripts executable
echo
echo "🔧 Making scripts executable..."
chmod +x scripts/*.sh scripts/phd-deepread 2>/dev/null || true

# Create necessary directories
echo
echo "📁 Creating directory structure..."
mkdir -p markdown_output structured_literature_notes generation_prompts canvas_templates logs

# Test installation
echo
echo "🧪 Testing installation..."
if python3 -c "import fitz, pytesseract" &> /dev/null; then
    echo "✓ Core dependencies installed successfully"
else
    echo "⚠ Some dependencies may be missing"
    echo "   Run 'pip install -r requirements.txt' manually if needed"
fi

# Installation complete
echo
echo "✅ Installation complete!"
echo
echo "Next steps:"
echo "1. Activate virtual environment (if not already):"
echo "     source .venv/bin/activate"
echo "2. Test the workflow with a sample PDF:"
echo "     phd-deepread extract examples/test_paper.pdf"
echo "3. View the workflow guide:"
echo "     phd-deepread guide"
echo
echo "For help, run: phd-deepread --help"
echo
echo "Happy researching! 🎓"