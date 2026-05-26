# Project Alexandria

> *A library for everything you know about every client.* Ask **Alex** — it has read every doc, meeting, and decision so you don't have to.

Build and maintain **incredibly detailed, per-client knowledge bases in Obsidian** — from documents, folders, code repos, PDFs, READMEs, and meeting notes. Point it at your material, and it produces a richly cross-linked wiki with stakeholder/engineer profiles, architecture & dependency graphs, decision logs, and a project timeline. Say `update` after anything changes and it agentically re-syncs.

Works in both **Claude Code** and **Codex CLI** (Agent Skills standard). Retrieval is simple structured-link navigation — no embeddings, no vector DB. Knowledge compounds: every source you add makes the next answer better.

**Requirements:** Obsidian, **Python 3** (standard library only — nothing to `pip install`), and **Claude Code** or **Codex**. macOS reads `.docx` via built-in `textutil`; on Linux/Windows it falls back to a built-in extractor (install `pandoc` for best results). `.pptx` / `.xlsx` / `.eml` / PDFs work everywhere with no extra tools.


## What you get

- **One vault, one folder per client**, multiple project KBs per client.
- **Any source** → cross-linked notes: documents, whole folders, Git repos, PDFs, web pages, meeting notes.
- **People graph** — stakeholder & engineer profiles (engineers mined from Git history), linked everywhere they appear.
- **Architecture docs** — system overview, module map, **Mermaid** dependency graphs, ownership ("who knows what") from commit history.
- **Provenance + incremental `update*`* — each note knows its source; `update` reprocesses only what changed (and only repos whose HEAD moved).
- **Decisions (ADRs), open-questions tracker, timeline, glossary**, per-KB dashboards.
- **Git auto-commit** of the vault, **scheduled auto-update**, and opt-in **autoresearch** to fill gaps from the web with citations.

## Install

Portable: only requires **Python 3** (standard library — no `pip install`) plus Claude Code and/or Codex. The two tools discover extensions differently, so they install differently. To use it on **another machine**, get this folder there first (`git clone …` or copy the `alexandria/` folder), keep it in place, then:

### Claude desktop app (Cowork) — project-level

The desktop app has **no `/plugin` command** and manages its built-in extensions through the app, so install per **project**: drop the skills/commands/agents into a working folder's `.claude/`:

```bash
bash bin/install-project.sh /path/to/your/working-folder   # default: current folder
```

Then open that folder in the app, start a fresh session, and type `**/alex**`. Re-run it for each project you want it in (skills load from the project you're working in). This also copies the scaffolder to `~/.alexandria/`.

### Claude Code CLI (terminal) — local plugin

If you use the `claude` CLI, the plugin route gives an all-projects install:

```
/plugin marketplace add /path/to/alexandria
/plugin                       # open the menu → install "alexandria", then enable it
```

(The `/plugin` menu avoids version-specific install syntax.) Then `bash bin/install.sh claude` once and type `**/alex**`.

### Codex CLI / OpenCode — symlink (discovered recursively)

```bash
bash bin/install.sh codex     # does the symlink + scaffolder copy, or manually:
ln -s "$(pwd)/skills" ~/.codex/skills/alexandria
```

Then say **"set up a knowledge base"**.

> `bin/install.sh` symlinks for Codex and prints the plugin steps for Claude Code; it also copies a stable scaffolder to `~/.alexandria/bin/`. The package install is once per machine. Vaults themselves are fully portable — each carries its runtime scripts in `.kb/bin/`, so a vault made on one machine works anywhere.

## Quickstart

1. `/alex` → scaffold a new vault (default `~/Knowledge Base`) and your first `Client / Project`. (`/alex` is the front door for everything; `/kb` works too.)
2. Open the folder in Obsidian (**Manage Vaults → Open folder as vault**) — graph colors, file tints, and templates are pre-set.
3. Add material: drop files into `Clients/<Client>/<Project>/.raw/` and say `**ingest`**, point at a path/repo, or — from any chat — attach a doc and say `**/kb-capture**` (it asks which vault/client/KB/folder, or creates new).
4. Ask **Alex** anything — `/alex what do you know about X?` or `/alex who are the stakeholders for <Client>?`
5. Added more material later? Say `**update**`.

## Commands

Start with **`/alex`** — the front door that routes everything (ask a question, or set up / ingest / check status). Under it sit 23 focused, composable skills (the router `kb` plus capabilities that call each other). Most-used commands:


| Command                             | What it does                                                                                                   |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `/alex`                             | **Ask Alex** - the front door: ask a question, or start anything (setup, ingest, status)                       |
| `/kb`                               | Router: scaffold, add client/KB, status, or route to the right skill                                           |
| `/kb-capture`                       | **Add an attached/pasted doc from chat** — asks vault → client → KB → folder (create-new at any level)         |
| `/kb-ingest <path or url>`          | Ingest docs / folder / repo / PDF / meeting notes                                                              |
| `/kb-update [Client/Project | all]` | Incrementally refresh after changes                                                                            |
| `/kb-ask`                           | **Ask the KB** — pick the client, get plain-language answers cited from notes (the front door)                 |
| `/kb-query <question>`              | Retrieval mechanics behind kb-ask; direct cited answer                                                         |
| `/kb-compose`                       | Draft an email / message / status update grounded in the KB (correct names, dates, decisions — never invented) |
| `/kb-brief <client/topic>`          | Synthesize a client overview, meeting prep, or deep-dive                                                       |
| `/kb-digest [period]`               | "What changed" report over a period                                                                            |
| `/kb-actions`                       | Track open action items & commitments — who owns what, what's overdue                                          |
| `/kb-canvas [kind]`                 | Visual Canvas board (architecture / people / overview)                                                         |
| `/kb-onboard <role>`                | Role-tailored onboarding pack                                                                                  |
| `/kb-research <topic>`              | Bounded web research → cited notes                                                                             |
| `/kb-export <scope> to <fmt>`       | Export to Word / PDF / PowerPoint readout / markdown bundle                                                    |
| `/kb-lint [fill gaps]`              | Health check + fixes; optional autoresearch                                                                    |
| `/kb-doctor`                        | Preflight: is the vault / Obsidian / Dataview / scripts set up right? (with fixes)                             |


Other skills trigger by phrase or via `/kb`: `kb-setup`, `kb-organize`, `kb-people`, `kb-architecture`, `kb-decisions`, `kb-timeline`, `kb-watch`. (In Codex, just use trigger phrases — e.g. "ingest this repo into Acme/Platform".)

**Agentic by design.** Orchestrators delegate to focused skills (e.g. `kb-ingest` → `kb-architecture` + `kb-people` + `kb-decisions`) and fan out subagents — `kb-source-agent`, `kb-repo-agent`, `kb-research-agent`, `kb-lint-agent` — to process sources, repos, and questions in parallel (Claude Code), sequentially elsewhere.

## Vault layout

```
<vault>/
├── .kb/config.json            settings + .kb/bin/ runtime scripts
├── _templates/  _attachments/  index.md
└── Clients/<Client>/
    ├── _client.md   People/                      ← stakeholders & engineers (client-wide)
    └── <Project>/
        ├── _index.md hot.md log.md questions.md glossary.md
        ├── .raw/  .manifest.json                  ← immutable sources + provenance
        └── Sources/ Concepts/ Entities/ Architecture/ Decisions/ Meetings/ Canvas/
```

Full detail: `[skills/kb/references/vault-layout.md](skills/kb/references/vault-layout.md)`.

## How it works

Seven dependency-free Python helpers (copied into every vault's `.kb/bin/`):

- `**kb_init.py**` — scaffold vaults, clients, KBs; write Obsidian config + templates.
- `**kb_manifest.py**` — hash sources, detect new/changed/deleted, record which notes each produced.
- `**kb_repo_scan.py**` — analyze a repo: languages, structure, entry points, dependencies, import graph, Git contributors/hotspots/ownership.
- `**kb_extract.py**` — read `.docx` / `.pptx` / `.xlsx` / `.eml` / `.txt` to text (stdlib, using `textutil`/`pandoc` when present).
- `**kb_doctor.py**` — preflight health check with one-line fixes.
- `**kb_review.py**` — generate the "Needs your attention" review note.
- `**kb_actions.py**` — roll up open action items by owner / due date into `Action Items.md`.

**23 composable skills** (the `kb` router + focused capabilities — `kb-ingest`, `kb-ask`, `kb-compose`, `kb-architecture`, `kb-people`, `kb-decisions`, `kb-actions`, `kb-update`, `kb-lint`, `kb-doctor`, …) orchestrate reading sources, writing cross-linked notes, and the post-write protocol (index → log → hot cache → provenance → commit). Skills call each other and fan out background subagents for big batches.

## Configuration

Per-vault settings in `.kb/config.json`: `git_autocommit`, `codebase_depth` (`architecture` | `deep` | `light`), `autoresearch`, `scheduled_update`. Scheduling options (`/loop`, `schedule`, cron) in `[skills/kb/references/scheduling.md](skills/kb/references/scheduling.md)`.

## Notes

- Sources in `.raw/` are versioned by default. If a KB holds large or sensitive files, add `.raw/` to `.gitignore`.

