# Alexandria — Complete Reference

> *A library for everything you know about every client. Ask **Alex** — it has read every doc, meeting, and decision so you don't have to.*

**This document is the full context for the project.** Hand it to a new chat (or a new contributor) and it will understand the whole system: what Alexandria is, how it's structured, every skill/agent/script, the vault model, the conventions, and the end-to-end workflows.

- **Repo / package:** `alexandria` (formerly drafted as `obsidian-kb`). MIT.
- **Runs in:** Claude Code (CLI + desktop app) and Codex CLI / OpenCode — anything supporting the **Agent Skills** standard.
- **Requires:** Obsidian, **Python 3** (standard library only — nothing to `pip install`), and Claude Code or Codex.
- **Counts:** 23 skills · 17 slash commands · 4 subagents · 7 runtime helper scripts.

---

## 1. What it is

Alexandria turns raw source material — documents, whole folders, code repos, PDFs, emails, meeting notes/transcripts, chat attachments — into a **richly cross-linked Obsidian knowledge base**, organised **one folder per client** with one or more **project KBs** under each client. The output is a navigable wiki: stakeholder/engineer profiles, architecture & dependency graphs, decision logs (ADRs), a meeting timeline, a one-shot Overview "home", dashboards, a glossary, and an open-questions tracker — every fact cited back to its source.

You then **ask it questions** ("ask Alex"), **draft comms from it**, get **briefings/onboarding packs**, and run **`update`** to keep it in sync. The goal: an account manager, head of engineering, solution engineer — anyone — doesn't have to retain the detail; the KB holds it.

**Retrieval is structured-link navigation, not embeddings**: read the Overview/index → follow `[[wikilinks]]` → drill into notes → cite. Simple, transparent, and it makes Obsidian's graph view a real map. Knowledge compounds: every source added makes the next answer better.

---

## 2. Core mental model

| Concept | Meaning |
|---|---|
| **Vault** | One Obsidian vault holds everything. Registered in `~/.alexandria/vaults.json`. |
| **Client** | A folder under `Clients/<Client>/`. People live at this level (shared across the client's projects). |
| **KB / project** | `Clients/<Client>/<Project>/` — one engagement/project. Has its own sources, notes, index, timeline. |
| **Sources are immutable** | Raw inputs are copied into `<KB>/.raw/` and never edited. Code repos are scanned in place (not copied). |
| **Generated knowledge** | Everything outside `.raw/` is agent-authored and links back to a source via `[[wikilinks]]`. |
| **Provenance + delta** | `<KB>/.manifest.json` hashes every source and records which notes it produced, so `update` only reprocesses what changed. |
| **The graph is the product** | Dense linking (people ↔ meetings ↔ decisions ↔ concepts) makes the wiki navigable and the graph meaningful. |

---

## 3. Repository layout

```
alexandria/
├── README.md              # public pitch + install + quickstart
├── OVERVIEW.md            # THIS file — full reference
├── AGENTS.md              # cross-agent discovery (Codex/OpenCode) + model + skill table
├── CLAUDE.md              # notes for developing the package in Claude Code
├── LICENSE                # MIT
├── .claude-plugin/
│   ├── plugin.json        # Claude Code plugin manifest (name: alexandria)
│   └── marketplace.json   # local marketplace (name: alexandria-marketplace)
├── bin/
│   ├── install.sh         # Codex symlink + Claude plugin steps + stable scaffolder copy
│   ├── install-project.sh # project-level install for the Claude desktop app
│   └── selftest.sh        # no-deps confidence check (scaffold temp vault, run scripts)
├── commands/              # 17 slash-command wrappers (/kb, /alex, /kb-ingest, …)
├── agents/                # 4 subagents (kb-source / kb-repo / kb-research / kb-lint)
└── skills/
    ├── kb/                # router skill + shared references + the 7 helper scripts
    │   ├── SKILL.md
    │   ├── references/    # vault-layout, frontmatter, dashboards, visuals, scheduling,
    │   │                  #   obsidian-plugins, overview-home, quality
    │   └── scripts/       # kb_init, kb_manifest, kb_repo_scan, kb_extract, kb_doctor, kb_review, kb_actions
    └── kb-*/SKILL.md      # the 22 focused skills (+ some with their own references/)
```

Helper scripts are **copied into every vault** at `<vault>/.kb/bin/`, so a vault works without the package present.

---

## 4. Installation

**Requirements:** Obsidian, Python 3 (stdlib only), Claude Code or Codex. macOS reads `.docx` via built-in `textutil`; Linux/Windows fall back to a built-in extractor (`pandoc` improves quality). `.pptx`/`.xlsx`/`.eml`/PDF work everywhere.

- **Claude Code — plugin (full experience, all projects):**
  ```
  /plugin marketplace add REllwood/Project-Alexandria
  /plugin            # install "alexandria", enable it
  ```
  Then `/alex`. The plugin bundles skills + commands + agents + helper scripts (no `install.sh` needed).
  *Desktop app (Cowork)* has no `/plugin`: `bash bin/install-project.sh /path/to/working-folder` instead.

- **Codex / OpenCode — Agent Skills (recursive discovery):** clone, then
  ```bash
  bash bin/install.sh codex     # or: ln -s "$(pwd)/skills" ~/.codex/skills/alexandria
  ```
  (Codex *prompts* are deprecated; skills use the same `SKILL.md` format.)

- **Cursor — front-door command:** clone, then
  ```bash
  bash bin/install.sh cursor    # writes ~/.cursor/commands/alex.md (the /alex front door)
  ```
  Cursor doesn't auto-discover skills; the command routes by reading the skills in your clone.

Verify any time with **`/kb-doctor`** or `bash bin/selftest.sh`.

---

## 5. The generated vault

```
<vault>/                              # e.g. ~/Knowledge Base  (registered in ~/.alexandria/vaults.json)
├── .obsidian/                        # graph colours, file-explorer tints, templates, properties hidden, Dataview
├── .kb/
│   ├── config.json                   # vault settings (see §15)
│   └── bin/                          # the 7 runtime scripts, copied in
├── _templates/  _attachments/  index.md   # index.md links every client
├── AGENTS.md  CLAUDE.md              # vault-level: how an agent should work inside this vault
└── Clients/
    └── <Client>/
        ├── _client.md                # client hub: status, KBs, key people
        ├── People/<Person>.md        # CLIENT-scoped people (stakeholders + engineers)
        └── <Project>/                # a KB
            ├── Overview.md           # ⭐ one-shot home: status, what's next, outstanding tasks, who's who, nav
            ├── _index.md             # catalog/dashboard (Dataview tables + MoC)
            ├── _review.md            # "Needs your attention" (auto: broken links, orphans, thin notes, open items)
            ├── hot.md log.md questions.md glossary.md
            ├── Stakeholder Map.md     # Mendelow power/interest map (people hub)
            ├── People Relationships.md# Mermaid org / working-relationship graph
            ├── Decisions Log.md       # scannable table of all decisions
            ├── .raw/                  # immutable sources
            ├── .manifest.json         # provenance + delta state
            └── Sources/ Concepts/ Entities/ Architecture/ Decisions/ Meetings/ Canvas/
```

**Special notes:** `Overview.md` (executive home), `_index.md` (full catalog/dashboard), `_review.md` (health checklist), `Stakeholder Map`, `People Relationships`, `Decisions Log`. Dotfiles (`.kb/`, `.raw/`, `.manifest.json`) are hidden from Obsidian.

---

## 6. Frontmatter taxonomy

Every note carries YAML frontmatter (kept minimised in-document via `propertiesInDocument: hidden`). Dates are ISO; people in arrays use `["[[Name]]"]`.

| `type` | Lives in | Key extra fields |
|---|---|---|
| `source` | `Sources/` | `kind` (pdf/doc/meeting/web/data/email/repo), `source_file`, `source_hash`, `people` |
| `person` | `<Client>/People/` | `name`, `role` (stakeholder/engineer/exec/sponsor/user/vendor), `job_title`, `org`, `email`, `aliases`, `projects`, `mendelow` |
| `concept` | `Concepts/` | `aliases` |
| `entity` | `Entities/` | `category` (system/product/org/service/dataset/tool) |
| `decision` | `Decisions/` | `status` (proposed/accepted/superseded/rejected), `deciders`, `date` |
| `meeting` | `Meetings/` | `date`, `attendees` |
| `architecture` | `Architecture/` | `repo`, `component` |
| `index` / `overview` / `review` | KB root | mocs / home / health note |
| `client` / `vault-index` | client / vault root | hubs |
| `hotcache` / `questions` / `glossary` | KB root | working files |

Shared fields: `type`, `client`, `project`, `tags`, `status`, `created`, `updated`.

---

## 7. Shared conventions (every skill follows these)

- **Resolve the vault:** cwd contains `.kb/config.json` → that's it; else search parents; else read `~/.alexandria/vaults.json` (`kb_init.py list-vaults`); else offer setup.
- **Resolve the KB:** `Clients/<Client>/<Project>/`. If ambiguous, list and ask — never let sources land in the wrong KB.
- **Quality bar** (`skills/kb/references/quality.md`): grounded + cited (no invented names/dates/numbers — unknowns go to `questions.md`), substantive (not one-liners), densely linked (zero orphans), one note per real entity (resolve aliases), honest (mark uncertainty; `[!contradiction]` for conflicts). *This is the anti-jibberish charter.*
- **Post-write protocol** (after any change): refresh `_index` links → prepend dated `log.md` line → refresh `hot.md` → record provenance (`kb_manifest.py record`) → regenerate `_review.md` → commit if `git_autocommit`.
- **Token mode** (`skills/kb/references/token-modes.md`): `standard` or `lean` per vault. Lean = tighter notes at ingest + bounded reading at query (search-first, ~5-note cap, answer + citations only). Grounding/citations/links are never cut; "answer lean" / "go deep" overrides per request.
- **Properties minimised** so notes read clean; metadata still powers Dataview/graph.

---

## 8. The 23 skills

The `kb` skill is the **router**; the rest are focused, composable capabilities. Skills **call other skills** and orchestrators **fan out subagents** for parallel work.

### Orchestration & structure
- **`kb`** — Router + shared conventions + `kb status`. Guided start (clickable options: set up / add / ask / status). Triggers: `/kb`, "knowledge base", "kb status".
- **`kb-setup`** — Scaffold & configure a new vault (Obsidian config, templates, `.kb/`, registry, vault-level AGENTS/CLAUDE), then prompt to install Obsidian plugins (Dataview). Triggers: "set up a knowledge base", "create a vault".
- **`kb-organize`** — Create/rename/move clients, KBs, folders while keeping wikilinks intact. Triggers: "new client", "add a project", "new KB", "create a folder", "rename/move".
- **`kb-doctor`** — Preflight health check (Python, document reader, vault, `.kb/bin` scripts, Obsidian + Dataview, registry, pending sources) with one-line fixes. Triggers: `/kb-doctor`, "check my kb setup".

### Capture & ingest
- **`kb-capture`** — Add an attached/pasted doc or link **from chat**: asks which vault → client → KB → folder (create-new at any level), files into `.raw/`, then ingests. Triggers: "add this to my vault", `/kb-capture`.
- **`kb-ingest`** — Ingest orchestrator. Classifies each source (doc / folder / code repo / PDF / web / meeting / email), stages into `.raw/`, processes only new/changed, and **delegates**: code→kb-architecture, people→kb-people, decisions→kb-decisions, meetings→kb-timeline. For folders/batches it writes a build-spec and **fans out background subagents**, then reconciles centrally. Triggers: "ingest", "add this repo/folder", "build a KB from this codebase".

### Knowledge builders (called by ingest; also standalone)
- **`kb-people`** — Build/maintain client people (stakeholders, sponsors, execs, vendors, engineers) as linked profiles with roles/orgs and an Involvement section; resolves aliases/duplicates; mines engineers from git history. Triggers: "update the people", "stakeholder map", "build engineer profiles".
- **`kb-architecture`** — From a repo scan: system overview, module map, **Mermaid** dependency graph (deep mode adds sequence/ER), key files, and an **ownership map** ("who knows what") from git history. Spawns `kb-repo-agent` per repo. Triggers: "document the architecture", "map this codebase", "dependency graph".
- **`kb-decisions`** — ADR-style decision records (context / decision / consequences / alternatives / deciders), linked to source + people; supersede chains. Triggers: "log this decision", "create an ADR", "what did we decide".
- **`kb-timeline`** — Meetings & project timeline: dated `Meetings/` notes with attendees (→ kb-people), decisions (→ kb-decisions), action items as checkboxes; maintains the timeline view. Triggers: "add these meeting notes", "ingest this transcript", "build the timeline".
- **`kb-canvas`** — Obsidian Canvas boards (`.canvas` JSON): architecture map, People/stakeholder map, or KB overview board. Triggers: "make a canvas", "visual map", `/kb-canvas`.

### Retrieval & synthesis
- **`kb-ask`** — The friendly **front door** for questions. **Always confirms the client first** (clickable, from `Clients/` folders), then KB, runs a freshness check, then answers scoped + **cited from the notes** (never from general knowledge). Triggers: `/kb-ask`, "ask the knowledge base", "what do we know about <client>".
- **`kb-query`** — The retrieval mechanics behind kb-ask (Overview/hot → index → drill → cite); also handles "who/ownership" lookups directly. Triggers: "what do you know about", "who owns", "who are the stakeholders".
- **`kb-compose`** — Draft outbound comms (email, status update, Slack/Teams, meeting follow-up, proposal) **grounded in the KB** — correct names/dates/Decisions, never invented; adds a "Sources (for your reference)" footer; can save the draft back. **Drafts, never sends.** Triggers: "write an email", "draft a message", `/kb-compose`.
- **`kb-brief`** — Synthesize a briefing: client overview, meeting prep, status brief, or topic deep-dive, with citations. Triggers: "give me a brief on", "prep me for the meeting", "exec summary".
- **`kb-digest`** — "What changed" digest over a period (new/updated sources, decisions, people, repo activity, questions). Triggers: "what changed this week", "weekly digest".
- **`kb-actions`** — Track open action items / commitments across the KB: who owns what, what's overdue / due-soon, "what we owe the client vs what's owed to us". Builds the plugin-free **[[Action Items]]** roll-up (via `kb_actions.py`) and complements the Overview's live task view; can hand overdue items to kb-compose for follow-ups. Triggers: "what's outstanding", "what's overdue", "action items for <client>", "what do we owe".
- **`kb-research`** — Bounded **web research** to fill open questions / enrich a topic, filed as cited `#researched` notes; spawns `kb-research-agent` per question. Gated on config + approval. Triggers: "research this and add to the KB", "autoresearch".
- **`kb-onboard`** — Role-tailored onboarding pack (composes kb-brief + kb-people + kb-architecture + Decisions/glossary + first-week pointers). Triggers: "onboarding pack", "get someone up to speed on".
- **`kb-export`** — Export a KB / section / brief to Word, PDF, a PowerPoint readout/QBR deck, or a markdown bundle; resolves wikilinks + diagrams (rendering Mermaid to images for slides); uses the docx/pdf/pptx skills. Triggers: "export the KB", "make a PDF of this brief", "make a deck", "QBR slides".

### Maintenance & lifecycle
- **`kb-update`** — Incremental, delta-driven re-sync. Detects new/changed/deleted sources + moved repo HEADs (via the manifest) and runs the agentic passes to bring the wiki back in sync; flags (never deletes) removed sources. Triggers: "update", "refresh the knowledge base", `/kb-update`.
- **`kb-lint`** — Health check + safe fixes (orphans, dead links, frontmatter, stale notes, duplicate people, un-ingested sources, thin notes, gaps); regenerates `_review.md`; optional autoresearch gap-fill. Triggers: "lint the kb", "find gaps", "clean up the wiki".
- **`kb-watch`** — Set up / change / remove **scheduled auto-update** (and optional digests) via `/loop`, the `schedule` skill, or cron. Triggers: "auto-update the KB", "schedule updates".

---

## 9. The 4 subagents (`agents/`)

Spawned in parallel (Claude Code) for batch work; sequential elsewhere. Each writes only its own notes and **returns** structured data for the orchestrator to merge.

- **`kb-source-agent`** — Process ONE staged source into notes (per the kb-ingest routine). Used for batch document ingestion.
- **`kb-repo-agent`** — Build architecture knowledge for ONE repo (scan → overview/modules/Mermaid + engineer profiles + ownership).
- **`kb-research-agent`** — Research ONE open question on the web and file a cited `#researched` note.
- **`kb-lint-agent`** — Read-only health scan of ONE KB; returns findings (orchestrator applies fixes).

---

## 10. The 17 slash commands

`/alex` (**ask Alex — the front door; routes everything**) · `/kb` · `/kb-capture` · `/kb-ingest` · `/kb-update` · `/kb-ask` · `/kb-query` · `/kb-compose` · `/kb-brief` · `/kb-digest` · `/kb-actions` · `/kb-canvas` · `/kb-onboard` · `/kb-research` · `/kb-export` · `/kb-lint` · `/kb-doctor`.

(Skills without a dedicated command — kb-setup, kb-organize, kb-people, kb-architecture, kb-decisions, kb-timeline, kb-watch — trigger by phrase or via `/kb`.)

---

## 11. The 7 runtime scripts (`skills/kb/scripts/`, copied to `<vault>/.kb/bin/`)

All standard-library-only, idempotent.

- **`kb_init.py`** — Scaffold vaults/clients/KBs; write `.obsidian` config + embedded note templates + vault-level AGENTS/CLAUDE; copy runtime scripts into `.kb/bin/`; manage the `~/.alexandria/vaults.json` registry.
  `vault --path --name [--git] [--client --kb]` · `client --vault --client` · `kb --vault --client --kb` · `register` · `list-vaults`
- **`kb_manifest.py`** — Source provenance + delta. `status --kb` (new/changed/unchanged/deleted + repo HEAD moves, JSON) · `record --kb --source --notes --kind` · `record-repo` · `forget` · `touch`.
- **`kb_repo_scan.py`** — Analyse a repo → JSON: languages, structure, entry points, dependencies, internal import graph, git contributors/hotspots/ownership/recent commits. `--path [--max-import-files] [--out]`.
- **`kb_extract.py`** — Extract text from `.docx` (textutil→pandoc→stdlib paragraph fallback), `.pptx`, `.xlsx`, `.eml`, `.txt`. PDFs: use the Read tool. `<file> [--max-chars]`.
- **`kb_doctor.py`** — Preflight health check with ✅/⚠️/❌ + fixes. `[--vault]`.
- **`kb_review.py`** — Generate `<KB>/_review.md` ("Needs your attention"): un-ingested sources, broken links, true orphans (no links in OR out), thin notes, open Decisions/questions. `--kb [--vault]`.
- **`kb_actions.py`** — Roll up open `- [ ]` action items → `<KB>/Action Items.md` (owner from the first wikilink, due dates via ISO/📅/`due:`/`by`, overdue + due-soon flags); plugin-free dashboard grouped by owner. `--kb [--vault] [--soon-days N] [--json]`.

---

## 12. Reference docs (`skills/.../references/`)

`kb/references/`: **vault-layout**, **frontmatter** (taxonomy), **dashboards** (Bases/Dataview), **visuals** (Mermaid timeline/quadrant/graph templates), **token-modes** (standard vs lean), **scheduling**, **obsidian-plugins**, **overview-home** (the one-shot home spec), **quality** (the quality bar).
Skill-specific: `kb-ingest/source-types`, `kb-architecture/codebase-pipeline`, `kb-people/people-extraction`, `kb-canvas/canvas-spec`, `kb-brief/briefs`, `kb-export/export`, `kb-capture/capture-flow`, `kb-lint/autoresearch`.

---

## 13. End-to-end workflows

**Set up & build:** `/alex` (or `/kb`) → choose "set up" → scaffold vault (default `~/Knowledge Base`) → prompt for Dataview → create first `Client/Project` → point at a folder/repo or `/kb-capture` → `kb-ingest` stages sources, writes a build-spec, **fans out subagents**, then reconciles (people dedup, decisions log, glossary, relationship graph, Overview, lint to zero broken links) → commit. Open the vault in Obsidian (graph colours/templates preset).

**Use daily:** `/alex` or `/kb-ask` (pick client → cited answers) · `/kb-compose` (KB-grounded emails) · `/kb-brief` / `/kb-onboard` · `/kb-digest`.

**Keep current:** drop new files → `/kb-update` (delta only) · `/kb-watch` to schedule it · `/kb-lint` + `_review.md` for health · `/kb-doctor` for setup.

---

## 14. Obsidian plugins

**Core (no install, pre-enabled):** Graph view (the source-of-truth map), Backlinks, Outgoing links, Page preview, Tag pane, Outline, Canvas. **Recommended community:** **Dataview** (live dashboards) — or **Bases** on Obsidian ≥ 1.9. The wiki works with **zero** plugins (plain Markdown + wikilinks); Dataview only adds live tables. `kb-setup` prompts and can auto-download Dataview into the vault.

---

## 15. Configuration — `<vault>/.kb/config.json`

```json
{
  "version": 1,
  "vault_name": "…",
  "git_autocommit": true,            // commit after each ingest/update
  "codebase_depth": "architecture",  // architecture | deep | light
  "token_mode": "standard",          // standard | lean (lean = tighter notes + bounded reads — low token use)
  "autoresearch": true,              // allow kb-research/kb-lint web gap-fill (still opt-in per run)
  "scheduled_update": false,         // set true when kb-watch wires a schedule
  "people_scope": "client"           // people notes live at the client level
}
```

---

## 16. Cross-agent portability

Skills use only `name` + `description` frontmatter (kepano convention) so any Agent-Skills-compatible agent reads them. **Claude Code:** install as a plugin (bundles skills + commands + agents); user-level `~/.claude/skills` is *not* a discovery path. **Codex/OpenCode:** symlink `skills/` into `~/.codex/skills/alexandria` (recursive discovery). **Desktop app (Cowork):** no `/plugin`; install per-project via `bin/install-project.sh`. Subagents run in parallel only where the runtime supports them; otherwise the same work runs sequentially.

---

## 17. Limitations & honest notes

- **AI-assisted — review the output.** An agent does the build; it's grounded + cited but not infallible. `/kb-doctor` checks setup; `_review.md` lists what needs a human. Treat the KB as a fast, well-organised first pass, not gospel.
- **Big builds use real tokens/time** (parallel agents). Point it at the most valuable sources first.
- **`kb-compose` drafts, never sends.**
- **Data stays local** (plain Markdown). Version `.raw/` with git only if appropriate; `.gitignore` it for large/sensitive material — and don't publish a client vault.
- **No CI/test suite yet** — `bin/selftest.sh` is the confidence check; tested by hand.

---

## 18. Worked example (reference build)

Built live from a real `~/Downloads` engagement folder — an enterprise client working with a delivery agency on a paid-media automation project (client/agency anonymised): ~74 source docs (decks, 10 stakeholder interviews, 54 Meetings/transcripts, planning sheets; 5 large videos referenced by path, not copied) → **178 notes** via 7 parallel agents: 51 meeting timeline notes, 55 people, 20 decisions + Decisions Log, 12 concepts, 19 sources, consolidated glossary + themed open-questions, a People Relationships Mermaid graph, a Dataview dashboard, a Canvas overview, and a one-shot Overview home — **0 unresolved links**. Cross-agent reconciliation resolved real identity conflicts (two people an early pass merged; a PMM vs an architect with the same surname; a contributor's wrong org). Demonstrates the intended flow: messy folder in → trustworthy, cited, navigable KB out.

---

## 19. System glossary

- **Alexandria / "Alex"** — this tool / its librarian persona.
- **Vault** — the Obsidian folder holding all clients.
- **KB** — a project knowledge base (`Clients/<Client>/<Project>/`).
- **`.raw/`** — immutable source files for a KB.
- **`.manifest.json`** — per-KB provenance + delta state.
- **Overview / `_index` / `_review`** — executive home / catalog dashboard / health checklist.
- **Stakeholder Map / People Relationships / Decisions Log** — the people (Mendelow), people-graph (Mermaid), and decision hubs.
- **build-spec** (`<vault>/.kb/build-spec.md`) — house style + canonical names + return format the batch subagents follow.
- **`~/.alexandria/`** — machine-level home: vault registry + a stable copy of the scaffolder.
- **Quality bar** — the grounded/substantive/linked/honest standard all notes must clear.
