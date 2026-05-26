---
name: kb-capture
description: Add something from the current chat — an attached or pasted document, a snippet, or a path/URL the user just shared — into a knowledge base. Interactively asks which vault, which client, which project KB, and which folder (offering to create a new client, KB, or folder at any level), files it into the right place, then ingests it into notes. Triggers include "add this to my vault", "save this to the knowledge base", "capture this", "/kb-capture", "file this document", "put this in the KB".
---

# kb-capture — add from chat to the vault

The quick-capture path: the user has content in the conversation and wants it filed. Full decision flow and edge cases: `references/capture-flow.md`.

## 1. Identify the content
- **Attached/uploaded file** → use the path the harness provides; copy it (don't assume it's already in a vault).
- **Pasted text** or a message they point to → save as a `.md`.
- **A URL** → treat as a web source.
- **"this conversation" / a decision reached in chat** → save the relevant portion of the transcript.

## 2. Ask where it goes (one compact set of questions)
Offer choices from what exists; allow create-new at each level. Use sensible defaults so the user can accept in one step, and **skip any level they already specified** ("add this to Acme/Billing as a meeting note" → infer all four).
1. **Vault** — `python3 <scripts>/kb_init.py list-vaults`. One → confirm; many → ask; none → **kb-setup**.
2. **Client** — list `Clients/*`; or **+ new client** → kb-organize.
3. **Project KB** — list that client's KBs; or **+ new KB** → kb-organize.
4. **Folder** — where the resulting note lives: `Sources/` (default), `Meetings/`, `Decisions/`, or **+ new folder** (ask its name) → kb-organize creates it.

## 3. Stage + ingest
Copy the content into the chosen KB's `.raw/`, then hand to **kb-ingest** to process it (which delegates to kb-people / kb-decisions / kb-timeline / kb-architecture as the content warrants). If the user chose a custom or specific folder, place the generated source note there.

## 4. Confirm
Tell the user exactly what was added — vault / client / KB / folder — and the notes created. The post-write protocol runs via kb-ingest.

## Composition
Calls: kb-setup (no vault), kb-organize (new client/KB/folder), kb-ingest (processing).
