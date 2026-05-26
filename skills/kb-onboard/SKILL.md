---
name: kb-onboard
description: Generate an onboarding pack for someone new to a client or project — the people they'll work with, the architecture they'll touch, key decisions and terminology, and where to start — assembled from the knowledge base and tailored to their role. Triggers include "onboarding pack", "onboard a new engineer", "get someone up to speed on", "ramp-up doc for", "new joiner brief".
---

# kb-onboard — ramp-up pack

Resolve vault + scope (client / KB) + the joiner's role (engineer, PM, designer, …). This skill **composes** the others.

## Assemble
1. **kb-brief** — client/KB overview: what it is, current state, recent decisions.
2. **kb-people** — who's who, filtered to those relevant to the role; for engineers, include the ownership map ("who knows what").
3. **kb-architecture** — the components they'll touch and where to start in the code.
4. **kb-decisions** + glossary — the load-bearing decisions and the domain terms.
5. **First week** — entry-point notes, the top sources to read, and open questions they could pick up.

## Output
A single tailored note `<KB>/onboarding/<role>-<date>.md`, linked from `_index.md`. Offer **kb-export** to produce a docx/pdf to hand to the person.

## Composition
Calls kb-brief, kb-people, kb-architecture, kb-decisions; optional kb-export.
