---
name: kb-actions
description: Track open action items and commitments across a client's knowledge base — the operational pulse for a project or account manager. Rolls up every open `- [ ]` action from meeting notes (and elsewhere) into who-owns-what, what's overdue, and what's due soon, and can split "what we owe the client" vs "what's owed to us". Builds a plain-Markdown `Action Items.md` dashboard (works with zero plugins) and complements the Overview's live task view. Triggers include "/kb-actions", "what's outstanding", "open action items", "what's overdue", "what do we owe <client>", "what are we waiting on", "action items for <client>", "track commitments".
---

# kb-actions — open commitments, by owner and due date

The day-to-day "what's outstanding?" view. Action items are captured as `- [ ]` checkboxes in meeting notes (owner linked, due date noted); this skill aggregates them so nobody has to scan every meeting.

Prerequisite: resolve the vault root and target KB (kb conventions). If the client/KB is ambiguous, list `Clients/*/*` and ask — scope every answer to one client.

## 1. Roll up (deterministic)
```bash
python3 "<vault>/.kb/bin/kb_actions.py" --kb "<KB dir>"          # writes <KB>/Action Items.md
python3 "<vault>/.kb/bin/kb_actions.py" --kb "<KB dir>" --json   # same data as JSON, to reason over
```
This scans the KB's notes for **open** `- [ ]` items (skipping `questions.md` and generated files), extracts the **owner** (first `[[wikilink]]` on the line) and a **due date** (ISO, `📅 YYYY-MM-DD`, `due: …`, `by …`), flags **overdue** / **due-soon**, and writes a grouped, plain-Markdown dashboard. It works without Dataview; the Overview's live `TASK` query is the plugin-powered twin.

## 2. Answer the question (synthesis)
From the JSON (or the dashboard), answer concisely and cite the source notes:
- **"What's outstanding / overdue?"** → lead with the overdue list (owner + due + source), then due-soon.
- **"What's open for <person>?"** → that owner's group.
- **"What do we owe the client vs what's owed to us?"** → label each owner by side using their `People/` note (`org` / `role`: client-side, our team, or `vendor`); group accordingly. If a person's side is unknown, say so rather than guess.
- **Unassigned or no-due items** → surface them as gaps to tighten (an action with no owner or date rarely gets done).

## 3. Offer the next move
- Overdue items → offer to draft a chase/nudge via **kb-compose** (grounded — real names, the actual ask, the date).
- Missing owners/dates → offer to add them to the source meeting note (then re-run the roll-up).

## Convention (so the roll-up stays accurate — enforced at ingest)
Write action items as checkboxes that lead with the owner and carry a date:
`- [ ] [[Jane Doe]] to send the revised SOW by 2026-05-10`
kb-timeline/kb-ingest already write meeting actions this way; keep it consistent so `kb_actions.py` can attribute and schedule them.

## Finish + composition
Link **[[Action Items]]** from the KB `Overview.md` and `_index.md`; then the post-write protocol (log → hot → commit if `git_autocommit`). Reads `- [ ]` items written by **kb-timeline** / **kb-ingest**; feeds **kb-digest** (what moved) and hands overdue items to **kb-compose** for follow-ups.
