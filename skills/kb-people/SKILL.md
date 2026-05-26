---
name: kb-people
description: Build and maintain people knowledge for a client — stakeholders, sponsors, execs, vendors, and engineers — as linked profile notes with roles, orgs, and an Involvement section assembled from every source, meeting, decision, and code area they touch. Resolves duplicates and aliases, and mines engineers from git history. Triggers include "update the people", "build engineer profiles", "stakeholder map", "add this person", "dedupe people", "who works on this".
---

# kb-people — the human graph

People notes live at the **client** level: `Clients/<Client>/People/`. Procedure, entity-resolution rules, role taxonomy, and the privacy note: `references/people-extraction.md`.

## Invoked from ingest (per source)
Extract every person. For each, create or update `People/<Name>.md` (role, org, job_title, `contact` only if present in the source, projects). Add a linked **Involvement** bullet (where they appeared). Resolve aliases against existing notes — **merge, never duplicate**.

## Invoked standalone
- **"Update/build the people for `<Client>`"** → re-scan that client's sources, plus contributors from tracked repos, and refresh all people notes; run a dedupe pass.
- **Engineers** come from git: use the repo scan's `contributors`/`ownership` (from **kb-architecture**). Create `role: engineer` notes with commit counts and active date ranges, and link the modules they own most.
- Pure **"who are the stakeholders?"** questions are retrieval → hand to **kb-query**.

## Human-graph hubs (always build/refresh — even standalone)
kb-people **owns** the two visual people hubs in the KB root; build them on first people-pass and refresh them whenever people change (don't leave this only to kb-ingest's reconcile). Specs + Mermaid templates: `../kb/references/visuals.md`.
- **`Stakeholder Map.md`** — a Mermaid `quadrantChart` (Mendelow **power × interest**) so a reader sees instantly who to manage closely vs keep informed, with every plotted person linked `[[Name]]` below it. Power/interest is a grounded judgement read of the sources; if someone can't be placed, list them as "unplaced" rather than guessing.
- **`People Relationships.md`** — a Mermaid `graph` of reporting lines + working relationships (the core graph view also shows the emergent network from co-attendance/links).
Both are KB-scoped (a person's power/interest is project-specific) but link the client-level `People/` notes.

## Finish + composition
Refresh the client `_client.md` "Key people", link people into relevant KB `_index.md` and `Overview.md`, then the post-write protocol. Reads kb-architecture scan output; feeds kb-query, kb-brief, kb-onboard, kb-canvas.
