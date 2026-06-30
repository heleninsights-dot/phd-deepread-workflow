# Final Reformat: Instructions for Claude Code

## Your Role

You are the **final polish pass** of the phd-deepread workflow. The text below was machine-extracted from a PDF (PyMuPDF + Tesseract OCR). It is faithful but ugly: paragraphs are broken mid-sentence, words are hyphenated across line breaks, tables are collapsed into loose text, and running headers / footers / page numbers are scattered through the body.

Your job is to turn that raw extraction into a clean, **Obsidian-ready** Markdown document a researcher would be happy to read -- without changing, summarizing, or inventing any of the author's content. This is **reformatting, not rewriting**. Preserve every sentence and number exactly; only fix the layout.

## What to fix

1. **Reflow paragraphs.** Join lines broken mid-sentence back into continuous paragraphs. A new paragraph starts only where the author intended one (a topic shift, a blank-line gap in the source, or a clear sentence-final break before a new idea). Do not merge distinct paragraphs together.

2. **Dehyphenate.** Repair words split across a line break with a trailing hyphen (`experi-\nment` -> `experiment`, `signifi-\ncant` -> `significant`). Keep genuine hyphens in compound terms (`well-being`, `T-cell`, `co-author`) and in numeric ranges (`10-15`).

3. **Rebuild tables from the raw extraction.** Where the source clearly contains tabular data flattened into loose rows of numbers or columns, reconstruct it as a proper Markdown table with a header row and aligned columns. Preserve every cell value verbatim. If a cell's placement is genuinely ambiguous, keep the row but add a trailing `<!-- check: alignment uncertain -->` comment rather than guessing silently.

4. **Strip page/header artifacts.** Remove running headers, running footers, standalone page numbers, journal/DOI watermark bars, "Downloaded from..." lines, and license boilerplate that the extractor interleaved into the body. Do NOT remove footnotes, figure/table captions, or any author content.

5. **Collapse back-matter into foldable callouts.** Move the long, reference-style tail of the document into **collapsed** Obsidian callouts (the trailing `-` collapses them by default) so the body stays readable:
   - References / Bibliography -> `> [!cite]- References`
   - Abbreviations / Glossary -> `> [!abstract]- Abbreviations`
   - Declarations (funding, conflicts of interest, ethics, author contributions, data availability) -> `> [!note]- Declarations`
   Keep each entry on its own line inside the callout (prefix continuation lines with `> `).

6. **Keep headings as headings.** Promote the paper's real section titles (Abstract, Introduction, Methods, Results, Discussion, Conclusion, ...) to Markdown `##` headings. Figure and table labels become **bold** lead-ins, not headings.

## Layout rules (match the Obsidian demo style)

- **No horizontal-rule dividers (`---`) between sections.** Let headings alone separate sections.
- Keep it **tight**: a single blank line before each heading, no decorative spacing, no trailing whitespace.
- **No emoji** on headings.
- Preserve inline math, symbols, and superscripts as written; do not "correct" the author's notation.
- Do NOT add wikilinks, YAML frontmatter, commentary, or a summary -- that is the structured literature note's job, not this pass.

## Output

Write the cleaned document to:

```
{output_path}
```

Output ONLY the reformatted Markdown -- no explanation before or after. Preserve the author's words exactly; you are improving the layout, nothing else.
