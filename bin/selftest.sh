#!/usr/bin/env bash
# selftest.sh — quick confidence check (no external deps, no network).
# Scaffolds a throwaway vault, exercises the runtime scripts, cleans up.
# Run after cloning to confirm the tool works on your machine.
set -euo pipefail
PKG="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
S="$PKG/skills/kb/scripts"
pass() { echo "  ✅ $1"; }

echo "alexandria selftest"
python3 -m py_compile "$S"/*.py && pass "scripts compile"

T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
export HOME="$T"   # isolate: keep the throwaway vault out of your real ~/.alexandria registry
python3 "$S/kb_init.py" vault --path "$T/V" --name Test --client Acme --kb Demo >/dev/null && pass "scaffold vault + client/KB"
KB="$T/V/Clients/Acme/Demo"; BIN="$T/V/.kb/bin"
printf 'Kickoff with Jane Doe.' > "$KB/.raw/note.md"
python3 "$BIN/kb_manifest.py" status --kb "$KB" >/dev/null && pass "manifest status"
python3 "$BIN/kb_extract.py" "$KB/.raw/note.md" >/dev/null && pass "extract text"
python3 "$BIN/kb_doctor.py" --vault "$T/V" >/dev/null && pass "doctor"
python3 "$BIN/kb_review.py" --kb "$KB" >/dev/null && [ -f "$KB/_review.md" ] && pass "review note"
python3 "$BIN/kb_actions.py" --kb "$KB" >/dev/null && [ -f "$KB/Action Items.md" ] && pass "action items rollup"

echo "selftest passed ✅  (you're good to go)"
