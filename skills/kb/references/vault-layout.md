# Vault layout

One vault. One folder per client. One or more project KBs per client.

```
<vault>/
├── .obsidian/                 Obsidian config (graph colors, snippets, defaults) — created by kb_init
├── .kb/                        system state (hidden from Obsidian via userIgnoreFilters)
│   ├── config.json             vault settings (see below)
│   └── bin/                    copied runtime scripts (kb_manifest.py, kb_repo_scan.py, kb_init.py)
├── _templates/                 note templates, one per type
├── _attachments/               images / pdfs embedded in notes
├── index.md                    vault-wide master index — links every client
└── Clients/
    └── <Client>/
        ├── _client.md          client hub: status, owner, list of KBs, key people
        ├── People/             CLIENT-scoped people (stakeholders + engineers across all this client's KBs)
        │   └── <Person>.md
        └── <Project-KB>/
            ├── _index.md        Map of Content + dashboard for this KB
            ├── hot.md           recent-context cache (read at session start)
            ├── log.md           append-only operation log (newest first)
            ├── questions.md      open-questions tracker
            ├── glossary.md       domain terms / acronyms
            ├── .raw/            immutable source files (agents read, never edit)
            ├── .manifest.json    provenance + delta state (per source hash → notes)
            ├── Sources/          one note per ingested source (summary + citations)
            ├── Concepts/         extracted ideas / topics
            ├── Entities/         orgs, products, systems, datasets, tools
            ├── Architecture/     codebase docs: overview, module map, Mermaid graphs
            ├── Decisions/        ADR-style decision records
            ├── Meetings/         meeting notes (YYYY-MM-DD-…) forming a timeline
            └── Canvas/           Obsidian Canvas visual boards (optional)
```

## Why this shape
- **Client-scoped people** — a stakeholder usually spans multiple projects, so people live once per client and are linked from each KB. Backlinks then show a person's whole footprint.
- **`.raw/` is immutable** — never edit sources in place; this keeps provenance honest and lets `update` hash-compare reliably.
- **Generated knowledge is agent-owned** — everything outside `.raw/` can be regenerated/refined; it always links back to a source.
- **Dotfolders hidden** — `.kb/`, `.raw/`, `.manifest.json` stay out of Obsidian's file explorer and search.

## .kb/config.json
```json
{
  "version": 1,
  "vault_name": "…",
  "git_autocommit": true,        // commit after each ingest/update
  "codebase_depth": "architecture", // architecture | deep | light
  "autoresearch": true,          // allow kb-lint web gap-fill (still opt-in per run)
  "scheduled_update": false,     // set true when a scheduler is wired up
  "people_scope": "client"       // where person notes live
}
```

## Naming
- Folders/files use the human name in **Title Case, always starting with a capital** — spaces kept, filesystem-unsafe characters removed; **never lowercase slugs**. `kb_init` capitalises client/KB folders; agents name notes by their title (see `quality.md` §6). Wikilinks use the note's path or basename.
- Meeting files start with the ISO date, then a Title-Case topic: `2026-05-25 Kickoff.md`.
- Exempt (fixed lowercase): hidden system/working files — `.raw/`, `.kb/`, `_index`, `_review`, `_client`, `hot`, `log`, `questions`, `glossary`.
