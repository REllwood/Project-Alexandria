#!/usr/bin/env python3
"""kb_doctor.py - preflight health check for an alexandria vault + environment.

Reports ✅ / ⚠️ / ❌ with one-line fixes, so a user can confirm everything is set
up right (or see exactly what to fix) without guessing. Standard library only.

Usage: kb_doctor.py [--vault DIR]
"""
import argparse, glob, json, os, shutil, subprocess, sys

OK, WARN, BAD = "✅", "⚠️", "❌"


def obsidian_installed():
    """Best-effort detection of the Obsidian desktop app across platforms.
    The vault is plain Markdown and works without it, but a non-technical user
    needs the app to actually see the graph, dashboards, and Canvas."""
    for p in ("/Applications/Obsidian.app",
              os.path.expanduser("~/Applications/Obsidian.app")):       # macOS
        if os.path.exists(p):
            return True
    if shutil.which("obsidian"):                                        # on PATH (Linux)
        return True
    for pat in ("/var/lib/flatpak/app/md.obsidian.Obsidian",            # flatpak
                os.path.expanduser("~/.local/share/flatpak/app/md.obsidian.Obsidian"),
                "/snap/obsidian",                                       # snap
                os.path.expanduser("~/Applications/Obsidian*.AppImage"),  # AppImage
                os.path.expanduser("~/.local/bin/obsidian*")):
        if glob.glob(pat):
            return True
    for env in ("LOCALAPPDATA", "PROGRAMFILES", "PROGRAMFILES(X86)"):    # Windows
        d = os.environ.get(env)
        if d and (os.path.exists(os.path.join(d, "Obsidian", "Obsidian.exe"))
                  or glob.glob(os.path.join(d, "Obsidian*", "Obsidian.exe"))):
            return True
    return False


def find_vault(arg):
    if arg:
        return os.path.abspath(arg)
    d = os.getcwd()
    while True:
        if os.path.exists(os.path.join(d, ".kb", "config.json")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    try:
        reg = json.load(open(os.path.expanduser("~/.alexandria/vaults.json")))
        if len(reg) == 1:
            return reg[0]["path"]
    except Exception:
        pass
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default="")
    args = ap.parse_args()
    rows = []
    def add(sym, msg, fix=""):
        rows.append((sym, msg, fix))

    add(OK if sys.version_info >= (3, 8) else BAD, f"Python {sys.version.split()[0]}", "need Python 3.8+")
    add(OK if (shutil.which("textutil") or shutil.which("pandoc")) else WARN,
        "Document reader (textutil/pandoc)",
        "macOS has textutil for .docx; .pptx/.xlsx use the bundled kb_extract.py (no install)")
    add(OK if shutil.which("git") else WARN, "git available", "needed for vault history + repo scans")
    add(OK if obsidian_installed() else WARN, "Obsidian app installed",
        "the vault is plain Markdown, but install the app to see graphs/dashboards: https://obsidian.md/download")

    reg = os.path.expanduser("~/.alexandria/vaults.json")
    add(OK if os.path.exists(reg) else WARN, "Vault registry", f"missing {reg} — run kb-setup or bin/install.sh")

    vault = find_vault(args.vault)
    if not vault or not os.path.isdir(vault):
        add(BAD, "Vault not found", "run /kb to set one up, or pass --vault PATH")
        return report(rows)
    add(OK, f"Vault: {vault}")
    add(OK if os.path.exists(f"{vault}/.kb/config.json") else BAD, ".kb/config.json present", "re-run kb_init vault")

    for s in ("kb_manifest.py", "kb_repo_scan.py", "kb_init.py", "kb_extract.py", "kb_review.py", "kb_doctor.py", "kb_actions.py"):
        add(OK if os.path.exists(f"{vault}/.kb/bin/{s}") else WARN, f".kb/bin/{s}", "re-run kb-setup to refresh runtime scripts")

    add(OK if os.path.isdir(f"{vault}/.obsidian") else WARN, ".obsidian config", "open the folder as a vault in Obsidian once")
    dv_files = os.path.exists(f"{vault}/.obsidian/plugins/dataview/main.js")
    try:
        dv_on = "dataview" in json.load(open(f"{vault}/.obsidian/community-plugins.json"))
    except Exception:
        dv_on = False
    if dv_files and dv_on:
        add(OK, "Dataview plugin (dashboards will render)")
    elif dv_on and not dv_files:
        add(BAD, "Dataview enabled but plugin files missing",
            "dashboards won't render — re-run kb-setup → [Auto-download Dataview], then reopen Obsidian")
    else:
        add(WARN, "Dataview plugin (live dashboards)",
            "optional — the wiki works without it; auto-download via kb-setup or install in Obsidian → Community plugins")

    clients = glob.glob(f"{vault}/Clients/*/")
    add(OK if clients else WARN, f"Clients: {len(clients)}", "add one with /kb (new client)")
    for man in sorted(glob.glob(f"{vault}/Clients/*/*/.manifest.json")):
        kb = os.path.dirname(man)
        rel = os.path.relpath(kb, f"{vault}/Clients")
        try:
            st = subprocess.run(["python3", f"{vault}/.kb/bin/kb_manifest.py", "status", "--kb", kb],
                                capture_output=True, text=True, timeout=30)
            summ = json.loads(st.stdout).get("summary", {})
            pend = summ.get("new", 0) + summ.get("changed", 0)
            add(OK if pend == 0 else WARN, f"{rel}: {pend} source(s) pending",
                "run /kb-update" if pend else "")
        except Exception:
            add(WARN, f"{rel}: manifest unreadable", "re-run kb-setup")
    report(rows)


def report(rows):
    print("\nalexandria · doctor\n" + "=" * 44)
    for sym, msg, fix in rows:
        print(f"{sym}  {msg}" + (f"   → {fix}" if sym != OK and fix else ""))
    bad = sum(1 for s, _, _ in rows if s == BAD)
    warn = sum(1 for s, _, _ in rows if s == WARN)
    print("=" * 44)
    print("All good — you're ready." if not bad and not warn
          else f"{bad} blocking · {warn} warning(s) — see the → fixes above.")


if __name__ == "__main__":
    main()
