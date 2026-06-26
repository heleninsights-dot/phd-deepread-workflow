# AGENTS.md — Install instructions for AI agents

This file tells an AI coding agent (e.g. **Claude Code** or **Codex**) how to install and verify the **phd-deepread** workflow on the user's machine. The user is non-technical and will trust you to run these steps end-to-end. Do not ask the user to type terminal commands themselves; execute them yourself and report results.

If anything in this file conflicts with the README, follow this file — the README is written for humans skimming, this is the executable spec.

### Detect which agent you are (paths differ)

This workflow installs as a skill, and each agent keeps skills in a different directory. Determine yours first and use it everywhere below as `<SKILLS_DIR>`:

| Agent | `<SKILLS_DIR>` |
|---|---|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.codex/skills/` |

So the installed skill lives at `<SKILLS_DIR>phd-deepread/`. If you can't tell which agent you are, check which directory exists.

---

## Prerequisites — confirm before installing

Before any install, confirm the user has both:

1. **A skill-capable AI coding agent** — this workflow runs inside Claude Code or Codex. If the user has neither, point them to claude.ai/code (Claude Code) or the Codex CLI and stop here.
2. **Obsidian** — the final output is a JSON canvas file that only renders in Obsidian. Without Obsidian, the user cannot visualize the paper. Point them to obsidian.md.

If the user only wants AI help reading a PDF, they don't need this tool — just drag the PDF into any AI chat and ask questions directly. This workflow is for people who want structured literature notes and a critical-thinking canvas in Obsidian.

---

## Goal

After install, all of the following must succeed:

1. The `phd-deepread` command runs from any directory.
2. `phd-deepread doctor` reports core dependencies as OK.
3. The skill is available in your agent (Claude Code or Codex), installed at `<SKILLS_DIR>phd-deepread/`.

The end-to-end value: extract a PDF → Claude generates a structured literature note → the user opens a 9-node critical-thinking canvas in Obsidian to visualize the paper.

---

## Install in 30 seconds

Paste this into Claude Code **or** Codex and it handles everything:

```
Install this skill for me: https://github.com/heleninsights-dot/phd-deepread-workflow
```

The agent clones the repo, finds SKILL.md, and installs the skill into its own skills directory (`<SKILLS_DIR>phd-deepread/`). If the repo is already installed, it will detect it and update instead. Restart the agent afterward if it asks you to, so the new skill is picked up.

Once the skill is installed, continue with the steps below.

### Step 1. Verify Python is available

```bash
python3 --version
```

Required: Python 3.10 or higher. If missing or older:
- macOS: suggest `brew install python@3.12` (do not run it without confirming).
- Other OSes: point the user to https://www.python.org/downloads/ and stop here.

### Step 2. Install the Python package (so the `phd-deepread` CLI is on PATH)

```bash
python3 -m pip install --user phd-deepread-workflow
```

If the user is in a virtual environment (`$VIRTUAL_ENV` is set), drop `--user`.

If `pip` complains about an externally-managed environment (PEP 668), retry with `--break-system-packages` only after confirming with the user, or create a venv at `<SKILLS_DIR>phd-deepread/.venv` and install into it.

### Step 3. Install Tesseract OCR (optional — only needed for scanned PDFs)

Ask the user: "Do you work with scanned PDFs (image-based, text not selectable)? [y/N]". Default no.

If yes:
- macOS: `brew install tesseract`
- Ubuntu/Debian: `sudo apt install -y tesseract-ocr`
- Windows: point to https://github.com/UB-Mannheim/tesseract/wiki and stop here.

If no, skip — the workflow degrades gracefully without it.

### Step 4. Verify the install

Run all three:

```bash
which phd-deepread
phd-deepread --help
ls <SKILLS_DIR>phd-deepread/SKILL.md   # ~/.claude/skills/... or ~/.codex/skills/...
```

All three must succeed. If `which phd-deepread` is empty, the user's shell PATH does not include the user-pip bin dir — add `export PATH="$HOME/.local/bin:$PATH"` to their shell rc (`~/.zshrc` on macOS default) and tell them to open a new terminal.

### Step 5. Tell the user it's ready

Say (verbatim is fine):

> Installed. In a new session (Claude Code or Codex), drag a PDF into the chat and ask "phd-deepread read this paper" — I'll do the rest.

---

## What NOT to do

- Do not set `ENABLE_EFFICIENT_ATTENTION` — it was for the legacy Surya OCR backend and is no longer used.
- Do not edit the user's `.zshrc`/`.bashrc` without confirming first.
- Do not run `pip install` with `sudo`.
- Do not delete an existing `<SKILLS_DIR>phd-deepread/` directory (`~/.claude/skills/...` or `~/.codex/skills/...`) — the user may have local edits.

---

## Verification command (use this if something looks wrong)

```bash
phd-deepread doctor
```

This reports Python version, PyMuPDF, Tesseract, and template paths. If `doctor` is not yet a subcommand on the installed version, fall back to `phd-deepread setup`.

---

## Repo URL

`https://github.com/heleninsights-dot/phd-deepread-workflow`
