# Dashboards (optional)

The KB `_index.md` is a hand-maintained Map of Content and always works. For **live** dashboards driven by frontmatter, offer one of these. Both are optional and require a plugin; only add them if the user wants them.

## Option A — Bases (native, Obsidian ≥ 1.9.10)
Create `<KB>/dashboard.base`. Bases reads frontmatter and renders sortable tables/cards with no plugin install. Minimal example:

```yaml
filters:
  and:
    - 'file.inFolder(this.file.folder)'
views:
  - type: table
    name: Sources
    filters:
      and:
        - 'type == "source"'
    order: [file.name, kind, updated]
  - type: table
    name: People
    filters:
      and:
        - 'type == "person"'
    order: [name, role, org]
  - type: table
    name: Open decisions
    filters:
      and:
        - 'type == "decision"'
        - 'status != "accepted"'
    order: [date, title, status]
```
The Bases schema evolves between Obsidian versions — verify it renders, and adjust property names if Obsidian flags them. Do not ship a `.base` that errors; fall back to Option B or the MoC.

## Option B — Dataview (community plugin)
Embed queries directly in `_index.md` (or a `dashboard.md`). Requires the Dataview plugin enabled.

````markdown
## Sources
```dataview
TABLE kind, updated FROM "Clients/<Client>/<Project>/Sources" SORT updated DESC
```

## People (this client)
```dataview
TABLE role, org, job_title FROM "Clients/<Client>/People" WHERE type = "person" SORT role
```

## Open questions & decisions
```dataview
LIST FROM "Clients/<Client>/<Project>" WHERE type = "decision" AND status != "accepted"
```
````

## Default
If unsure, keep the clean wikilink MoC in `_index.md` (no plugin dependency) and mention these as upgrades.
