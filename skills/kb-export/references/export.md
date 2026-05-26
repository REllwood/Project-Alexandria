# Export handling

## Scope selection
- A whole KB, a folder (e.g. `Architecture/`), an explicit set of notes, or a single brief.
- Follow `[[links]]` outward only to a sensible depth (default 1 hop) unless the user asks for the full closure. Don't sweep the entire vault by accident.
- Always exclude `.kb/`, `.raw/`, and `.manifest.json`.

## Resolving notes for a flat document
- **Wikilinks** — convert `[[Note]]` / `[[Note|alias]]` to either an internal anchor (if the target is included in the export) or a footnote/citation (if not). Keep the human text.
- **Embeds** — `![[image.png]]` → inline the image from `_attachments/`; `![[note]]` → inline that note's content (once; avoid loops).
- **Frontmatter** — drop YAML from the body; optionally surface `title`, `updated`, and `status` in a header.
- **Mermaid** — keep fenced ```mermaid blocks if the target renders them (many PDF pipelines do); otherwise render to an image and embed.
- **Callouts** — `> [!info]` etc. → a styled blockquote or a bold label line.

## Formats
- **Word (.docx)** — use the **docx** skill; map note H1/H2 to heading styles, add a generated table of contents.
- **PDF** — use the **pdf** skill (or docx → PDF).
- **Deck (.pptx)** — use the **pptx** skill; a client-facing readout / QBR (see below).
- **Markdown bundle** — a folder of cleaned `.md` + an `assets/` dir, with a generated `index.md` contents page; zip it.

## Readout / QBR deck (.pptx)
A presentation an account/project manager can take into a client review, built from the KB so every number and name is grounded. Default slide flow (drop empties; never invent to fill a slot):
1. **Title** — client × partner, project / SOW ref, date, "prepared from the knowledge base".
2. **Executive summary** — the Overview TL;DR (what this is + the prize), RAG status, target date.
3. **Status & what's next** — current phase + the next 3–5 milestones with dates.
4. **Timeline** — the visual timeline (render the Mermaid Gantt/event chart to an **image** and place it; pptx won't render Mermaid live).
5. **Key people** — sponsor / owner / leads, plus the **Stakeholder Map** quadrant rendered to an image.
6. **Recent decisions** — the latest few ADRs from the Decisions Log (one line each).
7. **Open items / asks** — overdue + key open action items (from **[[Action Items]]** / kb-actions) and top open questions — i.e. what you need from the client.
8. **Appendix / sources** — the source notes behind the deck.

Rendering Mermaid → image: ask the user's preferred path (e.g. a Mermaid renderer, or screenshot from Obsidian) if no headless renderer is available; if it can't be rendered, fall back to a clean bulleted text slide rather than shipping a broken diagram. Keep slides sparse — headline + a few bullets or one visual; detail stays in the KB.

## Front matter of the export
- A contents page (ordered by `_index.md` where available).
- A "Sources" section listing the cited source notes and any external URLs.
- A generated/exported date and the scope covered.

## Privacy
This is client material. Confirm the scope and recipient before exporting, and exclude anything the user flags as sensitive (e.g. personal contact details, internal-only decisions).
