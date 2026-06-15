---
name: kb-architecture
description: Generate and maintain codebase architecture knowledge from a repo — a system overview, module/component map, Mermaid dependency graph (and, in deep mode, sequence and ER diagrams), key files, and an ownership map of which engineers know which parts (mined from git history). Triggers include "document the architecture", "map this codebase", "ingest this repo", "build architecture docs", "dependency graph", "who owns this service".
---

# kb-architecture — codebase → architecture wiki

Full procedure, Mermaid patterns, and depth levels: `references/codebase-pipeline.md`.

## Run
1. Scan: `python3 "<vault>/.kb/bin/kb_repo_scan.py" --path "<repo>" --out "<KB>/.raw/_scan-<repo>.json"`, then `kb_manifest.py record-repo …`.
2. Read the repo's README/`docs`/ADRs for intent (the scan gives structure; prose gives why).
3. Create notes (depth = `.kb/config.json` `codebase_depth`), Title-Case capitalised filenames: `Architecture/<Repo> Overview.md`, `Architecture/<Repo> Dependencies.md` (Mermaid from `internal_edges`), and `Architecture/<Module>.md` per significant top-level dir.
4. Engineers + ownership → invoke **kb-people**: `role: engineer` notes from `contributors`; an ownership map linking engineers ↔ the modules they edit most.

## Multiple repos / batch
Spawn a **kb-repo-agent** per repo (parallel in Claude Code; sequential otherwise).

## Update
On a repo HEAD move: re-scan, refresh the overview's head/branch, add new contributors, revise ownership/hotspots, and reconcile the dependency graph if modules were added/removed. Bump `updated:`; don't rewrite unchanged module notes.

## Finish + composition
Post-write protocol. Calls kb-people; spawns kb-repo-agent; feeds kb-canvas (architecture board), kb-query, kb-onboard. Invoked by kb-ingest for code sources.
