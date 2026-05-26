---
name: kb-export
description: Export a knowledge base, a section, or a synthesized brief to a shareable format — a Word doc, a PDF, a PowerPoint readout/QBR deck, or a bundled markdown folder — resolving wikilinks and embedding or rendering diagrams. Triggers include "export the KB", "make a PDF of this brief", "share this as a doc", "export to Word", "make a deck", "client readout deck", "QBR slides", "export to PowerPoint", "package the knowledge base".
---

# kb-export — shareable output

Resolve vault + scope (a KB, a folder, a set of notes, or a brief). Link/diagram handling and format specifics: `references/export.md`.

## Build
1. **Collect** the notes in scope (follow `[[links]]` to a sensible depth — don't pull the whole vault unless asked).
2. **Resolve** — convert `[[wikilinks]]` to headings/anchors or footnotes; keep Mermaid if the target supports it, else render to images; inline `_attachments`.
3. **Produce** the format:
   - Word → the **docx** skill.
   - PDF → the **pdf** skill.
   - **Deck (PowerPoint) → the pptx skill** — a client readout / QBR built from the KB's `Overview.md` (status, what's next, key people, recent decisions, timeline, open asks). Render Mermaid diagrams (timeline Gantt, Stakeholder quadrant) to images first — slides don't render Mermaid live. Slide structure: `references/export.md`.
   - Markdown bundle → a folder of cleaned `.md` + assets, zipped.
   Strip `.kb`/`.raw` internals; add a generated contents page and source citations.

## Privacy
Confirm scope before exporting client data; exclude anything the user flags as sensitive.

## Composition
Pairs with kb-brief / kb-onboard (exports their output); pulls the readout deck from kb's Overview + kb-actions. Uses the docx / pdf / pptx skills.
