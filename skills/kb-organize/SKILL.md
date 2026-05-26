---
name: kb-organize
description: Create, rename, move, or restructure a knowledge base's clients, project KBs, and folders while keeping wikilinks intact. Use to add a client, add a project KB under a client, create a custom subfolder/topic area, or rename and relocate notes. Triggers include "new client", "add a project", "new KB", "create a folder", "rename this client/KB", "move this note", "restructure the vault".
---

# kb-organize — structure the vault

Resolve the vault root (kb conventions).

## Create
- **Client**: `python3 "<vault>/.kb/bin/kb_init.py" client --vault "<vault>" --client "<C>"` → link it under `## Clients` in `index.md`.
- **KB**: `python3 "<vault>/.kb/bin/kb_init.py" kb --vault "<vault>" --client "<C>" --kb "<P>"` → link it under `## Knowledge bases` in `<C>/_client.md`.
- **Custom subfolder** (topic area inside a KB): create the folder; if it will hold many notes, add a short MoC note linking it from `_index.md`.

## Rename / move (preserve links)
With the vault open in Obsidian, renames auto-update links. When editing files directly: rename/move, then `grep` the vault for `[[old name]]` and the old path, fix wikilinks and the `client`/`project` frontmatter, and update any `_index.md`/`_client.md` references.

## After any structural change
Refresh affected `_index.md` / `_client.md` / `index.md` links, append to `log.md`, and commit (post-write protocol). For large restructures, run **kb-lint** to catch orphans and dead links.

## Composition
Invoked by kb-setup (first client/KB) and kb-capture ("+ new folder/client/KB"). Pairs with kb-lint after restructures.
