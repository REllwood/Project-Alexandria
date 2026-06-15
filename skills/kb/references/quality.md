# Quality bar — make the KB valuable, not noise

Every note must earn its place. Apply this to all ingest / build / compose work; the
batch build-spec is derived from it. This is what keeps the output trustworthy instead of jibberish.

## 1. Grounded — no invention
- Every fact traces to a source in `.raw/`. Cite the source note.
- **Never invent** names, titles, dates, numbers, or commitments. If it isn't in a source, leave it out and add it to `questions.md`.
- Conflicting sources → record both with a `> [!contradiction]` callout; don't silently pick one.

## 2. Substantive — not one-liners
- A note captures the real content: *what it is, why it matters, the specifics* (decisions, numbers, owners), and what it connects to.
- Meeting notes capture the actual discussion / decisions / actions — never "had a standup".
- Summaries are tight but complete: a reader shouldn't need the source to get the point.

## 3. Linked — the graph is the product
- Link people, concepts, decisions, and related notes with `[[wikilinks]]`. Aim for **zero orphans**.
- **One note per real entity** — resolve aliases/duplicates (e.g. "Sam" = Samuel Lee) and record `aliases`.

## 4. Accurate identity & roles
- Match each person to the right note; don't conflate different people with similar names.
- Capture role + org so "who owns X / who are the stakeholders" answers correctly.

## 5. Honest & current
- Mark uncertainty explicitly; never present a guess as fact.
- Keep the `Overview` (status/next) and `_review` (needs-attention) current so the KB reflects reality.

## 6. Named with capitals — human, never a slug
- **Every folder, note filename, and title starts with a capital letter — never lowercase, no matter what.**
- Name each note by its real **Title Case** human name (`Payments Service`, `Q3 Kickoff Deck`) — *not* a lowercase-hyphenated slug (`payments-service`). The filename is what shows in the graph, file explorer, and Canvas, so it must read like a title. The filename = the note's title.
- Keep spaces; remove only filesystem-illegal characters (`\ / : * ? " < > |`). **Preserve** existing capitalisation of acronyms / product names (IBM, iOS, eBay) — don't lowercase or title-mangle them.
- **Exempt — leave their fixed lowercase names:** hidden system/working files & folders only — `.raw/`, `.kb/`, `.obsidian/`, `_index.md`, `_review.md`, `_client.md`, `hot.md`, `log.md`, `questions.md`, `glossary.md`. These are plumbing (most are hidden); their *displayed titles* are already capitalised.

## The test
Before finishing a note, ask: **would a new account manager / engineer trust this and act on it without re-reading the source?** If not, it isn't done.
