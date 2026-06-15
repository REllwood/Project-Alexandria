# Obsidian Canvas JSON (`.canvas`)

A Canvas is a single JSON object with `nodes` and `edges`. Write it, then validate it parses.

## Golden rule: navigation boards use **text nodes**, not file embeds
For overview / people / decisions boards (the kind a reader *navigates*), make each card a
**`text` node** containing a wikilink + one short line:

```json
{ "id": "n1", "type": "text",
  "text": "**[[Overview|📋 Overview]]**\nStatus, what's next, who's who",
  "x": 0, "y": 0, "width": 260, "height": 90 }
```

Why not `file` nodes here: an embedded file card renders (a) Canvas's own faint filename label,
(b) the note's inline title, and (c) the note's `# H1` — so the title appears **two or three
times**, and whole-note content **truncates** in a small card. Slug-named notes (sources) show an
ugly slug. A `text` node with `[[wikilink|Nice Title]]` shows the title **once**, never truncates,
and is still one click to the note. Use `file` embeds only when you genuinely want a live preview
of note *content* on the canvas (rare for nav boards) — and then size them ≥ 420×320.

## Shape
```json
{
  "nodes": [
    { "id": "g1", "type": "group", "label": "⭐ Start here", "x": -30, "y": -30,
      "width": 320, "height": 360 },
    { "id": "n1", "type": "text", "text": "**[[Overview|📋 Overview]]**\nStatus & what's next",
      "x": 0, "y": 0, "width": 260, "height": 90 },
    { "id": "n2", "type": "text", "text": "**[[_index|🗂 Index]]**\nFull catalog",
      "x": 0, "y": 150, "width": 260, "height": 90 },
    { "id": "t1", "type": "text", "text": "## Billing Platform\nArchitecture map",
      "x": 0, "y": -170, "width": 540, "height": 110 }
  ],
  "edges": [
    { "id": "e1", "fromNode": "n2", "fromSide": "right", "toNode": "n1", "toSide": "left",
      "label": "depends on" }
  ]
}
```

## Node types
- `text` — a markdown card. **The default** for nav boards: `**[[Note|Title]]**\nshort line`.
  Markdown renders (bold, headings, emoji), and the wikilink is clickable + counts in the graph.
- `file` — embeds a vault note (vault-relative path). Only for live content preview; size ≥ 420×320.
- `link` — an external URL (`"url": "https://…"`).
- `group` — a labeled container; place it first/behind and size it to **enclose its members**
  (membership is positional, by overlap).

Optional on any node: `"color"` — `"1"`–`"6"` (preset palette) or a hex like `"#8b5cf6"`. Tint each
zone's group to match the KB note-type colours (People green, Decisions red, Sources blue, …).

## Edges
`fromSide`/`toSide` ∈ `top|right|bottom|left`. `label` optional. Use edges for dependency arrows
and relationships (mainly on the architecture board).

## Layout math (do this so nothing overlaps or truncates)
Pick fixed sizes and step by size **+ gap** — never eyeball coordinates.
- **Card:** width **260**, height **90** (title + one line). Two lines of detail → height 110.
- **Row step** = card height **+ 60** (e.g. cards at y = 0, 150, 300 …). The 60 clears the next card.
- **Column step** = card width **+ 80** (group columns at x = 0, 340, 680 …).
- **Group that contains N stacked cards:** put cards at local y = 0,150,300…; size the group
  `width = card_w + 60` (30 padding each side), `height = N*150 - 60 + 90 (label+pad)`, and place
  it at `(card_x - 30, first_card_y - 70)` so the label bar sits above the first card.
- Snap everything to a 10px grid. Keep labels short — detail lives in the linked note, not the card.

## Board recipes
- **Overview board** — zones (groups) "⭐ Start here", "📚 Sources", "⚖️ Decisions", "👥 People",
  "❓ Track", each holding 2–5 **text-node** links. Curate: pin the *key* notes, not every note.
- **People map** — one text node per `People/` person (`[[Person|Name]]`, optional second line for
  role/title), grouped by role or org/team (Sponsors / Delivery / Tech / External …); optional edges
  for reporting lines. **Large groups:** if a group exceeds ~8 people, wrap it into 2 sub-columns
  (step the second column +280 in x) rather than one endless strip — or curate to the key people and
  let the header link the full **[[Stakeholder Map]]** (priority quadrant) and **[[People Relationships]]**
  (reporting lines). Size the group to the *tallest* column.
- **Architecture board** — one node per `Architecture/<Module>`; draw `internal_edges` as arrows;
  order left→right by dependency depth (roots left); wrap subsystems in groups. Text nodes
  (`[[module|module]]`) keep it clean; use `file` embeds only if you want the module note visible.

## Pitfalls (these caused real ugly boards)
- **Title shown 2–3×** → you used `file` embeds. Switch to `text` nodes. (Vault-wide, `kb_init`
  also sets `showInlineTitle:false` so even real embeds/notes don't double their title.)
- **Text cut off** → card too small for embedded note content. Use text nodes with short labels,
  or size file embeds ≥ 420×320.
- **Labels overlapping the card above** → row step too small. Use card-height + 60.
- **Cards spilling outside their group** → recompute group height from the card count (formula above).

## Validate
`python3 -c "import json;json.load(open('<file>.canvas'))"` — and open it once to eyeball spacing.
