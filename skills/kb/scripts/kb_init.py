#!/usr/bin/env python3
"""kb_init.py - scaffold an Obsidian knowledge-base vault, clients, and KBs.

Single vault, folder-per-client layout:

  <vault>/
    .obsidian/            graph colors, snippets, sane defaults (created here)
    .kb/                  system state (config + copied runtime scripts)
      config.json
      bin/                kb_manifest.py, kb_repo_scan.py, kb_init.py (self-copy)
    _templates/           note templates (one per note type)
    _attachments/         images / pdfs referenced by notes
    index.md              vault-wide master index
    Clients/
      <Client>/
        _client.md        client hub
        People/           stakeholders + engineers (shared across the client's KBs)
        <Project-KB>/
          _index.md       Map of Content for this KB
          hot.md log.md questions.md glossary.md
          .raw/           immutable sources
          .manifest.json  provenance / delta state
          Sources/ Concepts/ Entities/ Architecture/ Decisions/ Meetings/ Canvas/

Idempotent: existing files are never overwritten. Standard library only.

Usage:
  kb_init.py vault  --path VAULT --name NAME [--git] [--client C --kb K]
  kb_init.py client --vault VAULT --client C
  kb_init.py kb     --vault VAULT --client C --kb K
"""
import argparse
import datetime as _dt
import json
import os
import shutil
import subprocess
import sys

TODAY = _dt.date.today().isoformat()
REGISTRY = os.path.expanduser("~/.alexandria/vaults.json")


# ------------------------------------------------------------------- registry
def load_registry():
    try:
        with open(REGISTRY, encoding="utf-8") as fh:
            data = json.load(fh)
            return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def register_vault(path, name):
    """Add a vault to the global registry (de-duped by absolute path)."""
    path = os.path.abspath(path)
    vaults = [v for v in load_registry() if v.get("path") != path]
    vaults.append({"name": name, "path": path, "registered": TODAY})
    os.makedirs(os.path.dirname(REGISTRY), exist_ok=True)
    with open(REGISTRY, "w", encoding="utf-8") as fh:
        json.dump(vaults, fh, indent=2)
        fh.write("\n")
    return vaults


# ----------------------------------------------------------------- fs helpers
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def write_file(path, content, overwrite=False):
    if os.path.exists(path) and not overwrite:
        return False
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return True


def write_json(path, obj, overwrite=False):
    return write_file(path, json.dumps(obj, indent=2) + "\n", overwrite=overwrite)


def render(text, **kw):
    for k, v in kw.items():
        text = text.replace("%" + k + "%", v)
    return text


def slug(name):
    keep = "-_ "
    s = "".join(c if (c.isalnum() or c in keep) else " " for c in name).strip()
    return " ".join(s.split())


# ----------------------------------------------------------- .obsidian config
GRAPH_COLORS = [
    ("path:/People", 2278750),      # green
    ("path:/Architecture", 9133302),  # purple
    ("path:/Sources", 3900150),     # blue
    ("path:/Concepts", 16096779),   # amber
    ("path:/Entities", 15485081),   # pink
    ("path:/Decisions", 15680580),  # red
    ("path:/Meetings", 1357990),    # teal
]

KB_COLORS_CSS = """/* kb-colors: tint file-explorer rows by KB note type */
.nav-file-title[data-path*="/People/"], .nav-folder-title[data-path$="/People"] { color: #22c55e; }
.nav-file-title[data-path*="/Architecture/"], .nav-folder-title[data-path$="/Architecture"] { color: #8b5cf6; }
.nav-file-title[data-path*="/Sources/"], .nav-folder-title[data-path$="/Sources"] { color: #3b82f6; }
.nav-file-title[data-path*="/Concepts/"], .nav-folder-title[data-path$="/Concepts"] { color: #f59e0b; }
.nav-file-title[data-path*="/Entities/"], .nav-folder-title[data-path$="/Entities"] { color: #ec4899; }
.nav-file-title[data-path*="/Decisions/"], .nav-folder-title[data-path$="/Decisions"] { color: #ef4444; }
.nav-file-title[data-path*="/Meetings/"], .nav-folder-title[data-path$="/Meetings"] { color: #14b8a6; }
.nav-folder-title[data-path^="Clients"] { font-weight: 600; }
"""

CORE_PLUGINS = [
    "file-explorer", "global-search", "switcher", "graph", "backlink", "canvas",
    "outgoing-link", "tag-pane", "properties", "page-preview", "templates",
    "note-composer", "command-palette", "outline", "word-count", "bookmarks",
    "file-recovery", "daily-notes",
]


def scaffold_obsidian(vault):
    od = os.path.join(vault, ".obsidian")
    write_json(os.path.join(od, "app.json"), {
        "alwaysUpdateLinks": True,
        "newLinkFormat": "shortest",
        "useMarkdownLinks": False,
        "attachmentFolderPath": "_attachments",
        "userIgnoreFilters": [".kb/"],
        "showUnsupportedFiles": False,
        "templateFolder": "_templates",
        "propertiesInDocument": "hidden",
    })
    write_json(os.path.join(od, "appearance.json"),
               {"enabledCssSnippets": ["kb-colors"]})
    write_json(os.path.join(od, "core-plugins.json"), CORE_PLUGINS)
    write_json(os.path.join(od, "community-plugins.json"), [])
    write_json(os.path.join(od, "graph.json"), {
        "showTags": False, "showAttachments": False, "hideUnresolved": False,
        "showOrphans": True,
        "colorGroups": [{"query": q, "color": {"a": 1, "rgb": rgb}}
                        for q, rgb in GRAPH_COLORS],
        "scale": 1,
    })
    write_file(os.path.join(od, "snippets", "kb-colors.css"), KB_COLORS_CSS)


# --------------------------------------------------------------------- templates
TEMPLATES = {
    "source.md": """---
type: source
title: "{{title}}"
client:
project:
kind:            # pdf | doc | meeting | web | data | repo
source_file:     # relative path under .raw/
source_hash:
people: []
tags: [source]
status: active
created: {{date}}
updated: {{date}}
---

> [!info] Source
> Origin: `source_file`

## Summary

## Key points

## People & entities mentioned

## Open questions

## Related
""",
    "person.md": """---
type: person
name: "{{title}}"
client:
role:            # stakeholder | engineer | exec | sponsor | vendor | other
job_title:
org:
email:
contact:
projects: []
tags: [person]
status: active
created: {{date}}
updated: {{date}}
---

# {{title}}

**Role::**   ·  **Org::**   ·  **Email::**

## Summary

## Involvement
<!-- Backlinks (bottom of note) show every source, meeting, and decision this person touches. -->

## Notes
""",
    "concept.md": """---
type: concept
title: "{{title}}"
client:
project:
aliases: []
tags: [concept]
status: active
created: {{date}}
updated: {{date}}
---

# {{title}}

## Definition

## Details

## Related

## Sources
""",
    "entity.md": """---
type: entity
title: "{{title}}"
client:
project:
category:        # system | product | org | service | dataset | tool
tags: [entity]
status: active
created: {{date}}
updated: {{date}}
---

# {{title}}

## What it is

## Relationships

## Sources
""",
    "decision.md": """---
type: decision
title: "{{title}}"
client:
project:
status: proposed   # proposed | accepted | superseded | rejected
deciders: []
date: {{date}}
tags: [decision, adr]
created: {{date}}
updated: {{date}}
---

# {{title}}

## Context

## Decision

## Consequences

## Alternatives considered

## Sources
""",
    "meeting.md": """---
type: meeting
title: "{{title}}"
client:
project:
date: {{date}}
attendees: []
tags: [meeting]
status: active
created: {{date}}
updated: {{date}}
---

# {{title}}

**Date::** {{date}}  ·  **Attendees::**

## Context

## Discussion

## Decisions
<!-- link to Decisions/ notes created from this meeting -->

## Action items
- [ ]

## Open questions
""",
    "architecture.md": """---
type: architecture
title: "{{title}}"
client:
project:
repo:
component:
tags: [architecture]
status: active
created: {{date}}
updated: {{date}}
---

# {{title}}

## Overview

## Responsibilities

## Dependencies

```mermaid
graph TD
  A[Component] --> B[Depends on]
```

## Key files

## Owners
<!-- link to People/ engineers who own this area -->
""",
    "kb-index.md": """---
type: index
title: "{{title}}"
client:
project:
tags: [index, moc]
status: active
created: {{date}}
updated: {{date}}
---

# {{title}}

> [!abstract] Knowledge base
> Client::   ·  Project::   ·  Updated:: {{date}}

## Start here

## Sources

## People

## Architecture

## Concepts & entities

## Decisions

## Meetings (timeline)

## Open questions
![[questions]]

## Glossary
![[glossary]]
""",
}


def scaffold_templates(vault):
    for name, body in TEMPLATES.items():
        write_file(os.path.join(vault, "_templates", name), body)


# ------------------------------------------------------------------- seed files
VAULT_INDEX = """---
type: vault-index
title: "%NAME% — Knowledge Base"
tags: [index]
updated: %DATE%
---

# %NAME% — Knowledge Base

A persistent, compounding knowledge base. One folder per client; each client
holds one or more project knowledge bases. Built and maintained by the
`alexandria` skill (works in Claude Code and Codex).

## How to use
- Drop sources into a KB's `.raw/` folder, then say **`ingest`**.
- Say **`update`** to refresh after sources change.
- Ask **`what do you know about X?`** or **`who works on Y?`** to query.
- Say **`lint the kb`** to find gaps, orphans, and stale notes.

## Clients
<!-- one link per client hub, e.g. [[Clients/Acme/_client|Acme]] -->

"""

KB_README = """# .kb — system state (hidden from Obsidian)

This folder is owned by the `alexandria` skill. Safe to version with git.

- `config.json` — vault settings (git auto-commit, codebase depth, autoresearch).
- `bin/` — copied runtime scripts so the vault works without the original package:
  - `kb_manifest.py` — source provenance + change detection
  - `kb_repo_scan.py` — codebase / git-history analysis
  - `kb_init.py` — add new clients/KBs from inside the vault

Each KB's own state lives in `<Client>/<KB>/.manifest.json`.
"""

CLIENT_HUB = """---
type: client
client: "%CLIENT%"
tags: [client]
status: active
created: %DATE%
updated: %DATE%
---

# %CLIENT%

> [!info] Client
> Status:: active  ·  Owner::

## Knowledge bases
<!-- one link per project KB, e.g. [[%CLIENT%/Billing-Platform/_index|Billing Platform]] -->

## Key people
<!-- see ./People/ — stakeholders and engineers across this client's KBs -->

## At a glance
"""

KB_INDEX_SEED = """---
type: index
title: "%PROJECT% — Index"
client: "%CLIENT%"
project: "%PROJECT%"
tags: [index, moc]
status: active
created: %DATE%
updated: %DATE%
---

# %PROJECT%

> [!abstract] Knowledge base
> Client:: [[%CLIENT%/_client|%CLIENT%]]  ·  Project:: %PROJECT%  ·  Updated:: %DATE%

## Start here
_Nothing ingested yet. Drop files into `.raw/` and say `ingest`._

## Sources

## People

## Architecture

## Concepts & entities

## Decisions

## Meetings (timeline)

## Open questions
![[%PROJECT%/questions|Open questions]]

## Glossary
![[%PROJECT%/glossary|Glossary]]
"""

HOT_SEED = """---
type: hotcache
client: "%CLIENT%"
project: "%PROJECT%"
updated: %DATE%
---

# Hot cache — %PROJECT%
_Recent working context. Agents read this at session start and refresh it at session end._

## Current focus

## Recently ingested

## Active questions
"""

LOG_SEED = """# Operation log — %PROJECT%
_Append-only, most recent first. Each ingest/update/lint adds a dated line._

- %DATE% — KB created.
"""

QUESTIONS_SEED = """---
type: questions
client: "%CLIENT%"
project: "%PROJECT%"
tags: [questions]
updated: %DATE%
---

# Open questions — %PROJECT%
_Unknowns the KB has surfaced but not yet answered. `lint` and `autoresearch` work this list._

"""

GLOSSARY_SEED = """---
type: glossary
client: "%CLIENT%"
project: "%PROJECT%"
tags: [glossary]
updated: %DATE%
---

# Glossary — %PROJECT%
_Domain terms, acronyms, and product names specific to this KB._

"""

GITIGNORE = """.DS_Store
.obsidian/workspace*
.obsidian/cache
.trash/
**/__pycache__/
"""

VAULT_AGENTS = """# Knowledge base vault

This Obsidian vault is managed by the `alexandria` skill. One folder per client
under `Clients/`, each with one or more project knowledge bases (KBs).

When an agent works inside this vault:
1. This directory is the vault root (it contains `.kb/config.json`).
2. Read the relevant KB's `hot.md` (`Clients/<Client>/<Project>/hot.md`) at the
   start to restore recent context.
3. Use the kb skills: **ingest** (add sources), **update** (refresh after change),
   **query** (answer questions / people lookups), **lint** (maintain health).
4. Sources are immutable in `<KB>/.raw/`; generated notes link back via `[[wikilinks]]`.
5. Runtime helpers live in `.kb/bin/` (`kb_manifest.py`, `kb_repo_scan.py`, `kb_init.py`).

Navigate `index.md` → client `_client.md` → KB `_index.md` → specific notes.
Don't bulk-read the vault for unrelated tasks.
"""

VAULT_CLAUDE = """# %NAME% — knowledge base (Claude Code)

This folder is an Obsidian vault managed by the `alexandria` skill.
See `AGENTS.md` for the working model. Skills: `/alex` (ask Alex — the front door), `/kb`, `/kb-ingest`, `/kb-update`,
`/kb-query`, `/kb-lint`.

## Using this vault from another project
Add to that project's CLAUDE.md:

> ## Knowledge base
> Path: %VAULT%
> When you need context not in this project: read the relevant
> `Clients/<Client>/<Project>/hot.md`, then its `_index.md`, then drill into notes.
> Don't read the vault for unrelated tasks.
"""


# ---------------------------------------------------------------- subcommands
KB_SUBDIRS = ["Sources", "Concepts", "Entities", "Architecture",
              "Decisions", "Meetings", "Canvas", ".raw"]


def copy_runtime_scripts(vault):
    src_dir = os.path.dirname(os.path.abspath(__file__))
    dst_dir = os.path.join(vault, ".kb", "bin")
    ensure_dir(dst_dir)
    copied = []
    for fn in ("kb_manifest.py", "kb_repo_scan.py", "kb_init.py",
               "kb_extract.py", "kb_doctor.py", "kb_review.py", "kb_actions.py"):
        src = os.path.join(src_dir, fn)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dst_dir, fn))
            copied.append(fn)
    return copied


def make_client(vault, client):
    cdir = os.path.join(vault, "Clients", slug(client))
    ensure_dir(os.path.join(cdir, "People"))
    write_file(os.path.join(cdir, "_client.md"),
               render(CLIENT_HUB, CLIENT=client, DATE=TODAY))
    write_file(os.path.join(cdir, "People", ".gitkeep"), "")
    return cdir


def make_kb(vault, client, kb):
    cdir = make_client(vault, client)
    kdir = os.path.join(cdir, slug(kb))
    for sub in KB_SUBDIRS:
        ensure_dir(os.path.join(kdir, sub))
        write_file(os.path.join(kdir, sub, ".gitkeep"), "")
    write_file(os.path.join(kdir, "_index.md"),
               render(KB_INDEX_SEED, CLIENT=client, PROJECT=kb, DATE=TODAY))
    write_file(os.path.join(kdir, "hot.md"),
               render(HOT_SEED, CLIENT=client, PROJECT=kb, DATE=TODAY))
    write_file(os.path.join(kdir, "log.md"),
               render(LOG_SEED, PROJECT=kb, DATE=TODAY))
    write_file(os.path.join(kdir, "questions.md"),
               render(QUESTIONS_SEED, CLIENT=client, PROJECT=kb, DATE=TODAY))
    write_file(os.path.join(kdir, "glossary.md"),
               render(GLOSSARY_SEED, CLIENT=client, PROJECT=kb, DATE=TODAY))
    write_json(os.path.join(kdir, ".manifest.json"),
               {"kb": kb, "client": client, "sources": {}, "repos": {},
                "created": TODAY})
    return kdir


def cmd_vault(args):
    vault = os.path.abspath(args.path)
    ensure_dir(vault)
    scaffold_obsidian(vault)
    scaffold_templates(vault)
    ensure_dir(os.path.join(vault, "_attachments"))
    ensure_dir(os.path.join(vault, "Clients"))
    write_file(os.path.join(vault, "index.md"),
               render(VAULT_INDEX, NAME=args.name, DATE=TODAY))
    write_json(os.path.join(vault, ".kb", "config.json"), {
        "version": 1,
        "vault_name": args.name,
        "created": TODAY,
        "git_autocommit": bool(args.git),
        "codebase_depth": "architecture",
        "autoresearch": True,
        "scheduled_update": False,
        "people_scope": "client",
    })
    write_file(os.path.join(vault, ".kb", "README.md"), KB_README)
    write_file(os.path.join(vault, "AGENTS.md"), VAULT_AGENTS)
    write_file(os.path.join(vault, "CLAUDE.md"), render(VAULT_CLAUDE, NAME=args.name, VAULT=vault))
    copied = copy_runtime_scripts(vault)

    if args.git:
        write_file(os.path.join(vault, ".gitignore"), GITIGNORE)
        if not os.path.isdir(os.path.join(vault, ".git")):
            try:
                subprocess.run(["git", "init", "-q"], cwd=vault, timeout=30, check=False)
            except (OSError, subprocess.SubprocessError):
                pass

    if args.client and args.kb:
        make_kb(vault, args.client, args.kb)

    register_vault(vault, args.name)
    print(json.dumps({
        "vault": vault,
        "runtime_scripts": copied,
        "git": bool(args.git),
        "first_kb": (f"{args.client}/{args.kb}" if args.client and args.kb else None),
        "registry": REGISTRY,
    }, indent=2))


def cmd_register(args):
    register_vault(args.path, args.name)
    print(f"registered {args.name} -> {os.path.abspath(args.path)}")


def cmd_list_vaults(args):
    print(json.dumps(load_registry(), indent=2))


def cmd_client(args):
    cdir = make_client(os.path.abspath(args.vault), args.client)
    print(f"client ready: {cdir}")


def cmd_kb(args):
    kdir = make_kb(os.path.abspath(args.vault), args.client, args.kb)
    print(f"kb ready: {kdir}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("vault"); v.add_argument("--path", required=True)
    v.add_argument("--name", required=True); v.add_argument("--git", action="store_true")
    v.add_argument("--client", default=""); v.add_argument("--kb", default="")
    v.set_defaults(fn=cmd_vault)

    c = sub.add_parser("client"); c.add_argument("--vault", required=True)
    c.add_argument("--client", required=True); c.set_defaults(fn=cmd_client)

    k = sub.add_parser("kb"); k.add_argument("--vault", required=True)
    k.add_argument("--client", required=True); k.add_argument("--kb", required=True)
    k.set_defaults(fn=cmd_kb)

    rg = sub.add_parser("register"); rg.add_argument("--path", required=True)
    rg.add_argument("--name", required=True); rg.set_defaults(fn=cmd_register)
    lv = sub.add_parser("list-vaults"); lv.set_defaults(fn=cmd_list_vaults)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
