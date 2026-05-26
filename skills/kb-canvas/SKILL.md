---
name: kb-canvas
description: Create Obsidian Canvas visual boards for a knowledge base — an architecture map (module nodes plus dependency edges), a People/stakeholder map, or a KB overview board pinning the key notes into labeled zones. Triggers include "make a canvas", "visual map", "architecture board", "stakeholder map canvas", "/kb-canvas", "diagram the KB visually".
---

# kb-canvas — visual boards

An Obsidian Canvas is a `.canvas` JSON file. Node/edge/group format + layout helpers: `references/canvas-spec.md`.

## Boards
- **Architecture** — one node per `Architecture/<module>` note; edges from the repo scan's `internal_edges`. Lay out left→right by dependency depth.
- **People / stakeholders** — nodes for `People/` notes grouped by role; link to the KBs they touch.
- **KB overview** — pin `_index.md`, key sources, decisions, and the architecture board into labeled zones.

## Build
Write `<KB>/Canvas/<name>.canvas` as **valid Canvas JSON** (file-link nodes + groups + edges). Validate it parses (`python3 -c "import json,sys;json.load(open(...))"`). Keep node coordinates on a grid so it opens tidy.

## Finish + composition
Link the canvas from `_index.md`. Post-write protocol. Reads kb-architecture and kb-people output.
