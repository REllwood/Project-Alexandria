---
name: kb-ask
description: Ask questions about a client's knowledge base in plain language and get answers cited from the notes — the friendly front door so an account manager, head of engineering, solution engineer, or anyone doesn't have to retain the detail. ALWAYS confirms which client first (the user picks from the client folders), then which project KB, before answering, so every question is scoped to the right client. Triggers include "/alex", "ask Alex", "kb-ask", "/kb-ask", "ask the knowledge base", "ask about a client", "what do we know about <client>", "who owns X at <client>", "what's the status of <project>".
---

# kb-ask — ask the knowledge base (client-scoped)

The front door for getting answers out of a KB without digging through folders. It **always establishes the client first**, then answers with citations to the exact notes.

## 1. Pick the client (always — use clickable options)
Resolve the vault (kb conventions / `kb_init.py list-vaults`; if several vaults, ask which). Then list client folders — `ls "<vault>/Clients/"` — and present them with the **AskUserQuestion** tool so the user clicks one. If the user already named the client, just confirm it; if only one client exists, use it.

## 2. Pick the KB (if the client has several)
List `Clients/<Client>/*/`. One → use it. Several → ask which (or "all of this client's KBs").

## 2.5 Check freshness (quick — don't answer from a stale KB)
Before answering, run `python3 "<vault>/.kb/bin/kb_manifest.py" status --kb "<KB dir>"`. If it reports `new`/`changed` sources (files dropped into `.raw/` but not yet ingested) or tracked repos whose HEAD moved, tell the user the KB has un-ingested material and **offer to run kb-update first**. Either way, answer from the current notes — just don't present a stale KB as complete.

## 3. Answer — scoped, cited (delegate retrieval to kb-query)
Run the **kb-query** retrieval path **scoped to the chosen client/KB**:
1. Read the KB **[[Overview]]** (the one-shot home) and `hot.md` for current state.
2. Then `_index` (catalog/dashboard) to locate the right area.
3. Drill into the specific notes and follow `[[wikilinks]]`.
- **People / ownership** → `People/` + [[People Relationships]] + [[Stakeholder Map]].
- **Status / what's next / outstanding** → [[Overview]] + open action items + [[questions]].
- **Decisions** → [[Decisions Log]] + `Decisions/`.
- **History / when** → `Meetings/` by date.

Answer concisely, then **cite the notes used** as clickable links. If the KB lacks the answer, say so and offer to ingest a source or run **kb-research** — never answer client questions from general knowledge.

## 4. Follow-ups
Keep the chosen client/KB in context for follow-ups (don't re-ask each turn). Suggest useful next questions.

## Composition
Front door over **kb-query** (retrieval mechanics). Reads Overview / _index / people / decisions / meetings. Scopes every answer to one client the user explicitly selected.
