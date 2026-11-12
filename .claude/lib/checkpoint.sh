#!/usr/bin/env bash
# Checkpoint recorder for V-model evidence trail.
# Usage:
#   checkpoint.sh init <run-dir>
#   checkpoint.sh record <run-dir> <CP-id> PASS|FAIL|SKIP "<note>"
#   checkpoint.sh status <run-dir>
set -euo pipefail

ROOT="$(CDPATH= cd "$(dirname "$0")/../.." && pwd)"
LOG="$ROOT/.claude/logs/checkpoint-ledger.tsv"
cmd="${1:-}"
shift || true

escape_field() {
  local value="$1"
  value="${value//\\/\\\\}"
  value="${value//$'\t'/\\t}"
  value="${value//$'\r'/\\r}"
  value="${value//$'\n'/\\n}"
  printf '%s' "$value"
}

init_run() {
  local dir="$1"
  mkdir -p -- "$dir/evidence"
  if [[ ! -f "$dir/evidence/ledger.md" ]]; then
    cat > "$dir/evidence/ledger.md" <<'LEDGER'
# Evidence ledger

One row per verify pass. The observation records what was observed in the
artifact, never what a worker reported.

```text
EVIDENCE <AC-id> | <checkpoint> | PASS|FAIL | <observation> | <artifact-path-or-command>
```

## Rows

LEDGER
  fi
  printf 'initialized: %s/evidence/\n' "$dir"
}

record_cp() {
  local dir="$1" cp_id="$2" result="$3" note="${4:-}" ts encoded_note encoded_dir
  case "$result" in
    PASS|FAIL|SKIP) ;;
    *) printf 'invalid checkpoint outcome: %s\n' "$result" >&2; return 2 ;;
  esac
  if [[ "$cp_id" == *$'\t'* || "$cp_id" == *$'\r'* || "$cp_id" == *$'\n'* ]]; then
    printf 'checkpoint id must fit one TSV field\n' >&2
    return 2
  fi
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  encoded_note=$(escape_field "$note")
  encoded_dir=$(escape_field "$dir")
  mkdir -p -- "$dir/evidence" "$ROOT/.claude/logs"
  CHECKPOINT_LOCK="$ROOT/.claude/logs/checkpoint-ledger.lock"
  if ! mkdir -- "$CHECKPOINT_LOCK" 2>/dev/null; then
    printf 'checkpoint ledger busy; retry record after the current writer finishes\n' >&2
    return 2
  fi
  trap 'rmdir -- "$CHECKPOINT_LOCK" 2>/dev/null || true' EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM
  printf '%s\t%s\t%s\t%s\n' "$ts" "$cp_id" "$result" "$encoded_note" >> "$dir/evidence/checkpoints.tsv"
  [[ -f "$LOG" ]] || printf 'timestamp\tcp\tresult\tnote\trun_dir\n' >> "$LOG"
  printf '%s\t%s\t%s\t%s\t%s\n' "$ts" "$cp_id" "$result" "$encoded_note" "$encoded_dir" >> "$LOG"
  printf 'recorded: %s %s → %s/evidence/checkpoints.tsv\n' "$cp_id" "$result" "$dir"
}

status_run() {
  local dir="$1"
  if [[ -f "$dir/evidence/checkpoints.tsv" ]]; then
    column -t -s $'\t' "$dir/evidence/checkpoints.tsv" 2>/dev/null || cat -- "$dir/evidence/checkpoints.tsv"
  else
    printf 'no checkpoints yet: %s\n' "$dir"
  fi
}

case "$cmd" in
  init) init_run "${1:?run-dir}" ;;
  record) record_cp "${1:?run-dir}" "${2:?CP-id}" "${3:?PASS|FAIL|SKIP}" "${4:-}" ;;
  status) status_run "${1:?run-dir}" ;;
  *)
    printf 'usage: checkpoint.sh init|record|status <run-dir> [CP-id] [PASS|FAIL|SKIP] [note]\n' >&2
    exit 1
    ;;
esac
