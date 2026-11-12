# External calls

## Inventory boundary

This inventory covers executable updater Git calls, the offline indexer's Git subprocess, and CI acquisition. The seven maintained helpers contain no direct HTTP SDK client or MCP server. Optional playbooks can direct a host to call user-configured services; those workflow calls have partial coverage here. This is not a complete runtime registry.

The updater network target is `https://github.com/huytieu/COG-second-brain.git` through `cog-upstream`, branch `main`. Source identity is checked against source-coded HTTPS/SSH forms. Authentication belongs to Git. Fetch requests receive repository objects and refs; these arguments do not send vault bodies. Check/dry-run modes still fetch and may add local remote configuration.

## Updater call sites

All rows use the [framework update procedure](runbooks/framework-update.md) as their operational documentation. Line anchors describe the inspected source; the literal command remains the stable anchor after edits. There is no centralized logger handle. Test names refer to `tests/test_maintenance.py`. Every row has **no automatic retry**; an operator must diagnose before an explicit retry. Local probes are deliberately distinguished from network calls.

| Source | Literal call / stable anchor | Target and effect | Logging/error handling | Test evidence and limit |
|---|---|---|---|---|
| `cog-update.sh:306` | `if ! git remote get-url "$REMOTE_NAME" &>/dev/null; then` | Local config read; existence probe | Silent missing probe selects add | Configured fixture remotes; missing remote not isolated |
| `cog-update.sh:308` | `git remote add "$REMOTE_NAME" "$REMOTE_URL"` | Local config write; official remote | info before call, Git error/nonzero | Configured fixture remotes; no separate add fixture |
| `cog-update.sh:311` | `configured_url=$(git remote get-url "$REMOTE_NAME")` | Local config read; identity | err refuses foreign repository | test_updater_rejects_foreign_remote_without_framework_writes |
| `cog-update.sh:319` | `git fetch "$REMOTE_NAME" "$BRANCH" --quiet` | NETWORK: official upstream objects/refs | info request, ok outcome; Git stderr/nonzero; no automatic retry | All regression fetches redirect to local Git |
| `cog-update.sh:320` | `UPSTREAM_REF=$(git rev-parse --verify "${REMOTE_NAME}/${BRANCH}^{commit}")` | Local ref read; freeze fetched SHA | Exit failure propagates | Fixture success paths; invalid ref not isolated |
| `cog-update.sh:334` | `git show "${UPSTREAM_REF}:${VERSION_FILE}" 2>/dev/null \| tr -d '[:space:]' \|\| echo "unknown"` | Local object read; version | Suppressed stderr; unknown version rejected by main | Version fixtures; missing version not isolated |
| `cog-update.sh:340` | `entry=$(git ls-tree "$UPSTREAM_REF" -- "$file") \|\| { err "Cannot inspect upstream path: $file"; exit 2; }` | Local tree metadata; path existence and mode | Read failure exits2; absent paths skipped; mode differs selects update | Full-table absent paths; comparison/mode-only fixtures |
| `cog-update.sh:348` | `if ! git show "${UPSTREAM_REF}:${file}" > "$temporary"; then` | Local object read; comparison temporary | Read failure exits2; original unchanged | test_updater_comparison_failure_cannot_report_current |
| `cog-update.sh:390` | `if ! git show "${UPSTREAM_REF}:${file}" > "$temporary"; then` | Local object read; sibling replacement staging | Failure removes own temporary and returns nonzero | test_failed_git_show_cannot_truncate_live_framework |
| `cog-update.sh:395` | `object_mode=$(git ls-tree "$UPSTREAM_REF" -- "$file") \|\| { rm -f "$temporary"; return 1; }` | Local metadata; supported executable mode | Unsupported mode/read failure rejects replacement | test_updater_preserves_upstream_executable_bit |
| `cog-update.sh:420` | `[[ -n "$(git status --porcelain)" ]]` | Local tree read; dirty status | Boolean result drives warning | Success fixtures; not all status errors isolated |
| `cog-update.sh:474` | `if ! git rev-parse --is-inside-work-tree &>/dev/null; then` | Local checkout probe | err and nonzero outside repository | Fixture repositories; outside repo not isolated |
| `cog-update.sh:480` | `repository_root=$(git rev-parse --show-toplevel)` | Local checkout-root read | err on script/root mismatch | test_updater_uses_script_checkout_from_personal_subdirectory |
| `cog-update.sh:515` | `[[ -n "$(git status --porcelain)" ]] && echo ""` | Local tree read; warning formatting | Captured names not printed by this call | Fixture flows; separate call failure not isolated |
| `cog-update.sh:642` | `diff --color=auto <(cat "$f") <(git show "${UPSTREAM_REF}:${f}") \|\| true` | Local object read; optional interactive diff | Diff printed; ordinary difference status tolerated | Interactive skips covered; diff-choice branch not isolated |

`git status --porcelain` internally inspects untracked names; this documentation task does not run that updater path or inventory those names. Version/existence probes have documented fallbacks; some calls have no dedicated failure fixture. Object-comparison failures are explicit errors. The table records those limits without claiming full call-level test coverage.

## Other boundaries

| Source | Call or effect | Logging/tests/docs/retry |
|---|---|---|
| `scripts/doc_indexes.py:inventory` | `git -C <root> ls-files --cached -z`; local tracked/staged paths | Captured output, 30-second timeout, errors reported by main; indexer fixture tests; [development](DEVELOPMENT.md); no automatic retry |
| `tests/test_maintenance.py` | Temporary Git init/config/add/commit, local fixture fetch, isolated helper subprocesses | Assertions inspect codes/output/files; synthetic input only; [testing](TESTING.md); no real upstream request or provider probe |
| `scripts/build-agent-plugin.sh` | Local copy/move/remove, staging and writer lock | Explicit failure/lock/recovery diagnostics, copy/concurrency tests; [components](COMPONENTS.md); owner review before retry |
| Other maintained helpers | Local filesystem and Unix/Python subprocesses | Helper diagnostics and regression cases; [logging](logging.md); no network retry loop |
| `.github/workflows/ci.yml` | Runner checkout and Python acquisition | CI logs; no offline certification of Actions transport; [testing](TESTING.md); action/runner behavior is external |

CI pins checkout to `11d5960a326750d5838078e36cf38b85af677262` (v4) and setup-python to `a26af69be951a213d495a4c3e4e4022e16d87065` (v5), resolved through the official GitHub API on 2026-11-12. No latest-major claim is made. Dependabot checks GitHub Actions monthly. CI uses network infrastructure while repository tests and index checks use local fixtures.

## Five-standard coverage

| Standard | Current coverage |
|---|---|
| CLI trigger | PRESENT: updater CLI and offline helper/index commands |
| Centralized error log | GAP: console diagnostics exist; no shared sink or complete structured request/outcome coverage |
| Auto-remediation map | PARTIAL: manual recovery guidance; no machine registry or automatic loop |
| Dashboard card | EXCEPTION: no application/dashboard runtime exists |
| Datastore verification | EXCEPTION for application datastore; PARTIAL filesystem observations through validation, diff review, and synthetic tests |

This is not a five-standard pass. The parent optimizer assessment owns source remediation decisions. Do not invent a server registry, datastore, dashboard, or Node runtime to fill an architectural mismatch. Optional provider calls, credentials, and live post-conditions remain user-owned and untested here.
