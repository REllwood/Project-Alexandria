---
name: kb-canvas
description: Create Obsidian Canvas visual boards for a knowledge base — an architecture map (module nodes plus dependency edges), a People/stakeholder map, or a KB overview board pinning the key notes into labeled zones. Triggers include "make a canvas", "visual map", "architecture board", "stakeholder map canvas", "/kb-canvas", "diagram the KB visually".
---

# kb-canvas — visual boards

An Obsidian Canvas is a `.canvas` JSON file. Node/edge/group format + layout helpers: `references/canvas-spec.md`.

## Boards
- **KB overview** — labeled zones (⭐ Start here · 📚 Sources · ⚖️ Decisions · 👥 People · ❓ Track) of **curated** links to the key notes (Overview, _index, top sources/decisions/people). Pin the important few, not everything.
- **People / stakeholders** — one card per `People/` person, grouped by role; optional edges for reporting lines.
- **Architecture** — one node per `Architecture/<Module>` note; edges from the repo scan's `internal_edges`; laid out left→right by dependency depth.

## Build
Write `<KB>/Canvas/<name>.canvas` as **valid Canvas JSON**. Default each card to a **`text` node** with a wikilink + one short line — `**[[Note|Title]]**\nshort line` — NOT a file embed: embeds render the title two or three times, truncate content, and show ugly slugs. Use `file` embeds only when you truly want a live note preview (and size ≥ 420×320). Size and space nodes with the **layout math** in `references/canvas-spec.md` (card 260×90, row step +60, group sized to contain its cards) so nothing overlaps or truncates, tint each zone's group to the KB note-type colour, then validate it parses (`python3 -c "import json;json.load(open(...))"`) and eyeball spacing.

## Finish + composition
Link the canvas from `_index.md`. Post-write protocol. Reads kb-architecture and kb-people output.
