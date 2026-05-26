# Scheduled auto-update

Make a KB refresh itself as sources change. Pick whichever fits the user's environment, then set `scheduled_update: true` in `.kb/config.json`.

Scheduled runs must be **non-interactive**: process `new`/`changed` sources, flag (never delete) `deleted`/`missing` items, commit, and append a summary to `log.md`. Leave anything needing a human in `questions.md`.

## Claude Code — `/loop` (foreground, while you work)
Re-run an update on an interval in the current session:
```
/loop 30m update the knowledge base in <vault>
```
Good for a working session; stops when you end it.

## Claude Code — `schedule` (background routine)
For a recurring remote/background agent, use the `schedule` skill to create a cron-style routine that runs:
```
update all knowledge bases in <vault>
```
e.g. every weekday at 08:00. This survives across sessions.

## cron (any agent, headless)
Add a crontab entry that drives your agent CLI in headless mode against the vault. Example (Codex CLI; adapt the binary/flags to your setup):
```cron
0 8 * * 1-5  cd "<vault>" && codex exec "run kb-update on all KBs; non-interactive" >> "<vault>/.kb/cron.log" 2>&1
```
or Claude Code:
```cron
0 8 * * 1-5  cd "<vault>" && claude -p "run kb-update on all KBs, non-interactive" >> "<vault>/.kb/cron.log" 2>&1
```

## What changes get picked up
- New/edited files dropped into any `<KB>/.raw/`.
- New commits in tracked repos (the manifest stores each repo's last-seen HEAD).
Because detection is hash/HEAD based, scheduled runs are cheap when nothing changed.
