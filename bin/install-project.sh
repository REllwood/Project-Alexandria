#!/usr/bin/env bash
# install-project.sh — make alexandria available in ONE project (Claude Code,
# including the Claude desktop app / Cowork, which has no /plugin and loads
# skills from a project's .claude/ directory).
#
#   bash bin/install-project.sh [project-dir]   (default: current directory)
#
# Symlinks the skills, slash-commands, and subagents into <project>/.claude/,
# and copies the scaffolder + registry to ~/.alexandria/ for the first /kb.
set -euo pipefail

PKG="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJ="$(cd "${1:-$PWD}" && pwd)"

echo "Installing alexandria into project:"
echo "  $PROJ/.claude/"
mkdir -p "$PROJ/.claude/skills" "$PROJ/.claude/commands" "$PROJ/.claude/agents"

n=0
for d in "$PKG"/skills/*/; do
  [ -f "$d/SKILL.md" ] || continue
  ln -sfn "$d" "$PROJ/.claude/skills/$(basename "$d")"; n=$((n+1))
done
for c in "$PKG"/commands/*.md; do [ -e "$c" ] && ln -sfn "$c" "$PROJ/.claude/commands/$(basename "$c")"; done
for a in "$PKG"/agents/*.md;  do [ -e "$a" ] && ln -sfn "$a" "$PROJ/.claude/agents/$(basename "$a")"; done

mkdir -p "$HOME/.alexandria/bin"
cp "$PKG"/skills/kb/scripts/*.py "$HOME/.alexandria/bin/"

echo "  linked $n skills, $(ls "$PKG"/commands/*.md | wc -l | tr -d ' ') commands, $(ls "$PKG"/agents/*.md | wc -l | tr -d ' ') agents"
echo "  scaffolder -> ~/.alexandria/bin/"
cat <<EOF

Done. Now:
  1. In the Claude desktop app, open / work in:  $PROJ
  2. Start a new session there (or reload) so the skills load.
  3. Type  /kb  to scaffold your knowledge-base vault.

To use alexandria in another project, run this again with that path:
  bash bin/install-project.sh /path/to/other/project
EOF
