#!/bin/bash
# PhD Deep Read Workflow - Batch Processing Script
# Processes multiple PDFs through the workflow stages

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default values
INPUT_DIR=""
OUTPUT_DIR="batch_output"
EXTRACT_ONLY=false
GENERATE_PROMPTS=false
CREATE_CANVASES=false
SKIP_EXISTING=true
PAGE_RANGE=""
LANG="eng"

print_usage() {
    cat << EOF
Batch processing for PhD Deep Read workflow.

Usage: $0 [options] <input_directory>

Arguments:
  <input_directory>    Directory containing PDF files to process

Options:
  -o, --output DIR     Output directory (default: batch_output)
  --extract-only       Only run extraction, skip note generation
  --generate-prompts   Create Claude prompts for note generation
  --create-canvases    Create JSON canvas templates for each paper
  --no-skip            Reprocess existing files
  -p, --page-range R   Page range (e.g., "0,5" for first 6 pages)
  --lang L             Language for OCR (default: eng)
  -h, --help           Show this help message

Examples:
  $0 papers/ -o literature_notes/
  $0 papers/ --extract-only --no-skip
  $0 papers/ --generate-prompts --create-canvases
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            print_usage
            exit 0
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --extract-only)
            EXTRACT_ONLY=true
            shift
            ;;
        --generate-prompts)
            GENERATE_PROMPTS=true
            shift
            ;;
        --create-canvases)
            CREATE_CANVASES=true
            shift
            ;;
        --no-skip)
            SKIP_EXISTING=false
            shift
            ;;
        -p|--page-range)
            PAGE_RANGE="$2"
            shift 2
            ;;
        --lang)
            LANG="$2"
            shift 2
            ;;
        *)
            if [[ -z "$INPUT_DIR" ]]; then
                INPUT_DIR="$1"
                shift
            else
                echo -e "${RED}Error: Unknown argument $1${NC}"
                print_usage
                exit 1
            fi
            ;;
    esac
done

# Validate input
if [[ -z "$INPUT_DIR" ]]; then
    echo -e "${RED}Error: Input directory required${NC}"
    print_usage
    exit 1
fi

if [[ ! -d "$INPUT_DIR" ]]; then
    echo -e "${RED}Error: Input directory not found: $INPUT_DIR${NC}"
    exit 1
fi

# Create output directories
EXTRACT_DIR="$OUTPUT_DIR/markdown_output"
PROMPT_DIR="$OUTPUT_DIR/generation_prompts"
CANVAS_DIR="$OUTPUT_DIR/canvas_templates"
NOTE_DIR="$OUTPUT_DIR/structured_notes"

mkdir -p "$EXTRACT_DIR"
mkdir -p "$PROMPT_DIR"
mkdir -p "$CANVAS_DIR"
mkdir -p "$NOTE_DIR"

echo "🚀 PhD Deep Read Batch Processing"
echo "================================="
echo
echo "📂 Input directory: $INPUT_DIR"
echo "📂 Output directory: $OUTPUT_DIR"
echo "⚙️  Options:"
echo "   Extract only: $EXTRACT_ONLY"
echo "   Generate prompts: $GENERATE_PROMPTS"
echo "   Create canvases: $CREATE_CANVASES"
echo "   Skip existing: $SKIP_EXISTING"
echo "   Page range: ${PAGE_RANGE:-all}"
echo "   Language: $LANG"
echo

# Find PDF files
PDF_FILES=("$INPUT_DIR"/*.pdf)
if [[ ${#PDF_FILES[@]} -eq 0 ]] || [[ ! -f "${PDF_FILES[0]}" ]]; then
    echo -e "${RED}Error: No PDF files found in $INPUT_DIR${NC}"
    exit 1
fi

echo "📄 Found ${#PDF_FILES[@]} PDF file(s)"
echo

# Process each PDF
SUCCESS_EXTRACT=0
SUCCESS_PROMPT=0
SUCCESS_CANVAS=0

for pdf in "${PDF_FILES[@]}"; do
    PDF_NAME=$(basename "$pdf" .pdf)
    echo -e "${BLUE}=========================================${NC}"
    echo -e "${BLUE}Processing: $PDF_NAME${NC}"
    echo -e "${BLUE}=========================================${NC}"

    # Step 1: Extraction
    echo "📤 Step 1: PDF Extraction"
    EXTRACT_ARGS=("$pdf" "-o" "$EXTRACT_DIR")
    if [[ -n "$PAGE_RANGE" ]]; then
        EXTRACT_ARGS+=("-p" "$PAGE_RANGE")
    fi
    EXTRACT_ARGS+=("--lang" "$LANG")

    # Run extraction script
    if python "$SCRIPT_DIR/extract.py" "${EXTRACT_ARGS[@]}"; then
        echo -e "${GREEN}✓ Extraction successful${NC}"
        SUCCESS_EXTRACT=$((SUCCESS_EXTRACT + 1))
    else
        echo -e "${RED}✗ Extraction failed${NC}"
        continue
    fi

    # Find extraction subdirectory
    EXTRACT_SUBDIR=$(find "$EXTRACT_DIR" -type d -name "*$PDF_NAME*" | head -1)
    if [[ -z "$EXTRACT_SUBDIR" ]] || [[ ! -d "$EXTRACT_SUBDIR" ]]; then
        echo -e "${YELLOW}⚠ Could not find extraction subdirectory${NC}"
        continue
    fi

    echo "   Output: $EXTRACT_SUBDIR"
    echo

    # Step 2: Generate prompt (if requested)
    if [[ "$GENERATE_PROMPTS" == true ]] || [[ "$EXTRACT_ONLY" == false ]]; then
        echo "📝 Step 2: Generate Claude Prompt"
        PROMPT_FILE="$PROMPT_DIR/${PDF_NAME}_prompt.txt"

        if [[ -f "$PROMPT_FILE" ]] && [[ "$SKIP_EXISTING" == true ]]; then
            echo -e "${YELLOW}⚠ Prompt already exists, skipping${NC}"
        else
            if python "$SCRIPT_DIR/generate.py" "$EXTRACT_SUBDIR" -o "$PROMPT_FILE"; then
                echo -e "${GREEN}✓ Prompt generated${NC}"
                SUCCESS_PROMPT=$((SUCCESS_PROMPT + 1))
                echo "   Prompt: $PROMPT_FILE"
            else
                echo -e "${RED}✗ Prompt generation failed${NC}"
            fi
        fi
        echo
    fi

    # Step 3: Create canvas (if requested)
    if [[ "$CREATE_CANVASES" == true ]]; then
        echo "🎨 Step 3: Create Canvas Template"
        CANVAS_FILE="$CANVAS_DIR/${PDF_NAME}-CriticalThinking.canvas"

        if [[ -f "$CANVAS_FILE" ]] && [[ "$SKIP_EXISTING" == true ]]; then
            echo -e "${YELLOW}⚠ Canvas already exists, skipping${NC}"
        else
            # Try to extract paper info from metadata
            META_FILE=$(find "$EXTRACT_SUBDIR" -name "*_meta.json" | head -1)
            TITLE=""
            AUTHORS=""
            YEAR=""

            if [[ -f "$META_FILE" ]]; then
                # Simple extraction using grep (could be more robust)
                TITLE=$(grep -o '"title":"[^"]*' "$META_FILE" | head -1 | cut -d'"' -f4)
                AUTHORS=$(grep -o '"authors":\["[^"]*' "$META_FILE" | head -1 | cut -d'"' -f4)
                YEAR=$(grep -o '"year":"[^"]*' "$META_FILE" | head -1 | cut -d'"' -f4)
            fi

            CANVAS_ARGS=("-o" "$CANVAS_FILE")
            [[ -n "$TITLE" ]] && CANVAS_ARGS+=("--title" "$TITLE")
            [[ -n "$AUTHORS" ]] && CANVAS_ARGS+=("--authors" "$AUTHORS")
            [[ -n "$YEAR" ]] && CANVAS_ARGS+=("--year" "$YEAR")

            if python "$SCRIPT_DIR/canvas.py" "${CANVAS_ARGS[@]}"; then
                echo -e "${GREEN}✓ Canvas created${NC}"
                SUCCESS_CANVAS=$((SUCCESS_CANVAS + 1))
                echo "   Canvas: $CANVAS_FILE"
            else
                echo -e "${RED}✗ Canvas creation failed${NC}"
            fi
        fi
        echo
    fi

    echo
done

# Summary
echo "📊 Batch Processing Summary"
echo "=========================="
echo "Total PDFs: ${#PDF_FILES[@]}"
echo "Successful extractions: $SUCCESS_EXTRACT"
if [[ "$GENERATE_PROMPTS" == true ]] || [[ "$EXTRACT_ONLY" == false ]]; then
    echo "Successful prompts: $SUCCESS_PROMPT"
fi
if [[ "$CREATE_CANVASES" == true ]]; then
    echo "Successful canvases: $SUCCESS_CANVAS"
fi
echo
echo "📁 Output structure:"
echo "   $OUTPUT_DIR/"
echo "   ├── markdown_output/     # Extracted markdown and images"
if [[ "$GENERATE_PROMPTS" == true ]] || [[ "$EXTRACT_ONLY" == false ]]; then
    echo "   ├── generation_prompts/ # Claude prompts for note generation"
fi
if [[ "$CREATE_CANVASES" == true ]]; then
    echo "   ├── canvas_templates/  # JSON canvas templates"
fi
echo "   └── structured_notes/    # (Future) Generated literature notes"
echo
echo "🚀 Next steps:"
if [[ "$EXTRACT_ONLY" == false ]] && [[ "$GENERATE_PROMPTS" == false ]]; then
    echo "1. Review extracted content in $EXTRACT_DIR"
    echo "2. Use 'phd-deepread generate' on individual directories"
    echo "3. Or run batch with --generate-prompts to create Claude prompts"
else
    echo "1. Review extracted content in $EXTRACT_DIR"
    if [[ "$GENERATE_PROMPTS" == true ]]; then
        echo "2. Use prompts in $PROMPT_DIR with Claude Code"
        echo "3. Save generated notes to $NOTE_DIR"
    fi
    if [[ "$CREATE_CANVASES" == true ]]; then
        echo "4. Edit canvas templates in $CANVAS_DIR"
    fi
fi
echo
echo "✅ Batch processing complete!"