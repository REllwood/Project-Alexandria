---
name: kb-query
description: Answer questions from a client's Obsidian knowledge base by navigating its structured links and citing the exact notes — not training data. Handles general questions ("what do you know about X"), People/stakeholder lookups ("who are the stakeholders", "who is the sponsor", "who owns the billing service", "which engineers work on Y"), status ("what changed recently", "what decisions were made", "what are the open questions"), and cross-KB or cross-client questions. Triggers include "what do you know about", "who are the stakeholders", "who works on", "who owns", "query:", "ask the kb", "according to the wiki".
---

# kb-query — answer from the knowledge base

Answers come from the vault, with citations to specific notes. If the vault does not contain the answer, say so plainly and offer to ingest a source or run autoresearch — do **not** fill the gap from general knowledge and present it as KB content.

## Retrieval path (cheap → specific)
Resolve the vault root and the relevant scope (a KB, a client, or all clients).

**Shortcut — search-first for named things.** If the question names a specific person / system / decision / meeting, skip the walk: `grep` the KB (and `People/`) for the name and open the matching note(s) directly. The index walk below is for open-ended questions ("what's the status", "what do we know about…").

1. **Hot cache** — read the KB's `hot.md` first for recent working context.
2. **Index** — read the KB's `_index.md` (Map of Content) to locate relevant areas.
3. **Drill** — open the specific notes the index points to. Follow `[[wikilinks]]` outward as needed.
4. **Search** — if the index does not surface it, `grep`/`glob` the KB folder for keywords, frontmatter (`type:`, `role:`), and `[[links]]`.
5. **Synthesize** — answer concisely, then cite the notes used as clickable links (e.g. `[[Clients/Acme/Billing-Platform/Sources/kickoff]]`).

**Read discipline (every mode):** stop reading once the answer is grounded in the notes you've opened; never read `.raw/` originals unless a source note's summary is insufficient (and say so). In **lean** token mode (`.kb/config.json`, or the user says "answer lean"): at most ~5 notes / 1 link-hop, output = answer + citations only — see `../kb/references/token-modes.md`.

## People & stakeholder questions
People notes live at the client level: `Clients/<Client>/People/`.
- **"Who are the stakeholders / sponsor / execs?"** → read `People/` notes, filter by frontmatter `role`. List name, job title, org, and their involvement (from backlinks).
- **"Which engineers work on X?" / "Who owns the Y service?"** → combine `People/` (role: engineer) with the `Architecture/` ownership map (built from git history). Name the top owners and link both the person and the module notes.
- **"How is person Z involved?"** → open their person note and summarize its Involvement section + backlinks (every source, meeting, decision, and commit area touching them).

## Status questions
- **Recent changes** → read `log.md` (and `git log` if versioned).
- **Decisions** → list `Decisions/` notes (filter by `status`).
- **Open questions** → read `questions.md`.
- **Timeline** → read `Meetings/` in date order.

## Cross-KB / cross-client
Read the vault `index.md`, then the relevant `_client.md` hubs, then drill into each KB. State which KB each fact came from so the user can tell sources apart.

## After answering
If the question revealed an important new focus, optionally refresh the KB's `hot.md`. If it revealed a gap, offer to add it to `questions.md` and/or run **kb-lint**'s autoresearch.
