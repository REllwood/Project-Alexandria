---
name: kb-update
description: Incrementally refresh a client's Obsidian knowledge base after sources change. Detects new, changed, and deleted documents and new commits in tracked code repos, then runs the agentic passes needed to bring the wiki back in sync — re-ingesting changed sources, refreshing architecture and engineer profiles for updated repos, flagging notes whose sources disappeared, and reconciling cross-links, the index, and the timeline. Triggers include "update", "update the kb", "refresh the knowledge base", "I added new notes/Sources", "sync the wiki", "/kb-update".
---

# kb-update — keep the knowledge base in sync

`update` is delta-driven: it asks the manifest what changed and does only the work required. It reuses the **kb-ingest** processing routines — read that skill for how individual sources and codebases become notes.

## 1. Resolve scope
Resolve the vault root (kb skill conventions). Determine which KB(s) to update: the one in context, a named one, or **all** (`Clients/*/*/`). For "update everything", loop the steps below per KB.

## 2. Detect deltas
```bash
python3 "<vault>/.kb/bin/kb_manifest.py" status --kb "<KB dir>"
```
This yields, for each source: `new` / `changed` / `unchanged` / `deleted`, plus a `repos` section showing tracked repos whose HEAD moved (`changed`) or that went `missing`.

## 3. Apply changes (the agentic passes)
Work through the delta. Each item is an independent pass — in Claude Code, **fan out subagents** (one per item, in parallel); otherwise do them in sequence.

- **New / changed documents** → spawn a **kb-source-agent** per source (it runs the kb-ingest per-source routine: source note, people, concepts, entities, decisions, questions). For `changed`, the agent updates existing notes in place and bumps `updated:` rather than duplicating.
- **Changed repos** (HEAD moved) → spawn a **kb-repo-agent** per repo (re-scan, refresh `Architecture/` notes, add new contributors, update commit counts/date ranges, revise the "who owns what" map, note new/removed modules and dependencies, re-record the repo). Or invoke **kb-architecture** directly.
- **Deleted sources** → do **not** silently delete derived notes. Add a `> [!warning] Stale: source removed` callout at the top of each affected note (the manifest lists the notes each source produced), add an entry to `questions.md` ("confirm whether X is still valid"), and `kb_manifest.py forget --source …`. Let the user decide whether to remove the notes.
- **Missing repos** → flag in `questions.md` and the log; the path may have moved. Ask the user for the new path.

## 4. Reconcile
After per-source passes:
- Re-resolve cross-links so new notes connect to existing ones (and fix any newly dead links).
- Refresh the KB `_index.md` (every note reachable), the **meeting timeline**, and any dashboard.
- Re-run the people merge check (new sources may introduce aliases of existing people).

## 5. Finish
Record provenance for each processed source (`kb_manifest.py record …`), prepend a dated summary line to `log.md`, refresh `hot.md`, and commit if `git_autocommit` is on. Report a concise diff to the user: counts of notes created/updated, new people, repo changes, and any stale/flagged items needing their attention.

## Scheduled / unattended runs
When invoked by a scheduler (see the kb skill's `references/scheduling.md`), run non-interactively: process all `new`/`changed` items, flag (never delete) for `deleted`/`missing`, commit, and write the summary to `log.md`. Do not block on questions — leave them in `questions.md` for the next interactive session.
