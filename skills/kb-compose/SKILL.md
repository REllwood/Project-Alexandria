---
name: kb-compose
description: Draft outbound communication grounded in a client's knowledge base — emails, status updates, Slack/Teams messages, meeting follow-ups, short proposals — using the KB as the source of truth so names, titles, dates, decisions, and status are correct and current. Picks the client first (like kb-ask), pulls the relevant facts, drafts in the requested format and tone, never invents facts, and can save the draft back into the KB. Triggers include "write an email", "draft a message", "write a status update", "reply to this using the KB", "/kb-compose", "draft a note to <person> about <topic>".
---

# kb-compose — write things using the KB as the source of truth

Drafts outbound comms grounded in the knowledge base so an account manager / lead / engineer doesn't have to hold the detail in their head — the facts come from the notes.

## 1. Establish client + KB (like kb-ask)
Pick the client from `Clients/` (clickable options), then the KB. Run the freshness check (`kb_manifest.py status`) and offer **kb-update** if there's un-ingested material — you don't want to write from stale facts.

## 2. Confirm the brief (clickable where useful)
If not already clear, ask: **format** (email / Slack message / status update / meeting follow-up / proposal snippet), **audience** (who + seniority — link their person note), **tone** (formal / friendly / concise), and the **goal/ask**.

## 3. Gather the facts (kb-query retrieval, scoped)
Pull only what the message needs from the KB: the recipient's role/context (`People/`), relevant **status / next steps** ([[Overview]]), **decisions** ([[Decisions Log]]), **open items** ([[questions]] / `_review`), and recent **meetings**. Use only what's in the KB. If a needed fact is missing, **ask or flag it — never invent** names, dates, numbers, or commitments.

## 4. Draft
- Lead with the point; keep it tight; use the exact names, titles, dates and decisions from the KB.
- Match the format and tone. If a **brand-voice** skill/guideline is available, apply it.
- **Do not put `[[wikilinks]]` in the outbound text** (the recipient can't use them). Instead append a small **"Sources (for your reference)"** footer listing the KB notes you drew on — for the sender to verify, to be deleted before sending.

## 5. Offer to save / hand off
Offer to: **save the draft** into the KB as a comms note (`Sources/comms/<date>-<slug>.md`, `kind: email`/`message`, linked to recipients + topic) so it's part of the record; and/or **export** via kb-export. **kb-compose drafts — it never sends.**

## Composition
Uses kb-ask / kb-query retrieval (client-scoped); optional brand-voice for tone; can save back via the kb-ingest comms-note routine or export via kb-export.
