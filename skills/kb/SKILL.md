---
name: kb
description: Router and shared conventions for the alexandria system, which builds and maintains detailed per-client knowledge bases in an Obsidian vault. Use to set up a vault, see status, or when a request touches the knowledge base but the specific operation is unclear. Delegates to focused skills for capture, ingest, people, architecture, decisions, timeline, canvas, query, briefs, digests, research, onboarding, export, update, lint, and scheduling. Triggers include "/kb", "/alex", "ask Alex", "knowledge base", "set up a KB", "kb status", "what can the knowledge base do".
---

# kb — orchestrator & shared conventions

**Alexandria** turns sources (documents, folders, code repos, PDFs, meeting notes, chat attachments) into a richly cross-linked Obsidian wiki: **one vault, a folder per client, one or more project KBs per client**, with People/engineer profiles, architecture and dependency graphs, decision logs, timelines, briefs, and dashboards. Retrieval is structured-link navigation (index → `[[wikilinks]]` → pages → cite), not embeddings.

This skill **routes** and defines the conventions every other skill depends on. Read `references/vault-layout.md` and `references/frontmatter.md` before creating notes.

**The deliverable is a source-of-truth wiki, not a pile of notes.** Link aggressively so the Obsidian **graph view** becomes a navigable map (no orphans); every fact cites a source; and every build offers a visual **Canvas** overview and recommends the Obsidian plugins that power graphs and dashboards. Each KB gets a one-shot **[[Overview]] home** (status · what's next · outstanding tasks · who's who · where everything is) so nobody digs through folders — see `references/overview-home.md`. Note **properties are minimised** (`propertiesInDocument: hidden`) so notes read clean while still powering Dataview/graph. Every note must clear the **quality bar** (`references/quality.md`) — grounded + cited, substantive, linked, honest; never invented filler.

## Guided start (interactive — always prefer clickable options)
Don't free-type a plan at the user. At each decision point use the **AskUserQuestion** tool to present options they click, each with a recommended default. On `/kb` (or when intent is unclear), ask first:
- **Set up a new knowledge base** → kb-setup (scaffold + prompt for Obsidian plugins)
- **Add sources to a knowledge base** — a folder, files, a repo, or chat attachments → kb-capture / kb-ingest
- **Ask the knowledge base something** → kb-query
- **Check status / health** → kb status / kb-lint

Then guide the chosen path with further option-based questions — vault location, client/project (list existing + "+ new"), ingest scope/depth — always with a recommended default. Fall back to free text only for things options can't capture (a file path, a name). After setup or a big build, **prompt the user about required/recommended Obsidian plugins** (see kb-setup).

## Operation map — route to the focused skill

| Intent | Skill |
|---|---|
| Create / configure a vault | **kb-setup** |
| Create / rename / move clients, KBs, folders | **kb-organize** |
| "Add this (attached/pasted) to my vault" — interactive filing | **kb-capture** |
| Ingest a path/repo/folder/url into a KB | **kb-ingest** (delegates onward) |
| Build/refresh people & stakeholder profiles | **kb-people** |
| Build/refresh codebase architecture docs & graphs | **kb-architecture** |
| Record / maintain decisions (ADRs) | **kb-decisions** |
| Build/refresh the meeting & event timeline | **kb-timeline** |
| Visual board (Canvas) of architecture / people / KB | **kb-canvas** |
| **Ask the KB** — plain-language Q&A, client-scoped (the front door) | **kb-ask** (picks client → cited answer) |
| Retrieval mechanics behind an answer | **kb-query** |
| Synthesize a brief (client brief, meeting prep) | **kb-brief** |
| "What changed" digest over a period | **kb-digest** |
| Track open action items / commitments (who owns what, overdue) | **kb-actions** |
| Web research → file into the KB with citations | **kb-research** |
| Onboarding pack for a new team member | **kb-onboard** |
| Export a KB/section to docx/pdf/markdown | **kb-export** |
| Incrementally sync after sources change | **kb-update** |
| Health check + fixes | **kb-lint** |
| Check setup / environment health ("is it set up right?") | **kb-doctor** |
| Set up scheduled auto-update | **kb-watch** |

## Agentic composition (skills call skills)
These skills are designed to compose. When a skill needs another capability, it **invokes that skill** (the Skill tool in Claude Code, or by following its SKILL.md) rather than re-implementing it. For heavy or batched work, orchestrators **spawn the matching subagent** (in `agents/`) — in parallel where the runtime supports it (Claude Code), sequentially otherwise (e.g. Codex). Example chains:
- **kb-capture** → kb-organize (new folder) → kb-ingest → (kb-people / kb-architecture / kb-decisions).
- **kb-ingest** classifies sources and delegates: code → kb-architecture, people → kb-people, decisions → kb-decisions, meetings → kb-timeline; batches fan out to `kb-source-agent`.
- **kb-onboard** → kb-brief + kb-people + kb-architecture, assembled into one pack.

## Resolve the vault root (always, first)
1. cwd contains `.kb/config.json` → that's the vault.
2. Else search parents for `.kb/config.json`.
3. Else read the registry: `python3 <scripts>/kb_init.py list-vaults` (or `~/.alexandria/vaults.json`). One match → use it; several → ask; none → offer **kb-setup**.

Run runtime scripts from `<vault>/.kb/bin/`; use vault-relative paths.

## Resolve the target KB
A KB is `Clients/<Client>/<Project>/`. Infer from context or the active note. If ambiguous, list `Clients/*/*/_index.md` and ask. Never let sources land in the wrong KB silently.

## kb status
List vaults (registry), and for the active vault list clients → KBs (`Clients/*/*/_index.md`). For each KB, run `kb_manifest.py status` to show ingested vs. pending sources, and surface counts of people, decisions, and open questions.

## Shared post-write protocol (EVERY writing skill ends with this)
After creating/changing notes in a KB:
1. **Index** — add/refresh `[[wikilinks]]` in the KB `_index.md` (no orphans).
2. **Log** — prepend a dated line to `log.md` (what changed, which sources).
3. **Hot cache** — refresh `hot.md` (current focus, recently ingested, active questions).
4. **Provenance** — `kb_manifest.py record …` for each source so `update` can detect deltas.
5. **Commit** — if `.kb/config.json` `git_autocommit` is true: `git -C "<vault>" add -A && git -C "<vault>" commit -q -m "<op>: <summary>"`. Confirm before the first commit of a session unless already authorized.

## Locating scripts
Prefer `<vault>/.kb/bin/`. If missing (older vault), re-run this skill's bundled `scripts/kb_init.py vault --path "<vault>" --name "<name>"` (idempotent; refreshes `.kb/bin/` + config without touching notes).

## References
- `references/vault-layout.md` · `references/frontmatter.md` · `references/dashboards.md` · `references/visuals.md` · `references/scheduling.md`
