# Alexandria (Claude Code)

This repo is the **alexandria** skill package — a Claude Code plugin and a portable
Agent Skills bundle. It builds per-client Obsidian knowledge bases from documents,
folders, code repos, PDFs, and meeting notes.

**23 skills** (router `kb` + focused capabilities) and **4 subagents** (`agents/`).
See `AGENTS.md` for the full grouped list and the composition model. Skill logic
lives in `skills/<name>/SKILL.md`; deterministic helpers in `skills/kb/scripts/`.
Skills compose (skills call skills); orchestrators fan out the agents for parallel work.

## Working in this repo
- Edit skills under `skills/<name>/SKILL.md` and their `references/`.
- Edit helper scripts in `skills/kb/scripts/` — they're copied into each vault's
  `.kb/bin/` by `kb_init.py`, so keep them standard-library-only and idempotent.
- Test changes with: scaffold a throwaway vault (`kb_init.py vault …`), exercise
  `kb_manifest.py` and `kb_repo_scan.py`, then delete the temp vault.

## Note
This file is for developing the *package*. Each generated vault gets its own
`CLAUDE.md` / `AGENTS.md` (written by `kb_init.py`) describing how to use the KB
from inside that vault.
