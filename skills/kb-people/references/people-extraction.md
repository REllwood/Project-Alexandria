# People & the human graph

People notes are the backbone of "who are the stakeholders / who works on this". They live at the **client** level (`Clients/<Client>/People/`) and are linked from every KB that touches them.

## Capture (per person)
Use the `person.md` template. Fill what the sources actually say:
- `name`, `role` (stakeholder / engineer / exec / sponsor / vendor / other), `job_title`, `org`.
- `email` / `contact` — only if present in a source. Don't hunt for or guess contact details.
- `projects` — KBs they're involved in (wikilinks).
- **Involvement** — a bullet per appearance, linked: "Raised the billing concern in [[Sources/kickoff]]", "Owns [[Architecture/payments]] (most commits)", "Attended [[Meetings/2026-05-25-kickoff]]".

## Entity resolution (avoid duplicates)
Before creating a person note, check `People/` for an existing match:
- Same email ⇒ same person, even if names differ.
- "J. Doe", "Jane Doe", "jane.doe" ⇒ likely one person; prefer the fullest name as the note title and add others to `aliases`.
- Git authors: dedupe on `name`+`email`; one human may commit under several emails — merge them, keep all emails in the body.
When unsure whether two are the same, keep separate and add a `questions.md` item rather than wrongly merging.

## Roles
- **stakeholder** — has interest/influence in the project (client-side leads, PMs, sponsors).
- **engineer** — builds it; usually sourced from git history.
- **exec / sponsor** — senior decision-makers / budget owners.
- **vendor** — external suppliers/partners.
Infer role from context; if a person is both (e.g. an engineering lead who's also a stakeholder), pick the primary and note the other in the body.

## Building the graph
Every mention links `[[Person]]`. Backlinks then assemble each person's full footprint automatically — sources, meetings, decisions, and code areas. This is what makes the Obsidian graph show the real working network around a client.

## Privacy
Keep only what's needed for the work and present in the sources. This is client data — don't synthesize personal details, and follow any sensitivity the user flags for a client.
