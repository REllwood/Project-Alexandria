---
description: Incrementally refresh a knowledge base after sources or tracked repos change
argument-hint: "[<Client>/<Project> | all]"
---

Follow the **kb-update** skill (`skills/kb-update/SKILL.md`): detect deltas via the manifest (new/changed/deleted sources, moved repo HEADs), run the agentic passes to re-sync notes, reconcile links/index/timeline, then commit and report a concise diff.

Scope: $ARGUMENTS
