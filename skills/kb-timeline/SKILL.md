---
name: kb-timeline
description: Build and maintain a chronological timeline of a project from meeting notes and dated events — creating dated meeting notes with attendees, decisions, and action items, and keeping a project timeline view in the KB index. Triggers include "add these meeting notes", "ingest this transcript", "build the timeline", "what happened when", "meeting notes", "project history".
---

# kb-timeline — meetings & project timeline

Resolve vault + KB. Meetings live in `Meetings/YYYY-MM-DD-<topic>.md` (`meeting.md` template).

## Per meeting / transcript
Read the source, then create the dated meeting note: context, discussion, **attendees** (link each via **kb-people**), **decisions** (create via **kb-decisions**), **action items** as a task list, and open questions → `questions.md`. The ISO-dated filename + `date` frontmatter is what orders the timeline.

## Timeline view (text)
Maintain a "Meetings (timeline)" section in the KB `_index.md` (most recent first, linked). For a live view, the kb skill's `references/dashboards.md` shows a Dataview/Bases query ordered by date.

## Visual timeline (always — this is the at-a-glance picture)
Build/refresh **one** Mermaid chronology at the top of the `_index.md` timeline section (and link it from `Overview.md`) so a reader sees the whole engagement without scrolling notes — see `../kb/references/visuals.md`:
- **Gantt** when the project has dated phases/milestones (the default for an engagement): phases as `section`s, key dates as `:milestone`.
- **Event timeline** when it's a stream of meetings/decisions without clean ranges.
Bars/events come only from dated sources (meeting dates, stated phase/go-live dates, decisions); never invent dates — unknowns go to `questions.md`. Keep labels short and link the underlying notes beneath the diagram. Refresh it whenever a new dated event is ingested.

## Finish + composition
Post-write protocol. Calls kb-people, kb-decisions. Invoked by kb-ingest for meeting/transcript sources; feeds kb-digest, kb-brief. Action items written here as `- [ ]` (with a linked `[[owner]]` and a due date) feed **kb-actions** and the Overview's live task view — always use checkbox syntax.
