# The Overview = one-shot KB home

Every KB's `Overview.md` is the hero note. Anyone — account manager, head of engineering, solution engineer, a new joiner — should understand the whole engagement from this **one page without opening folders**. Build it on first ingest and refresh its status/next on every `update`.

## Sections (in order)
1. **At-a-glance callout** — client, partner, engagement/SOW ref, phase, status (🟢/🟡/🔴), target date, sponsor / budget owner / delivery lead (all linked).
2. **TL;DR** — 2–4 sentences: what this is and the prize. Link the core concept + the scope decision.
3. **Status & what's next** — where it is now; the next 3–5 milestones with dates.
4. **Outstanding action items (live)** — a Dataview `TASK FROM "<KB>/Meetings" WHERE !completed`, plus a link to **[[Action Items]]** (the plugin-free roll-up built by kb-actions: overdue + by-owner) and a hand-curated key-blockers / watch-list.
5. **Open questions** — one-line summary + link to `questions.md`.
6. **Key people** — sponsor / owner / leads by name (linked), then [[Stakeholder Map]] + [[People Relationships]].
7. **Recent decisions** — link [[Decisions Log]] + the latest few ADRs.
8. **Recent activity** — Dataview table of the last ~6 meetings by date, plus a link to the **visual timeline** (Mermaid Gantt/event chronology, owned by kb-timeline — see `visuals.md`).
9. **Where everything is** — a navigation table (area · count · links) so nobody hunts through folders.
10. **How to use** — ask via `/kb-ask`, add via `/kb-update` / `/kb-capture`, full catalog in `_index`.

## Principles
- It must answer, at a glance: *what is this · status · what's next · what's outstanding · who's who · where do I find X*.
- Use **live Dataview** for tasks and recent activity so it stays current; **hand-write** status/next (that's judgement).
- Keep `_index.md` as the full **catalog/dashboard**; the Overview is the **executive home** and links to it. Don't duplicate.
- Outstanding action items rely on meeting notes writing tasks as `- [ ]` checkboxes (owner linked) — enforce that in ingest.
