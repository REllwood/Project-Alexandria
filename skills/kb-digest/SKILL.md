---
name: kb-digest
description: Produce a "what changed" digest for a knowledge base over a period — new and updated sources, new decisions, new people, code-repo activity, and questions opened or answered — across one KB, a client, or the whole vault. Triggers include "what changed this week", "weekly digest", "kb digest", "what's new in the KB", "activity summary", "since last month".
---

# kb-digest — change digest

Resolve vault + scope + period (default: last 7 days, or since the last digest noted in `log.md`).

## Gather changes
- `log.md` entries in the period; `git -C "<vault>" log --since="<period>"` if versioned.
- `kb_manifest.py status` for pending sources, and tracked repos whose HEAD moved.
- Notes whose `updated:` falls in the period (grep/glob frontmatter).

## Output
A scannable, grouped digest: **New sources · New/changed decisions · New people · Repo activity** (commits, new contributors) **· Questions opened/closed · Suggested next actions** (e.g. run kb-update / kb-lint). Save to `<KB>/digests/<date>.md` on request.

## Composition
Reads log / manifest / git. Suggests kb-update and kb-lint. Pairs with **kb-watch** for scheduled digests.
