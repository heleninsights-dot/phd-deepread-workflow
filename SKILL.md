---
name: phd-deepread
description: Process academic PDFs into structured Obsidian literature notes and 9-node critical-thinking canvases. Activate when the user shares a PDF (drag-in or path) and asks to read, summarize, analyze, or "deeply read" it — or when they say things like "phd-deepread read this paper", "make a literature note", "critique this paper", or "build a canvas for this paper".
tags: [pdf, academic, research, obsidian, literature-review]
allowed-tools: [Bash, Write, Read, Edit, Glob, Grep]
---

# PhD Deep Read Workflow

Turn a PDF into three artifacts the user can drop straight into Obsidian:

1. **Extracted Markdown** — full PDF text via PyMuPDF (fast path) with Tesseract OCR fallback for scanned pages.
2. **Structured literature note** — YAML frontmatter, Dataview callouts, wikilinks, summary, critique, action items. You write this from the extracted text using the `clauderules.md` template.
3. **9-node critical-thinking canvas** — Obsidian Canvas JSON with core argument, assumptions, evidence, alternatives, methodological critique, personal relevance, future directions, critical questions, hypothesis center.

## When to activate

The user shares an academic PDF — typically by dragging it into the chat or pasting a path — and asks for any of:

- "phd-deepread read this paper" / "deep read this" / "read this and make a note"
- "summarize this paper" / "give me a literature note"
- "critique this" / "build a critical-thinking canvas"
- "batch-process this folder of PDFs"

If they only want a quick summary (no Obsidian artifacts), this skill is overkill — answer directly instead.

## How to run it

You drive the `phd-deepread` CLI on the user's behalf. The user does not type these commands.

### Single paper (most common)

```bash
phd-deepread run /path/to/paper.pdf
```

This produces three things in `markdown_output/<paper_name>/`:
- `<paper>.md` — extracted text
- A prompt file in `structured_literature_notes/<paper>.md` — **this is a prompt, not a finished note**
- `<paper>.canvas` — blank 9-node template

**You then write the literature note yourself.** Read the prompt file, follow the instructions inside (it includes the full `clauderules.md` template), and overwrite the prompt file with the finished note. The prompt asks for YAML frontmatter, Dataview callouts, extensive wikilinks, and academic tone — follow that exactly.

After the note is written, populate the canvas from it:

```bash
phd-deepread canvas -o markdown_output/<paper>/<paper>.canvas \
  --from-note structured_literature_notes/<paper>.md --overwrite
```

This maps note sections to canvas nodes by regex. Some nodes (assumptions, alternative-explanations) are auto-populated from related sections; the rest pull directly from the note. The user can refine any node in Obsidian.

### Step by step (when the user wants control)

```bash
phd-deepread extract /path/to/paper.pdf            # PDF → markdown
phd-deepread generate markdown_output/<paper>/ -o notes/<paper>.md   # build prompt
phd-deepread canvas -o notes/<paper>.canvas --title "..." --authors "..." --year "..."
```

### Batch a folder

```bash
phd-deepread batch /path/to/folder -o batch_output/ --create-canvases
```

Then loop over each `<paper>_prompt.txt` and write the finished note next to it.

## Verifying output

```bash
phd-deepread verify markdown_output/<paper>/
```

Checks formatting, YAML frontmatter, callouts, wikilinks.

## Templates

- `scripts/templates/clauderules.md` — the literature-note template you must follow when writing the note. Loaded by `generate.py` via `importlib.resources`.
- `scripts/templates/critical-thinking.canvas` — base canvas layout used by `canvas.py`.

Do not edit these as part of normal use.

## Troubleshooting

- **"command not found: phd-deepread"** — the package isn't installed or PATH is wrong. Run `phd-deepread doctor` (if available) or fall back to `python3 -m pip install --user phd-deepread-workflow` and tell the user to open a new terminal.
- **"Tesseract not found"** — only matters for scanned (image-based) PDFs. Suggest `brew install tesseract` (macOS) or `sudo apt install tesseract-ocr` (Linux).
- **Template not found** — package install incomplete; suggest `pip install --upgrade phd-deepread-workflow`.

## Examples in this repo

- `examples/example-output.md` — what a finished literature note looks like.
- `examples/example-canvas.canvas` — what a populated canvas looks like.

Match those styles when writing your own.
