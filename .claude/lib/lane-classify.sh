#!/usr/bin/env bash
# Risk lane classifier — adapted from dwarves-kit lane-classify pattern.
# Usage:
#   lane-classify.sh classify "<task summary>"
#   lane-classify.sh explain "<task summary>"
set -euo pipefail

cmd="${1:-classify}"
shift || true
text="${*:-}"
case "$cmd" in classify|explain) ;; *) printf 'usage: lane-classify.sh classify|explain "<summary>"\n' >&2; exit 2 ;; esac

score=0
reasons=()

# Consume the complete literal input. grep -q can close a pipe early; Bash 3.2
# here strings need writable temporary storage. A matcher error must fail closed.
matches() {
  local match_exit=0
  printf '%s\n' "$text" | grep -iE "$1" >/dev/null || match_exit=$?
  case "$match_exit" in
    0|1) return "$match_exit" ;;
    *) printf 'risk matcher failed (grep exit %s)\n' "$match_exit" >&2; exit 2 ;;
  esac
}

# Hard gates
if matches 'security|credential|secret|prod(uction)?|delete all|rm -rf'; then
  if [[ "$cmd" == "explain" ]]; then
    printf 'lane=full score=0 reasons=hard-risk\n'
  else
    printf 'full\n'
  fi
  exit 0
fi

if matches 'bug|broken|regression|fails|error 5|root cause'; then
  if [[ "$cmd" == "explain" ]]; then
    printf 'lane=bug score=0 reasons=hard-bug\n'
  else
    printf 'bug\n'
  fi
  exit 0
fi

if matches 'backfill|retrofit|audit only|document existing|no behavior change'; then
  if [[ "$cmd" == "explain" ]]; then
    printf 'lane=backfill score=0 reasons=hard-backfill\n'
  else
    printf 'backfill\n'
  fi
  exit 0
fi

if matches '(^|[^[:alnum:]_])(typo|one line|single word|label only|status reply|fix typo)([^[:alnum:]_]|$)'; then
  if [[ "$cmd" == "explain" ]]; then
    echo "lane=tiny score=0 reasons=hard-tiny"
  else
    echo "tiny"
  fi
  exit 0
fi

# Soft signals
matches '(^|[^[:alnum:]_])(typo|one line|single word|label only|status reply)([^[:alnum:]_]|$)' && { score=$((score+3)); reasons+=("tiny-signal"); }
matches 'brief|team-brief|slack|jira|multi-source|publish|deploy|ship' && { score=$((score+2)); reasons+=("full-signal"); }
matches 'spec|acceptance|test|verify|cross-repo|milestone' && { score=$((score+1)); reasons+=("normal+"); }

word_count=$(printf '%s\n' "$text" | wc -w | tr -d ' ')
[[ "$word_count" -lt 8 ]] && { score=$((score+1)); reasons+=("short"); }

lane="normal"
[[ $score -ge 3 ]] && lane="full"
[[ $score -le 0 && $word_count -lt 12 ]] && lane="tiny"

if [[ "$cmd" == "explain" ]]; then
  printf 'lane=%s score=%s reasons=%s\n' "$lane" "$score" "${reasons[*]:-none}"
else
  echo "$lane"
fi
