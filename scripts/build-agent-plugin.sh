#!/usr/bin/env bash
# Regenerate skills/ from canonical .claude/skills without deleting a valid
# mirror before copying succeeds. Run one writer per checkout.
set -euo pipefail

ROOT_DIR="$(CDPATH= cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
if [[ ! -d .claude/skills || -L .claude/skills ]]; then
  printf 'Canonical .claude/skills must be a regular directory\n' >&2
  exit 1
fi

LOCK_DIR="$ROOT_DIR/.claude/.build-agent-plugin.lock"
STAGE=""
cleanup() {
  local build_exit=$?
  trap - EXIT
  if [[ -n "$STAGE" && ( -e "$STAGE/previous" || -L "$STAGE/previous" ) && ! -e skills && ! -L skills ]]; then
    if ! mv "$STAGE/previous" skills; then
      printf 'Mirror recovery failed; preserve and inspect %s\n' "$STAGE" >&2
      STAGE=""
      build_exit=1
    fi
  fi
  if [[ -n "$STAGE" ]] && ! rm -rf -- "$STAGE"; then
    printf 'Mirror staging cleanup failed; inspect %s\n' "$STAGE" >&2
    build_exit=1
  fi
  if ! rm -f -- "$LOCK_DIR/pid" || ! rmdir -- "$LOCK_DIR"; then
    printf 'Mirror lock cleanup failed; inspect %s\n' "$LOCK_DIR" >&2
    build_exit=1
  fi
  exit "$build_exit"
}

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  printf 'Another mirror build is active, or its lock needs owner review: %s\n' "$LOCK_DIR" >&2
  exit 1
fi
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
printf '%s\n' "$$" > "$LOCK_DIR/pid"
STAGE=$(mktemp -d "$ROOT_DIR/.skills-stage.XXXXXX")
cp -R .claude/skills "$STAGE/skills"
# Remove only known generated artifacts in this task-owned copy. Canonical and
# primary checkout metadata are never deleted by this cleanup.
find "$STAGE/skills" \( -name .DS_Store -o -name __pycache__ -o -name '*.pyc' -o -name '*.pyo' \) -prune -exec rm -rf -- {} +
if [[ -e skills || -L skills ]]; then mv skills "$STAGE/previous"; fi
mv "$STAGE/skills" skills
count=$(find skills -name SKILL.md | wc -l | tr -d ' ')
printf 'Mirrored .claude/skills → skills/ (%s skills, Agent Plugins spec 1.0.0)\n' "$count"
