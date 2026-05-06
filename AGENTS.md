# AGENTS.md — Install instructions for AI agents

This file tells an AI agent (e.g. Claude Code) how to install and verify the **phd-deepread** workflow on the user's machine. The user is non-technical and will trust you to run these steps end-to-end. Do not ask the user to type terminal commands themselves; execute them yourself and report results.

If anything in this file conflicts with the README, follow this file — the README is written for humans skimming, this is the executable spec.

---

## Goal

After install, all of the following must succeed:

1. The `phd-deepread` command runs from any directory.
2. `phd-deepread doctor` (or `phd-deepread setup`) reports core dependencies as OK.
3. The skill is discoverable to Claude Code at `~/.claude/skills/phd-deepread/SKILL.md`.

---

## Install path A — Claude Code skill (preferred)

Use this when the user is in Claude Code. It makes the skill load automatically in every future Claude Code session.

### Step 1. Clone the repo into the user's skills directory

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/heleninsights-dot/phd-deepread-workflow.git ~/.claude/skills/phd-deepread
```

If `~/.claude/skills/phd-deepread` already exists, do **not** delete it. Run `git -C ~/.claude/skills/phd-deepread pull --ff-only` instead and tell the user you updated the existing install.

### Step 2. Verify Python is available

```bash
python3 --version
```

Required: Python 3.10 or higher. If missing or older:
- macOS: suggest `brew install python@3.12` (do not run it without confirming).
- Other OSes: point the user to https://www.python.org/downloads/ and stop here.

### Step 3. Install the Python package (so the `phd-deepread` CLI is on PATH)

```bash
python3 -m pip install --user phd-deepread-workflow
```

If the user is in a virtual environment (`$VIRTUAL_ENV` is set), drop `--user`.

If `pip` complains about an externally-managed environment (PEP 668), retry with `--break-system-packages` only after confirming with the user, or create a venv at `~/.claude/skills/phd-deepread/.venv` and install into it.

### Step 4. Install Tesseract OCR (optional — only needed for scanned PDFs)

Ask the user: "Do you work with scanned PDFs (image-based, text not selectable)? [y/N]". Default no.

If yes:
- macOS: `brew install tesseract`
- Ubuntu/Debian: `sudo apt install -y tesseract-ocr`
- Windows: point to https://github.com/UB-Mannheim/tesseract/wiki and stop here.

If no, skip — the workflow degrades gracefully without it.

### Step 5. Verify the install

Run all three:

```bash
which phd-deepread
phd-deepread --help
ls ~/.claude/skills/phd-deepread/SKILL.md
```

All three must succeed. If `which phd-deepread` is empty, the user's shell PATH does not include the user-pip bin dir — add `export PATH="$HOME/.local/bin:$PATH"` to their shell rc (`~/.zshrc` on macOS default) and tell them to open a new terminal.

### Step 6. Tell the user it's ready

Say (verbatim is fine):

> Installed. In a new Claude Code session, drag a PDF into the chat and ask "process this paper with phd-deepread" — I'll do the rest.

---

## Install path B — Pip only (no Claude Code)

Use this when the user does not have Claude Code, or explicitly asks for the standalone CLI.

```bash
python3 -m pip install --user phd-deepread-workflow
phd-deepread --help
```

Optional Tesseract install: same as path A, step 4.

---

## What NOT to do

- Do not set `ENABLE_EFFICIENT_ATTENTION` — it was for the legacy Surya OCR backend and is no longer used.
- Do not edit the user's `.zshrc`/`.bashrc` without confirming first.
- Do not run `pip install` with `sudo`.
- Do not delete an existing `~/.claude/skills/phd-deepread/` directory — the user may have local edits.

---

## Verification command (use this if something looks wrong)

```bash
phd-deepread doctor
```

This reports Python version, PyMuPDF, Tesseract, and template paths. If `doctor` is not yet a subcommand on the installed version, fall back to `phd-deepread setup`.

---

## Repo URL

`https://github.com/heleninsights-dot/phd-deepread-workflow`
