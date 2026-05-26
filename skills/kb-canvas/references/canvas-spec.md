# Obsidian Canvas JSON (`.canvas`)

A Canvas is a single JSON object with `nodes` and `edges`. Write it, then validate it parses.

## Shape
```json
{
  "nodes": [
    { "id": "n1", "type": "file", "file": "Clients/Acme/Platform/Architecture/core.md",
      "x": 0, "y": 0, "width": 320, "height": 200 },
    { "id": "n2", "type": "file", "file": "Clients/Acme/Platform/Architecture/api.md",
      "x": 420, "y": 0, "width": 320, "height": 200 },
    { "id": "t1", "type": "text", "text": "## Billing Platform\nArchitecture map",
      "x": 0, "y": -160, "width": 740, "height": 100 },
    { "id": "g1", "type": "group", "label": "Backend", "x": -40, "y": -40,
      "width": 820, "height": 300 }
  ],
  "edges": [
    { "id": "e1", "fromNode": "n2", "fromSide": "left",
      "toNode": "n1", "toSide": "right", "label": "depends on" }
  ]
}
```

## Node types
- `file` — embeds a vault note (use the vault-relative path). Best for pinning wiki pages.
- `text` — a markdown card (titles, notes, zone descriptions).
- `link` — an external URL (`"url": "https://…"`).
- `group` — a labeled container; place it first/behind and size it to enclose member nodes (membership is positional, by overlap).

Optional on any node: `"color"` — `"1"`–`"6"` (preset palette) or a hex like `"#8b5cf6"`.

## Edges
`fromSide`/`toSide` ∈ `top|right|bottom|left`. `label` optional. Use edges for dependency arrows and relationships.

## Layout tips
- Snap coordinates to a grid (e.g. multiples of 20). Default node ~320×200; group padding ~40.
- **Architecture board**: order module nodes left→right by dependency depth (roots left), draw `internal_edges` as arrows, wrap subsystems in groups.
- **People map**: cluster `People/` nodes into role groups (stakeholders / engineers / vendors); link to the KB notes they touch.
- **Overview board**: zones (groups) for "Start here", "Sources", "Decisions", "Architecture", each holding a few pinned file nodes.
- Validate: `python3 -c "import json;json.load(open('<file>.canvas'))"`.
