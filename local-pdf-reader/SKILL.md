---
name: local-pdf-reader
description: Use when the user asks to read, extract, inspect, or summarize the contents of a local PDF file path, including full text, specific pages, highlighted text, and annotation-backed titles. This skill is especially useful on macOS when common PDF CLI tools or Python PDF libraries are unavailable, because it falls back to a bundled PDFKit-based script.
---

# Local PDF Reader

## Overview

This skill handles local PDF-reading tasks from an absolute file path.
It supports three common cases:

- Read the full text of a PDF
- Read one page or a page range
- Extract highlighted text or titles from PDF highlight annotations

Use the bundled script first when the environment lacks `pdftotext`, Python PDF packages, or OCR tools.

## Workflow

1. Confirm the file exists and note the page count:

```bash
file "/abs/path/to/file.pdf"
bash scripts/read_local_pdf.sh pages "/abs/path/to/file.pdf"
```

2. Choose the extraction mode:

- Full document text:

```bash
bash scripts/read_local_pdf.sh text "/abs/path/to/file.pdf"
```

- Specific page:

```bash
bash scripts/read_local_pdf.sh text "/abs/path/to/file.pdf" 12
```

- Page range:

```bash
bash scripts/read_local_pdf.sh text "/abs/path/to/file.pdf" 12 15
```

- Highlighted text:

```bash
bash scripts/read_local_pdf.sh highlights "/abs/path/to/file.pdf"
```

3. Post-process for the user's intent:

- If the user asked what is highlighted, report the extracted highlight text grouped by page.
- If the user asked for titles, keep only the title-like lines instead of dumping all text.
- If the user asked for a summary, read the relevant page text first, then summarize.

## Heuristics

- Prefer `highlights` when the user mentions "标黄", "highlight", "annotations", or asks which titles were highlighted.
- Prefer `text` when the user asks to read page content, extract a section, or summarize the PDF.
- If highlight extraction returns nothing, say that the PDF may not contain saved highlight annotations. Then fall back to page text extraction.
- The bundled script reads text-based PDFs. For scanned PDFs, you may need OCR; this skill does not bundle OCR.

## Output Discipline

- Keep page numbers in the result when multiple pages are involved.
- Do not dump the whole document unless the user asked for it.
- When titles are clearly identifiable, return just the titles first and mention that they were extracted from PDF highlights or page text.

## Bundled Script

The script compiles a temporary Objective-C helper against macOS `PDFKit` and supports:

- `pages`
- `text`
- `highlights`

Run it from the skill directory or reference it by absolute path.
