#!/usr/bin/env python3
"""kb_repo_scan.py - analyze a code repository and emit a structured JSON report.

The agent turns this JSON into wiki pages: an architecture overview, a module
map, a Mermaid dependency graph, engineer/contributor profiles, and an
"ownership" map (who knows which part of the codebase).

Everything here is best-effort and heuristic. It never imports or executes
project code; it only reads files and shells out to `git`. Standard library only.

Usage:
  kb_repo_scan.py --path REPO [--max-import-files N] [--out FILE]

Output: JSON to stdout (or --out file). Keys:
  name, path, is_git, remote, head, branch, file_count, loc_total,
  languages[], structure[], entry_points[], dependencies{},
  internal_edges[], contributors[], hotspots[], ownership{}, recent_commits[]
"""
import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "env", "__pycache__", ".mypy_cache",
    ".pytest_cache", "dist", "build", ".next", ".nuxt", "out", "target", "vendor",
    ".idea", ".vscode", ".obsidian", "coverage", ".cache", ".gradle", "Pods",
    "bin", "obj", ".terraform", ".tox", "site-packages", ".turbo", ".parcel-cache",
}
LANG_BY_EXT = {
    ".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript", ".ts": "TypeScript",
    ".tsx": "TypeScript", ".go": "Go", ".rs": "Rust", ".java": "Java", ".kt": "Kotlin",
    ".rb": "Ruby", ".php": "PHP", ".cs": "C#", ".cpp": "C++", ".cc": "C++", ".c": "C",
    ".h": "C/C++ header", ".hpp": "C++ header", ".swift": "Swift", ".scala": "Scala",
    ".sh": "Shell", ".sql": "SQL", ".css": "CSS", ".scss": "SCSS", ".html": "HTML",
    ".vue": "Vue", ".svelte": "Svelte", ".dart": "Dart", ".ex": "Elixir", ".exs": "Elixir",
    ".clj": "Clojure", ".r": "R", ".m": "Objective-C", ".lua": "Lua", ".tf": "Terraform",
    ".yaml": "YAML", ".yml": "YAML", ".md": "Markdown",
}
CODE_EXTS = {e for e, l in LANG_BY_EXT.items()
             if l not in ("Markdown", "YAML", "CSS", "SCSS", "HTML")}


def run(path, *args, timeout=60):
    try:
        out = subprocess.run(["git", "-C", path, *args],
                             capture_output=True, text=True, timeout=timeout)
        return out.stdout if out.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def is_git_repo(path):
    return bool(run(path, "rev-parse", "--is-inside-work-tree").strip() == "true")


def top_segment(rel):
    """First path segment, or '(root)' for files at the repo root."""
    parts = rel.replace("\\", "/").split("/")
    return parts[0] if len(parts) > 1 else "(root)"


def count_lines(path):
    try:
        with open(path, "rb") as fh:
            return fh.read().count(b"\n") + 1
    except OSError:
        return 0


# ---------------------------------------------------------------- file walk
def walk_repo(root):
    files = []
    for dirpath, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for n in names:
            if n.startswith("."):
                continue
            full = os.path.join(dirpath, n)
            rel = os.path.relpath(full, root)
            files.append((rel, full))
    return files


def analyze_languages(files):
    by_lang = defaultdict(lambda: {"files": 0, "loc": 0})
    loc_total = 0
    for rel, full in files:
        ext = os.path.splitext(rel)[1].lower()
        lang = LANG_BY_EXT.get(ext)
        if not lang:
            continue
        lines = count_lines(full)
        loc_total += lines
        by_lang[lang]["files"] += 1
        by_lang[lang]["loc"] += lines
    langs = [{"language": k, **v} for k, v in by_lang.items()]
    langs.sort(key=lambda x: x["loc"], reverse=True)
    return langs, loc_total


def analyze_structure(root, files):
    """Top-level directories with file counts + a one-line role guess."""
    counts = Counter()
    for rel, _ in files:
        counts[top_segment(rel)] += 1
    role_hint = {
        "src": "source", "lib": "library code", "app": "application code",
        "test": "tests", "tests": "tests", "spec": "tests", "docs": "documentation",
        "doc": "documentation", "api": "API layer", "server": "backend/server",
        "client": "frontend/client", "web": "frontend", "frontend": "frontend",
        "backend": "backend", "cmd": "entrypoints (Go)", "internal": "internal packages",
        "pkg": "packages", "scripts": "scripts/tooling", "config": "configuration",
        "migrations": "database migrations", "models": "data models",
        "components": "UI components", "services": "services", "utils": "utilities",
        "public": "static assets", "assets": "static assets", "infra": "infrastructure",
        "terraform": "infrastructure", "k8s": "kubernetes manifests",
    }
    out = []
    for name, c in counts.most_common():
        out.append({"name": name, "files": c, "role": role_hint.get(name.lower(), "")})
    return out


def detect_entry_points(root, files):
    relset = {rel.replace("\\", "/") for rel, _ in files}
    hits = []
    candidates = [
        "main.py", "__main__.py", "app.py", "manage.py", "wsgi.py", "asgi.py",
        "index.js", "index.ts", "server.js", "server.ts", "main.go", "main.rs",
        "Main.java", "main.cpp", "index.php", "Program.cs",
    ]
    for rel in sorted(relset):
        base = rel.split("/")[-1]
        if base in candidates or rel in (f"src/{c}" for c in candidates):
            hits.append({"file": rel, "why": "conventional entry point"})

    # package.json scripts/bin/main
    pj = os.path.join(root, "package.json")
    if os.path.exists(pj):
        try:
            data = json.load(open(pj, encoding="utf-8"))
            if data.get("main"):
                hits.append({"file": data["main"], "why": "package.json main"})
            for k in (data.get("bin") or {}):
                hits.append({"file": str((data["bin"] or {})[k]), "why": f"bin: {k}"})
            start = (data.get("scripts") or {}).get("start")
            if start:
                hits.append({"file": "package.json", "why": f"npm start: {start}"})
        except (ValueError, OSError):
            pass

    for marker, why in [("Dockerfile", "container entrypoint"),
                        ("docker-compose.yml", "service composition"),
                        ("Makefile", "build/run targets")]:
        if marker in relset:
            hits.append({"file": marker, "why": why})
    # de-dup preserving order
    seen, uniq = set(), []
    for h in hits:
        key = (h["file"], h["why"])
        if key not in seen:
            seen.add(key); uniq.append(h)
    return uniq[:25]


def detect_dependencies(root):
    deps = {}

    def safe_read(name):
        p = os.path.join(root, name)
        try:
            return open(p, encoding="utf-8").read() if os.path.exists(p) else None
        except OSError:
            return None

    pj = safe_read("package.json")
    if pj:
        try:
            data = json.loads(pj)
            names = sorted(set(list((data.get("dependencies") or {}).keys()) +
                              list((data.get("devDependencies") or {}).keys())))
            if names:
                deps["package.json"] = names
        except ValueError:
            pass

    req = safe_read("requirements.txt")
    if req:
        names = []
        for line in req.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                names.append(re.split(r"[=<>!~ \[]", line)[0])
        if names:
            deps["requirements.txt"] = sorted(set(filter(None, names)))

    pp = safe_read("pyproject.toml")
    if pp:
        found = re.findall(r'^\s*"?([A-Za-z0-9_.\-]+)"?\s*[=>~]', pp, re.M)
        block = re.search(r"dependencies\s*=\s*\[(.*?)\]", pp, re.S)
        names = set()
        if block:
            names |= set(re.findall(r'["\']([A-Za-z0-9_.\-]+)', block.group(1)))
        if names:
            deps["pyproject.toml"] = sorted(names)

    gomod = safe_read("go.mod")
    if gomod:
        names = re.findall(r"^\s+([\w./\-]+)\s+v[\d]", gomod, re.M)
        if names:
            deps["go.mod"] = sorted(set(names))

    cargo = safe_read("Cargo.toml")
    if cargo:
        block = re.search(r"\[dependencies\](.*?)(\n\[|\Z)", cargo, re.S)
        if block:
            names = re.findall(r"^([A-Za-z0-9_\-]+)\s*=", block.group(1), re.M)
            if names:
                deps["Cargo.toml"] = sorted(set(names))

    gemfile = safe_read("Gemfile")
    if gemfile:
        names = re.findall(r"^\s*gem\s+['\"]([^'\"]+)", gemfile, re.M)
        if names:
            deps["Gemfile"] = sorted(set(names))

    return deps


# ---------------------------------------------------- internal import graph
PY_IMPORT = re.compile(r"^\s*(?:from\s+(\.[\w.]*|\w[\w.]*)\s+import|import\s+(\w[\w.]*))", re.M)
JS_IMPORT = re.compile(r"""(?:import[^'"]*from\s*|require\s*\(\s*|import\s*\(\s*)['"]([^'"]+)['"]""")


def build_import_graph(root, files, max_files):
    top_dirs = {top_segment(rel) for rel, _ in files} - {"(root)"}
    edges = Counter()
    scanned = 0
    for rel, full in files:
        ext = os.path.splitext(rel)[1].lower()
        if ext not in (".py", ".js", ".jsx", ".ts", ".tsx"):
            continue
        if scanned >= max_files:
            break
        scanned += 1
        src_dir = top_segment(rel)
        try:
            text = open(full, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if ext == ".py":
            for m in PY_IMPORT.finditer(text):
                mod = (m.group(1) or m.group(2) or "").lstrip(".")
                target = mod.split(".")[0]
                if target and target in top_dirs and target != src_dir:
                    edges[(src_dir, target)] += 1
        else:
            for m in JS_IMPORT.finditer(text):
                spec = m.group(1)
                if spec.startswith("."):
                    resolved = os.path.normpath(os.path.join(os.path.dirname(rel), spec))
                    target = top_segment(resolved.replace("\\", "/"))
                    if target and target in top_dirs and target != src_dir:
                        edges[(src_dir, target)] += 1
    return [{"from": a, "to": b, "weight": w}
            for (a, b), w in sorted(edges.items(), key=lambda x: -x[1])]


# ----------------------------------------------------------------- git data
def git_contributors(path):
    log = run(path, "log", "--no-merges", "-n", "8000",
              "--pretty=format:@@%an|%ae|%ad", "--date=short", "--numstat")
    if not log:
        return [], {}, []
    people = {}
    ownership = defaultdict(Counter)   # top_dir -> Counter(author -> commits-ish)
    cur = None
    for line in log.splitlines():
        if line.startswith("@@"):
            name, email, date = (line[2:].split("|") + ["", "", ""])[:3]
            key = name or email
            cur = people.setdefault(key, {
                "name": name, "email": email, "commits": 0,
                "insertions": 0, "deletions": 0, "first": date, "last": date,
            })
            cur["commits"] += 1
            if date:
                cur["first"] = min(cur["first"] or date, date)
                cur["last"] = max(cur["last"] or date, date)
        elif cur and line.strip():
            parts = line.split("\t")
            if len(parts) == 3:
                ins, dele, fpath = parts
                cur["insertions"] += int(ins) if ins.isdigit() else 0
                cur["deletions"] += int(dele) if dele.isdigit() else 0
                ownership[top_segment(fpath)][cur["name"] or cur["email"]] += 1
    contributors = sorted(people.values(), key=lambda p: p["commits"], reverse=True)
    own = {d: [{"name": n, "edits": c} for n, c in cnt.most_common(3)]
           for d, cnt in ownership.items()}
    return contributors[:40], own, []


def git_hotspots(path):
    log = run(path, "log", "-n", "4000", "--name-only", "--pretty=format:")
    if not log:
        return []
    c = Counter(l.strip() for l in log.splitlines() if l.strip())
    return [{"file": f, "changes": n} for f, n in c.most_common(25)]


def git_recent(path):
    log = run(path, "log", "-n", "15", "--no-merges",
              "--pretty=format:%h|%ad|%an|%s", "--date=short")
    out = []
    for line in log.splitlines():
        parts = line.split("|", 3)
        if len(parts) == 4:
            out.append({"sha": parts[0], "date": parts[1],
                        "author": parts[2], "subject": parts[3]})
    return out


# ----------------------------------------------------------------------- main
def scan(path, max_import_files):
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        sys.exit(f"error: not a directory: {path}")
    files = walk_repo(path)
    langs, loc_total = analyze_languages(files)
    report = {
        "name": os.path.basename(path),
        "path": path,
        "is_git": is_git_repo(path),
        "remote": None, "head": None, "branch": None,
        "file_count": len(files),
        "loc_total": loc_total,
        "languages": langs,
        "structure": analyze_structure(path, files),
        "entry_points": detect_entry_points(path, files),
        "dependencies": detect_dependencies(path),
        "internal_edges": build_import_graph(path, files, max_import_files),
        "contributors": [], "hotspots": [], "ownership": {}, "recent_commits": [],
    }
    if report["is_git"]:
        report["remote"] = (run(path, "remote", "get-url", "origin").strip() or
                            run(path, "config", "--get", "remote.origin.url").strip() or None)
        report["head"] = run(path, "rev-parse", "HEAD").strip() or None
        report["branch"] = run(path, "rev-parse", "--abbrev-ref", "HEAD").strip() or None
        report["contributors"], report["ownership"], _ = git_contributors(path)
        report["hotspots"] = git_hotspots(path)
        report["recent_commits"] = git_recent(path)
    return report


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--path", required=True)
    ap.add_argument("--max-import-files", type=int, default=4000)
    ap.add_argument("--out", default="-")
    args = ap.parse_args()
    report = scan(args.path, args.max_import_files)
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out == "-":
        print(text)
    else:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
