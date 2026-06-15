# Token modes — `standard` vs `lean`

Alexandria spends tokens in two places: **writing** the KB (ingest/build) and **reading** it
(ask/query/brief/compose). The per-vault `token_mode` in `.kb/config.json` trades richness for
cost. `standard` is the default; `lean` is the low-token mode — notes are tighter and reading is
bounded, so answers may be less nuanced, but every fact is still grounded and cited.

## What `lean` changes at write time

| Output | `standard` (default) | `lean` |
|---|---|---|
| Source notes | Full summary + key points + people/entities sections | ≤6 bullet key points; no narrative prose |
| Concepts / Entities | A note per significant idea/system | Notes only for **load-bearing** entities (in ≥2 sources, or central to the project); everything else becomes a glossary one-liner |
| Meeting notes | Context + discussion + decisions + actions | Date/attendees + **decisions + action items** + ≤4 discussion bullets |
| People profiles | Profile + involvement narrative | Frontmatter + one-line role + linked Involvement bullets only |
| Codebase docs | Per `codebase_depth` | Treat `codebase_depth` as `light` (overview + structure + entry points) unless the user explicitly asks for more |
| Canvas / extras | Offered after builds | Skipped unless asked |
| Subagent batching | ~8–12 sources per agent | ~15–20 per agent (fewer agents → less repeated build-spec/context overhead) |

**Never cut, in any mode:** grounding + citations, `[[wikilinks]]` (the graph is the product),
provenance (`kb_manifest.py record`), the post-write protocol, `Overview`/`_index`/`_review`
upkeep, and the quality bar's no-invention rule. **Lean cuts elaboration, not trust.**

## What `lean` changes at read time (ask / query / brief)

These first three are good discipline in **both** modes; lean makes them hard limits:

- **Search-first for named things.** If the question names a person/system/decision, `grep` the
  KB for it and open the matching note(s) directly — cheaper than walking Overview → index → links.
- **Stop when grounded.** Once the notes you've read support the answer, stop reading.
- **Never read `.raw/`** unless a source note's summary is insufficient — and say you did.

Lean limits: read at most **~5 notes / 1 link-hop** before answering. If that isn't enough,
give the best supported answer, name what else you'd read, and ask before continuing. Output is
**answer + citations** — skip suggested follow-ups and elaboration. Briefs/digests: tight
bullets, one screen.

## Switching

- Set at scaffold (kb-setup confirms; default `standard`). Change any time: edit
  `.kb/config.json` → `"token_mode": "lean"` — or just say "switch this vault to lean mode".
- **Per-request override** beats the config for one run: "answer lean", "do a lean ingest",
  or conversely "go deep on this one" in a lean vault.
- A strategy that works well: **lean for bulk/low-value folders, standard for the core docs** —
  richness compounds where it matters.
