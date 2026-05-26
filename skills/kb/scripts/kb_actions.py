#!/usr/bin/env python3
"""kb_actions.py - roll up open action items / commitments for a KB.

Scans the KB's notes for open `- [ ]` checkboxes (action items, usually written
into meeting notes), extracts the OWNER (the first [[wikilink]] on the line) and
a DUE date (ISO date, `📅 YYYY-MM-DD`, `due: …`, or `by …`), flags overdue and
due-soon, and writes `<KB>/Action Items.md` — a plain-Markdown dashboard that
works with ZERO plugins (the Overview's live Dataview TASK query complements it
for vaults that have Dataview).

This is the operational pulse for an account/project manager: what's open, who
owns it, what's overdue. It is a READ-ONLY rollup, regenerated on each build /
update / actions run — tick items off in their source note, not here.

Open questions (`questions.md`) also use `- [ ]` but are NOT action items, so
that file (and other generated/working files) is skipped.

Standard library only. Idempotent.

Usage:
  kb_actions.py --kb "<KB dir>" [--vault DIR] [--soon-days N] [--json]
"""
import argparse, datetime, glob, json, os, re

# `- [ ]` lines in these notes are open questions / generated dashboards / working
# files — not action items.
SKIP_FILES = {"questions", "_review", "Action Items", "glossary", "hot", "log", "_index", "Overview"}

OPEN_BOX_RE = re.compile(r'^\s*[-*]\s+\[ \]\s+(.*\S)\s*$')
WIKILINK_RE = re.compile(r'\[\[([^\]]+?)\]\]')
DATE_RE = re.compile(r'(\d{4}-\d{2}-\d{2})')
# explicit due markers take priority over a bare date elsewhere on the line
DUE_RE = re.compile(r'(?:📅|\bdue\b\s*[:=]?\s*|\bby\b\s+|\(by\s+)\s*(\d{4}-\d{2}-\d{2})', re.I)


def base(f):
    return os.path.splitext(os.path.basename(f))[0]


def parse_due(text):
    m = DUE_RE.search(text)
    if m:
        return m.group(1)
    m = DATE_RE.search(text)            # fallback: any ISO date on the line
    return m.group(1) if m else None


def clean_text(text):
    """Tidy one-line summary: keep [[wikilinks]] (navigable), strip the due markers."""
    t = re.sub(r'\s*📅\s*\d{4}-\d{2}-\d{2}', '', text)
    t = re.sub(r'\s*\(by\s+\d{4}-\d{2}-\d{2}\)', '', t, flags=re.I)
    t = re.sub(r'\s*\bdue\b\s*[:=]?\s*\d{4}-\d{2}-\d{2}', '', t, flags=re.I)
    t = re.sub(r'\s*\bby\s+\d{4}-\d{2}-\d{2}', '', t, flags=re.I)
    return re.sub(r'\s+', ' ', t).strip(' .·-')


def drop_leading_owner(text):
    """Drop a leading [[owner]] link (shown via the group header) — owner is always
    the first wikilink, so this only fires on the owner, never a mid-sentence link."""
    m = WIKILINK_RE.match(text)
    return text[m.end():].strip(' .·-') if m else text


def scan(kb):
    items = []
    for f in sorted(glob.glob(f"{kb}/**/*.md", recursive=True)):
        if "/.raw/" in f or base(f) in SKIP_FILES:
            continue
        note = base(f)
        try:
            content = open(f, encoding="utf-8").read()
        except OSError:
            continue
        for line in content.splitlines():
            m = OPEN_BOX_RE.match(line)
            if not m:
                continue
            raw = m.group(1)
            owner_m = WIKILINK_RE.search(raw)
            owner = (owner_m.group(1).split('|')[0].split('/')[-1].strip()
                     if owner_m else None)
            items.append({"text": clean_text(raw), "owner": owner,
                          "due": parse_due(raw), "note": note})
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", required=True)
    ap.add_argument("--vault", default="")
    ap.add_argument("--soon-days", type=int, default=7)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    KB = os.path.abspath(a.kb)
    today = datetime.date.today()
    today_iso = today.isoformat()
    client = os.path.basename(os.path.dirname(KB))
    project = os.path.basename(KB)
    items = scan(KB)

    def due_date(it):
        try:
            return datetime.date.fromisoformat(it["due"]) if it["due"] else None
        except ValueError:
            return None

    overdue, soon = [], []
    for it in items:
        d = due_date(it)
        it["overdue"] = bool(d and d < today)
        it["soon"] = bool(d and today <= d <= today + datetime.timedelta(days=a.soon_days))
        if it["overdue"]:
            overdue.append(it)
        elif it["soon"]:
            soon.append(it)
    unassigned = [it for it in items if not it["owner"]]
    overdue.sort(key=lambda it: it["due"] or "")

    summary = {"open": len(items), "overdue": len(overdue), "due_soon": len(soon),
               "unassigned": len(unassigned), "owners": len({it["owner"] for it in items if it["owner"]})}

    if a.json:
        print(json.dumps({"kb": project, "client": client, "as_of": today_iso,
                          "summary": summary, "items": items}, indent=2, ensure_ascii=False))
        return

    def marker(it):
        return "🔴 " if it["overdue"] else ("🟡 " if it["soon"] else "")

    parts = [f"""---
type: actions
title: "Action Items"
client: {client}
project: "{project}"
tags: [actions, tracker]
updated: {today_iso}
---

# ✅ Action Items — {project}
_Auto-generated rollup ({today_iso}). Read-only — tick items off in their source note; this is regenerated on each build / update / `/kb-actions` run._

> [!summary] {summary['open']} open · {summary['overdue']} overdue · {summary['due_soon']} due within {a.soon_days}d · {summary['unassigned']} unassigned
"""]

    if overdue:
        body = "\n".join(f"- **{it['due']}** — {it['text']}"
                         + ("" if it['owner'] else " · ⚠️ unassigned")
                         + f" · in [[{it['note']}]]" for it in overdue)
        parts.append(f"## 🔴 Overdue ({len(overdue)})\n{body}\n")
    else:
        parts.append("## 🔴 Overdue\n_None_ ✅\n")

    # master list, grouped by owner (owners alphabetical, Unassigned last)
    by_owner = {}
    for it in items:
        by_owner.setdefault(it["owner"] or "￿Unassigned", []).append(it)
    lines = []
    for owner in sorted(by_owner):
        group = sorted(by_owner[owner], key=lambda it: (it["due"] is None, it["due"] or ""))
        unassigned_group = owner == "￿Unassigned"
        label = "Unassigned" if unassigned_group else f"[[{owner}]]"
        lines.append(f"### {label} ({len(group)})")
        for it in group:
            text = it["text"] if unassigned_group else drop_leading_owner(it["text"])
            due = f" · due {it['due']}" if it["due"] else ""
            lines.append(f"- {marker(it)}{text}{due} · in [[{it['note']}]]")
    parts.append("## 👤 Open by owner\n" + ("\n".join(lines) if lines else "_None_ ✅") + "\n")

    open(f"{KB}/Action Items.md", "w", encoding="utf-8").write("\n".join(parts))
    print(f"Action Items.md → open:{summary['open']} overdue:{summary['overdue']} "
          f"due_soon:{summary['due_soon']} unassigned:{summary['unassigned']}")


if __name__ == "__main__":
    main()
