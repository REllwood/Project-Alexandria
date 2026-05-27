#!/usr/bin/env bash
# install.sh — make alexandria discoverable by Claude Code, Codex, and/or Cursor.
#
#   bash bin/install.sh [codex|claude|cursor|all]   (default: all)
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
  echo "Claude Code (install as a plugin — bundles all skills + commands + agents):"
  echo "  In your Claude Code session, run:"
  echo "    /plugin marketplace add REllwood/Project-Alexandria   # (or '$PKG' for this local clone)"
  echo "    /plugin                         # open the menu → install 'alexandria', then enable it"
  echo "  (using the /plugin menu avoids version-specific install syntax)"
}

install_cursor() {
  echo "Cursor (front-door /alex command — reads the skills from this clone):"
  mkdir -p "$HOME/.cursor/commands"
  cat > "$HOME/.cursor/commands/alex.md" <<EOF
# /alex — Alexandria knowledge base

You are **Alex**, the librarian for the Alexandria knowledge base — you've read
every client's documents, meetings, and decisions so the user doesn't have to.

The Alexandria skills live in this folder:
  $SKILLS

- If the user asked a **question**, follow \`$SKILLS/kb-ask/SKILL.md\` (confirm the
  client, then answer with citations to the notes — never invent).
- Otherwise (set up a vault, ingest sources, status, people, architecture,
  decisions, briefs, actions, export, …) follow \`$SKILLS/kb/SKILL.md\` (the router)
  and route to the right skill under \`$SKILLS\`.

Helper scripts (standard-library Python) are at \`$SKILLS/kb/scripts/\` and get copied
into each vault's \`.kb/bin/\`. Resolve the vault via ~/.alexandria/vaults.json or a
parent .kb/config.json.
EOF
  echo "  wrote $HOME/.cursor/commands/alex.md  ->  reads $SKILLS"
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
  cursor) install_cursor ;;
  all)    install_codex; echo; install_claude; echo; install_cursor ;;
  *) echo "usage: bash bin/install.sh [codex|claude|cursor|all]"; exit 1 ;;
esac
echo; install_runtime

cat <<EOF

Done. Next:
  • Claude Code: run the /plugin steps above, then type  /alex  to scaffold a vault.
  • Codex CLI:   say  "ask Alex to set up a knowledge base".
  • Cursor:      type  /alex  in chat.
The first run creates the vault and copies runtime scripts into <vault>/.kb/bin/.
EOF
