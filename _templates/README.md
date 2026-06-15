# _templates (package)

Note templates are **embedded in `skills/kb/scripts/kb_init.py`** and written into each
vault's own `_templates/` folder at scaffold time. That keeps every vault self-contained
regardless of how the skill was installed (Claude Code plugin, Codex symlink, etc.).

To change a template:
- for **new** vaults → edit the `TEMPLATES` dict in `kb_init.py`.
- for an **existing** vault → edit the files in that vault's `_templates/` directory.

This folder is intentionally just this pointer — there are no duplicate template files
here to drift out of sync.
