#!/usr/bin/env python3
"""kb_manifest.py - source provenance + delta tracking for an Obsidian KB.

A "KB" is a single project folder, e.g. Clients/Acme/Billing-Platform/.
Each KB owns:
  .raw/            immutable source files (the agent reads, never edits)
  .manifest.json   this script's state: per-source hash + which notes it produced

The agent calls this to answer two questions:
  - "what changed since last ingest?"  -> `status`
  - "remember that I ingested X into notes Y" -> `record`

Pure standard library. Works on Python 3.8+. No third-party deps.

Usage:
  kb_manifest.py status      --kb DIR
  kb_manifest.py record      --kb DIR --source REL [--notes a.md,b.md] [--kind KIND]
  kb_manifest.py record-repo --kb DIR --name NAME --path REPO [--commit SHA]
  kb_manifest.py forget      --kb DIR --source REL
  kb_manifest.py touch       --kb DIR

`status` prints JSON to stdout:
  {
    "kb": "...", "raw_dir": "...",
    "sources": [{"path": "...", "status": "new|changed|unchanged", "hash": "...", "bytes": N, "kind": "..."}],
    "deleted": ["path", ...],           # in manifest but missing from .raw/
    "repos":   [{"name": "...", "status": "new|changed|unchanged|missing", "head": "...", "last_commit": "..."}],
    "summary": {"new": N, "changed": N, "unchanged": N, "deleted": N}
  }
"""
import argparse
import datetime as _dt
import hashlib
import json
import os
import subprocess
import sys

MANIFEST_NAME = ".manifest.json"
RAW_DIR = ".raw"
SKIP_NAMES = {".DS_Store", ".manifest.json", "Thumbs.db"}


def now_iso():
    return _dt.datetime.now().astimezone().replace(microsecond=0).isoformat()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest_path(kb):
    return os.path.join(kb, MANIFEST_NAME)


def load_manifest(kb):
    p = manifest_path(kb)
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (json.JSONDecodeError, OSError):
            data = {}
    else:
        data = {}
    data.setdefault("kb", os.path.basename(os.path.abspath(kb)))
    data.setdefault("sources", {})
    data.setdefault("repos", {})
    return data


def save_manifest(kb, data):
    data["updated"] = now_iso()
    with open(manifest_path(kb), "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def iter_raw_files(kb):
    raw = os.path.join(kb, RAW_DIR)
    if not os.path.isdir(raw):
        return
    for root, dirs, files in os.walk(raw):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in files:
            if name in SKIP_NAMES or name.startswith("."):
                continue
            full = os.path.join(root, name)
            rel = os.path.relpath(full, raw)
            yield rel, full


def git(path, *args):
    try:
        out = subprocess.run(
            ["git", "-C", path, *args],
            capture_output=True, text=True, timeout=30,
        )
        if out.returncode != 0:
            return ""
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def cmd_status(args):
    kb = args.kb
    man = load_manifest(kb)
    known = man["sources"]
    seen = set()
    sources = []
    counts = {"new": 0, "changed": 0, "unchanged": 0, "deleted": 0}

    for rel, full in sorted(iter_raw_files(kb)):
        seen.add(rel)
        digest = sha256_file(full)
        prev = known.get(rel)
        if prev is None:
            st = "new"
        elif prev.get("hash") != digest:
            st = "changed"
        else:
            st = "unchanged"
        counts[st] += 1
        sources.append({
            "path": rel,
            "status": st,
            "hash": digest,
            "bytes": os.path.getsize(full),
            "kind": (prev or {}).get("kind", guess_kind(rel)),
        })

    deleted = sorted(set(known) - seen)
    counts["deleted"] = len(deleted)

    repos = []
    for name, info in sorted(man["repos"].items()):
        path = info.get("path", "")
        if not path or not os.path.isdir(path):
            repos.append({"name": name, "status": "missing", "head": None,
                          "last_commit": info.get("last_commit")})
            continue
        head = git(path, "rev-parse", "HEAD") or None
        last = info.get("last_commit")
        if last is None:
            st = "new"
        elif head and head != last:
            st = "changed"
        else:
            st = "unchanged"
        repos.append({"name": name, "status": st, "head": head, "last_commit": last,
                      "path": path})

    print(json.dumps({
        "kb": man.get("kb"),
        "raw_dir": os.path.join(kb, RAW_DIR),
        "sources": sources,
        "deleted": deleted,
        "repos": repos,
        "summary": counts,
    }, indent=2, ensure_ascii=False))


def guess_kind(rel):
    ext = os.path.splitext(rel)[1].lower()
    return {
        ".pdf": "pdf", ".md": "markdown", ".markdown": "markdown",
        ".txt": "text", ".docx": "doc", ".doc": "doc",
        ".csv": "data", ".json": "data", ".html": "web", ".htm": "web",
        ".vtt": "transcript", ".srt": "transcript",
    }.get(ext, "file")


def cmd_record(args):
    kb = args.kb
    man = load_manifest(kb)
    raw_full = os.path.join(kb, RAW_DIR, args.source)
    if not os.path.exists(raw_full):
        sys.exit(f"error: source not found in {RAW_DIR}/: {args.source}")
    notes = [n.strip() for n in (args.notes or "").split(",") if n.strip()]
    prev = man["sources"].get(args.source, {})
    man["sources"][args.source] = {
        "hash": sha256_file(raw_full),
        "bytes": os.path.getsize(raw_full),
        "kind": args.kind or prev.get("kind") or guess_kind(args.source),
        "notes": sorted(set(prev.get("notes", []) + notes)),
        "ingested_at": now_iso(),
    }
    save_manifest(kb, man)
    print(f"recorded {args.source} -> {len(man['sources'][args.source]['notes'])} note(s)")


def cmd_record_repo(args):
    kb = args.kb
    man = load_manifest(kb)
    head = git(args.path, "rev-parse", "HEAD") or args.commit
    man["repos"][args.name] = {
        "path": os.path.abspath(args.path),
        "last_commit": head,
        "scanned_at": now_iso(),
    }
    save_manifest(kb, man)
    print(f"recorded repo {args.name} @ {head}")


def cmd_forget(args):
    kb = args.kb
    man = load_manifest(kb)
    if args.source in man["sources"]:
        del man["sources"][args.source]
        save_manifest(kb, man)
        print(f"forgot {args.source}")
    else:
        print(f"not tracked: {args.source}")


def cmd_touch(args):
    save_manifest(args.kb, load_manifest(args.kb))
    print(f"manifest ready at {manifest_path(args.kb)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status"); s.add_argument("--kb", required=True); s.set_defaults(fn=cmd_status)
    r = sub.add_parser("record"); r.add_argument("--kb", required=True)
    r.add_argument("--source", required=True); r.add_argument("--notes", default="")
    r.add_argument("--kind", default=""); r.set_defaults(fn=cmd_record)
    rr = sub.add_parser("record-repo"); rr.add_argument("--kb", required=True)
    rr.add_argument("--name", required=True); rr.add_argument("--path", required=True)
    rr.add_argument("--commit", default=""); rr.set_defaults(fn=cmd_record_repo)
    f = sub.add_parser("forget"); f.add_argument("--kb", required=True)
    f.add_argument("--source", required=True); f.set_defaults(fn=cmd_forget)
    t = sub.add_parser("touch"); t.add_argument("--kb", required=True); t.set_defaults(fn=cmd_touch)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
