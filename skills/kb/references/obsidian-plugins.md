# Obsidian plugins for the KB

The knowledge base is a **source-of-truth wiki**: its value is the linked graph, backlinks, and dashboards. Most of that is **core** Obsidian (no install). A couple of **community** plugins make dashboards dynamic. Always *prompt* the user — never silently require an install, and never let core navigation depend on a plugin.

## The Obsidian app itself (check first)
Everything below assumes Obsidian is installed. A non-technical user often won't have it yet — `kb_doctor.py` reports **"Obsidian app installed"**. If it's missing, point them to **https://obsidian.md/download** (free; macOS / Windows / Linux), then **Manage Vaults → Open folder as vault** → pick the vault. The vault is just Markdown files, so nothing is lost without the app — but the graph/dashboards/Canvas only render inside Obsidian.

## Core plugins (built in — `kb_init` pre-enables these)
| Plugin | Why |
|---|---|
| **Graph view** | The visual source-of-truth map, driven by `[[wikilinks]]`. Color groups are pre-set in `graph.json`. |
| Backlinks / Outgoing links | Every connection into/out of a note. |
| Page preview | Hover to preview linked notes. |
| Tag pane, Outline, Search | Navigation. |
| Canvas | Visual boards (kb-canvas). |
Just confirm enabled (Settings → Core plugins). No download needed.

## Recommended community plugins
| Plugin | Why | Needed for |
|---|---|---|
| **Dataview** | Query frontmatter into live tables/lists | Dynamic dashboards (`dashboards.md`, Option B) |
| **Bases** *(core in Obsidian ≥ 1.9)* | Native database views | Dashboards (Option A) — prefer over Dataview if available |
| Templater *(optional)* | Auto-fill templates | Faster manual note creation |
| Obsidian Git *(optional)* | Auto-commit from inside Obsidian | In-app history (complements `git_autocommit`) |
| Excalidraw *(optional)* | Freehand diagrams / annotate images | Hand-drawn sketches |

## How to prompt + install
Ask with clickable options: **[Guide me] / [Auto-download Dataview] / [Skip]**.

**Guide me (safest):** Settings → Community plugins → turn off Restricted mode → Browse → search the plugin → Install → Enable. The dashboard note's Dataview/Bases blocks then render.

**Auto-download (Dataview example)** — with Obsidian closed:
```bash
P="<vault>/.obsidian/plugins/dataview"; mkdir -p "$P"
base="https://github.com/blacksmithgu/obsidian-dataview/releases/latest/download"
for f in main.js manifest.json styles.css; do curl -fsSL "$base/$f" -o "$P/$f"; done
# add "dataview" to the JSON array in <vault>/.obsidian/community-plugins.json, then reopen Obsidian
```
Verify files are non-empty, then tell the user to reopen Obsidian. Record the choice in `.kb/config.json` so you don't re-ask.

## Source-of-truth posture
The wiki must stand on plain Markdown + `[[wikilinks]]` with **zero** plugins. Dataview/Bases only *enhance* dashboards. The graph view (core) is the always-on map.
