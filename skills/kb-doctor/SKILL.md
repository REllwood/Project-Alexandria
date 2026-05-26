---
name: kb-doctor
description: Health-check the alexandria setup and environment — verifies Python, the document reader, the vault, the .kb/bin runtime scripts, the Obsidian config + Dataview plugin, the vault registry, and pending sources per KB — then reports what's wrong with one-line fixes. Triggers include "/kb-doctor", "kb doctor", "check my kb setup", "is the knowledge base set up correctly", "diagnose the kb", "kb health".
---

# kb-doctor — preflight / "is everything OK?" check

Resolve the vault (kb conventions). Run the checker:
```bash
python3 "<vault>/.kb/bin/kb_doctor.py" --vault "<vault>"
```
If no vault exists yet, run the bundled `../kb/scripts/kb_doctor.py` to check just the environment.

Relay the ✅ / ⚠️ / ❌ report and **offer to fix each issue**:
- **Dataview missing** → auto-download via **kb-setup** (or install in Obsidian → Community plugins).
- **`.kb/bin` script missing** → re-run **kb-setup** (idempotent; refreshes scripts).
- **`.obsidian` missing** → open the folder as a vault in Obsidian once.
- **Sources pending** → run **kb-update**.
- **No vault / registry** → run **kb-setup**.

Keep it friendly and concrete — this is the command to run right after install to confirm you're good to go, or any time something feels off.
