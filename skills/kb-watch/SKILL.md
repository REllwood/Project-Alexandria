---
name: kb-watch
description: Set up, change, or remove scheduled automatic updates (and optional digests) for a knowledge base so it refreshes itself as sources change. Triggers include "auto-update the KB", "schedule updates", "watch this vault", "run update every morning", "stop the scheduled updates", "weekly digest automatically".
---

# kb-watch — scheduled auto-update

Resolve the vault. Mechanisms and exact commands (Claude Code `/loop`, the `schedule` skill, cron): the kb skill's `references/scheduling.md`.

## Set up
1. Pick the mechanism for the user's environment — a background routine via the **schedule** skill is best for unattended runs; `/loop` for a working session; cron otherwise.
2. Schedule a **non-interactive** run of **kb-update** (and optionally **kb-digest**) on the chosen cadence. Scheduled kb-update processes new/changed, flags (never deletes) removed/missing items, commits, and logs — leaving anything needing a human in `questions.md`.
3. Set `.kb/config.json` `scheduled_update: true` and note the cadence in the vault `log.md`.

## Change / remove
List and edit or remove the routine via the scheduler used; set `scheduled_update` back to `false` if removed.

## Composition
Drives kb-update (and optionally kb-digest) on a schedule.
