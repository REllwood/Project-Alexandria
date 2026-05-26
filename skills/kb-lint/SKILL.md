---
name: kb-lint
description: Health-check and maintain a client's Obsidian knowledge base — find orphan notes, dead/broken wikilinks, missing or malformed frontmatter, stale notes whose source was removed or changed, duplicate people (alias collisions), un-ingested sources sitting in .raw, thin or under-linked notes, and gaps in the index. Reports findings by category and applies safe fixes. Optionally runs autoresearch to fill open questions from the web with citations. Triggers include "lint the kb", "health check", "find orphans", "find gaps", "clean up the wiki", "fill the gaps", "autoresearch".
---

# kb-lint — keep the knowledge base healthy

Resolve the vault root and target KB (kb skill conventions). For several KBs, spawn a **kb-lint-agent** per KB (read-only, in parallel in Claude Code) to gather findings, then apply fixes centrally from this skill.

## Checks (report grouped, most actionable first)

1. **Un-ingested sources** — `kb_manifest.py status --kb <KB>` → any `new`/`changed` sources not yet turned into notes. Offer to hand off to **kb-ingest**.
2. **Dead links** — `[[wikilinks]]` (and `![[embeds]]`) pointing to notes that do not exist. List source → missing target.
3. **Orphans** — notes with no inbound links (unreachable from `_index.md`). Usually fixed by linking them into the index or a related note.
4. **Frontmatter** — notes missing `type`, `client`, or `updated`, or using a `type` outside the taxonomy in `references/frontmatter.md` (kb skill).
5. **Stale** — notes with a `> [!warning] Stale` flag (source removed), or `updated:` far older than their source's last change. Confirm or refresh.
6. **Duplicate people** — person notes that look like the same human (e.g. "J. Smith" vs "Jane Smith", same email). Propose a merge.
7. **Thin / under-linked** — notes with almost no body or only one link; candidates to enrich or merge.
8. **Open questions** — count and surface `questions.md`; offer autoresearch (below).

## Fixes
- **Safe, auto-applicable** (with a one-line note to the user): add orphans to the index, repair obviously-correct links, add missing `updated:` dates, normalize `type` values.
- **Needs confirmation**: merging duplicate people, deleting notes, rewriting content. Show the proposed change first.

## Autoresearch gap-fill (opt-in)
When open questions remain and the user wants them filled, **delegate to kb-research** (it spawns a kb-research-agent per question, files cited `#researched` notes, and resolves items in `questions.md`). Gated on `.kb/config.json` `autoresearch: true`, an available web tool, and user approval. The research program (limits, source preferences, honesty rules) is in `references/autoresearch.md`.

## Finish
Regenerate the persistent review note: `python3 "<vault>/.kb/bin/kb_review.py" --kb "<KB dir>"` → `_review.md` ("Needs your attention": un-ingested sources, broken links, orphans, thin notes, open Decisions/questions). Then prepend a dated summary to `log.md` (what was checked/fixed/remains), refresh `hot.md` if focus changed, and commit if `git_autocommit` is on. Give the user a short scorecard and point them at [[_review|Needs your attention]].

## References
- `references/autoresearch.md` — research program: source preferences, confidence scoring, limits.
