# Autoresearch program

Bounded web research to fill gaps in a KB. Opt-in only: requires `autoresearch: true` in config, an available web tool, and the user's go-ahead for the run. Edit this file to tune behavior per domain.

## Loop (per question)
1. **Search** — form 1–2 focused queries from the open question.
2. **Fetch** — open the top credible results (max 3 per question).
3. **Synthesize** — write the answer in the relevant note (`Concepts/`, `Entities/`, or a new `Sources/<Title>.md` tagged `#researched`), with inline citations to the URLs used.
4. **Resolve** — remove the answered item from `questions.md`, linking to the note that now answers it.

## Limits (defaults)
- Max **3 rounds** per run; max **8 pages** fetched total.
- Max **3 sources** cited per question.
- Stop early when the question is answered with adequate confidence.

## Source preferences (general)
Prefer, in order: official/primary docs and filings → reputable technical or news sources → community sources. Avoid content farms and unattributed pages. For a specialized domain, override this list (e.g. "prefer PubMed", "prefer SEC filings", "prefer vendor docs").

## Confidence & honesty
- Tag each researched claim with its source. If sources conflict, record both and flag with a `> [!contradiction]` callout.
- If credible sources can't answer it, leave the question in `questions.md` marked "researched, unresolved" — never fabricate.
- Researched content is clearly marked (`#researched`) so it's distinguishable from client-sourced knowledge.
