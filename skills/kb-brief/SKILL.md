---
name: kb-brief
description: Synthesize a briefing from a knowledge base — a client overview, a meeting-prep brief, a status brief, or a topic deep-dive — pulling from sources, people, decisions, architecture, and the timeline, with citations to the notes used. Triggers include "give me a brief on", "prep me for the meeting", "client overview", "brief me on X", "summarize what we know about", "exec summary".
---

# kb-brief — synthesized briefings

Resolve vault + scope (client / KB / topic). Brief shapes and section templates: `references/briefs.md`.

## Build
1. **Gather** — `hot.md`, `_index.md`, then the relevant sources / people / decisions / architecture / timeline notes (use kb-query's retrieval path).
2. **Synthesize** for the requested shape:
   - *Client overview*: who they are, their KBs, key people, current state, recent decisions, open questions.
   - *Meeting prep*: attendees (people notes), relevant Decisions/questions, recent activity, likely topics.
   - *Topic deep-dive*: what we know about X, strongest evidence first.
3. **Cite** the notes used. Flag gaps and offer **kb-research**.

## Output
Default: a chat answer. On request, save as `<KB>/briefs/<slug>.md` and/or hand to **kb-export** for docx/pdf.

## Composition
Uses kb-query retrieval; reads kb-people / kb-architecture / kb-decisions / kb-timeline; feeds kb-onboard, kb-export.
