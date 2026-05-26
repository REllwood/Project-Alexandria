# Reading the different source types

`.raw/` is immutable. Copy the source in first, then read it. Compute nothing by hand that the manifest already hashes.

**Easiest path:** `python3 "<vault>/.kb/bin/kb_extract.py" "<file>"` extracts text from `.docx` (via `textutil`), `.pptx`, `.xlsx`, `.txt`/`.csv` using only the standard library — no pandoc needed. For PDFs, use the Read tool (it reads PDFs directly). The per-format notes below are detail / fallback.

## PDF
Use the Read tool directly on the `.pdf` — it extracts text (and reads scanned pages). For PDFs over ~10 pages, read in page ranges (`pages: "1-10"`, then `"11-20"`). Capture: title, authors, dates, key sections, figures/tables worth noting, and any People/orgs.

## Word / `.docx`, `.doc`
Convert to text first:
- macOS: `textutil -convert txt -stdout "file.docx"`
- cross-platform: `pandoc "file.docx" -t markdown`
Then read the output. (If the `docx` skill is available, it can extract structure, tracked changes, and comments.)

## PowerPoint / `.pptx`
`pandoc` or the `pptx` skill to pull slide text + speaker notes. Summarize per-section, not per-slide.

## Transcripts `.vtt` / `.srt`
Strip timestamps and cue numbers; collapse into speaker-attributed prose. Treat as a **meeting** if it's a call recording: extract attendees, decisions, action items.

## Web pages / URLs
Fetch readable content (WebFetch, or the `defuddle` skill if present). Save the cleaned article as `.raw/<slug>.md` with the URL in frontmatter, then process like a document. Always keep the source URL for citation.

## Spreadsheets / `.csv` / `.json` data
Don't transcribe rows. Describe the dataset: columns/fields, row count, what each represents, notable values, and how it connects to Entities/Concepts. Link to the file in `.raw/`.

## Images / diagrams
Use the Read tool to view the image and describe it (architecture diagrams → capture the boxes/arrows as text and, if useful, redraw as Mermaid). Store the image in `_attachments/` if it should embed in a note.

## Email (.eml, .msg, or pasted)
`.eml` files: `kb_extract.py` parses the headers (From / To / Cc / Date / Subject) and body via the stdlib `email` module. For a **pasted** email, save the text into `.raw/` as `<slug>.md`. For Outlook `.msg`, convert to `.eml`/text first (or paste the text).
Create a source note with `kind: email`: title = the subject; link the **sender and every recipient** to their person notes (create new people as needed); pull out any **decisions** and **action items**; if it's part of a thread or a meeting follow-up, slot it into the **timeline** (date from the email). Keep the original in `.raw/`.

## Folders
Walk the folder. Separate code (→ codebase pipeline) from documents. For a documents folder, copy the relevant files into `.raw/<folder>/` preserving structure, then process each new/changed file.
