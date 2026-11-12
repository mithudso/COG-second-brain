#!/usr/bin/env bash
# COG Upstream Update Script
# Safely updates framework files (skills, docs, scripts) without touching your personal content.
#
# Usage:
#   ./cog-update.sh            Interactive update
#   ./cog-update.sh --check    Check for updates (fetches Git metadata; no framework-file changes)
#   ./cog-update.sh --dry-run  Preview changes (fetches Git metadata; no framework-file changes)
#   ./cog-update.sh --force    Update all framework files without prompting
#   ./cog-update.sh --validate Run packaging validator only
#   ./cog-update.sh --help     Show this help message

set -euo pipefail

COG_SCRIPT_ROOT="$(CDPATH= cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

# ── Configuration ────────────────────────────────────────────────────
REMOTE_NAME="cog-upstream"
REMOTE_URL="https://github.com/huytieu/COG-second-brain.git"
BRANCH="main"
VERSION_FILE="COG-VERSION"
UPSTREAM_REF="${REMOTE_NAME}/${BRANCH}"
VALIDATOR_SCRIPT="scripts/validate-agent-surface.sh"

# Framework files — these are safe to overwrite (your content is never in this list)
FRAMEWORK_FILES=(
  # Core docs
  "README.md"
  "SETUP.md"
  "AGENTS.md"
  "GEMINI.md"
  "CHANGELOG.md"
  "CONTRIBUTING.md"
  "LICENSE"
  "COG-VERSION"
  "cog-update.sh"
  "docs/AGENT-SUPPORT.md"
  "docs/SKILL-DISTILLATION.md"
  "WORKFLOW.md"
  ".claude/lib/checkpoint.sh"
  ".claude/lib/lane-classify.sh"
  ".github/MARKETPLACE.md"
  "scripts/validate-agent-surface.sh"

  # Claude Code skills
  ".claude/skills/onboarding/SKILL.md"
  ".claude/skills/braindump/SKILL.md"
  ".claude/skills/daily-brief/SKILL.md"
  ".claude/skills/weekly-checkin/SKILL.md"
  ".claude/skills/knowledge-consolidation/SKILL.md"
  ".claude/skills/url-dump/SKILL.md"
  ".claude/skills/loop-engineering/SKILL.md"
  ".claude/skills/scout/SKILL.md"
  ".claude/skills/update-cog/SKILL.md"
  ".claude/skills/team-brief/SKILL.md"
  ".claude/skills/comprehensive-analysis/SKILL.md"
  ".claude/skills/meeting-transcript/SKILL.md"
  ".claude/skills/auto-research/SKILL.md"
  ".claude/skills/create-user-story/SKILL.md"
  ".claude/skills/generate-prd/SKILL.md"
  ".claude/skills/generate-release-notes/SKILL.md"
  ".claude/skills/export-open-issues/SKILL.md"
  ".claude/skills/publish-to-confluence/SKILL.md"
  ".claude/skills/update-knowledge-base/SKILL.md"
  ".claude/skills/memory-hygiene/SKILL.md"
  ".claude/skills/content-factory/SKILL.md"
  ".claude/skills/closed-loop/SKILL.md"
  ".claude/skills/ultragoal/SKILL.md"
  ".claude/skills/harvest/SKILL.md"
  ".claude/skills/retro/SKILL.md"
  ".claude/skills/review-cockpit/SKILL.md"
  ".claude/skills/no-ai-slop/SKILL.md"
  ".claude/skills/slop-gate/SKILL.md"
  ".claude/skills/slop-gate/scripts/scan.py"
  ".claude/skills/voice-baseline/SKILL.md"
  ".claude/skills/voice-baseline/scripts/census.py"
  ".claude/skills/editorial-illustrations/SKILL.md"
  ".claude/skills/data-forms/SKILL.md"
  ".claude/skills/museum-art/SKILL.md"
  ".claude/skills/daily-journal/SKILL.md"
  ".claude/skills/taste-skill/SKILL.md"
  ".claude/skills/product-ui-taste/SKILL.md"

  # Skill reference files (bundled lookup material, loaded on demand)
  ".claude/skills/closed-loop/references/report-template.html"
  ".claude/skills/closed-loop/references/spec-template.md"
  ".claude/skills/data-forms/references/forms.md"
  ".claude/skills/editorial-illustrations/references/design-system.md"
  ".claude/skills/editorial-illustrations/references/elements.md"
  ".claude/skills/editorial-illustrations/references/worked-examples.md"
  ".claude/skills/knowledge-consolidation/references/templates.md"
  ".claude/skills/museum-art/references/_synthesis.md"
  ".claude/skills/museum-art/references/artic.md"
  ".claude/skills/museum-art/references/cleveland.md"
  ".claude/skills/museum-art/references/getty.md"
  ".claude/skills/museum-art/references/met.md"
  ".claude/skills/museum-art/references/nga.md"
  ".claude/skills/museum-art/references/rijksmuseum.md"
  ".claude/skills/museum-art/references/smithsonian.md"
  ".claude/skills/museum-art/references/smk.md"
  ".claude/skills/onboarding/references/profile-templates.md"
  ".claude/skills/onboarding/references/welcome-guide.md"
  ".claude/skills/retro/references/retro-template.md"
  ".claude/skills/review-cockpit/references/session-review-template.md"
  ".claude/skills/product-ui-taste/references/block-skeletons.md"
  ".claude/skills/product-ui-taste/references/canonical-sources.md"
  ".claude/skills/product-ui-taste/references/install-commands.md"
  ".claude/skills/taste-skill/references/canonical-sources.md"
  ".claude/skills/taste-skill/references/design-systems-install.md"
  ".claude/skills/taste-skill/references/liquid-glass.md"
  ".claude/skills/taste-skill/references/motion-skeletons.md"
  ".claude/skills/taste-skill/references/pattern-vocabulary.md"
  ".claude/skills/team-brief/references/agent-prompts.md"
  ".claude/skills/team-brief/references/brief-frontmatter.md"
  ".claude/skills/team-brief/references/publish-templates.md"

  # Role packs
  ".claude/roles/_template.md"
  ".claude/roles/product-manager.md"
  ".claude/roles/engineer.md"
  ".claude/roles/engineering-lead.md"
  ".claude/roles/designer.md"
  ".claude/roles/founder.md"
  ".claude/roles/marketer.md"

  # Worker agents
  ".claude/agents/worker-data-collector.md"
  ".claude/agents/worker-researcher.md"
  ".claude/agents/worker-file-ops.md"
  ".claude/agents/worker-executor.md"
  ".claude/agents/worker-publisher.md"
  ".claude/agents/brief-people-updater.md"
  ".claude/agents/task-verifier.md"
  ".claude/agents/integration-verifier.md"
  ".claude/agents/fix-agent.md"
  ".claude/agents/harvest-curator.md"

  # People CRM
  "05-knowledge/people/README.md"
  "06-templates/people-profile-template.md"

  # Framework config
  "CLAUDE.md"

  # Kiro powers
  ".kiro/powers/cog-onboarding/POWER.md"
  ".kiro/powers/cog-braindump/POWER.md"
  ".kiro/powers/cog-daily-brief/POWER.md"
  ".kiro/powers/cog-weekly-checkin/POWER.md"
  ".kiro/powers/cog-knowledge-consolidation/POWER.md"
  ".kiro/powers/cog-url-dump/POWER.md"
  ".kiro/powers/cog-update/POWER.md"

  # Antigravity (agy CLI + IDE)
  ".agents/rules/cog.md"
  ".agents/skills/auto-research/SKILL.md"
  ".agents/skills/braindump/SKILL.md"
  ".agents/skills/closed-loop/SKILL.md"
  ".agents/skills/comprehensive-analysis/SKILL.md"
  ".agents/skills/content-factory/SKILL.md"
  ".agents/skills/create-user-story/SKILL.md"
  ".agents/skills/daily-brief/SKILL.md"
  ".agents/skills/daily-journal/SKILL.md"
  ".agents/skills/data-forms/SKILL.md"
  ".agents/skills/editorial-illustrations/SKILL.md"
  ".agents/skills/export-open-issues/SKILL.md"
  ".agents/skills/generate-prd/SKILL.md"
  ".agents/skills/generate-release-notes/SKILL.md"
  ".agents/skills/harvest/SKILL.md"
  ".agents/skills/knowledge-consolidation/SKILL.md"
  ".agents/skills/loop-engineering/SKILL.md"
  ".agents/skills/meeting-transcript/SKILL.md"
  ".agents/skills/memory-hygiene/SKILL.md"
  ".agents/skills/museum-art/SKILL.md"
  ".agents/skills/no-ai-slop/SKILL.md"
  ".agents/skills/slop-gate/SKILL.md"
  ".agents/skills/voice-baseline/SKILL.md"
  ".agents/skills/onboarding/SKILL.md"
  ".agents/skills/product-ui-taste/SKILL.md"
  ".agents/skills/publish-to-confluence/SKILL.md"
  ".agents/skills/retro/SKILL.md"
  ".agents/skills/review-cockpit/SKILL.md"
  ".agents/skills/scout/SKILL.md"
  ".agents/skills/taste-skill/SKILL.md"
  ".agents/skills/team-brief/SKILL.md"
  ".agents/skills/ultragoal/SKILL.md"
  ".agents/skills/update-cog/SKILL.md"
  ".agents/skills/update-knowledge-base/SKILL.md"
  ".agents/skills/url-dump/SKILL.md"
  ".agents/skills/weekly-checkin/SKILL.md"
  ".agents/agents/brief-people-updater.md"
  ".agents/agents/worker-data-collector.md"
  ".agents/agents/worker-executor.md"
  ".agents/agents/worker-file-ops.md"
  ".agents/agents/worker-publisher.md"
  ".agents/agents/worker-researcher.md"
  ".agents/agents/task-verifier.md"
  ".agents/agents/integration-verifier.md"
  ".agents/agents/fix-agent.md"
  ".agents/agents/harvest-curator.md"

  # Gemini CLI
  ".gemini/commands/onboarding.toml"
  ".gemini/commands/braindump.toml"
  ".gemini/commands/daily-brief.toml"
  ".gemini/commands/weekly-checkin.toml"
  ".gemini/commands/knowledge-consolidation.toml"
  ".gemini/commands/url-dump.toml"
  ".gemini/commands/update-cog.toml"
  ".gemini/skills/onboarding.md"
  ".gemini/skills/braindump.md"
  ".gemini/skills/daily-brief.md"
  ".gemini/skills/weekly-checkin.md"
  ".gemini/skills/knowledge-consolidation.md"
  ".gemini/skills/url-dump.md"
  ".gemini/skills/update-cog.md"

  # Plugin metadata
  ".claude-plugin/plugin.json"
  ".cursor-plugin/plugin.json"
  ".cursorrules"
  "marketplace-entry.json"
  "plugin.json"
  "scripts/build-agent-plugin.sh"

  # Git infrastructure
  ".gitignore"

  # Public maintenance helpers and static contributor references
  ".editorconfig"
  ".gitattributes"
  ".github/CODEOWNERS"
  ".github/ISSUE_TEMPLATE/bug_report.md"
  ".github/ISSUE_TEMPLATE/feature_request.md"
  ".github/PULL_REQUEST_TEMPLATE.md"
  ".github/SECURITY.md"
  ".github/copilot-instructions.md"
  ".github/dependabot.yml"
  ".github/workflows/ci.yml"
  "docs/ARCHITECTURE.md"
  "docs/COMPONENTS.md"
  "docs/DEVELOPMENT.md"
  "docs/INSTALLATION.md"
  "docs/MCP.md"
  "docs/SECURITY.md"
  "docs/TESTING.md"
  "docs/archive/README.md"
  "docs/caching-and-optimization.md"
  "docs/external-calls.md"
  "docs/integrations-and-assumptions.md"
  "docs/known-issues.md"
  "docs/logging.md"
  "docs/onboarding.md"
  "docs/requirements.md"
  "docs/runbooks/framework-update.md"
  "docs/runbooks/validation.md"
  "docs/wiki/index.md"
  "docs/wiki/maintenance.md"
  "scripts/doc_indexes.py"
  "tests/test_maintenance.py"
)

# ── Helpers ──────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

info()  { echo -e "${CYAN}ℹ${RESET}  $*"; }
ok()    { echo -e "${GREEN}✓${RESET}  $*"; }
warn()  { echo -e "${YELLOW}⚠${RESET}  $*"; }
err()   { echo -e "${RED}✗${RESET}  $*" >&2; }

usage() {
  cat <<'EOF'
COG Upstream Update Script

Updates framework files (skills, docs, scripts) from the official COG repo
without touching your personal content (braindumps, profiles, notes).

Usage:
  ./cog-update.sh            Interactive update (prompts per file)
  ./cog-update.sh --check    Check for updates (fetches Git metadata; no framework-file changes)
  ./cog-update.sh --dry-run  Preview changes (fetches Git metadata; no framework-file changes)
  ./cog-update.sh --force    Update all framework files without prompting
  ./cog-update.sh --validate Run packaging validator only
  ./cog-update.sh --help     Show this help message

How it works:
  1. Adds/fetches the upstream remote (cog-upstream)
  2. Compares each framework file against the upstream version
  3. Offers to update changed files (interactive mode) or updates all (--force)
  4. Warns if your working tree is already dirty before replacing framework files
  5. Runs the packaging validator after updates when available
  6. Only listed framework paths change; personal notes and profiles are outside that list
     (tracked framework README/template files inside vault folders are included)

Run from a COG checkout. Linked framework paths are rejected. Review local edits before replacing framework files.
EOF
}

# ── Ensure remote exists & fetch ─────────────────────────────────────
ensure_remote() {
  if ! git remote get-url "$REMOTE_NAME" &>/dev/null; then
    info "Adding remote ${BOLD}${REMOTE_NAME}${RESET} → ${REMOTE_URL}"
    git remote add "$REMOTE_NAME" "$REMOTE_URL"
  else
    local configured_url
    configured_url=$(git remote get-url "$REMOTE_NAME")
    configured_url="${configured_url%/}"
    case "$configured_url" in
      "$REMOTE_URL"|"https://github.com/huytieu/COG-second-brain"|"git@github.com:huytieu/COG-second-brain.git"|"ssh://git@github.com/huytieu/COG-second-brain.git") ;;
      *) err "Refusing $REMOTE_NAME: its URL does not identify the official COG upstream"; return 1 ;;
    esac
  fi
  info "Fetching latest from ${BOLD}${REMOTE_NAME}/${BRANCH}${RESET}..."
  git fetch "$REMOTE_NAME" "$BRANCH" --quiet
  UPSTREAM_REF=$(git rev-parse --verify "${REMOTE_NAME}/${BRANCH}^{commit}")
  ok "Fetched upstream metadata"
}

# ── Get local and upstream versions ──────────────────────────────────
local_version() {
  if [[ -f "$VERSION_FILE" ]]; then
    cat "$VERSION_FILE" | tr -d '[:space:]'
  else
    echo "unknown"
  fi
}

upstream_version() {
  git show "${UPSTREAM_REF}:${VERSION_FILE}" 2>/dev/null | tr -d '[:space:]' || echo "unknown"
}

# ── Diff a single file ──────────────────────────────────────────────
file_has_changes() {
  local file="$1" entry temporary comparison_exit=0
  entry=$(git ls-tree "$UPSTREAM_REF" -- "$file") || { err "Cannot inspect upstream path: $file"; exit 2; }
  [[ -n "$entry" ]] || return 1  # A genuinely absent upstream path is skipped.
  case "${entry%% *}" in
    100755) [[ -f "$file" && -x "$file" ]] || return 0 ;;
    100644) if [[ ! -f "$file" || -x "$file" ]]; then return 0; fi ;;
    *) err "Unsupported upstream file mode for $file"; exit 2 ;;
  esac
  temporary=$(mktemp "${TMPDIR:-/tmp}/cog-compare.XXXXXX") || exit 2
  if ! git show "${UPSTREAM_REF}:${file}" > "$temporary"; then
    rm -f "$temporary"
    err "Cannot compare upstream framework file: $file"
    exit 2
  fi
  cmp -s "$temporary" "$file" || comparison_exit=$?
  rm -f "$temporary"
  case "$comparison_exit" in
    0) return 1 ;;
    1) return 0 ;;
    *) err "Cannot compare local framework file: $file"; exit 2 ;;
  esac
}

# ── Update a single file from upstream ───────────────────────────────
validate_framework_path() {
  local remaining="$1" current="." segment
  while [[ -n "$remaining" ]]; do
    segment="${remaining%%/*}"
    if [[ "$remaining" == */* ]]; then remaining="${remaining#*/}"; else remaining=""; fi
    if [[ -z "$segment" || "$segment" == ".." ]]; then
      err "Refusing invalid framework path: $1"
      return 1
    fi
    current="$current/$segment"
    if [[ -L "$current" ]]; then
      err "Refusing linked framework path: $1"
      return 1
    fi
  done
  if [[ -e "$1" && ! -f "$1" ]]; then
    err "Refusing non-regular framework destination: $1"
    return 1
  fi
}

update_file() {
  local file="$1" dir temporary object_mode
  validate_framework_path "$file" || return 1
  dir=$(dirname "$file")
  [[ "$dir" == "." ]] || mkdir -p "$dir"
  temporary=$(mktemp "$dir/.cog-update.XXXXXX")
  if ! git show "${UPSTREAM_REF}:${file}" > "$temporary"; then
    rm -f "$temporary"
    err "Could not read upstream framework file: $file"
    return 1
  fi
  object_mode=$(git ls-tree "$UPSTREAM_REF" -- "$file") || { rm -f "$temporary"; return 1; }
  object_mode="${object_mode%% *}"
  case "$object_mode" in
    100644|100755) ;;
    *) rm -f "$temporary"; err "Unsupported upstream file mode for $file"; return 1 ;;
  esac
  if ! chmod "${object_mode#100}" "$temporary" || ! mv -f "$temporary" "$file"; then
    rm -f "$temporary"
    err "Could not replace framework file: $file"
    return 1
  fi
}

# Unique, private backups stay ignored by the repository's backup rules.
backup_file() {
  local file="$1" backup
  validate_framework_path "$file" || return 1
  if [[ -f "$file" ]]; then
    backup=$(mktemp "${file}.backup-$(date +%Y%m%d-%H%M%S)-XXXXXX")
    if ! cp "$file" "$backup"; then rm -f "$backup"; return 1; fi
    printf '%s\n' "$backup"
  fi
}

worktree_is_dirty() {
  [[ -n "$(git status --porcelain)" ]]
}

warn_if_dirty() {
  if worktree_is_dirty; then
    warn "Your working tree has uncommitted changes. Framework updates can replace local framework edits; review before applying."
  fi
}

# Regenerate the Agent Plugins standard mirror (root skills/) after framework
# updates so it never drifts from the updated .claude/skills/.
rebuild_agent_plugin() {
  if [[ -x "scripts/build-agent-plugin.sh" ]]; then
    ./scripts/build-agent-plugin.sh || { err "Agent plugin mirror rebuild failed"; return 1; }
  fi
}

run_validator() {
  validate_framework_path "$VALIDATOR_SCRIPT" || return 1
  if [[ -x "$VALIDATOR_SCRIPT" ]]; then
    echo ""
    info "Running ${BOLD}${VALIDATOR_SCRIPT}${RESET}..."
    if "$VALIDATOR_SCRIPT"; then
      ok "Packaging validation passed"
      return 0
    else
      warn "Packaging validation reported issues. Review before committing."
      return 1
    fi
  else
    err "Validator not executable at ${VALIDATOR_SCRIPT}; no validation was performed"
    return 1
  fi
}

# ── Main logic ───────────────────────────────────────────────────────
main() {
  local mode="interactive"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --check)    mode="check";    shift ;;
      --dry-run)  mode="dry-run";  shift ;;
      --force)    mode="force";    shift ;;
      --validate) mode="validate"; shift ;;
      --help|-h)  usage; exit 0 ;;
      *) err "Unknown option: $1"; usage; exit 1 ;;
    esac
  done

  # Resolve paths from the checkout containing this script, not the caller.
  cd "$COG_SCRIPT_ROOT"

  # Sanity check — are we in a git repo?
  if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    err "Not inside a git repository. Run this from your COG folder."
    exit 1
  fi

  local repository_root
  repository_root=$(git rev-parse --show-toplevel)
  repository_root=$(CDPATH= cd "$repository_root" && pwd -P)
  if [[ "$repository_root" != "$COG_SCRIPT_ROOT" ]]; then
    err "The updater must live at the COG Git checkout root"
    exit 1
  fi

  if [[ ! -f "$VERSION_FILE" || ! -f .claude-plugin/plugin.json ]]; then
    err "This is not a COG framework checkout"
    exit 1
  fi

  if [[ "$mode" == "validate" ]]; then
    run_validator
    exit $?
  fi

  echo ""
  echo -e "${BOLD}COG Upstream Update${RESET}"
  echo -e "─────────────────────"
  echo ""

  for file in "${FRAMEWORK_FILES[@]}"; do validate_framework_path "$file" || return 1; done
  ensure_remote

  local lv uv
  lv=$(local_version)
  uv=$(upstream_version)

  info "Local version:    ${BOLD}${lv}${RESET}"
  info "Upstream version: ${BOLD}${uv}${RESET}"
  echo ""

  if [[ "$mode" == "interactive" || "$mode" == "force" ]]; then
    warn_if_dirty
    [[ -n "$(git status --porcelain)" ]] && echo ""
  fi

  if [[ "$uv" == "unknown" ]]; then
    err "Could not read upstream version. Check your internet connection."
    exit 1
  fi

  # Serialize comparison and replacement so concurrent revisions cannot interleave.
  if [[ "$mode" == "interactive" || "$mode" == "force" ]]; then
    UPDATE_LOCK="$COG_SCRIPT_ROOT/.cog-update.lock"
    if ! mkdir "$UPDATE_LOCK" 2>/dev/null; then
      err "Another updater is active, or its lock needs owner review: $UPDATE_LOCK"
      return 2
    fi
    trap 'rmdir -- "$UPDATE_LOCK" 2>/dev/null || true' EXIT
    trap 'exit 130' INT
    trap 'exit 143' TERM
  fi

  # Collect changed files
  local changed=()
  local new_files=()
  for file in "${FRAMEWORK_FILES[@]}"; do
    if file_has_changes "$file"; then
      if [[ -f "$file" ]]; then
        changed+=("$file")
      else
        new_files+=("$file")
      fi
    fi
  done

  local total=$(( ${#changed[@]} + ${#new_files[@]} ))

  if [[ $total -eq 0 ]]; then
    ok "Everything is up to date! (v${lv})"
    exit 0
  fi

  info "${BOLD}${#changed[@]}${RESET} file(s) changed, ${BOLD}${#new_files[@]}${RESET} new file(s) available"
  echo ""

  # ── Check mode ───────────────────────────────────────────────────
  if [[ "$mode" == "check" ]]; then
    if [[ ${#changed[@]} -gt 0 ]]; then
      echo -e "${BOLD}Changed:${RESET}"
      for f in "${changed[@]}"; do echo "  ~ $f"; done
    fi
    if [[ ${#new_files[@]} -gt 0 ]]; then
      echo -e "${BOLD}New:${RESET}"
      for f in "${new_files[@]}"; do echo "  + $f"; done
    fi
    echo ""
    info "Run ${BOLD}./cog-update.sh${RESET} to update, or ${BOLD}./cog-update.sh --dry-run${RESET} to preview."
    exit 0
  fi

  # ── Dry-run mode ─────────────────────────────────────────────────
  if [[ "$mode" == "dry-run" ]]; then
    echo -e "${BOLD}Dry run — no changes will be made:${RESET}"
    echo ""
    if [[ ${#changed[@]} -gt 0 ]]; then
      echo "Would update:"
      for f in "${changed[@]}"; do echo "  ~ $f"; done
    fi
    if [[ ${#new_files[@]} -gt 0 ]]; then
      echo "Would create:"
      for f in "${new_files[@]}"; do echo "  + $f"; done
    fi
    echo ""
    info "Run ${BOLD}./cog-update.sh --force${RESET} to apply all, or ${BOLD}./cog-update.sh${RESET} for interactive mode."
    exit 0
  fi

  # ── Force mode ───────────────────────────────────────────────────
  if [[ "$mode" == "force" ]]; then
    local updated=0
    # Empty-array expansion under nounset fails on macOS Bash 3.2.
    local apply_files=()
    if [[ ${#changed[@]} -gt 0 ]]; then apply_files+=("${changed[@]}"); fi
    if [[ ${#new_files[@]} -gt 0 ]]; then apply_files+=("${new_files[@]}"); fi
    for f in "${apply_files[@]}"; do
      if [[ -f "$f" ]]; then
        backup_file "$f" >/dev/null
      fi
      update_file "$f"
      ok "Updated: $f"
      updated=$((updated + 1))
    done
    echo ""
    ok "Updated ${updated} file(s) to v${uv}"
    info "Private backups saved as *.backup-YYYYMMDD-HHMMSS-XXXXXX alongside originals"
    rebuild_agent_plugin
    run_validator
    exit 0
  fi

  # ── Interactive mode ─────────────────────────────────────────────
  local updated=0 skipped=0

  # New files first
  if [[ ${#new_files[@]} -gt 0 ]]; then
    echo -e "${BOLD}New files available:${RESET}"
    for f in "${new_files[@]}"; do
      echo -ne "  ${GREEN}+${RESET} ${f} — add? [Y/n] "
      read -r answer
      if [[ -z "$answer" || "$answer" =~ ^[Yy] ]]; then
        update_file "$f"
        ok "Added: $f"
        updated=$((updated + 1))
      else
        warn "Skipped: $f"
        skipped=$((skipped + 1))
      fi
    done
    echo ""
  fi

  # Changed files
  if [[ ${#changed[@]} -gt 0 ]]; then
    echo -e "${BOLD}Changed files:${RESET}"
    for f in "${changed[@]}"; do
      echo -ne "  ${YELLOW}~${RESET} ${f} — update? [Y/n/d(iff)/b(ackup+update)] "
      read -r answer
      case "$answer" in
        d|D|diff)
          diff --color=auto <(cat "$f") <(git show "${UPSTREAM_REF}:${f}") || true
          echo -ne "  Update this file? [Y/n/b] "
          read -r answer2
          if [[ -z "$answer2" || "$answer2" =~ ^[Yy] ]]; then
            update_file "$f"
            ok "Updated: $f"
            updated=$((updated + 1))
          elif [[ "$answer2" =~ ^[Bb] ]]; then
            local bk
            bk=$(backup_file "$f")
            update_file "$f"
            ok "Updated: $f (backup: $bk)"
            updated=$((updated + 1))
          else
            warn "Skipped: $f"
            skipped=$((skipped + 1))
          fi
          ;;
        b|B)
          local bk
          bk=$(backup_file "$f")
          update_file "$f"
          ok "Updated: $f (backup: $bk)"
          updated=$((updated + 1))
          ;;
        n|N|no|NO|No)
          warn "Skipped: $f"
          skipped=$((skipped + 1))
          ;;
        ""|y|Y|yes|YES|Yes)
          update_file "$f"
          ok "Updated: $f"
          updated=$((updated + 1))
          ;;
        *) err "Unrecognized answer; no change applied to $f"; return 2 ;;
      esac
    done
  fi

  echo ""
  echo -e "${BOLD}Summary:${RESET}"
  ok "${updated} file(s) updated"
  [[ $skipped -gt 0 ]] && warn "${skipped} file(s) skipped"
  echo ""

  if [[ $updated -gt 0 ]]; then
    rebuild_agent_plugin
    run_validator
    info "Review changes with ${BOLD}git diff${RESET}, then commit when ready:"
    echo "  git add -A && git commit -m \"Update COG framework to v${uv}\""
  fi
}

main "$@"
