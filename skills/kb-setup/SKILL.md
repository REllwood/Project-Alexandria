---
name: kb-setup
description: Scaffold and configure a new Obsidian knowledge-base vault for the alexandria system — the vault skeleton, Obsidian config (graph colors, file tints, templates), .kb/config.json, vault-level agent files, and registry entry. Triggers include "set up a knowledge base", "create a vault", "scaffold the KB vault", "new knowledge base vault", and the first run of /kb when no vault exists.
---

# kb-setup — create a vault

1. Confirm **location + name**. Default `~/Knowledge Base`. Confirm settings (defaults: `git_autocommit` on, `codebase_depth` = architecture, `token_mode` = standard — offer `lean` for low token use: tighter notes, bounded reads, cheaper but less rich; see `../kb/references/token-modes.md` — `autoresearch` on). Ask before writing outside the cwd.
2. Scaffold. No vault exists yet, so run the scaffolder from a package location. Prefer the stable copy that `bin/install.sh` creates; otherwise use the bundled script inside the **kb** skill (`<kb skill dir>/scripts/kb_init.py`):
   ```bash
   # preferred (created by bin/install.sh); fall back to the kb skill's scripts/kb_init.py
   python3 ~/.alexandria/bin/kb_init.py vault --path "<vault>" --name "<Name>" --git [--client "<C>" --kb "<P>"]
   ```
   This also writes vault-level `AGENTS.md`/`CLAUDE.md`, copies runtime scripts into `<vault>/.kb/bin/`, and registers the vault in `~/.alexandria/vaults.json`.
3. **Make sure the Obsidian app is installed, then open the vault.** Many users (especially non-technical ones) won't have Obsidian yet — run `python3 "<vault>/.kb/bin/kb_doctor.py" --vault "<vault>"`, which reports whether the app is found. If it's missing, point them to **https://obsidian.md/download** (free; macOS / Windows / Linux) first. Then: **Manage Vaults → Open folder as vault** → select `<vault>` — graph colours, file tints, and templates are pre-set.
4. Offer next steps: create the first client/KB (**kb-organize**) and ingest a first source (**kb-ingest**) or capture one from chat (**kb-capture**).

Adjust settings later by editing `.kb/config.json` (see the kb skill's `references/vault-layout.md`).
Register an existing, unregistered vault:
```bash
python3 "<vault>/.kb/bin/kb_init.py" register --path "<vault>" --name "<name>"
```

## Obsidian plugins (prompt the user — don't assume)
The wiki's value comes from Obsidian features, so after scaffolding, **prompt the user** (clickable options) to enable/install what's needed. First detect what's present: read `<vault>/.obsidian/community-plugins.json`; core plugins are pre-enabled by `kb_init`.
- **Core (no install — just confirm enabled):** Graph view, Backlinks, Outgoing links, Page preview, Tag pane, Outline, Canvas. These power the graph / source-of-truth experience and ship enabled.
- **Recommended community plugins:** **Dataview** (dynamic dashboards/queries) — or **Bases** if their Obsidian ≥ 1.9 has it (core). Optional: **Templater**, **Obsidian Git** (in-app auto-commit), **Excalidraw**.

Ask with options: **[Guide me to install in Obsidian] / [Auto-download Dataview for me] / [Skip for now]**. For "guide me", give the exact steps (Settings → Community plugins → Browse → search → Install → Enable). For auto-download + version notes, see `../kb/references/obsidian-plugins.md`. Ask once; record the choice in `.kb/config.json`.

## Verify — close the loop (don't leave a non-technical user stuck)
After they've installed Obsidian (and optionally Dataview) and opened the vault, run `python3 "<vault>/.kb/bin/kb_doctor.py" --vault "<vault>"` once more and confirm the key rows are green — especially **Obsidian app installed** and **Dataview plugin (dashboards will render)**. Don't declare setup done while those show ❌. If Dataview is *enabled but its files are missing*, re-run the auto-download and reopen Obsidian. (The wiki itself works with zero plugins — this just confirms the richer graph/dashboard views light up.)

## Composition
Hands off to: kb-organize (first client/KB), kb-ingest / kb-capture (first source).
