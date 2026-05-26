---
name: kb-research
description: Run bounded, agentic web research to answer open questions or enrich a topic, then file the findings into the knowledge base as cited, hash-tagged #researched notes. Triggers include "research this and add to the KB", "fill the open questions", "look up X and file it", "autoresearch", "enrich the KB on Y".
---

# kb-research — web research → KB

Requires `.kb/config.json` `autoresearch: true`, an available web search/fetch tool, and the user's go-ahead. The research program (source preferences, limits, confidence rules) lives in the kb-lint reference `../kb-lint/references/autoresearch.md`.

## Loop
For each open question/topic, spawn a **kb-research-agent** (parallel per question in Claude Code; sequential otherwise). Each agent: search → fetch 1–3 credible sources → synthesize **with citations** → file as `Sources/<slug>.md` tagged `#researched`, create/update related `Concepts/`·`Entities/` notes, and resolve the matching item in `questions.md`.

## Limits & honesty
Max ~3 rounds and ~8 pages per run; ≤3 citations per question. Never present unsourced claims as KB fact. Conflicting sources get a `> [!contradiction]` callout; anything credible sources can't settle stays in `questions.md` marked "researched, unresolved".

## Finish + composition
Post-write protocol. Spawns kb-research-agent; feeds kb-query and kb-brief. Often invoked by **kb-lint**'s gap-fill step.
