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

## The test
Before finishing a note, ask: **would a new account manager / engineer trust this and act on it without re-reading the source?** If not, it isn't done.
