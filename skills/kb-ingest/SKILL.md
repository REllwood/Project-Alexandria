---
name: kb-ingest
description: Ingest sources into a client's Obsidian knowledge base and orchestrate the specialists that build knowledge from them. Classifies each source (document, folder, code repo, PDF, README, web page, meeting/transcript), stages it into the KB's immutable .raw/, processes only new or changed items, and delegates to kb-architecture (code), kb-people (stakeholders/engineers), kb-decisions (ADRs), and kb-timeline (meetings) — fanning out kb-source-agent subagents for batches. Triggers include "ingest", "ingest this", "add this repo/folder/doc/pdf to the KB", "build a knowledge base from this codebase", "ingest all of these".
---

# kb-ingest — turn sources into knowledge (orchestrator)

Prerequisite: resolve the vault root and target KB (kb skill conventions). No target KB? Offer **kb-organize** to create one first.

## 0. Confirm with the user first (clickable options)
Before building, use the **AskUserQuestion** tool to confirm, each with a recommended default:
- **Which client / project KB** — list existing (`Clients/*/*`) plus "+ new".
- **Scope / depth** — e.g. *backbone first* (core docs → people, overview, concepts, decisions) vs *everything* (also every meeting note → full timeline) vs *let me pick*.
- **Large / binary files** — for big folders, confirm skipping large media (e.g. video) that can't be read; reference them by path instead.
Proceed only once confirmed — this keeps sources out of the wrong KB and avoids surprising the user with a huge run. After building, prompt about Obsidian plugins if not already done (see kb-setup).

## 1. Classify & stage
For each source, decide its type and stage it:

| Type | Detect | Stage |
|---|---|---|
| Code repo | `.git`, or `package.json`/`pyproject.toml`/`go.mod`/code `src/` | Do **not** copy. Hand to **kb-architecture** (scans in place, registers path). |
| Folder of docs | a directory without code markers | Copy doc files into `.raw/<folder>/`. |
| Document / PDF / README | single file | Copy into `.raw/`. |
| Web page / URL | http(s) | Fetch readable text → `.raw/<slug>.md` (keep URL). |
| Meeting / transcript | `.vtt`/`.srt`, or content is a call/meeting | Copy into `.raw/`; route to the meeting routine. |
| Email (`.eml`, pasted, or a thread) | an email or `.eml` file | Copy into `.raw/`; source note `kind: email`, link sender + recipients to people, extract Decisions/actions, thread into the timeline. |

`.raw/` is immutable — copy in, never edit there. Reading specifics per format: `references/source-types.md`.

## 2. Find the delta
```bash
python3 "<vault>/.kb/bin/kb_manifest.py" status --kb "<KB dir>"
```
Process only `new`/`changed`. Skip `unchanged`.

## 3. Process each source

### Documents / web / PDFs — per-source routine
Read the source fully, then:
1. **Source note** — `Sources/<slug>.md` from the `source.md` template; fill `source_file`, `source_hash` (from status), `kind`, `client`, `project`. Body: tight summary + key points. This is the citable anchor.
2. **Concepts / entities** — create or **merge** `Concepts/` and `Entities/` notes; link back to the source.
3. **People** → invoke **kb-people** for this source (extract, resolve, link).
4. **Decisions** → invoke **kb-decisions** for any decision/commitment found.
5. **Open questions / glossary** → append to the KB `questions.md` / `glossary.md`.
6. **Cross-link** everything with `[[wikilinks]]`.

### Meetings
Route to **kb-timeline** (creates the dated `Meetings/` note, extracts attendees → kb-people, decisions → kb-decisions, action items, and slots it into the timeline).

### Code repos
Route to **kb-architecture** (scan → overview, module map, Mermaid dependency graph, engineer profiles via kb-people, ownership map).

## 4. Folders & big batches — spin up parallel agents (the default)
For a folder or any multi-source batch, don't grind through it serially — fan out, the hand-holdy build:
1. **Stage** all readable sources into `.raw/` (reference huge binaries like video by path, don't copy). Use `.kb/bin/kb_extract.py` for docx/pptx/xlsx/txt; the Read tool for PDFs.
2. **Write a build-spec** to `<vault>/.kb/build-spec.md`: house style (frontmatter + linking), the canonical people-name list, and the RETURN format — derived from the **quality bar** (`../kb/references/quality.md`: grounded + cited, substantive, densely linked, honest, never invented). Every agent reads it so output is consistent, valuable, and conflict-free.
3. **Partition** sources into batches (~8–12 each) by type (interviews / decks / meetings / code).
4. **Spawn one background subagent per batch** (`kb-source-agent`, `kb-repo-agent`, or general-purpose carrying the spec) so the build runs in parallel. Each agent creates ONLY its own notes (`Sources/`, `Meetings/`) and **returns** structured data (decisions, questions, glossary, new people, relationships) — it must NOT edit shared files. Tell the user what you launched; let it run.

## 5. Reconcile (orchestrator-owned, after agents return)
- **People** — create the newly-found people; dedupe + resolve aliases/identity conflicts; fix mis-links.
- **Decisions** — deduped ADR notes + a scannable **[[Decisions Log]]**.
- **Glossary / questions** — merge and consolidate (themed).
- **Graphs** — build the **[[People Relationships]]** Mermaid map; the Obsidian graph also emerges from meeting co-attendance.
- **Overview home** — build/refresh `Overview.md` (see `../kb/references/overview-home.md`).
- **Link health** — re-scan for unresolved `[[links]]` and fix until ~zero (the lint pass). Action items must be `- [ ]` checkboxes so the Overview's live task query works.

## 6. Finish
`kb_manifest.py record …` provenance for every source; regenerate the review note (`python3 "<vault>/.kb/bin/kb_review.py" --kb "<KB dir>"` → `_review.md`); then the post-write protocol (index → log → hot → commit). Report what was created and point the user at [[_review|Needs your attention]].

## Composition
Calls: kb-people, kb-decisions, kb-timeline, kb-architecture, kb-organize (for new structure). Spawns: `kb-source-agent`, and via kb-architecture, `kb-repo-agent`.

## References
- `references/source-types.md` — reading PDFs, docx, transcripts, web, data, images, folders.
