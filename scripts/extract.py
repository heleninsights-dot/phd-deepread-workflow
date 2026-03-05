#!/usr/bin/env python3
"""
PhD Deep Read Workflow - PDF Extraction Script
Custom Text-First decision tree using PyMuPDF with optional Tesseract OCR fallback.

This script implements a custom decision tree:
1. Pre-scan PDF with PyMuPDF to assess searchable text percentage
2. If 80%+ pages have searchable text (>100 chars), extract directly with PyMuPDF
3. For pages with insufficient text, use Tesseract OCR (if available)
4. Always extract images with PyMuPDF
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import tempfile
import shutil

# Try to import required libraries
try:
    import fitz  # PyMuPDF
    PDFTEXT_AVAILABLE = True
except ImportError:
    PDFTEXT_AVAILABLE = False
    print("⚠ PyMuPDF (fitz) not available. Install with: pip install PyMuPDF")

# Optional OCR with Tesseract
try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    # Check if tesseract command is available
    try:
        subprocess.run(["tesseract", "--version"], capture_output=True, check=True)
        TESSERACT_AVAILABLE = True
        print("✅ Tesseract command available (pytesseract not installed)")
    except:
        print("⚠ Tesseract OCR not available. Install with: brew install tesseract AND pip install pytesseract pillow")

# Constants
SEARCHABLE_TEXT_THRESHOLD = 100  # Minimum characters to consider page searchable
SEARCHABLE_PAGE_PERCENTAGE = 0.8  # 80% of pages must be searchable to use PyMuPDF for all

def check_dependencies():
    """Check if required dependencies are available."""
    if not PDFTEXT_AVAILABLE:
        print("❌ PyMuPDF (fitz) is required but not installed.")
        print("Install with: pip install PyMuPDF")
        return False

    print("✅ PyMuPDF available")
    if TESSERACT_AVAILABLE:
        print("✅ Tesseract OCR available (optional)")
    else:
        print("⚠ Tesseract OCR not available - OCR fallback disabled")

    return True

def assess_pdf_searchability(pdf_path: Path, threshold: int = SEARCHABLE_TEXT_THRESHOLD) -> Tuple[List[int], List[int]]:
    """
    Assess PDF searchability using PyMuPDF.

    Returns:
        Tuple of (searchable_page_indices, non_searchable_page_indices)
    """
    searchable_pages = []
    non_searchable_pages = []

    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        for page_num in range(total_pages):
            page = doc[page_num]
            text = page.get_text()

            # Check if page has sufficient searchable text
            if len(text.strip()) >= threshold:
                searchable_pages.append(page_num)
            else:
                non_searchable_pages.append(page_num)

            # Also check for images that might indicate complex layouts
            image_list = page.get_images()
            # If page has many images but little text, might need OCR
            # (This is a simple heuristic)

        doc.close()

        print(f"📊 PDF Assessment: {len(searchable_pages)}/{total_pages} pages searchable")
        print(f"   Searchable pages: {searchable_pages}")
        print(f"   Non-searchable pages: {non_searchable_pages}")

        return searchable_pages, non_searchable_pages

    except Exception as e:
        print(f"❌ Error assessing PDF: {e}")
        # If assessment fails, assume all pages need OCR
        return [], list(range(len(doc))) if 'doc' in locals() else []

def extract_with_pymupdf(pdf_path: Path, page_nums: List[int], output_dir: Path) -> Dict:
    """
    Extract text and images from specific pages using PyMuPDF.

    Returns:
        Dictionary with extraction metadata
    """
    metadata = {
        "pages": [],
        "text_extraction_method": "pdftext",
        "block_counts": []
    }

    try:
        doc = fitz.open(pdf_path)

        for page_num in page_nums:
            if page_num >= len(doc):
                continue

            page = doc[page_num]
            page_metadata = {
                "page_number": page_num,
                "text_extraction_method": "pdftext",
                "block_counts": {},
                "extracted_text": "",
                "image_count": 0
            }

            # Extract text
            text = page.get_text()
            page_metadata["extracted_text"] = text

            # Count characters, words, lines
            char_count = len(text)
            word_count = len(text.split())
            line_count = len(text.split('\n'))

            page_metadata["block_counts"] = {
                "characters": char_count,
                "words": word_count,
                "lines": line_count
            }

            # Extract images
            image_list = page.get_images()
            image_count = len(image_list)
            page_metadata["image_count"] = image_count

            # Save images
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n - pix.alpha < 4:  # CMYK or RGB
                        pix = fitz.Pixmap(fitz.csRGB, pix)

                    image_filename = f"_page_{page_num}_Picture_{img_index}.png"
                    image_path = output_dir / image_filename
                    pix.save(str(image_path))
                    pix = None

                    print(f"   Saved image: {image_filename}")
                except Exception as e:
                    print(f"   ⚠ Could not save image {img_index}: {e}")
                    if 'pix' in locals():
                        pix = None

            metadata["pages"].append(page_metadata)

        doc.close()

        print(f"✅ PyMuPDF extraction: {len(page_nums)} pages")
        return metadata

    except Exception as e:
        print(f"❌ Error extracting with PyMuPDF: {e}")
        return metadata

def extract_with_ocr(pdf_path: Path, page_nums: List[int], output_dir: Path, lang: str = "eng") -> Dict:
    """
    Extract text from specific pages using Tesseract OCR.

    Note: Requires tesseract-ocr installed and pytesseract Python package.
    """
    metadata = {
        "pages": [],
        "text_extraction_method": "tesseract",
        "block_counts": []
    }

    if not TESSERACT_AVAILABLE:
        print("❌ Tesseract OCR not available. Skipping OCR pages.")
        return metadata

    try:
        doc = fitz.open(pdf_path)

        for page_num in page_nums:
            if page_num >= len(doc):
                continue

            page = doc[page_num]
            page_metadata = {
                "page_number": page_num,
                "text_extraction_method": "tesseract",
                "block_counts": {},
                "extracted_text": "",
                "image_count": 0
            }

            # Convert page to high-resolution image for OCR
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
            img_data = pix.tobytes("png")

            # Save temporary image
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp.write(img_data)
                tmp_path = tmp.name

            try:
                # Use pytesseract if available
                if 'pytesseract' in sys.modules:
                    from PIL import Image
                    img = Image.open(tmp_path)
                    text = pytesseract.image_to_string(img, lang=lang)
                else:
                    # Use tesseract command line
                    txt_path = tmp_path + ".txt"
                    subprocess.run(["tesseract", tmp_path, txt_path[:-4], "-l", lang],
                                 capture_output=True, check=True)
                    with open(txt_path, "r") as f:
                        text = f.read()
                    os.remove(txt_path)

                page_metadata["extracted_text"] = text
                page_metadata["block_counts"] = {
                    "characters": len(text),
                    "words": len(text.split()),
                    "lines": len(text.split('\n'))
                }

                print(f"   Page {page_num}: {len(text)} characters via OCR")

            except Exception as e:
                print(f"❌ OCR failed for page {page_num}: {e}")
                page_metadata["extracted_text"] = ""
                page_metadata["block_counts"] = {"error": str(e)}

            finally:
                # Clean up temporary file
                try:
                    os.remove(tmp_path)
                except:
                    pass

            # Extract images from page (even for OCR pages)
            image_list = page.get_images()
            page_metadata["image_count"] = len(image_list)

            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n - pix.alpha < 4:
                        pix = fitz.Pixmap(fitz.csRGB, pix)

                    image_filename = f"_page_{page_num}_Picture_{img_index}.png"
                    image_path = output_dir / image_filename
                    pix.save(str(image_path))
                    pix = None
                except Exception as e:
                    print(f"   ⚠ Could not save image {img_index}: {e}")
                    if 'pix' in locals():
                        pix = None

            metadata["pages"].append(page_metadata)

        doc.close()

        print(f"✅ Tesseract OCR extraction: {len(page_nums)} pages")
        return metadata

    except Exception as e:
        print(f"❌ Error in OCR extraction: {e}")
        return metadata

def combine_extractions(pdf_path: Path, pymupdf_metadata: Dict, ocr_metadata: Dict,
                       output_dir: Path, total_pages: int) -> Dict:
    """
    Combine extractions from both methods and create final output.
    """
    # Create combined metadata
    combined_metadata = {
        "pdf_filename": pdf_path.name,
        "total_pages": total_pages,
        "pages": [],
        "extraction_summary": {
            "pdftext_pages": len(pymupdf_metadata.get("pages", [])),
            "ocr_pages": len(ocr_metadata.get("pages", [])),
            "total_extracted": 0
        }
    }

    # Combine page metadata in order
    all_pages = []

    # Add PyMuPDF pages
    for page_meta in pymupdf_metadata.get("pages", []):
        all_pages.append({
            "page_id": page_meta["page_number"],
            "text_extraction_method": "pdftext",
            "block_counts": page_meta.get("block_counts", {}),
            "extracted_text": page_meta.get("extracted_text", ""),
            "image_count": page_meta.get("image_count", 0)
        })

    # Add OCR pages
    for page_meta in ocr_metadata.get("pages", []):
        all_pages.append({
            "page_id": page_meta["page_number"],
            "text_extraction_method": "tesseract",
            "block_counts": page_meta.get("block_counts", {}),
            "extracted_text": page_meta.get("extracted_text", ""),
            "image_count": page_meta.get("image_count", 0)
        })

    # Sort by page number
    all_pages.sort(key=lambda x: x["page_id"])

    # Create markdown file
    markdown_content = f"# {pdf_path.stem}\n\n"
    markdown_content += f"Extracted with PhD Deep Read Workflow (Text-First decision tree)\n\n"

    for page in all_pages:
        page_num = page["page_id"]
        method = page["text_extraction_method"]

        markdown_content += f"--- PAGE {page_num + 1} ---\n"
        markdown_content += f"Extraction method: {method}\n\n"

        text = page["extracted_text"]
        if text.strip():
            markdown_content += text
        else:
            markdown_content += f"[No text extracted from page {page_num + 1}]\n"

        markdown_content += "\n\n"

    # Save markdown file
    markdown_path = output_dir / f"{pdf_path.stem}.md"
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    # Save metadata
    combined_metadata["pages"] = all_pages
    combined_metadata["extraction_summary"]["total_extracted"] = len(all_pages)

    metadata_path = output_dir / f"{pdf_path.stem}_meta.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(combined_metadata, f, indent=2)

    print(f"📄 Created markdown file: {markdown_path}")
    print(f"📊 Created metadata file: {metadata_path}")

    return combined_metadata

def main():
    parser = argparse.ArgumentParser(
        description="Extract text from PDFs using Text-First decision tree (PyMuPDF + optional Tesseract OCR)"
    )
    parser.add_argument("pdf_path", help="Path to PDF file")
    parser.add_argument("-o", "--output_dir", default="markdown_output",
                       help="Output directory (default: markdown_output)")
    parser.add_argument("-p", "--page_range",
                       help="Page range (e.g., '0,5' for pages 0-5). If not specified, process all pages.")
    parser.add_argument("--lang", default="eng",
                       help="Language for OCR (default: eng)")
    parser.add_argument("--threshold", type=int, default=SEARCHABLE_TEXT_THRESHOLD,
                       help=f"Minimum characters to consider page searchable (default: {SEARCHABLE_TEXT_THRESHOLD})")
    parser.add_argument("--percentage", type=float, default=SEARCHABLE_PAGE_PERCENTAGE,
                       help=f"Percentage of pages that must be searchable to use PyMuPDF for all (default: {SEARCHABLE_PAGE_PERCENTAGE})")
    parser.add_argument("--force-ocr", action="store_true",
                       help="Force OCR for all pages (skip Text-First decision tree)")
    parser.add_argument("--force-text", action="store_true",
                       help="Force text extraction for all pages (skip OCR)")
    parser.add_argument("--no-ocr", action="store_true",
                       help="Disable OCR fallback (only use PyMuPDF)")

    args = parser.parse_args()

    # Check dependencies
    if not check_dependencies():
        return 1

    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists() or pdf_path.suffix.lower() != ".pdf":
        print(f"❌ Invalid PDF file: {pdf_path}")
        return 1

    # Create output directory
    output_dir = Path(args.output_dir) / pdf_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎓 PhD Deep Read Workflow - Text-First Extraction")
    print(f"=================================================")
    print(f"📄 PDF: {pdf_path.name}")
    print(f"📂 Output: {output_dir}")
    print(f"🌍 Language: {args.lang}")
    print()

    # Determine page range
    page_nums = []
    total_pages = 0

    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        doc.close()

        if args.page_range:
            try:
                start_str, end_str = args.page_range.split(",")
                start = int(start_str)
                end = int(end_str)
                page_nums = list(range(start, end + 1))
            except ValueError:
                print(f"❌ Invalid page range format: {args.page_range}")
                print("Use format: start,end (e.g., '0,5' for pages 0-5)")
                return 1
        else:
            page_nums = list(range(total_pages))

    except Exception as e:
        print(f"❌ Error opening PDF: {e}")
        return 1

    print(f"📊 Processing {len(page_nums)} pages (of {total_pages} total)")

    # Decision tree logic
    if args.force_ocr:
        print("⚙️ Mode: Force OCR (all pages use Tesseract)")
        searchable_pages = []
        ocr_pages = page_nums

    elif args.force_text:
        print("⚙️ Mode: Force Text Extraction (all pages use PyMuPDF)")
        searchable_pages = page_nums
        ocr_pages = []

    elif args.no_ocr:
        print("⚙️ Mode: Text extraction only (OCR disabled)")
        searchable_pages = page_nums
        ocr_pages = []

    else:
        print("⚙️ Mode: Text-First Decision Tree")

        # Assess PDF searchability
        searchable_pages, ocr_pages = assess_pdf_searchability(pdf_path, threshold=args.threshold)

        # Filter by page range
        searchable_pages = [p for p in searchable_pages if p in page_nums]
        ocr_pages = [p for p in ocr_pages if p in page_nums]

        # If most pages are searchable, use PyMuPDF for all
        searchable_ratio = len(searchable_pages) / len(page_nums) if page_nums else 0

        if searchable_ratio >= args.percentage:
            print(f"✅ {searchable_ratio:.1%} pages searchable - Using PyMuPDF for all pages")
            searchable_pages = page_nums
            ocr_pages = []
        else:
            print(f"📊 Searchable pages: {len(searchable_pages)}")
            print(f"📊 OCR pages: {len(ocr_pages)}")

    # Extract with PyMuPDF
    pymupdf_metadata = {"pages": []}
    if searchable_pages:
        pymupdf_metadata = extract_with_pymupdf(pdf_path, searchable_pages, output_dir)

    # Extract with OCR (if needed and available)
    ocr_metadata = {"pages": []}
    if ocr_pages and TESSERACT_AVAILABLE and not args.no_ocr:
        ocr_metadata = extract_with_ocr(pdf_path, ocr_pages, output_dir, args.lang)
    elif ocr_pages and not TESSERACT_AVAILABLE:
        print(f"⚠ {len(ocr_pages)} pages need OCR but Tesseract not available.")
        print("   Install: brew install tesseract AND pip install pytesseract pillow")
        # Add placeholder metadata for OCR pages
        for page_num in ocr_pages:
            ocr_metadata["pages"].append({
                "page_number": page_num,
                "text_extraction_method": "none",
                "block_counts": {"error": "OCR not available"},
                "extracted_text": "",
                "image_count": 0
            })

    # Combine results
    combined_metadata = combine_extractions(pdf_path, pymupdf_metadata, ocr_metadata,
                                           output_dir, total_pages)

    # Print summary
    print("\n📊 Extraction Summary")
    print("===================")
    print(f"Total pages processed: {len(page_nums)}")
    print(f"PyMuPDF (fast text): {len(searchable_pages)} pages")
    print(f"OCR (complex): {len(ocr_pages)} pages")

    if ocr_pages and not TESSERACT_AVAILABLE:
        print(f"⚠ OCR pages were not processed (Tesseract not installed)")

    # Calculate character counts
    total_chars = 0
    for page in combined_metadata.get("pages", []):
        text = page.get("extracted_text", "")
        total_chars += len(text)

    print(f"Total characters extracted: {total_chars:,}")

    if ocr_pages and TESSERACT_AVAILABLE:
        print("\n💡 Note: OCR pages may have lower accuracy than direct text extraction.")
        print("   Review OCR pages carefully, especially for tables and complex layouts.")

    print(f"\n✅ Extraction complete!")
    print(f"📁 Output directory: {output_dir}")

    return 0

if __name__ == "__main__":
    sys.exit(main())