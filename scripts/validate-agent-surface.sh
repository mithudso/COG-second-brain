#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(CDPATH= cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

info()  { echo -e "${CYAN}ℹ${RESET}  $*"; }
ok()    { echo -e "${GREEN}✓${RESET}  $*"; }
warn()  { echo -e "${YELLOW}⚠${RESET}  $*"; }
err()   { echo -e "${RED}✗${RESET}  $*" >&2; }

failures=0
warnings=0

record_failure() {
  err "$*"
  failures=$((failures + 1))
}

record_warning() {
  warn "$*"
  warnings=$((warnings + 1))
}

if ! command -v python3 >/dev/null 2>&1; then
  record_failure "python3 is required for validation"
  exit 1
fi

info "Validating packaged agent surfaces from $ROOT_DIR"

if python3 -m json.tool .claude-plugin/plugin.json >/dev/null 2>&1; then
  ok ".claude-plugin/plugin.json is valid JSON"
else
  record_failure ".claude-plugin/plugin.json is not valid JSON"
fi

if python3 -m json.tool marketplace-entry.json >/dev/null 2>&1; then
  ok "marketplace-entry.json is valid JSON"
else
  record_failure "marketplace-entry.json is not valid JSON"
fi

# Agent Plugins standard surface (agent-plugins.org, spec 1.0.0):
# root plugin.json manifest + root skills/ mirror of .claude/skills/.
if python3 - <<'PY' >/dev/null 2>&1
import json
with open('plugin.json') as f:
    data = json.load(f)
if data.get('$schema') != 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json' or data.get('name') != 'cog-second-brain':
    raise ValueError('Invalid Agent Plugins schema/name')
PY
then
  ok "plugin.json is valid JSON and declares the Agent Plugins 1.0.0 schema"
else
  record_failure "plugin.json is missing, invalid JSON, or missing \$schema/name (Agent Plugins spec 1.0.0)"
fi

if [[ -d skills ]] && diff -r .claude/skills skills >/dev/null 2>&1; then
  ok "skills/ mirror matches .claude/skills (Agent Plugins surface in sync)"
else
  record_failure "skills/ mirror is missing or drifted from .claude/skills — run ./scripts/build-agent-plugin.sh"
fi

manifest_tmp="$(mktemp)"
trap 'rm -f -- "$manifest_tmp"' EXIT
python3 - <<'PY' > "$manifest_tmp"
import json
import re
from pathlib import Path
with open('.claude-plugin/plugin.json') as f:
    data = json.load(f)
entries = data.get('skills', [])
if not isinstance(entries, list):
    raise ValueError('Plugin skills must be a list')
root = Path.cwd().resolve()
canonical = {path.as_posix() for path in Path('.claude/skills').glob('*/SKILL.md')}
names, paths = set(), set()
for skill in entries:
    if not isinstance(skill, dict):
        raise ValueError('Each plugin skill must be an object')
    name, path = skill.get('name'), skill.get('path')
    if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('Invalid plugin skill name')
    if path != f'.claude/skills/{name}/SKILL.md':
        raise ValueError(f'Non-canonical plugin path for {name}')
    if name in names or path in paths:
        raise ValueError(f'Duplicate plugin skill: {name}')
    target = Path(path)
    if target.is_symlink() or root not in target.resolve().parents:
        raise ValueError(f'Linked or escaping plugin skill: {name}')
    # A narrow guard for required fields and the observed invalid plain scalar.
    # This intentionally does not replace a complete YAML parser.
    for surface in (target, Path('.agents/skills') / name / 'SKILL.md'):
        text = surface.read_text(encoding='utf-8')
        parts = text.split('---', 2)
        if len(parts) != 3 or parts[0].strip():
            raise ValueError(f'Missing skill frontmatter: {surface}')
        header = parts[1]
        found_name = re.search(r'^name:[ \t]*([^\n]+)$', header, re.M)
        description = re.search(r'^description:[ \t]*([^\n]+)$', header, re.M)
        if not found_name or found_name[1].strip().strip('\"\'') != name or not description:
            raise ValueError(f'Invalid required skill fields: {surface}')
        scalar = description[1].strip()
        if not scalar.startswith(('\"', "'", '>', '|')) and re.search(r':(?:\s|$)', scalar.split(' #', 1)[0]):
            raise ValueError(f'Unquoted colon in skill description: {surface}')
    names.add(name)
    paths.add(path)
    print(f'{name}\t{path}')
if paths != canonical:
    raise ValueError(f'Plugin coverage mismatch: missing={sorted(canonical-paths)!r}, extra={sorted(paths-canonical)!r}')
PY

if python3 - <<'PY_CURSOR'
import json
from pathlib import Path
with open('.cursor-plugin/plugin.json') as f:
    cursor = json.load(f)
with open('.claude-plugin/plugin.json') as f:
    canonical = json.load(f)
expected_agents = {p.stem for p in Path('.claude/agents').glob('*.md')}
if cursor.get('version') != canonical['version']:
    raise ValueError('Cursor version differs')
if cursor.get('skills') != canonical['skills']:
    raise ValueError('Cursor skills differ')
if len(cursor['agents']) != len(set(cursor['agents'])):
    raise ValueError('Duplicate Cursor agent')
if set(cursor['agents']) != expected_agents:
    raise ValueError('Cursor agents differ')
PY_CURSOR
then
  ok "Cursor version, skills and agent inventory match canonical surfaces"
else
  record_failure "Cursor packaging differs from canonical version, skills or agents"
fi

manifest_count=$(wc -l < "$manifest_tmp" | tr -d ' ')
claude_skill_count=$(find .claude/skills -name SKILL.md | wc -l | tr -d ' ')

if [[ "$manifest_count" == "$claude_skill_count" ]]; then
  ok "Plugin manifest skill count matches shipped Claude skills ($manifest_count)"
else
  record_failure "Plugin manifest declares $manifest_count skills but .claude/skills contains $claude_skill_count SKILL.md files"
fi

while IFS=$'\t' read -r name path; do
  [[ -z "$name" ]] && continue

  if [[ -f "$path" ]]; then
    ok "Manifest path exists for $name → $path"
  else
    record_failure "Manifest path missing for $name → $path"
  fi

  if grep -Eq "^###[[:blank:]]+/$name([[:blank:]]|$)" AGENTS.md; then
    ok "AGENTS.md documents /$name"
  else
    record_failure "AGENTS.md is missing /$name"
  fi
done < "$manifest_tmp"

rm -f "$manifest_tmp"

plugin_version=$(python3 - <<'PY'
import json
with open('.claude-plugin/plugin.json') as f:
    print(json.load(f)['version'])
PY
)
marketplace_version=$(python3 - <<'PY'
import json
with open('marketplace-entry.json') as f:
    print(json.load(f)['version'])
PY
)
cog_version=$(tr -d '[:space:]' < COG-VERSION)
agent_plugin_version=$(python3 - <<'PY'
import json
with open('plugin.json') as f:
    print(json.load(f)['version'])
PY
)

if [[ "$plugin_version" == "$marketplace_version" && "$plugin_version" == "$cog_version" && "$plugin_version" == "$agent_plugin_version" ]]; then
  ok "Version is aligned across .claude-plugin/plugin.json, plugin.json, marketplace-entry.json, and COG-VERSION ($cog_version)"
else
  record_failure "Version mismatch: .claude-plugin/plugin.json=$plugin_version plugin.json=$agent_plugin_version marketplace-entry.json=$marketplace_version COG-VERSION=$cog_version"
fi

reference_search_exit=0
grep -n "agents\.md" README.md SETUP.md CONTRIBUTING.md .github/MARKETPLACE.md >/dev/null 2>&1 || reference_search_exit=$?
case "$reference_search_exit" in
  0) record_failure "Found lowercase 'agents.md' references in packaging docs; use AGENTS.md consistently" ;;
  1) ok "Packaging docs consistently use AGENTS.md casing" ;;
  *) record_failure "Could not inspect all packaging docs for AGENTS.md casing" ;;
esac

count_surface_files() {
  local directory="$1"
  shift
  if [[ -d "$directory" ]]; then
    find "$directory" "$@" | wc -l | tr -d ' '
  else
    printf '0\n'
  fi
}
kiro_count=$(count_surface_files .kiro/powers -name POWER.md)
gemini_commands_count=$(count_surface_files .gemini/commands -type f)
gemini_skills_count=$(count_surface_files .gemini/skills -type f)

if [[ "$kiro_count" == "7" ]]; then
  ok "Kiro core surface count is $kiro_count"
else
  record_warning "Expected 7 Kiro powers, found $kiro_count"
fi

if [[ "$gemini_commands_count" == "7" && "$gemini_skills_count" == "7" ]]; then
  ok "Gemini core surface counts are aligned (commands=$gemini_commands_count, skills=$gemini_skills_count)"
else
  record_warning "Expected 7 Gemini commands and 7 Gemini skills, found commands=$gemini_commands_count skills=$gemini_skills_count"
fi

if [[ -f docs/AGENT-SUPPORT.md ]]; then
  ok "docs/AGENT-SUPPORT.md exists"
else
  record_failure "docs/AGENT-SUPPORT.md is missing"
fi

if [[ $failures -gt 0 ]]; then
  echo
  err "Validation failed with $failures error(s) and $warnings warning(s)"
  exit 1
fi

echo
ok "Validation passed with $warnings warning(s)"
