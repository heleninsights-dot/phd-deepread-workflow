#!/usr/bin/env python3
"""
PhD Deep Read Workflow - JSON Canvas Creation Script
Generates critical-thinking JSON Canvas files with 9 interconnected nodes.

This script creates a structured canvas for deep critical analysis of academic papers,
based on the template from ValverdePhotobiomodulation2022-CriticalThinking.canvas.
"""

import argparse
import json
import sys
import os
from pathlib import Path
from datetime import datetime
import importlib.resources

def create_canvas_template(paper_title="", paper_authors="", paper_year=""):
    """Create a canvas template with 9 critical-thinking nodes."""

    # Base template with placeholder content
    canvas = {
        "nodes": [
            {
                "id": "core-argument",
                "type": "text",
                "text": "# Core Argument Structure\n\n**Primary Claim:** [State the paper's central claim]\n\n**Logical Chain:**\n1. [First premise or evidence]\n2. [Second premise or evidence]\n3. [Third premise or evidence]\n4. **Therefore:** [Conclusion]\n\n**Argument Type:** [e.g., Hypothetical synthesis, causal inference, mechanistic explanation]",
                "x": -1320,
                "y": -960,
                "width": 700,
                "height": 410,
                "color": "2"
            },
            {
                "id": "assumptions",
                "type": "text",
                "text": "# Key Assumptions\n\n**Explicit Assumptions:**\n1. [Assumption 1]\n2. [Assumption 2]\n3. [Assumption 3]\n\n**Implicit Assumptions:**\n1. [Hidden assumption 1]\n2. [Hidden assumption 2]\n3. [Hidden assumption 3]\n\n**Questionable Assumptions:**\n1. [Potentially problematic assumption 1]\n2. [Potentially problematic assumption 2]\n3. [Potentially problematic assumption 3]",
                "x": -1320,
                "y": -400,
                "width": 700,
                "height": 600,
                "color": "3"
            },
            {
                "id": "evidence-assessment",
                "type": "text",
                "text": "# Evidence Strength Assessment\n\n**Strongest Evidence:**\n• [Evidence 1]\n• [Evidence 2]\n• [Evidence 3]\n\n**Moderate Evidence:**\n• [Evidence 4]\n• [Evidence 5]\n• [Evidence 6]\n\n**Weakest Evidence:**\n• [Evidence 7]\n• [Evidence 8]\n• [Evidence 9]\n\n**Critical Gap:** [The most important missing evidence]",
                "x": -1360,
                "y": 350,
                "width": 700,
                "height": 600,
                "color": "4"
            },
            {
                "id": "alternative-explanations",
                "type": "text",
                "text": "# Alternative Explanations & Pathways\n\n**Independent Effects Model:**\n[Describe how observed effects might be independent rather than connected]\n\n**Common Mechanism Model:**\n[Describe alternative underlying mechanisms]\n\n**Placebo/Non-specific Effects:**\n[Describe potential non-specific effects]\n\n**Confounding Factors:**\n• [Confounding factor 1]\n• [Confounding factor 2]\n• [Confounding factor 3]\n\n**Competing Hypotheses:**\n• [Alternative hypothesis 1]\n• [Alternative hypothesis 2]\n• [Alternative hypothesis 3]",
                "x": -360,
                "y": 50,
                "width": 800,
                "height": 600,
                "color": "5"
            },
            {
                "id": "methodological-critique",
                "type": "text",
                "text": "# Methodological Limitations\n\n**Study Design Issues:**\n• [Design issue 1]\n• [Design issue 2]\n• [Design issue 3]\n\n**Model/System Concerns:**\n• [Model limitation 1]\n• [Model limitation 2]\n• [Model limitation 3]\n\n**Translation Challenges:**\n• [Translation challenge 1]\n• [Translation challenge 2]\n• [Translation challenge 3]\n\n**Measurement Issues:**\n• [Measurement problem 1]\n• [Measurement problem 2]\n• [Measurement problem 3]",
                "x": 640,
                "y": -950,
                "width": 700,
                "height": 500,
                "color": "6"
            },
            {
                "id": "personal-relevance",
                "type": "text",
                "text": "# Personal Relevance & Connections\n\n**Research Interests Alignment:**\n• [Connection to interest 1]\n• [Connection to interest 2]\n• [Connection to interest 3]\n\n**Connections to My Work:**\n• [[Related concept 1]]\n• [[Related concept 2]]\n• [[Related concept 3]]\n\n**Critical Thinking Development:**\n• [What this paper teaches about critical thinking]\n• [Methodological lessons]\n• [Conceptual insights]\n\n**Learning Points:**\n• [Key takeaway 1]\n• [Key takeaway 2]\n• [Key takeaway 3]",
                "x": 720,
                "y": -200,
                "width": 700,
                "height": 500,
                "color": "7"
            },
            {
                "id": "future-directions",
                "type": "text",
                "text": "# Future Research Directions\n\n**Immediate Next Steps (1-2 years):**\n1. [Step 1]\n2. [Step 2]\n3. [Step 3]\n\n**Medium-term Goals (3-5 years):**\n1. [Goal 1]\n2. [Goal 2]\n3. [Goal 3]\n\n**Long-term Vision (5+ years):**\n1. [Vision 1]\n2. [Vision 2]\n3. [Vision 3]\n\n**High-Impact Studies Needed:**\n• [Study type 1]\n• [Study type 2]\n• [Study type 3]",
                "x": 640,
                "y": 400,
                "width": 700,
                "height": 500,
                "color": "8"
            },
            {
                "id": "critical-questions-enhanced",
                "type": "text",
                "text": "# Enhanced Critical Questions\n\n**For Hypothesis Testing:**\n1. What would falsify the hypothesis?\n2. Are there boundary conditions?\n3. What's the minimal evidence needed for confidence?\n\n**For Mechanism Elucidation:**\n1. Which mechanisms are most critical?\n2. Does timing/sequence matter?\n3. Are there synergistic/antagonistic effects?\n\n**For Clinical/Applied Implementation:**\n1. Cost-effectiveness compared to alternatives?\n2. Practical implementation barriers?\n3. How to measure outcomes effectively?\n\n**For Scientific Field:**\n1. Does this challenge current paradigms?\n2. What similar approaches could be explored?\n3. How to balance basic vs. translational research?",
                "x": -860,
                "y": 1280,
                "width": 1640,
                "height": 500,
                "color": "9"
            },
            {
                "id": "hypothesis-center",
                "type": "text",
                "text": f"# Central Hypothesis Re-examined\n\n**{paper_title if paper_title else 'Paper Title'}**\n{'**' + paper_authors + ' (' + paper_year + ')**' if paper_authors and paper_year else ''}\n\n**Innovation Score:** [High/Medium/Low]\n• [Reason 1]\n• [Reason 2]\n• [Reason 3]\n\n**Plausibility Score:** [High/Medium/Low]\n• [Reason 1]\n• [Reason 2]\n• [Reason 3]\n\n**Evidence Score:** [High/Medium/Low]\n• [Reason 1]\n• [Reason 2]\n• [Reason 3]",
                "fontSize": 16,
                "x": -300,
                "y": -760,
                "width": 700,
                "height": 430,
                "color": "1"
            }
        ],
        "edges": [
            {"id": "edge1", "fromNode": "core-argument", "fromSide": "right", "toNode": "hypothesis-center", "toSide": "left"},
            {"id": "edge2", "fromNode": "assumptions", "fromSide": "right", "toNode": "hypothesis-center", "toSide": "left"},
            {"id": "edge3", "fromNode": "evidence-assessment", "fromSide": "right", "toNode": "hypothesis-center", "toSide": "left"},
            {"id": "edge4", "fromNode": "hypothesis-center", "fromSide": "right", "toNode": "alternative-explanations", "toSide": "left"},
            {"id": "edge5", "fromNode": "hypothesis-center", "fromSide": "right", "toNode": "methodological-critique", "toSide": "left"},
            {"id": "edge6", "fromNode": "hypothesis-center", "fromSide": "right", "toNode": "personal-relevance", "toSide": "left"},
            {"id": "edge7", "fromNode": "hypothesis-center", "fromSide": "bottom", "toNode": "future-directions", "toSide": "top"},
            {"id": "edge8", "fromNode": "core-argument", "fromSide": "bottom", "toNode": "critical-questions-enhanced", "toSide": "top"},
            {"id": "edge9", "fromNode": "assumptions", "fromSide": "bottom", "toNode": "critical-questions-enhanced", "toSide": "top"},
            {"id": "edge10", "fromNode": "evidence-assessment", "fromSide": "bottom", "toNode": "critical-questions-enhanced", "toSide": "top"},
            {"id": "edge11", "fromNode": "alternative-explanations", "fromSide": "bottom", "toNode": "critical-questions-enhanced", "toSide": "top"},
            {"id": "edge12", "fromNode": "methodological-critique", "fromSide": "bottom", "toNode": "critical-questions-enhanced", "toSide": "top"},
            {"id": "edge13", "fromNode": "personal-relevance", "fromSide": "bottom", "toNode": "critical-questions-enhanced", "toSide": "top"},
            {"id": "edge14", "fromNode": "future-directions", "fromSide": "bottom", "toNode": "critical-questions-enhanced", "toSide": "top"},
            {"id": "edge15", "fromNode": "core-argument", "fromSide": "right", "toNode": "evidence-assessment", "toSide": "left"},
            {"id": "edge16", "fromNode": "core-argument", "fromSide": "right", "toNode": "assumptions", "toSide": "left"}
        ]
    }

    return canvas

def load_existing_template(template_arg):
    """Load an existing canvas template file.

    template_arg can be a string path or Path object.
    Uses absolute path logic relative to this script's directory.
    """
    # Get the directory where THIS script is sitting
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Look inside its own sub-folder for the template
    template_path = os.path.join(base_dir, str(template_arg))

    # Convert to Path for convenience
    path = Path(template_path)
    if not path.exists():
        raise RuntimeError(f"Canvas template not found: {template_path}")

    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load template file {path}: {e}")

def generate_citekey(paper_info):
    """Generate a citekey from paper information."""
    first_author = paper_info.get('first_author', 'Author').replace(' ', '')
    first_word = paper_info.get('title', 'Title').split()[0] if paper_info.get('title') else 'Paper'
    year = paper_info.get('year', 'Year')
    return f"{first_author}{first_word}{year}"

def main():
    parser = argparse.ArgumentParser(
        description="Generate JSON Canvas files for critical thinking analysis of academic papers"
    )
    parser.add_argument("-o", "--output", required=True,
                       help="Output canvas file path (should end with .canvas)")
    parser.add_argument("-t", "--template", help="Existing canvas template to use (optional)")
    parser.add_argument("--title", help="Paper title")
    parser.add_argument("--authors", help="Paper authors (comma-separated)")
    parser.add_argument("--year", help="Publication year")
    parser.add_argument("--citekey", help="Citekey for the paper (auto-generated if not provided)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing file")

    args = parser.parse_args()

    output_path = Path(args.output)

    # Check if file exists
    if output_path.exists() and not args.overwrite:
        print(f"❌ File already exists: {output_path}")
        print("   Use --overwrite to replace it.")
        return 1

    try:
        # Create canvas
        if args.template:
            canvas = load_existing_template(args.template)
            print(f"📋 Loaded template: {args.template}")
        else:
            canvas = create_canvas_template(args.title, args.authors, args.year)
            print("📋 Created new canvas template with 9 critical-thinking nodes")

        # Update hypothesis-center node with paper info if provided
        if args.title or args.authors or args.year:
            for node in canvas["nodes"]:
                if node["id"] == "hypothesis-center":
                    # Update the text with actual paper info
                    title = args.title or "Paper Title"
                    authors_year = ""
                    if args.authors and args.year:
                        authors_year = f"**{args.authors} ({args.year})**"

                    # Keep the rest of the template
                    node["text"] = f"# Central Hypothesis Re-examined\n\n**{title}**\n{authors_year}\n\n**Innovation Score:** [High/Medium/Low]\n• [Reason 1]\n• [Reason 2]\n• [Reason 3]\n\n**Plausibility Score:** [High/Medium/Low]\n• [Reason 1]\n• [Reason 2]\n• [Reason 3]\n\n**Evidence Score:** [High/Medium/Low]\n• [Reason 1]\n• [Reason 2]\n• [Reason 3]"
                    break

        # Write canvas file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(canvas, f, indent='\t', ensure_ascii=False)

        # Generate citekey suggestion
        paper_info = {
            "first_author": args.authors.split(',')[0].strip() if args.authors else "Author",
            "title": args.title,
            "year": args.year
        }
        citekey = args.citekey or generate_citekey(paper_info)

        print(f"✅ Canvas created: {output_path}")
        print(f"📝 Suggested filename: {citekey}-CriticalThinking.canvas")
        print()
        print("🎯 Nodes included:")
        print("  1. core-argument        6. personal-relevance")
        print("  2. assumptions          7. future-directions")
        print("  3. evidence-assessment  8. critical-questions-enhanced")
        print("  4. alternative-explanations  9. hypothesis-center")
        print("  5. methodological-critique")
        print()
        print("🔗 16 edges connecting nodes for structured critical thinking")
        print()
        print("📋 Next steps:")
        print("  1. Open the canvas in Obsidian (with Canvas plugin)")
        print("  2. Fill in each node with your critical analysis")
        print("  3. Adjust positions, colors, and connections as needed")
        print("  4. Use the json-canvas skill for further editing")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())