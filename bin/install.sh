#!/usr/bin/env bash
# install.sh — make alexandria discoverable by Codex and/or Claude Code.
#
#   bash bin/install.sh [codex|claude|all]   (default: all)
#
# Codex / OpenCode discover skills recursively under ~/.codex/skills, so we
# symlink the whole skills/ dir there.
# Claude Code does NOT load user-level ~/.claude/skills — it loads skills from a
# project's .claude/skills or from an installed PLUGIN. So for Claude Code we
# print the local-plugin install steps (the plugin bundles skills+commands+agents).
set -euo pipefail

PKG="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-all}"
SKILLS="$PKG/skills"

link() { # link <src> <dest>
  mkdir -p "$(dirname "$2")"
  ln -sfn "$1" "$2"
  echo "  linked $2 -> $1"
}

install_codex() {
  echo "Codex / OpenCode (symlink — discovered recursively):"
  link "$SKILLS" "$HOME/.codex/skills/alexandria"
  [ -d "$HOME/.opencode" ] && link "$SKILLS" "$HOME/.opencode/skills/alexandria" || true
}

install_claude() {
  echo "Claude Code (install as a local plugin — bundles all skills + commands + agents):"
  echo "  In your Claude Code session, run:"
  echo "    /plugin marketplace add $PKG"
  echo "    /plugin                         # open the menu → install 'alexandria', then enable it"
  echo "  (using the /plugin menu avoids version-specific install syntax)"
}

install_runtime() {
  # A stable copy of the helper scripts for the very first scaffold (before any
  # vault exists). Lives alongside the vault registry at ~/.alexandria/.
  echo "Runtime scripts + registry home:"
  mkdir -p "$HOME/.alexandria/bin"
  cp "$SKILLS"/kb/scripts/*.py "$HOME/.alexandria/bin/"
  echo "  copied scaffolder -> $HOME/.alexandria/bin/"
}

case "$TARGET" in
  codex)  install_codex ;;
  claude) install_claude ;;
  all)    install_codex; echo; install_claude ;;
  *) echo "usage: bash bin/install.sh [codex|claude|all]"; exit 1 ;;
esac
echo; install_runtime

cat <<EOF

Done. Next:
  • Claude Code: run the /plugin steps above, then type  /kb  to scaffold a vault.
  • Codex CLI:   say  "set up a knowledge base"  to trigger the kb skill.
The first /kb run creates the vault and copies runtime scripts into <vault>/.kb/bin/.
EOF
