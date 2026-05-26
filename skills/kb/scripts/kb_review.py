#!/usr/bin/env python3
"""kb_review.py - generate a "Needs your attention" note for a KB.

Lint-as-a-note so the human always knows what to check: un-ingested sources,
broken links, genuinely-disconnected (orphan) notes, thin notes, and open
Decisions/questions. Writes `<KB>/_review.md`. Standard library only.

Link resolution is vault-wide (matches Obsidian). An "orphan" is a note with
NO links in AND NO links out (a truly isolated dot in the graph) — meeting/
source notes catalogued via Dataview are not flagged just for lacking backlinks.

Usage: kb_review.py --kb "<KB dir>" [--vault DIR]
"""
import argparse, datetime, glob, json, os, re, subprocess

SKIP = {"_index", "Overview", "hot", "log", "glossary", "questions", "_client",
        "Stakeholder Map", "People Relationships", "Decisions Log", "Action Items",
        "_review", "index"}


def base(f):
    return os.path.splitext(os.path.basename(f))[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kb", required=True)
    ap.add_argument("--vault", default="")
    a = ap.parse_args()
    KB = os.path.abspath(a.kb)
    VAULT = os.path.abspath(a.vault) if a.vault else os.path.dirname(os.path.dirname(os.path.dirname(KB)))
    TODAY = datetime.date.today().isoformat()
    client = os.path.basename(os.path.dirname(KB))
    people = f"{VAULT}/Clients/{client}/People"

    all_notes = [n for n in glob.glob(f"{VAULT}/**/*.md", recursive=True) if "/.raw/" not in n]
    scoped = [n for n in glob.glob(f"{KB}/**/*.md", recursive=True) + glob.glob(f"{people}/*.md")
              if "/.raw/" not in n]
    scoped_set = set(scoped)

    # resolvable names/aliases across the WHOLE vault (matches Obsidian)
    names, aliases = set(), set()
    for f in all_notes:
        names.add(base(f).lower())
        for m in re.findall(r'(?m)^aliases:\s*\[(.*?)\]', open(f, encoding="utf-8").read(2000)):
            for al in re.findall(r'"([^"]+)"', m):
                aliases.add(al.lower())
    resolvable = names | aliases

    inbound = {base(f): 0 for f in scoped}      # how many notes link TO this scoped note
    outbound = {base(f): 0 for f in scoped}     # how many links this scoped note has OUT
    broken = []
    for f in all_notes:
        fb = base(f)
        for m in re.findall(r'\[\[([^\]]+)\]\]', open(f, encoding="utf-8").read()):
            tgt = m.split('|')[0].split('#')[0].strip()
            if not tgt:
                continue
            b = tgt.split('/')[-1]
            if b in inbound:
                inbound[b] += 1
            if f in scoped_set:
                outbound[fb] = outbound.get(fb, 0) + 1
                if b.lower() not in resolvable and tgt.lower() not in resolvable:
                    broken.append((os.path.relpath(f, VAULT), tgt))

    orphans = [n for n in inbound if inbound[n] == 0 and outbound.get(n, 0) == 0 and n not in SKIP]
    thin = [os.path.relpath(f, VAULT) for f in scoped
            if base(f) not in SKIP
            and len(re.sub(r'^---.*?---', '', open(f, encoding="utf-8").read(), flags=re.S).strip()) < 200]

    pend = []
    try:
        st = subprocess.run(["python3", f"{VAULT}/.kb/bin/kb_manifest.py", "status", "--kb", KB],
                            capture_output=True, text=True, timeout=30)
        pend = [s["path"] for s in json.loads(st.stdout).get("sources", []) if s["status"] in ("new", "changed")]
    except Exception:
        pass

    qf = f"{KB}/questions.md"
    open_q = len(re.findall(r'(?m)^\s*- \[ \]', open(qf, encoding="utf-8").read())) if os.path.exists(qf) else 0
    open_dec = []
    for f in glob.glob(f"{KB}/Decisions/*.md"):
        h = open(f, encoding="utf-8").read(500)
        m = re.search(r'(?m)^status:\s*(\w+)', h)
        if m and m.group(1) not in ("accepted", "rejected", "superseded"):
            t = re.search(r'(?m)^title:\s*"(.*?)"', h)
            open_dec.append((t.group(1) if t else base(f), m.group(1)))

    def sec(title, items, fmt):
        if not items:
            return f"## {title}\n_None_ ✅\n"
        body = "\n".join(fmt(i) for i in items[:30])
        more = "" if len(items) <= 30 else f"\n…and {len(items)-30} more"
        return f"## {title} ({len(items)})\n{body}{more}\n"

    parts = [f"""---
type: review
title: "Needs your attention"
client: {client}
project: "{os.path.basename(KB)}"
tags: [review, lint]
updated: {TODAY}
---

# 🔎 Needs your attention — {os.path.basename(KB)}
_Auto-generated health check — regenerated on each build / update / lint ({TODAY})._

> [!summary] {len(pend)} pending sources · {len(broken)} broken links · {len(orphans)} orphans · {len(thin)} thin notes · {open_q} open questions · {len(open_dec)} open decisions
"""]
    parts.append(sec("📥 Un-ingested sources — run /kb-update", pend, lambda p: f"- `{p}`"))
    parts.append(sec("🔗 Broken links", broken, lambda b: f"- [[{b[1]}]] — in `{b[0]}`"))
    parts.append(sec("🌱 Disconnected notes (no links in or out)", orphans, lambda n: f"- [[{n}]]"))
    parts.append(sec("📏 Thin notes (<200 chars — enrich or merge)", thin, lambda p: f"- `{p}`"))
    parts.append(sec("⏳ Open decisions (unresolved)", open_dec, lambda d: f"- [[{d[0]}]] — *{d[1]}*"))
    parts.append(f"## ❓ Open questions\n{open_q} open — see [[questions|Open questions]].\n")
    open(f"{KB}/_review.md", "w", encoding="utf-8").write("\n".join(parts))
    print(f"_review.md → pending:{len(pend)} broken:{len(broken)} orphans:{len(orphans)} "
          f"thin:{len(thin)} open_q:{open_q} open_dec:{len(open_dec)}")


if __name__ == "__main__":
    main()
