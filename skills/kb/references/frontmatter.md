# Frontmatter taxonomy

Every note carries YAML frontmatter. Consistent `type` + fields are what power the graph colors, the file-explorer tints, dashboards, and queries. Dates are ISO `YYYY-MM-DD`. Links inside arrays use wikilink strings: `people: ["[[Jane Doe]]"]`.

## Shared fields (all notes)
- `type` — one of the types below (required).
- `client` — client name (required except `vault-index`).
- `project` — KB/project name (omit for client-level notes: `client`, `index` at client scope, person).
- `tags` — list; include the type as a tag.
- `status` — `active | draft | stale` (default `active`).
- `created`, `updated` — ISO dates. Bump `updated` on every edit.

## Types and their extra fields

| `type` | Lives in | Key extra fields |
|---|---|---|
| `vault-index` | `index.md` | — |
| `client` | `<Client>/_client.md` | — |
| `index` | `<KB>/_index.md` | `aliases?` |
| `source` | `Sources/` | `kind` (pdf/doc/meeting/web/data/repo), `source_file` (path in `.raw/`), `source_hash`, `people` |
| `person` | `<Client>/People/` | `name`, `role` (stakeholder/engineer/exec/sponsor/vendor/other), `job_title`, `org`, `email`, `contact`, `projects` |
| `concept` | `Concepts/` | `aliases` |
| `entity` | `Entities/` | `category` (system/product/org/service/dataset/tool) |
| `decision` | `Decisions/` | `status` (proposed/accepted/superseded/rejected), `deciders`, `date` |
| `meeting` | `Meetings/` | `date`, `attendees` |
| `architecture` | `Architecture/` | `repo`, `component` |
| `hotcache` | `hot.md` | — |
| `questions` | `questions.md` | — |
| `glossary` | `glossary.md` | — |

## Conventions
- **Provenance** — every generated note should link to at least one `source` note. Source notes carry `source_file` + `source_hash` so `update` can detect change.
- **People as links** — when a note mentions a person, link `[[<Person>]]` and add the person to its `people:` array when material. This builds the people graph.
- **Aliases** — use `aliases:` to capture other names/acronyms so links and search resolve (e.g. a concept "RAG" with alias "Retrieval-Augmented Generation").
- **No invented facts** — if a field is unknown, leave it blank rather than guessing. Unknowns worth resolving go in `questions.md`.
