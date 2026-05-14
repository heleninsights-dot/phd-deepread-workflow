#!/usr/bin/env python3
"""
PhD Deep Read Workflow - JSON Canvas Creation Script
Generates critical-thinking JSON Canvas files with 9 interconnected nodes.

This script creates a structured canvas for deep critical analysis of academic papers,
based on the template from ValverdePhotobiomodulation2022-CriticalThinking.canvas.

Use --from-note to populate canvas nodes from a generated literature note via
best-effort regex section mapping.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime
import importlib.resources

def create_canvas_template(paper_title="", paper_authors="", paper_year=""):
    """Create a canvas template with 9 critical-thinking nodes."""

    # Base template with annotation prompts
    canvas = {
        "nodes": [
            {
                "id": "core-argument",
                "type": "text",
                "text": "# Core Argument\n\n**Primary Claim:** [The paper's central claim — one sentence]\n\n**Logical Chain:**\n1. [Premise / evidence 1]\n2. [Premise / evidence 2]\n3. [Premise / evidence 3]\n→ **Therefore:** [Conclusion]\n\n**Argument Type:** [Causal / mechanistic / correlational / descriptive]\n\n**Strongest Evidence:** [The single piece of evidence that carries the most weight, with numbers]",
                "x": -1320,
                "y": -960,
                "width": 700,
                "height": 410,
                "color": "2"
            },
            {
                "id": "assumptions",
                "type": "text",
                "text": "# Key Assumptions\n\n**Explicit Assumptions:**\n1. [Assumption the authors state — quote if possible]\n2. [Another stated assumption]\n\n**Implicit Assumptions:**\n1. [Hidden assumption needed for the argument to work]\n2. [Another unstated assumption]\n\n**Most Questionable:** [Which assumption, if wrong, would most damage the conclusions? Why?]",
                "x": -1320,
                "y": -400,
                "width": 700,
                "height": 600,
                "color": "3"
            },
            {
                "id": "evidence-assessment",
                "type": "text",
                "text": "# Evidence Assessment\n\n**Strongest Evidence:**\n• [Finding with statistical support]\n• [Finding with statistical support]\n\n**Weakest Evidence:**\n• [Finding and why it's weak]\n\n**Critical Gap:** [The most important missing evidence]\n\n**Replication:** [Are key findings replicated within the paper? Across other papers?]\n\n**Validity Concerns:** [Internal / external / construct / statistical conclusion — which are threatened?]",
                "x": -1360,
                "y": 350,
                "width": 700,
                "height": 600,
                "color": "4"
            },
            {
                "id": "alternative-explanations",
                "type": "text",
                "text": "# Alternative Explanations\n\n**Competing Hypotheses:**\n1. [Alternative explanation 1]\n2. [Alternative explanation 2]\n\n**Could Confounding Explain This?**\n[Most serious confound and whether the design controls for it]\n\n**Reverse Causation Risk:**\n[Could the effect run in the opposite direction?]\n\n**Plausibility vs. Authors' Claim:**\n[Are the alternatives MORE or LESS plausible? Why?]",
                "x": -360,
                "y": 50,
                "width": 800,
                "height": 600,
                "color": "5"
            },
            {
                "id": "methodological-critique",
                "type": "text",
                "text": "# Methodological Critique\n\n**Strongest Design Choice:**\n[Specific choice + why it strengthens the evidence]\n\n**Most Serious Limitation:**\n[Limitation + which validity it threatens: internal/external/construct/statistical conclusion]\n\n**Limitations NOT Discussed by Authors:**\n[At least one gap the authors don't acknowledge]\n\n**Statistical Concerns:**\n[Power, multiplicity, model assumptions, p-hacking risk]\n\n**Design Alternatives:**\n[What design would have been stronger, and why wasn't it used?]",
                "x": 640,
                "y": -950,
                "width": 700,
                "height": 500,
                "color": "6"
            },
            {
                "id": "personal-relevance",
                "type": "text",
                "text": "# Personal Relevance\n\n**Connections to My Research:**\n• [Specific link to your work — a shared mechanism, method, or question]\n• [Another connection]\n\n**What I Can Use Directly:**\n• [Method / protocol / finding you can apply now]\n\n**What This Changes for Me:**\n[Does this support, challenge, or complicate your existing understanding?]",
                "x": 720,
                "y": -200,
                "width": 700,
                "height": 500,
                "color": "7"
            },
            {
                "id": "future-directions",
                "type": "text",
                "text": "# Future Research Directions\n\n**Immediate (1-2 years):**\n1. [Specific follow-up study]\n2. [Specific follow-up study]\n\n**Medium-term (3-5 years):**\n1. [Research program direction]\n\n**Long-term Vision (5+ years):**\n1. [Field-level direction]\n\n**The Most Important Unanswered Question:**\n[One question + what study design would answer it]",
                "x": 640,
                "y": 400,
                "width": 700,
                "height": 500,
                "color": "8"
            },
            {
                "id": "critical-questions-enhanced",
                "type": "text",
                "text": "# Critical Questions\n\n**What Would Falsify the Hypothesis?**\n[Specific result that would prove it wrong]\n\n**Where Is the Argument Weakest?**\n[The step in the logical chain with least support]\n\n**What Are the Boundary Conditions?**\n[When / where / for whom does this NOT apply?]\n\n**What's the Minimum Evidence for Confidence?**\n[What would it take for you to believe this conclusion?]\n\n**Does This Challenge a Paradigm?**\n[Does it overturn, refine, or confirm existing understanding?]",
                "x": -860,
                "y": 1280,
                "width": 1640,
                "height": 500,
                "color": "9"
            },
            {
                "id": "hypothesis-center",
                "type": "text",
                "text": f"# Central Hypothesis Re-examined\n\n**{paper_title if paper_title else 'Paper Title'}**\n{'**' + paper_authors + ' (' + paper_year + ')**' if paper_authors and paper_year else ''}\n\n**Updated Understanding:** [Your synthesis after critically examining all angles]\n\n**Innovation:** [High/Medium/Low] — [Why?]\n**Evidence Strength:** [High/Medium/Low] — [Why?]\n**Practical Potential:** [High/Medium/Low] — [Why?]\n\n**Remaining Uncertainties:** [What you still don't know or fully trust]",
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
    First tries to load via importlib.resources from scripts.templates package.
    Falls back to filesystem path relative to script directory.
    """
    # Convert to string and normalize path separators
    template_str = str(template_arg)

    # Extract filename from potential path (e.g., "templates/critical-thinking.canvas" -> "critical-thinking.canvas")
    filename = os.path.basename(template_str)

    # Try to load via importlib.resources first (when package is installed)
    try:
        # Use importlib.resources to read file from scripts.templates package
        # Note: requires scripts.templates to be a proper package (has __init__.py)
        template_data = importlib.resources.files("scripts.templates").joinpath(filename).read_text(encoding='utf-8')
        return json.loads(template_data)
    except (ImportError, FileNotFoundError, AttributeError, json.JSONDecodeError) as e:
        # Fallback to filesystem path relative to script directory
        # This works when running from source or if resources aren't available
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(base_dir, template_str)

        path = Path(template_path)
        if not path.exists():
            raise RuntimeError(f"Canvas template not found: {template_path} (tried package resource '{filename}' and filesystem)")

        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as fs_e:
            raise RuntimeError(f"Failed to load template file {path}: {fs_e}")

def generate_citekey(paper_info):
    """Generate a citekey from paper information."""
    first_author = paper_info.get('first_author', 'Author').replace(' ', '')
    first_word = paper_info.get('title', 'Title').split()[0] if paper_info.get('title') else 'Paper'
    year = paper_info.get('year', 'Year')
    return f"{first_author}{first_word}{year}"

def populate_nodes_from_note(note_text, canvas):
    """Basic section-to-node mapping without an API call. Best-effort regex extraction."""
    import re

    section_map = {
        r"(?:Research Gap|Hypothesis|Central Hypothesis|Problem Context)(.*?)(?=\n## |\Z)": "core-argument",
        r"(?:Methodology|Evidence Base|Key Techniques|Study Characteristics)(.*?)(?=\n## |\Z)": "evidence-assessment",
        r"(?:Critical Analysis|Strengths|Limitations)(.*?)(?=\n## |\Z)": "methodological-critique",
        r"(?:Open Questions)(.*?)(?=\n## |\Z)": "critical-questions-enhanced",
        r"(?:Connections|Integration|Personal Relevance)(.*?)(?=\n## |\Z)": "personal-relevance",
        r"(?:Action Items|Next Steps)(.*?)(?=\n## |\Z)": "future-directions",
        r"(?:Summary|Conclusion|Key Takeaway|Final Assessment)(.*?)(?=\n## |\Z)": "hypothesis-center",
    }

    node_text = {node["id"]: node["text"] for node in canvas["nodes"]}

    for pattern, node_id in section_map.items():
        match = re.search(pattern, note_text, re.DOTALL | re.IGNORECASE)
        if match:
            extracted = match.group(0).strip()
            if len(extracted) > 50:
                # Truncate very long sections for canvas display
                if len(extracted) > 800:
                    extracted = extracted[:800] + "\n\n[...truncated for canvas — see full literature note]"
                node_text[node_id] = extracted

    # Derive assumptions and alternative-explanations from the populated nodes
    # assumptions: pull from core-argument's hypothesis and methodology critique
    if node_text.get("core-argument"):
        arg_text = node_text["core-argument"]
        # Extract hypothesis-related content as proxy for assumptions
        hypo_match = re.search(r"(?:Central Hypothesis|Hypothesis|Implicit:)(.*?)(?=\n###|\n##|\Z)", arg_text, re.DOTALL | re.IGNORECASE)
        if hypo_match and len(hypo_match.group(0)) > 30:
            node_text["assumptions"] = "# Assumptions (derived from hypothesis)\n\n**Central Hypothesis from Note:**\n" + hypo_match.group(0).strip()[:500]

    # alternative-explanations: derive from methodological critique — refine in Obsidian if needed
    if node_text.get("methodological-critique"):
        crit_text = node_text["methodological-critique"]
        alt_match = re.search(r"(?:Limitations|not discussed|threat to)(.*?)(?=\n###|\n##|\Z)", crit_text, re.DOTALL | re.IGNORECASE)
        if alt_match and len(alt_match.group(0)) > 30:
            node_text["alternative-explanations"] = "# Alternative Explanations (derived from critique)\n\n**From Limitations Analysis:**\n" + alt_match.group(0).strip()[:500]

    for node in canvas["nodes"]:
        if node["id"] in node_text:
            node["text"] = node_text[node["id"]]
    return canvas


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
    parser.add_argument("--from-note", dest="from_note", metavar="NOTE_PATH",
                       help="Path to a generated literature note (.md) — populate canvas nodes from it")

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

        # Populate nodes from literature note if provided
        if args.from_note:
            note_path = Path(args.from_note)
            if not note_path.exists():
                print(f"❌ Literature note not found: {note_path}", file=sys.stderr)
                return 1
            note_text = note_path.read_text(encoding='utf-8')
            print("📝 Populating canvas nodes from note (section mapping)...")
            canvas = populate_nodes_from_note(note_text, canvas)

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
        print("  2. Review and refine each node — the prompts inside guide your critical analysis")
        print("  3. Adjust positions, colors, and connections as needed")
        print("  4. Use the json-canvas skill for further editing")

        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())