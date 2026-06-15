---
name: kb-decisions
description: Capture and maintain decision records (ADR-style) in a knowledge base — context, the decision, consequences, alternatives considered, and deciders — linked to their source and the people who made them. Triggers include "log this decision", "record a decision", "create an ADR", "track decisions", "mark this decision superseded", "what did we decide".
---

# kb-decisions — decision log (ADRs)

Resolve vault + KB. Decisions live in `Decisions/` using the `decision.md` template (`status`: proposed / accepted / superseded / rejected).

## Create
For each decision (from a source, a meeting, or stated directly by the user): `Decisions/<Title>.md` (Title Case, capitalised — never a lowercase slug) with **context**, **decision**, **consequences**, and **alternatives considered**. Set `deciders` (link people via **kb-people**) and `date`. Link the originating source/meeting.

## Maintain
- **Supersede**: set the old note `status: superseded` and link to the replacement; the new note links back.
- **"What did we decide about X?"** is retrieval → hand to **kb-query** (filter `type: decision`).

## Finish + composition
Link decisions into the KB `_index.md` and any meeting that produced them. Post-write protocol. Invoked by kb-ingest and kb-timeline; feeds kb-brief, kb-digest, kb-onboard.
