---
name: pdf-visual-audit
description: Use when Codex needs to repair or verify extracted Markdown/text from a local PDF by visually auditing rendered PDF pages, especially when equations, LaTeX, tables, page order, two-column text, headers/footers, or figure captions are scrambled by PDF text extraction. Use for tasks like fixing formulas in converted MD, reconstructing numbered equations from a paper PDF, comparing clean text against the PDF, or producing agent-readable reference files while preserving raw extraction audit text.
---

# PDF Visual Audit

## Purpose

Use this skill when text extraction is not enough. The core move is to render the PDF pages to images, inspect the page visually, then repair the clean Markdown against the rendered source of truth.

This complements text extraction skills. Use text extraction to find candidate locations, but trust rendered PDF pages for formulas, layout, tables, and two-column ordering.

## Workflow

1. Locate the source PDF and converted artifacts.

   Prefer explicit paths from the user. If a directory contains `reference.pdf`, `reference.full.md`, `pages/page-XX.md`, `chunks.jsonl`, or `reference.raw.txt`, treat the PDF as the visual source of truth and the Markdown as the editable artifact.

2. Render the relevant PDF pages.

   Use the bundled renderer on macOS:

   ```bash
   bash scripts/render_pdf_pages.sh /abs/path/file.pdf /tmp/pdf-pages 4
   ```

   The third argument is scale. Use `3` or `4` for formula reading. Add page bounds when only a range matters:

   ```bash
   bash scripts/render_pdf_pages.sh /abs/path/file.pdf /tmp/pdf-pages 4 4 8
   ```

3. Inspect rendered pages.

   Use `view_image` on full pages first. If formulas are small, crop with `sips` into temporary files and inspect those. Keep crops in `/tmp` or `/private/tmp`.

4. Reconstruct clean Markdown.

   Convert equations into block LaTeX:

   ```markdown
   $$
   ...
   \tag{19}
   $$
   ```

   Prefer the PDF's notation exactly: hats, tildes, bars, superscripts, subscripts, calligraphic force symbols, case definitions, sums, and integration bounds. Do not infer notation from broken text when the rendered PDF shows otherwise.

5. Preserve audit material.

   If page files contain both `## Clean Text` and `## Raw PDFKit Text`, edit only `Clean Text` unless the user explicitly asks to rewrite raw extraction. Raw blocks are useful evidence of extraction failure.

6. Synchronize derived artifacts.

   If `reference.full.md` is assembled from `pages/page-XX.md`, regenerate it from clean page text after page edits. If `chunks.jsonl` exists, rebuild it so retrieval does not keep old broken formula fragments.

7. Validate.

   Run targeted checks before finishing:

   ```bash
   rg -n "ZaccT|Zta|JCLIP|Coc k|Col k|πθold|σ2|µθ|^[ˆ˜¯˚]$" reference.full.md chunks.jsonl
   rg -n -F "\tag{" reference.full.md
   ```

   Also check math delimiters are balanced:

   ```bash
   python3 - <<'PY'
   from pathlib import Path
   for f in [Path("reference.full.md"), *Path("pages").glob("page-*.md")]:
       text = f.read_text()
       if f.name.startswith("page-"):
           text = text.split("## Clean Text", 1)[1].split("## Raw PDFKit Text", 1)[0]
       if text.count("$$") % 2:
           print("unbalanced $$", f, text.count("$$"))
   PY
   ```

## Formula Repair Heuristics

- Treat standalone `ˆ`, `˜`, `¯`, `˚`, `Z`, and `X` lines as extraction artifacts until verified visually.
- For numbered equations, count tags and compare against the PDF sequence. Missing or duplicated tags usually reveal a bad page splice.
- For two-column papers, check whether text blocks crossed columns. Reorder paragraphs according to the rendered page, not the extracted line order.
- For formulas split across pages, remove dangling half-sentences on the previous page and complete the sentence on the next page when the PDF shows a page break.
- For paper conversions, use `\mathrm{...}` for semantic superscripts like `tr`, `au`, `ch`, `wt`, `ob`, `in`, `out`, `CLIP`; use `\mathcal{...}` only when the PDF uses calligraphic symbols.
- Keep variables consistent across equations and explanatory text.

## Renderer Notes

The bundled script compiles a temporary Objective-C helper using macOS `CoreGraphics` and writes PNG pages. It applies a vertical flip by default because CoreGraphics bitmap coordinates otherwise commonly produce inverted PDF pages in command-line rendering.

If a page looks inverted after rendering, rerun with `--no-flip`:

```bash
bash scripts/render_pdf_pages.sh /abs/path/file.pdf /tmp/pdf-pages 4 1 1 --no-flip
```

If `pdftoppm`, `mutool`, or a reliable OCR/Mathpix tool is available, it can be used as an aid. Still verify against rendered pages before writing formulas into Markdown.
