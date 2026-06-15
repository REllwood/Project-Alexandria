# Alexandria — agent instructions

> *A library for everything you know about every client.*

A portable **Agent Skills** package that builds and maintains detailed, per-client knowledge bases in an Obsidian vault. Works with any agent that supports the Agent Skills standard — **Claude Code**, **Codex CLI**, OpenCode, and similar. Skills use only `name` + `description` frontmatter so every compatible agent can read them.

## Install (skill discovery)

**Claude Code** — `~/.claude/skills` is not a discovery path; install as a **plugin** (bundles all skills + commands + agents). In a Claude Code session:

```
/plugin marketplace add REllwood/Project-Alexandria
/plugin     # menu → install "alexandria", then enable
```

**Codex / OpenCode** discover skills recursively — clone the repo, then symlink `skills/` in:

```bash
ln -s "$(pwd)/skills" ~/.codex/skills/alexandria      # Codex
ln -s "$(pwd)/skills" ~/.opencode/skills/alexandria   # OpenCode
```

**Cursor** — no skill auto-discovery; install a front-door `/alex` command that reads the skills from your clone:

```bash
bash bin/install.sh cursor    # writes ~/.cursor/commands/alex.md
```

`bash bin/install.sh [codex|claude|cursor|all]` automates the symlink/command, prints the Claude Code plugin steps, and copies a stable scaffolder to `~/.alexandria/bin/`.

## Skills (23)

`kb` is the router; the rest are focused, composable capabilities. Skills call other skills, and orchestrators spawn the agents below for parallel work.

| Group | Skills |
|---|---|
| Orchestration / structure | `kb` (router + shared conventions + status), `kb-setup` (scaffold vault), `kb-organize` (clients/KBs/folders), `kb-doctor` (setup/health check) |
| Capture / ingest | `kb-capture` (add-from-chat: asks vault/client/KB/folder), `kb-ingest` (classify → delegate → batch) |
| Knowledge builders | `kb-people`, `kb-architecture`, `kb-decisions`, `kb-timeline`, `kb-canvas` |
| Retrieval / synthesis | `kb-ask` (client-scoped front door), `kb-query`, `kb-compose` (KB-grounded drafting), `kb-brief`, `kb-digest`, `kb-actions` (open commitments tracker), `kb-research`, `kb-onboard`, `kb-export` |
| Maintenance / lifecycle | `kb-update` (incremental sync), `kb-lint` (health), `kb-watch` (scheduled auto-update) |

Each `skills/<name>/SKILL.md` carries `name` + `description` (with trigger phrases) and lists what it calls/spawns under "Composition".

## Agents (Claude Code subagents, for parallelism)
`agents/`: `kb-source-agent` (one source → notes), `kb-repo-agent` (one repo → architecture), `kb-research-agent` (one question → cited note), `kb-lint-agent` (read-only KB scan). Orchestrators fan these out in parallel in Claude Code; in Codex/others the same work runs sequentially. Discover them by symlinking into `~/.claude/agents/` (the installer does this).

## Model

- **One vault, folder per client, multiple KBs per client.** Layout: `skills/kb/references/vault-layout.md`.
- **Sources are immutable** (`<KB>/.raw/`); **generated knowledge** lives elsewhere and links back via `[[wikilinks]]`.
- **Retrieval = structured-link navigation** (index → links → pages → cite), not embeddings.
- **Provenance + delta** via `<KB>/.manifest.json`, managed by `kb_manifest.py`; this drives incremental `update`.
- **Runtime scripts** are copied into each vault at `<vault>/.kb/bin/` (so a vault works without this package).
- **Vault registry** at `~/.alexandria/vaults.json` lists known vaults (written by `kb_init.py`); `kb-capture`/`kb` use it to offer choices. Inspect with `kb_init.py list-vaults`.
- **Token modes** — `.kb/config.json` `token_mode: standard | lean`. Lean trades richness for low token use (tighter notes, bounded reads); grounding/citations are never cut. Spec: `skills/kb/references/token-modes.md`.

## Bootstrap (when opened inside a vault)

1. Resolve the vault root (a dir containing `.kb/config.json`).
2. Read the relevant KB's `hot.md` to restore recent context.
3. Follow the `kb` skill to route the user's request.

## Reference
- Helper scripts: `skills/kb/scripts/{kb_init,kb_manifest,kb_repo_scan}.py`
- Pattern inspiration: Andrej Karpathy's LLM Wiki + per-client structure.
