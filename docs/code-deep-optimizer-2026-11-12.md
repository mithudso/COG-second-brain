# Code deep optimizer, 2026-11-12

Full repository structural mode; no quick mode, changed-only scope, file cap, advisory features, live updater/integration, model execution or semantic indexing. Source-only fresh per-file contexts reviewed7canonical baseline helpers and3new executable/CI targets. Two generated Python mirrors are excluded only after byte comparison. All 284 baseline paths are recorded in [coverage ledger](maintenance-coverage-2026-11-12.json). All 18 tracked vault-layout/template paths are unchanged. Instructional playbooks retain body text;8malformed YAML description scalars were quoted without changing their values.

## Per-iteration severity

| Diagnostic iteration | Critical | High | Medium | Low | Nit |
|---|---:|---:|---:|---:|---:|
| 1 | 0 | 1 | 28 | 5 | 0 |
| 2 | 0 | 0 | 24 | 4 | 0 |
| 3 | 0 | 0 | 1 | 0 | 0 |
| 4 | 0 | 0 | 1 | 0 | 0 |
|5 (post-merge local validation)|0|0|2|0|0|
| Final after directed repair verification | 0 | 0 | 0 | 2 | 0 |

Iteration1 includes two parent-corroborated updater failures beyond the initial per-file reports. Iteration2 includes new test/CI tooling and metadata corrections. Iterations3and4 are directed repairs of the two independent-gate findings; no third gate ran. Initial Low observations were repaired or reclassified after concrete evidence. Final Medium+ count is the directed repair result. Both independent gate attempts dissented before their fixes. No independent audit of the last fix remains, and no defect-free claim is made.

## Findings

Every row is FIXED and verified by the named synthetic regression or exact check. Locations point to the final repair anchor; original triggers were captured in source-only review snapshots and red regression logs outside the repository. The table is complete for corroborated High/Medium findings.

| Iteration / pass | Final repair anchor | Severity | Reproducible finding | Fix / verification | Status |
|---|---|---|---|---|---|
| 1 / C1 | `cog-update.sh:603` | High | First postincrement under set -e aborts the first update/skip. | assignment counters; `test_force_updates_every_file_and_preserves_vault` | FIXED |
| 1 / C2 | `cog-update.sh:395` | Medium | New upstream executable becomes mode0644. | preserve supported upstream mode; `test_updater_preserves_upstream_executable_bit` | FIXED |
| 1 / C3 | `cog-update.sh:471` | Medium | Invocation from personal subdirectory writes framework paths there. | resolve and verify script checkout root; `test_updater_uses_script_checkout_from_personal_subdirectory` | FIXED |
| 1 / S1 | `cog-update.sh:363` | Medium | Linked target/parent overwrites outside the framework. | refuse linked components; `test_update_rejects_symlinked_framework_without_touching_target` | FIXED |
| 1 / S2 | `cog-update.sh:389` | Medium | Failed git show truncates live file. | sibling temporary then rename; `test_failed_git_show_cannot_truncate_live_framework` | FIXED |
| 1 / S3 | `cog-update.sh:437` | Medium | Missing validator returns successful --validate. | missing validator is a failure; `test_validate_mode_fails_when_validator_is_absent` | FIXED |
| 1 / S3 | `cog-update.sh:305` | Medium | Foreign cog-upstream accepted as official. | check upstream identity and pin fetched SHA; `test_updater_rejects_foreign_remote_without_framework_writes` | FIXED |
| 1 / S4 | `cog-update.sh:594` | Medium | Bash3.2 nounset rejects empty force arrays. | guard empty-array appends; `test_updater_handles_only_new_files_on_system_bash` | FIXED |
| 1 / C1 | `cog-update.sh:1` | Medium | Validator failure was discarded after apply. | propagate rebuild/validation failure; `test_packaging_failure_propagates_after_updates` | FIXED |
| 1 / S2 | `.gitignore:62` | Medium | Backup names were not ignored; backup collisions also risked replacement. | unique private backups and matching ignore rule; `test_update_backups_are_ignored` | FIXED |
| 1 / S2 | `.claude/lib/checkpoint.sh:72` | Medium | Status unnecessarily creates logs and fails on read-only trees. | status only reads; `test_checkpoint_status_does_not_create_log_directory` | FIXED |
| 1 / S3 | `.claude/lib/checkpoint.sh:46` | Medium | Invalid outcome enters audit ledger. | enum validation before writes; `test_checkpoint_invalid_outcome_writes_no_record` | FIXED |
| 1 / S5 | `.claude/lib/checkpoint.sh:14` | Medium | echo -e lets note escapes forge TSV records. | literal printf with escaped field separators; `test_checkpoint_preserves_note_as_one_literal_record` | FIXED |
| 1 / C1 | `.claude/lib/lane-classify.sh:18` | Medium | Early-closing grep-q plus pipefail misses large hard-risk input. | consume complete literal input; `test_lane_hard_gate_survives_large_multiline_summary` | FIXED |
| 1 / S3 | `.claude/lib/lane-classify.sh:18` | Medium | xpg_echo interprets backslash-c and hides risk terms. | printf literal input; `test_lane_treats_backslashes_literally_and_explains_hard_gates` | FIXED |
| 1 / C1 | `.claude/skills/slop-gate/scripts/scan.py:90` | Medium | Inline backticks preempt fenced exhibit stripping. | strip fences before inline quotes; `test_scanner_ignores_fenced_exhibits` | FIXED |
| 1 / C2 | `.claude/skills/slop-gate/scripts/scan.py:189` | Medium | Edit scans only fragment and misses full-document threshold. | reconstruct unique/replace-all candidate; `test_scanner_edit_checks_the_complete_candidate` | FIXED |
| 1 / S3 | `.claude/skills/slop-gate/scripts/scan.py:64` | Medium | Substring path exclusions exempt similarly named prose. | component matching; `test_scanner_exemptions_match_path_components` | FIXED |
| 1 / P1 | `.claude/skills/slop-gate/scripts/scan.py:42` | Medium | Multiline whitespace prefixes produce quadratic scans. | horizontal line whitespace; `test_scanner_whitespace_prefix_has_bounded_runtime` | FIXED |
| 1 / C1 | `.claude/skills/voice-baseline/scripts/census.py:103` | Medium | Unseen corpus watchwords are never checked. | check complete watchlist including zero counts; `test_census_checks_unseen_watchwords_and_phrase_boundaries` | FIXED |
| 1 / C2 | `.claude/skills/voice-baseline/scripts/census.py:74` | Medium | Phrase substrings inflate unrelated words. | word boundaries around phrases; `test_census_checks_unseen_watchwords_and_phrase_boundaries` | FIXED |
| 1 / C1 | `.claude/skills/voice-baseline/scripts/census.py:38` | Medium | Contracted That is kicker is missed. | straight/curly contractions; `test_census_contractions_and_paragraph_endings` | FIXED |
| 1 / C1 | `.claude/skills/voice-baseline/scripts/census.py:35` | Medium | Hard wraps falsely count paragraph-ending verdicts. | blank-line/EOF boundary; `test_census_contractions_and_paragraph_endings` | FIXED |
| 1 / C3 | `.claude/skills/voice-baseline/scripts/census.py:174` | Medium | Previous --out report feeds the next census. | exclude real output/draft paths; `test_census_excludes_its_previous_output` | FIXED |
| 1 / S2 | `.claude/skills/voice-baseline/scripts/census.py:180` | Medium | os.walk permission failure produces a false complete report. | surface traversal errors; `test_census_rejects_incomplete_traversal` | FIXED |
| 1 / S2 | `scripts/build-agent-plugin.sh:46` | Medium | Mirror deleted before failed copy. | stage before replacing old mirror; `test_builder_keeps_previous_mirror_if_copy_fails` | FIXED |
| 1 / P2 | `scripts/build-agent-plugin.sh:36` | Medium | Concurrent builders nest or damage mirrors. | single-writer lock; `test_builder_serializes_competing_writers` | FIXED |
| 1 / S3 | `scripts/validate-agent-surface.sh:116` | Medium | Duplicate manifest entries mask missing skill. | unique exact canonical set; `test_validator_rejects_duplicate_manifest_coverage` | FIXED |
| 1 / S2 | `scripts/validate-agent-surface.sh:196` | Medium | Missing/erroring search masquerades as success. | portable grep status distinction; `test_validator_search_errors_cannot_report_success` | FIXED |
| 2 / S4 | `.claude/lib/checkpoint.sh:9` | Medium | CDPATH output corrupts captured checkout paths. | neutralize CDPATH in root-resolving cd calls; `test_checkpoint_cdpath_does_not_change_ledger_root` | FIXED |
| 2 / P2 | `.claude/lib/checkpoint.sh:58` | Medium | First-time writers can append duplicate TSV headers. | lock before either ledger append; busy means retry; `test_checkpoint_busy_ledger_fails_without_partial_record` | FIXED |
| 2 / C1 | `.claude/lib/lane-classify.sh:57` | Medium | typo substring in typography downgrades a full task. | tiny phrase boundaries; `test_lane_typography_cannot_trigger_tiny_override` | FIXED |
| 2 / S2 | `.claude/lib/lane-classify.sh:18` | Medium | Here-string storage/matcher failures become successful normal lane. | pipe without early close; fail on grep errors; `test_lane_matcher_failure_cannot_return_low_risk` | FIXED |
| 2 / C1 | `.claude/skills/slop-gate/scripts/scan.py:189` | Medium | Removing slop-ok marker bypasses scanning. | exempt only final candidate; `test_scanner_edit_removing_exemption_scans_result` | FIXED |
| 2 / C2 | `.claude/skills/slop-gate/scripts/scan.py:68` | Medium | Tilde/indented/long fences leak exhibits. | marker-aware line state; `test_markdown_fences_support_tildes_indent_and_long_markers` | FIXED |
| 2 / C3 | `.claude/skills/slop-gate/scripts/scan.py:230` | Medium | Exempt binary UTF8 decode aborts batch. | exclude path before decoding; continue IO failures; `test_scanner_exempt_binary_does_not_abort_batch` | FIXED |
| 2 / S3 | `.claude/skills/slop-gate/scripts/scan.py:118` | Medium | build/../draft.md bypasses path checks. | normalize path before matching components; `test_scanner_normalizes_parent_components_before_exemption` | FIXED |
| 2 / P1 | `.claude/skills/slop-gate/scripts/scan.py:42` | Medium | Overlapping heading whitespace stalls on 32KB spaces. | remove overlapping quantifiers; `test_heading_blank_lines_have_bounded_runtime_in_both_scanners` | FIXED |
| 2 / C1 | `.claude/skills/voice-baseline/scripts/census.py:35` | Medium | Question/exclamation sentence boundaries hide verdicts. | include sentence boundary punctuation; `test_census_verdict_sentence_boundaries_include_questions` | FIXED |
| 2 / S3 | `.claude/skills/voice-baseline/scripts/census.py:45` | Medium | Valid fenced code corrupts corpus rates. | marker-aware line state; `test_markdown_fences_support_tildes_indent_and_long_markers` | FIXED |
| 2 / P1 | `.claude/skills/voice-baseline/scripts/census.py:39` | Medium | Blank-line prefixes cause quadratic heading scans. | horizontal whitespace only; `test_heading_blank_lines_have_bounded_runtime_in_both_scanners` | FIXED |
| 2 / C1 | `cog-update.sh:379` | Medium | Directory destination receives hidden temporary rather than replacement. | refuse non-regular destination; `test_updater_refuses_directory_destination` | FIXED |
| 2 / C3 | `cog-update.sh:667` | Medium | Typing no accepted as update. | explicit affirmative/refusal answers; `test_interactive_no_preserves_framework_edits` | FIXED |
| 2 / S1 | `cog-update.sh:437` | Medium | --validate executes linked external validator. | validate path before execution; `test_validate_mode_refuses_linked_validator` | FIXED |
| 2 / S2 | `cog-update.sh:338` | Medium | Git object read errors report everything current. | distinguish missing paths and failed reads; `test_updater_comparison_failure_cannot_report_current` | FIXED |
| 2 / P2 | `cog-update.sh:525` | Medium | Two updater revisions interleave framework contents. | serialize complete compare/apply writer; `test_updater_busy_lock_preserves_framework` | FIXED |
| 2 / S2 | `scripts/build-agent-plugin.sh:26` | Medium | Old-stage cleanup failure strands builder lock. | release lock even when staging cleanup fails; `test_builder_releases_lock_when_old_stage_cleanup_fails` | FIXED |
| 2 / S3 | `scripts/validate-agent-surface.sh:57` | Medium | PYTHONOPTIMIZE removes mandatory assert validations. | explicit exceptions in all validation blocks; `test_validator_mandatory_checks_survive_python_optimization` | FIXED |
| 2 / S2 | `tests/test_maintenance.py:53` | Medium | Timeout leaves stalled child alive. | kill/reap owned process group and close pipes; `test_fixture_timeout_kills_and_reaps_owned_group` | FIXED |
| 2 / T4 | `tests/test_maintenance.py:36` | Medium | Partial barrier line blocks readline indefinitely. | bounded byte reads under deadline; `test_partial_fixture_marker_expires_without_waiting_for_newline` | FIXED |
| 2 / C2 | `.cursor-plugin/plugin.json:4` | Medium | Cursor version, skill and verifier inventories drift. | align five versions/35 skills/10 agents; `test_validator_rejects_stale_cursor_package` | FIXED |
| 2 / T3 | `.github/workflows/ci.yml:29` | Medium | Single bash-n invocation checks only its first file. | loop syntax gate across every shell helper; `local exact loop and CI matrix` | FIXED |
| 2 / T3 | `scripts/validate-agent-surface.sh:112` | Medium | Eight SKILL frontmatters fail YAML on bare colon-space descriptions. | quote scalars preserving descriptions/bodies; narrow regression guard; `test_validator_rejects_unquoted_colon_in_skill_description` | FIXED |
| 3 / C1/C2/S4 | `cog-update.sh:342` | Medium | Byte-only selection skips executable-mode-only changes. | compare supported upstream executable state before byte comparison; `test_updater_repairs_mode_only_missing_executable_bit / test_updater_repairs_mode_only_unexpected_executable_bit` | FIXED |
| 4 / C3/S2/P1 | `.claude/skills/voice-baseline/scripts/census.py:39` | Medium | Lazy heading capture plus trailing whitespace remains quadratic on a32KB space suffix. | remove overlapping suffix matcher; preserve first-word counts; `test_heading_blank_lines_have_bounded_runtime_in_both_scanners (both adverse cases on both scripts)` | FIXED |

Low repairs also cover malformed non-object hook payloads, consistent explain output, temporary-manifest cleanup, missing optional surface warnings, exact command heading boundaries and staged-file mutation detection in CI. Two residual Low observations remain: Markdown entity/formatting in unusual retrieval-map labels can alter the displayed label while the encoded target stays correct; unreadable Stop transcripts retain the existing best-effort fail-open policy without a diagnostic. Neither has a corroborated Medium impact in this scoped offline framework.

## Verify gate

| Command / evidence | Baseline | Final candidate | Verdict |
|---|---|---|---|
| Per-file `bash -n` loop; Python AST syntax | PASS | PASS | PASS |
| `./scripts/validate-agent-surface.sh` | PASS on baseline packaging | PASS,35 skills/10 agents/five versions | PASS |
| Synthetic red counterexamples | No existing suite; original14-test set had14failing assertions | Subsequent red snapshots reproduce newly reported defects | Evidence retained |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` | No existing suite | 63 tests pass after the source-parity follow-up; latest full run retained in delivery evidence | PASS |
| `python3 scripts/doc_indexes.py --check` | No map/gate | PASS; all 323 tracked/staged paths accounted | PASS |
|4 JSON manifests,17 TOML configs,35 canonical/pointer identities | Static baseline inspected | PASS | PASS |
|90 skill/agent frontmatters plus3metadata YAML files (local Ruby Psych) |8malformed skill frontmatters | PASS | PASS |
| Local Markdown links, whitespace and intended path review | Existing docs retained | PASS | PASS |
|Remote CI | No repository workflow | Final pushed head must pass4matrix jobs before merge; exact run IDs in delivery receipt | Delivery gate |

The project enforces no numeric line coverage target. Tests assert behavior, error messages, return codes, permissions, bytes and preservation, including controlled concurrency and deadline cleanup. Test subprocesses use temporary Git repos with empty templates, isolated Git configuration and local fixture fetch rewrites. No real upstream fetch or live vault procedure is tested. No shipped held-out eval plus must-pass set exists; empirical champion/challenger mode is unavailable (`cannot auto-improve`). No champion or embedding action was directly requested or invoked. Historical fixture dispatch remains separately unverified pending the task-specific metadata audit.

## Activated skills and repository passes

- `repo-bootstrapper`, its audit checklist/coding standards and the local mdb-tam bootstrap prompt inform factual metadata/docs/CI exceptions.
- `lang-python` informs stdlib CLI/parser/resource behavior. `software-engineering-patterns` code-reviewer/coding-standards references inform all fix passes.
- `security-review` informs untrusted hook payloads, paths, updater identity and source-as-data boundaries. `devops-containers-cicd` informs CI/delivery; `devops-observability` informs diagnostics and literal ledgers.
- `technical-writing-craft` routing/reference guidance informs API/runbook/prose checks. No web/server/database/framework stacks are invented.
- Repo passes M3/T2/T3/cross-file M2/T4: independent command helpers and existing lib layout remain; no UI-wide settings store is applicable. Configurable thresholds live with their standalone scanners. Duplicated fence state is intentionally small and self-contained because the two scripts ship independently in generated packages. No mandatory third-party Python runtime dependency manifest exists; exact Actions refs were verified via the official GitHub API and SHA pinned. CI uses Ubuntu/macOS with Python3.11/3.13. The fixture suite is isolated and fast enough to run serially; deadline bugs were fixed rather than adding parallel-runner dependencies.

All 18fix-track passes are active somewhere at repo scope. Per-file T4 is N/A on non-tests, and UI/server/auth/datastore checks are N/A with architectural reasons. There is no feature implementation or advisory mode. Source injection gates found no reviewer-directed directives.

## Unified per-file diffs

Diff excerpts are capped at12lines per file; truncation is explicitly reported. The full task diff remains reviewable in Git/PR.

### `.agents/skills/closed-loop/SKILL.md`

```diff
diff --git a/.agents/skills/closed-loop/SKILL.md b/.agents/skills/closed-loop/SKILL.md
index 4e3522d..72c8566 100644
--- a/.agents/skills/closed-loop/SKILL.md
+++ b/.agents/skills/closed-loop/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: closed-loop
-description: Run one task through the V-model verification loop: CP-2 plan → CP-3 build → CP-3v component verify → CP-4 integration verify (full lane) → CP-5 acceptance. The worker never grades its own homework; evidence rows trace back to AC-n. Opt-in: invoke with /closed-loop or by asking for the closed loop, proper verification, or an evidence trail. Ordinary work does not run this.
+description: "Run one task through the V-model verification loop: CP-2 plan → CP-3 build → CP-3v component verify → CP-4 integration verify (full lane) → CP-5 acceptance. The worker never grades its own homework; evidence rows trace back to AC-n. Opt-in: invoke with /closed-loop or by asking for the closed loop, proper verification, or an evidence trail. Ordinary work does not run this."
 ---

 Read `.claude/skills/closed-loop/SKILL.md` and execute it exactly as written — that file is the authoritative
```
Complete diff.

### `.agents/skills/editorial-illustrations/SKILL.md`

```diff
diff --git a/.agents/skills/editorial-illustrations/SKILL.md b/.agents/skills/editorial-illustrations/SKILL.md
index 368c7d8..c009515 100644
--- a/.agents/skills/editorial-illustrations/SKILL.md
+++ b/.agents/skills/editorial-illustrations/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: editorial-illustrations
-description: Generate meaning-carrying editorial data-illustrations in the monotykamary / Linear aesthetic (near-black grayscale, Inter display + mono labels, hairline framed figures) with a single coral accent. This is a GENERATIVE GUIDE, not a template gallery: it teaches the "claim -> geometry" method so any session can invent the RIGHT figure for what a post actually argues, then render it as a self-contained, theme-aware, reduced-motion-safe HTML/SVG figure. Use when writing/illustrating a blog post, essay, spec, or slide and you want a chart, diagram, or illustration that carries a thesis (not decoration) in the house style. Triggers: "make a chart/diagram/illustration for this", "visualize this argument", "monotykamary/Linear style figure", "editorial graphic".
+description: "Generate meaning-carrying editorial data-illustrations in the monotykamary / Linear aesthetic (near-black grayscale, Inter display + mono labels, hairline framed figures) with a single coral accent. This is a GENERATIVE GUIDE, not a template gallery: it teaches the \"claim -> geometry\" method so any session can invent the RIGHT figure for what a post actually argues, then render it as a self-contained, theme-aware, reduced-motion-safe HTML/SVG figure. Use when writing/illustrating a blog post, essay, spec, or slide and you want a chart, diagram, or illustration that carries a thesis (not decoration) in the house style. Triggers: \"make a chart/diagram/illustration for this\", \"visualize this argument\", \"monotykamary/Linear style figure\", \"editorial graphic\"."
 ---

 Read `.claude/skills/editorial-illustrations/SKILL.md` and execute it exactly as written — that file is the authoritative
```
Complete diff.

### `.agents/skills/retro/SKILL.md`

```diff
diff --git a/.agents/skills/retro/SKILL.md b/.agents/skills/retro/SKILL.md
index d6d953b..caf7295 100644
--- a/.agents/skills/retro/SKILL.md
+++ b/.agents/skills/retro/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: retro
-description: CP-7 retrospective: audit checkpoints, evidence quality, action items, and harvest candidates. Closes the V-model cycle and feeds the next run. Use via /retro after ship, escalate, or significant session.
+description: "CP-7 retrospective: audit checkpoints, evidence quality, action items, and harvest candidates. Closes the V-model cycle and feeds the next run. Use via /retro after ship, escalate, or significant session."
 ---

 Read `.claude/skills/retro/SKILL.md` and execute it exactly as written — that file is the authoritative
```
Complete diff.

### `.agents/skills/review-cockpit/SKILL.md`

```diff
diff --git a/.agents/skills/review-cockpit/SKILL.md b/.agents/skills/review-cockpit/SKILL.md
index 63d1339..a2391b5 100644
--- a/.agents/skills/review-cockpit/SKILL.md
+++ b/.agents/skills/review-cockpit/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: review-cockpit
-description: Produce and continuously maintain ONE living review document for a multi-item session — a cockpit header (Progress checklist, Working folder, Context) plus per-item review cards that you approve or request changes on directly in the doc or side panel. Use whenever a session has multiple deliverables you need to review/approve (meeting-processing + planning, multi-ticket work, briefs with several drafts, any "do X, then plan/draft Y and Z"). The doc is the interaction surface: you edit it (or reply in chat) to approve/change; the agent keeps it live as work progresses.
+description: "Produce and continuously maintain ONE living review document for a multi-item session — a cockpit header (Progress checklist, Working folder, Context) plus per-item review cards that you approve or request changes on directly in the doc or side panel. Use whenever a session has multiple deliverables you need to review/approve (meeting-processing + planning, multi-ticket work, briefs with several drafts, any \"do X, then plan/draft Y and Z\"). The doc is the interaction surface: you edit it (or reply in chat) to approve/change; the agent keeps it live as work progresses."
 ---

 Read `.claude/skills/review-cockpit/SKILL.md` and execute it exactly as written — that file is the authoritative
```
Complete diff.

### `.agents/skills/slop-gate/SKILL.md`

```diff
diff --git a/.agents/skills/slop-gate/SKILL.md b/.agents/skills/slop-gate/SKILL.md
index 72abaf8..51b9eed 100644
--- a/.agents/skills/slop-gate/SKILL.md
+++ b/.agents/skills/slop-gate/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: slop-gate
-description: Deterministic pre-publish scan that refuses AI-slop tells in anything about to be written, published, or sent: files, artifacts, slide titles, table headers, diagram labels, chat messages, commit messages. Use before publishing or sending any deliverable, in CI, or wired as a Claude Code hook so the check runs without being remembered. The editorial counterpart is no-ai-slop, which rewrites; this one blocks.
+description: "Deterministic pre-publish scan that refuses AI-slop tells in anything about to be written, published, or sent: files, artifacts, slide titles, table headers, diagram labels, chat messages, commit messages. Use before publishing or sending any deliverable, in CI, or wired as a Claude Code hook so the check runs without being remembered. The editorial counterpart is no-ai-slop, which rewrites; this one blocks."
 ---

 Read `.claude/skills/slop-gate/SKILL.md` and execute it exactly as written; that file is the authoritative
```
Complete diff.

### `.agents/skills/ultragoal/SKILL.md`

```diff
diff --git a/.agents/skills/ultragoal/SKILL.md b/.agents/skills/ultragoal/SKILL.md
index 26c5c7f..20ed018 100644
--- a/.agents/skills/ultragoal/SKILL.md
+++ b/.agents/skills/ultragoal/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: ultragoal
-description: Run a large, multi-session goal (e.g. shipping a whole side product) through the full V-model closed loop, one phase at a time, with cross-session state and a final north-star acceptance gate. Ultragoals never downgrade the lane: every phase runs CP-1→CP-6 with adversarial verification. Opt-in: invoke with /ultragoal or by calling something a long-running goal. Ordinary work does not run this.
+description: "Run a large, multi-session goal (e.g. shipping a whole side product) through the full V-model closed loop, one phase at a time, with cross-session state and a final north-star acceptance gate. Ultragoals never downgrade the lane: every phase runs CP-1→CP-6 with adversarial verification. Opt-in: invoke with /ultragoal or by calling something a long-running goal. Ordinary work does not run this."
 ---

 Read `.claude/skills/ultragoal/SKILL.md` and execute it exactly as written — that file is the authoritative
```
Complete diff.

### `.claude-plugin/plugin.json`

```diff
diff --git a/.claude-plugin/plugin.json b/.claude-plugin/plugin.json
index f091c5d..35757d4 100644
--- a/.claude-plugin/plugin.json
+++ b/.claude-plugin/plugin.json
@@ -1,6 +1,6 @@
 {
   "name": "cog-second-brain",
-  "version": "3.13.0",
+  "version": "3.13.1",
   "description": "Self-evolving second brain with 35 AI agent skills, 10 agents, and people CRM. Closed-loop harness release: a V-model verification lifecycle (spec to evidence, criterion-traced checkpoints), read-only verifier agents that observe artifacts instead of trusting worker summaries, risk lanes, multi-session ultragoals with a north-star acceptance gate, plus craft skills for writing, visual work, and a paired anti-slop design system for marketing and product UI. Inspired by Garry Tan's gstack specialist sessions, gbrain knowledge patterns, and dwarves-kit closed-loop execution. Works with Claude Code, Antigravity, Cursor, Kiro, Gemini CLI, Codex, and any markdown-reading agent.",
   "author": {
     "name": "Huy Tieu",
```
45 additional diff lines omitted.

### `.claude/lib/checkpoint.sh`

```diff
diff --git a/.claude/lib/checkpoint.sh b/.claude/lib/checkpoint.sh
index 55b79a0..a76cd68 100755
--- a/.claude/lib/checkpoint.sh
+++ b/.claude/lib/checkpoint.sh
@@ -6,16 +6,23 @@
 #   checkpoint.sh status <run-dir>
 set -euo pipefail

-ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
+ROOT="$(CDPATH= cd "$(dirname "$0")/../.." && pwd)"
 LOG="$ROOT/.claude/logs/checkpoint-ledger.tsv"
-mkdir -p "$ROOT/.claude/logs"
```
83 additional diff lines omitted.

### `.claude/lib/lane-classify.sh`

```diff
diff --git a/.claude/lib/lane-classify.sh b/.claude/lib/lane-classify.sh
index b7f55c1..58cf961 100755
--- a/.claude/lib/lane-classify.sh
+++ b/.claude/lib/lane-classify.sh
@@ -8,27 +8,51 @@ set -euo pipefail
 cmd="${1:-classify}"
 shift || true
 text="${*:-}"
+case "$cmd" in classify|explain) ;; *) printf 'usage: lane-classify.sh classify|explain "<summary>"\n' >&2; exit 2 ;; esac

 score=0
 reasons=()
```
67 additional diff lines omitted.

### `.claude/skills/review-cockpit/SKILL.md`

```diff
diff --git a/.claude/skills/review-cockpit/SKILL.md b/.claude/skills/review-cockpit/SKILL.md
index 94544d9..2683ada 100644
--- a/.claude/skills/review-cockpit/SKILL.md
+++ b/.claude/skills/review-cockpit/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: review-cockpit
-description: Produce and continuously maintain ONE living review document for a multi-item session — a cockpit header (Progress checklist, Working folder, Context) plus per-item review cards that you approve or request changes on directly in the doc or side panel. Use whenever a session has multiple deliverables you need to review/approve (meeting-processing + planning, multi-ticket work, briefs with several drafts, any "do X, then plan/draft Y and Z"). The doc is the interaction surface: you edit it (or reply in chat) to approve/change; the agent keeps it live as work progresses.
+description: "Produce and continuously maintain ONE living review document for a multi-item session — a cockpit header (Progress checklist, Working folder, Context) plus per-item review cards that you approve or request changes on directly in the doc or side panel. Use whenever a session has multiple deliverables you need to review/approve (meeting-processing + planning, multi-ticket work, briefs with several drafts, any \"do X, then plan/draft Y and Z\"). The doc is the interaction surface: you edit it (or reply in chat) to approve/change; the agent keeps it live as work progresses."
 ---

 # review-cockpit
```
Complete diff.

### `.claude/skills/slop-gate/SKILL.md`

```diff
diff --git a/.claude/skills/slop-gate/SKILL.md b/.claude/skills/slop-gate/SKILL.md
index 634e498..7d4357d 100644
--- a/.claude/skills/slop-gate/SKILL.md
+++ b/.claude/skills/slop-gate/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: slop-gate
-description: Deterministic pre-publish scan that refuses AI-slop tells in anything about to be written, published, or sent: files, artifacts, slide titles, table headers, diagram labels, chat messages, commit messages. Use before publishing or sending any deliverable, in CI, or wired as a Claude Code hook so the check runs without being remembered. The editorial counterpart is no-ai-slop, which rewrites; this one blocks.
+description: "Deterministic pre-publish scan that refuses AI-slop tells in anything about to be written, published, or sent: files, artifacts, slide titles, table headers, diagram labels, chat messages, commit messages. Use before publishing or sending any deliverable, in CI, or wired as a Claude Code hook so the check runs without being remembered. The editorial counterpart is no-ai-slop, which rewrites; this one blocks."
 ---

 <!-- slop-ok: this skill quotes the tells it blocks -->
```
Complete diff.

### `.claude/skills/slop-gate/scripts/scan.py`

```diff
diff --git a/.claude/skills/slop-gate/scripts/scan.py b/.claude/skills/slop-gate/scripts/scan.py
index e8a64f5..99bfe8f 100755
--- a/.claude/skills/slop-gate/scripts/scan.py
+++ b/.claude/skills/slop-gate/scripts/scan.py
@@ -7,7 +7,7 @@ Usage
     cat draft.md | python3 scan.py -    # scan stdin
     python3 scan.py --hook              # Claude Code PreToolUse/Stop hook mode (JSON on stdin)

-Exit codes: 0 clean, 1 tells found (so it works in CI and in a pre-commit hook).
+Exit codes: 0 clean, 1 tells found, 2 unreadable input (batch checks continue).

 Two tiers
```
172 additional diff lines omitted.

### `.claude/skills/voice-baseline/scripts/census.py`

```diff
diff --git a/.claude/skills/voice-baseline/scripts/census.py b/.claude/skills/voice-baseline/scripts/census.py
index 35334fd..7231e2e 100755
--- a/.claude/skills/voice-baseline/scripts/census.py
+++ b/.claude/skills/voice-baseline/scripts/census.py
@@ -33,26 +33,46 @@ WATCH = [
 # "The <noun> <past-tense verb> <short predicate>." parked at the end of a paragraph,
 # where it lands like a verdict instead of carrying a fact.
 VERDICT = re.compile(
-    r"(?:^|\. )The [a-z][a-z-]{2,14} (?:was|were|is|are|went|took|did|does|fell|lives|sits|stays|goes|came|holds|catches|kills|works|stops|moves|breaks)\b[^.\n]{0,40}\.\s*$",
+    r"(?:^|[.!?][ \t]+)The [a-z][a-z-]{2,14} (?:was|were|is|are|went|took|did|does|fell|lives|sits|stays|goes|came|holds|catches|kills|works|stops|moves|breaks)\b[^.\n]{0,40}\.[ \t]*(?=\n[ \t]*\n|\n?\Z)",
     re.M)
-KICKER = re.compile(r"\bThat (?:is|was|'s) (?:the|all|it|what|why)\b[^.\n]{0,40}\.", re.I)
```
128 additional diff lines omitted.

### `.cursor-plugin/plugin.json`

```diff
diff --git a/.cursor-plugin/plugin.json b/.cursor-plugin/plugin.json
index 5c13d6c..ecda146 100644
--- a/.cursor-plugin/plugin.json
+++ b/.cursor-plugin/plugin.json
@@ -1,8 +1,8 @@
 {
   "name": "cog-second-brain",
   "displayName": "COG: Agentic Second Brain",
-  "version": "3.12.0",
-  "description": "Self-evolving second brain powered by AI agents, Obsidian markdown, and Git. 33 skills, 10 agents (6 workers + 4 read-only verifiers), people CRM with tiered enrichment. Closed-loop harness release: V-model verification lifecycle with criterion-traced evidence, risk lanes, multi-session ultragoals with a north-star acceptance gate, craft skills for writing and visuals, and paired anti-slop design skills for marketing and product UI. Works with Claude Code, Cursor, Kiro, Gemini CLI, and Codex.",
+  "version": "3.13.1",
+  "description": "Self-evolving second brain powered by AI agents, Obsidian markdown, and Git. 35 skills, 10 agents (6 workers + 3 read-only verification roles + fix-agent), people CRM with tiered enrichment. Closed-loop harness release: V-model verification lifecycle with criterion-traced evidence, risk lanes, multi-session ultragoals with a north-star acceptance gate, craft skills for writing and visuals, and paired anti-slop design skills for marketing and product UI. Works with Claude Code, Cursor, Kiro, Gemini CLI, and Codex.",
```
35 additional diff lines omitted.

### `.github/FUNDING.yml`

```diff
diff --git a/.github/FUNDING.yml b/.github/FUNDING.yml
index 813cdbf..75f9728 100644
--- a/.github/FUNDING.yml
+++ b/.github/FUNDING.yml
@@ -2,7 +2,7 @@

 github: mithudso
 patreon: mithudso
-venmo: @Mitchphudson
+venmo: "@Mitchphudson"
 paypal: https://www.paypal.com/ncp/payment/8WLQPBK6PHFX2
 cashapp:
```
1 additional diff lines omitted.

### `.gitignore`

```diff
diff --git a/.gitignore b/.gitignore
index f19a7d4..e09053f 100644
--- a/.gitignore
+++ b/.gitignore
@@ -57,3 +57,14 @@ Thumbs.db
 .github/SUBMISSION-CHECKLIST.md
 .github/SUBMISSION-TEMPLATES.md
 .github/MARKETPLACE.md
+
+# Updater temporary files and private backups
+*.backup-*
+.cog-update.*
```
7 additional diff lines omitted.

### `AGENTS.md`

```diff
diff --git a/AGENTS.md b/AGENTS.md
index 87b8c51..36c3500 100644
--- a/AGENTS.md
+++ b/AGENTS.md
@@ -1079,3 +1079,8 @@ COG follows these principles:
 - **Self-evolving:** Patterns and frameworks grow over time
 - **Low friction:** Quick capture, systematic organization
 - **Obsidian Tasks compatible:** All tasks include emoji due dates
+
+
+## Local framework maintenance
+
```
1 additional diff lines omitted.

### `CHANGELOG.md`

```diff
diff --git a/CHANGELOG.md b/CHANGELOG.md
index 736b081..4b98147 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -2,6 +2,13 @@

 All notable changes to COG (Cognition + Obsidian + Git) will be documented in this file.

+## [3.13.1] - 2026-11-12
+
+- Repair complete upstream update control flow, atomic per-file replacement, executable modes, checkout and symlink boundaries, remote identity, and validation failures.
+- Preserve literal checkpoint records and risk-gate detection. Correct slop and voice scanners for fenced exhibits, complete edits, phrase boundaries, report exclusion, and traversal failures.
```
6 additional diff lines omitted.

### `CLAUDE.md`

```diff
diff --git a/CLAUDE.md b/CLAUDE.md
index 25b6f02..26abff7 100644
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -225,7 +225,7 @@ Role packs live in `.claude/roles/`. New roles can be added by dropping a file f
 - `COMPETITIVE-WATCHLIST.md` — Companies/people being tracked

 ### Framework files (updated via `cog-update.sh` or `/update-cog`)
-- `.claude/skills/`: Claude Code skills (33 skills)
+- `.claude/skills/`: Claude Code skills (35 skills)
 - `.claude/agents/` - Worker and verifier agent definitions (10 agents)
 - `.claude/roles/` — Role packs for personalized recommendations
```
14 additional diff lines omitted.

### `COG-VERSION`

```diff
diff --git a/COG-VERSION b/COG-VERSION
index 4eba2a6..c10780c 100644
--- a/COG-VERSION
+++ b/COG-VERSION
@@ -1 +1 @@
-3.13.0
+3.13.1
```
Complete diff.

### `CONTRIBUTING.md`

```diff
diff --git a/CONTRIBUTING.md b/CONTRIBUTING.md
index a3281f9..42a0f39 100644
--- a/CONTRIBUTING.md
+++ b/CONTRIBUTING.md
@@ -39,7 +39,7 @@ We welcome ideas for new features or improvements:
 4. **If your PR changes the framework** (skills, docs, scripts):
    - Bump the version in `COG-VERSION` (e.g., `3.2.0` → `3.3.0`)
    - Add a changelog entry in `CHANGELOG.md`
-   - If adding a new file, add it to the `FRAMEWORK_FILES` array in `cog-update.sh`
+   - Add new source/static reference files to `FRAMEWORK_FILES` in `cog-update.sh`. Keep personal workflow logs, run-specific audit reports and generated local path maps outside the upstream replacement list; stage reviewed framework paths and regenerate maps locally after updates.
    - Update `marketplace-entry.json` and `.claude-plugin/plugin.json` version fields
    - Keep the support matrix truthful in `README.md`, `SETUP.md`, `AGENTS.md`, and `docs/AGENT-SUPPORT.md`
```
10 additional diff lines omitted.

### `GEMINI.md`

```diff
diff --git a/GEMINI.md b/GEMINI.md
index a720b33..156e79f 100644
--- a/GEMINI.md
+++ b/GEMINI.md
@@ -37,3 +37,8 @@ Use `/onboarding`, `/braindump`, `/daily-brief`, `/weekly-checkin`, `/knowledge-
 - Respect domain separation: personal, professional, project-specific
 - Never fabricate sources or dates
 - All files are editable by the user — treat configuration as knowledge
+
+
+## Local framework maintenance
+
```
1 additional diff lines omitted.

### `README.md`

```diff
diff --git a/README.md b/README.md
index e05dc5d..04ab5ea 100644
--- a/README.md
+++ b/README.md
@@ -11,7 +11,7 @@
 ```mermaid
 graph LR
     A[You] -- natural language --> B[AI Agent]
-    B -- runs --> C[33 Skills]
+    B -- runs --> C[35 Skills]
     C -- delegates to --> W[6 Workers]
     C -- verified by --> V[4 Read-Only Verifiers]
```
37 additional diff lines omitted.

### `SETUP.md`

```diff
diff --git a/SETUP.md b/SETUP.md
index aad6baa..e9a4a12 100644
--- a/SETUP.md
+++ b/SETUP.md
@@ -44,10 +44,10 @@ That's it! You now have a working second brain.
 **What just happened?**
 - The cloned `COG-second-brain` folder IS your second brain
 - COG now exposes a clear multi-agent support matrix:
-  - `.claude/skills/` - 33 Claude Code skills (full surface)
+  - `.claude/skills/` - 35 Claude Code skills (full surface)
   - `.kiro/powers/` - 7 Kiro powers (core workflows)
   - `.gemini/commands/` + `.gemini/skills/` - 7 Gemini CLI commands (core workflows)
```
23 additional diff lines omitted.

### `WORKFLOW.md`

```diff
diff --git a/WORKFLOW.md b/WORKFLOW.md
index 7040eb2..73fece7 100644
--- a/WORKFLOW.md
+++ b/WORKFLOW.md
@@ -184,3 +184,8 @@ Run output lives under `04-projects/harness/`, which is created on the first har
 ## No install step

 The harness has no installer. `.claude/lib/*.sh` ship executable, run directories are created on demand, and COG ships no hooks. If a skill body ever tells you to run `install-harness.sh`, that reference is stale; report it.
+
+
+## Local maintenance reference
+
```
1 additional diff lines omitted.

### `cog-update.sh`

```diff
diff --git a/cog-update.sh b/cog-update.sh
index f91e269..708f1b6 100755
--- a/cog-update.sh
+++ b/cog-update.sh
@@ -4,19 +4,22 @@
 #
 # Usage:
 #   ./cog-update.sh            Interactive update
-#   ./cog-update.sh --check    Check for available updates (no changes)
-#   ./cog-update.sh --dry-run  Show what would change (no changes)
+#   ./cog-update.sh --check    Check for updates (fetches Git metadata; no framework-file changes)
+#   ./cog-update.sh --dry-run  Preview changes (fetches Git metadata; no framework-file changes)
```
401 additional diff lines omitted.

### `docs/AGENT-SUPPORT.md`

```diff
diff --git a/docs/AGENT-SUPPORT.md b/docs/AGENT-SUPPORT.md
index 17b77e0..4733e45 100644
--- a/docs/AGENT-SUPPORT.md
+++ b/docs/AGENT-SUPPORT.md
@@ -8,36 +8,54 @@ This document is the packaging contract: it tells contributors and maintainers w

 | Surface | Shipped format | Coverage | Status |
 |---|---|---:|---|
-| Claude Code | `.claude/skills/*/SKILL.md` | 33 skills | Full native surface |
-| Antigravity | `.agents/skills/*/SKILL.md` + `.agents/agents/*.md` | 33 skills + 10 agents | Full surface (pointer-stub format — delegates to `.claude/`, which stays authoritative) |
-| [Agent Plugins](https://agent-plugins.org) standard | Root `plugin.json` + `skills/` (generated mirror) | 33 skills | Spec 1.0.0 conformant; rebuild with `scripts/build-agent-plugin.sh` |
-| Universal agent docs | `AGENTS.md` | 17 commands | Full documented fallback |
```
83 additional diff lines omitted.

### `marketplace-entry.json`

```diff
diff --git a/marketplace-entry.json b/marketplace-entry.json
index 0679ebf..3a81f36 100644
--- a/marketplace-entry.json
+++ b/marketplace-entry.json
@@ -7,7 +7,7 @@
     "url": "https://github.com/huytieu"
   },
   "description": "Self-evolving second brain with 35 AI skills, 10 agents, and people CRM. Closed-loop harness release: V-model verification lifecycle with criterion-traced evidence, read-only verifier agents, risk lanes, multi-session ultragoals with a north-star acceptance gate, craft skills for writing and visuals, and paired anti-slop design skills for marketing and product UI. Inspired by Garry Tan's gstack and gbrain, and dwarves-kit. Works with Claude Code, Antigravity, Cursor, Kiro, Gemini CLI, Codex.",
-  "version": "3.13.0",
+  "version": "3.13.1",
   "keywords": [
     "second-brain",
```
1 additional diff lines omitted.

### `plugin.json`

```diff
diff --git a/plugin.json b/plugin.json
index 2ca889c..02782c4 100644
--- a/plugin.json
+++ b/plugin.json
@@ -1,7 +1,7 @@
 {
   "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
   "name": "cog-second-brain",
-  "version": "3.13.0",
+  "version": "3.13.1",
   "description": "Self-evolving second brain with 35 AI agent skills, 10 agents, and people CRM. Closed-loop harness: a V-model verification lifecycle (spec to evidence, criterion-traced checkpoints), read-only verifier agents that observe artifacts instead of trusting worker summaries, risk lanes, multi-session ultragoals with a north-star acceptance gate, plus craft skills for writing, visual work, and a paired anti-slop design system for marketing and product UI. Works with Claude Code, Antigravity, Cursor, Kiro, Gemini CLI, Codex, and any Agent Plugins conformant client.",
   "author": {
```
1 additional diff lines omitted.

### `scripts/build-agent-plugin.sh`

```diff
diff --git a/scripts/build-agent-plugin.sh b/scripts/build-agent-plugin.sh
index 00fb4de..c584291 100755
--- a/scripts/build-agent-plugin.sh
+++ b/scripts/build-agent-plugin.sh
@@ -1,27 +1,50 @@
 #!/usr/bin/env bash
-# build-agent-plugin.sh — regenerate the Agent Plugins standard surface.
-#
-# COG conforms to the Agent Plugins specification 1.0.0 (https://agent-plugins.org):
-# a root plugin.json manifest plus a root skills/ directory. The canonical skills
-# live in .claude/skills/ (that is what the distill and update flows write); this
-# script mirrors them to skills/ so any standard-conformant client can load COG
```
61 additional diff lines omitted.

### `scripts/validate-agent-surface.sh`

```diff
diff --git a/scripts/validate-agent-surface.sh b/scripts/validate-agent-surface.sh
index b02be22..1f76c92 100755
--- a/scripts/validate-agent-surface.sh
+++ b/scripts/validate-agent-surface.sh
@@ -1,7 +1,7 @@
 #!/usr/bin/env bash
 set -euo pipefail

-ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
+ROOT_DIR="$(CDPATH= cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
 cd "$ROOT_DIR"

```
137 additional diff lines omitted.

### `skills/review-cockpit/SKILL.md`

```diff
diff --git a/skills/review-cockpit/SKILL.md b/skills/review-cockpit/SKILL.md
index 94544d9..2683ada 100644
--- a/skills/review-cockpit/SKILL.md
+++ b/skills/review-cockpit/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: review-cockpit
-description: Produce and continuously maintain ONE living review document for a multi-item session — a cockpit header (Progress checklist, Working folder, Context) plus per-item review cards that you approve or request changes on directly in the doc or side panel. Use whenever a session has multiple deliverables you need to review/approve (meeting-processing + planning, multi-ticket work, briefs with several drafts, any "do X, then plan/draft Y and Z"). The doc is the interaction surface: you edit it (or reply in chat) to approve/change; the agent keeps it live as work progresses.
+description: "Produce and continuously maintain ONE living review document for a multi-item session — a cockpit header (Progress checklist, Working folder, Context) plus per-item review cards that you approve or request changes on directly in the doc or side panel. Use whenever a session has multiple deliverables you need to review/approve (meeting-processing + planning, multi-ticket work, briefs with several drafts, any \"do X, then plan/draft Y and Z\"). The doc is the interaction surface: you edit it (or reply in chat) to approve/change; the agent keeps it live as work progresses."
 ---

 # review-cockpit
```
Complete diff.

### `skills/slop-gate/SKILL.md`

```diff
diff --git a/skills/slop-gate/SKILL.md b/skills/slop-gate/SKILL.md
index 634e498..7d4357d 100644
--- a/skills/slop-gate/SKILL.md
+++ b/skills/slop-gate/SKILL.md
@@ -1,6 +1,6 @@
 ---
 name: slop-gate
-description: Deterministic pre-publish scan that refuses AI-slop tells in anything about to be written, published, or sent: files, artifacts, slide titles, table headers, diagram labels, chat messages, commit messages. Use before publishing or sending any deliverable, in CI, or wired as a Claude Code hook so the check runs without being remembered. The editorial counterpart is no-ai-slop, which rewrites; this one blocks.
+description: "Deterministic pre-publish scan that refuses AI-slop tells in anything about to be written, published, or sent: files, artifacts, slide titles, table headers, diagram labels, chat messages, commit messages. Use before publishing or sending any deliverable, in CI, or wired as a Claude Code hook so the check runs without being remembered. The editorial counterpart is no-ai-slop, which rewrites; this one blocks."
 ---

 <!-- slop-ok: this skill quotes the tells it blocks -->
```
Complete diff.

### `skills/slop-gate/scripts/scan.py`

```diff
diff --git a/skills/slop-gate/scripts/scan.py b/skills/slop-gate/scripts/scan.py
index e8a64f5..99bfe8f 100755
--- a/skills/slop-gate/scripts/scan.py
+++ b/skills/slop-gate/scripts/scan.py
@@ -7,7 +7,7 @@ Usage
     cat draft.md | python3 scan.py -    # scan stdin
     python3 scan.py --hook              # Claude Code PreToolUse/Stop hook mode (JSON on stdin)

-Exit codes: 0 clean, 1 tells found (so it works in CI and in a pre-commit hook).
+Exit codes: 0 clean, 1 tells found, 2 unreadable input (batch checks continue).

 Two tiers
```
172 additional diff lines omitted.

### `skills/voice-baseline/scripts/census.py`

```diff
diff --git a/skills/voice-baseline/scripts/census.py b/skills/voice-baseline/scripts/census.py
index 35334fd..7231e2e 100755
--- a/skills/voice-baseline/scripts/census.py
+++ b/skills/voice-baseline/scripts/census.py
@@ -33,26 +33,46 @@ WATCH = [
 # "The <noun> <past-tense verb> <short predicate>." parked at the end of a paragraph,
 # where it lands like a verdict instead of carrying a fact.
 VERDICT = re.compile(
-    r"(?:^|\. )The [a-z][a-z-]{2,14} (?:was|were|is|are|went|took|did|does|fell|lives|sits|stays|goes|came|holds|catches|kills|works|stops|moves|breaks)\b[^.\n]{0,40}\.\s*$",
+    r"(?:^|[.!?][ \t]+)The [a-z][a-z-]{2,14} (?:was|were|is|are|went|took|did|does|fell|lives|sits|stays|goes|came|holds|catches|kills|works|stops|moves|breaks)\b[^.\n]{0,40}\.[ \t]*(?=\n[ \t]*\n|\n?\Z)",
     re.M)
-KICKER = re.compile(r"\bThat (?:is|was|'s) (?:the|all|it|what|why)\b[^.\n]{0,40}\.", re.I)
```
128 additional diff lines omitted.

New files are explicitly listed in the coverage ledger. Their full contents are the task diff; generated maps contain only paths/classification and no private bodies.

## Blind re-audit

Both fresh-context independent audits read all 10 maintained executable/CI targets plus6contract files in source-only snapshots. Neither received this report, earlier findings, diffs, README/AGENTS or audit history. Generated mirror equality, packaging and vault hashes were verified separately.

| Attempt | Corroborated result | Directed repair / evidence |
|---|---|---|
|1|Medium: byte-only updater selection misses executable-state-only changes|Two red fixtures fail before correction; add/remove-bit cases pass after correction, including core.filemode=false.|
|2|Medium: census lazy heading capture overlaps a trailing-space matcher|The extended32000-space case times out after5seconds before repair and passes after overlap removal; both scanners receive both whitespace cases.|

**BLIND-AUDIT-DISSENT** remains the exit status. The two allowed blind attempts are exhausted. The last repair has directed static review, meaningful regression coverage and passing conventional checks, but has no third independent blind audit. No corroborated Medium+ issue remains after repair; this statement is bounded by that verification limit.

## Recommendations

Not enabled (`--suggest` absent).

## Implemented features

Not enabled. Observable changes address corroborated bugs and required repository tooling.

## Summary

5 iterations ·18 active passes ·full repository profile ·Final C/H/M/L 0/0/0/2 ·Verify: PASS ·Status: BLIND-AUDIT-DISSENT

Convergence contract: `~/.claude/skill-consolidation/convergence-and-severity.md`; deterministic helper verdicts and streaming checkpoints are retained with the external run evidence. No heuristic edit-distance claim is made here.

## Snapshot and rollback

Snapshot: `/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z`. Restore only into this task’s isolated checkout before delivery; after cleanup, recreate an isolated review checkout first. These commands intentionally do not target the primary vault or live install.

```bash
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.agents/skills/closed-loop/SKILL.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.agents/skills/closed-loop/SKILL.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.agents/skills/editorial-illustrations/SKILL.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.agents/skills/editorial-illustrations/SKILL.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.agents/skills/retro/SKILL.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.agents/skills/retro/SKILL.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.agents/skills/review-cockpit/SKILL.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.agents/skills/review-cockpit/SKILL.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.agents/skills/slop-gate/SKILL.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.agents/skills/slop-gate/SKILL.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.agents/skills/ultragoal/SKILL.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.agents/skills/ultragoal/SKILL.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.claude-plugin/plugin.json" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.claude-plugin/plugin.json"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.claude/lib/checkpoint.sh" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.claude/lib/checkpoint.sh"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.claude/lib/lane-classify.sh" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.claude/lib/lane-classify.sh"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.claude/skills/review-cockpit/SKILL.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.claude/skills/review-cockpit/SKILL.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.claude/skills/slop-gate/SKILL.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.claude/skills/slop-gate/SKILL.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.claude/skills/slop-gate/scripts/scan.py" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.claude/skills/slop-gate/scripts/scan.py"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.claude/skills/voice-baseline/scripts/census.py" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.claude/skills/voice-baseline/scripts/census.py"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.cursor-plugin/plugin.json" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.cursor-plugin/plugin.json"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.github/FUNDING.yml" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.github/FUNDING.yml"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.gitignore" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.gitignore"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/AGENTS.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/AGENTS.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/CHANGELOG.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/CHANGELOG.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/CLAUDE.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/CLAUDE.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/COG-VERSION" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/COG-VERSION"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/CONTRIBUTING.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/CONTRIBUTING.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/GEMINI.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/GEMINI.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/README.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/README.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/SETUP.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/SETUP.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/WORKFLOW.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/WORKFLOW.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/cog-update.sh" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/cog-update.sh"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/docs/AGENT-SUPPORT.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/AGENT-SUPPORT.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/marketplace-entry.json" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/marketplace-entry.json"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/plugin.json" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/plugin.json"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/scripts/build-agent-plugin.sh" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/scripts/build-agent-plugin.sh"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/scripts/validate-agent-surface.sh" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/scripts/validate-agent-surface.sh"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/skills/review-cockpit/SKILL.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/skills/review-cockpit/SKILL.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/skills/slop-gate/SKILL.md" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/skills/slop-gate/SKILL.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/skills/slop-gate/scripts/scan.py" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/skills/slop-gate/scripts/scan.py"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/skills/voice-baseline/scripts/census.py" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/skills/voice-baseline/scripts/census.py"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.editorconfig"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.gitattributes"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.github/CODEOWNERS"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.github/ISSUE_TEMPLATE/bug_report.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.github/ISSUE_TEMPLATE/feature_request.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.github/PULL_REQUEST_TEMPLATE.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.github/SECURITY.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.github/copilot-instructions.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.github/dependabot.yml"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/.github/workflows/ci.yml"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/ARCHITECTURE.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/COMPONENTS.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/DEVELOPMENT.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/INSTALLATION.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/MCP.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/SECURITY.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/TESTING.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/archive/README.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/caching-and-optimization.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/code-deep-optimizer-2026-11-12.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/codebase-overview.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/external-calls.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/high_signal_file_index.json"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/integrations-and-assumptions.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/known-issues.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/logging.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/maintenance-coverage-2026-11-12.json"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/onboarding.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/repo-bootstrap-audit-2026-11-12.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/requirements.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/runbooks/framework-update.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/runbooks/validation.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/wiki/index.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/docs/wiki/maintenance.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/llms.txt"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/memory.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/prompts.md"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/scripts/doc_indexes.py"
rm -f -- "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-second-brain/tests/test_maintenance.py"
```

index: skipped (semantic/embedding pause); offline path maps refreshed and path-validated without content or vectors.

memory-central: no prior COG lessons/conventions files found; no global user memory file changed. Durable source lessons were captured through Stele during implementation; the report does not imply those bugs were known before this run.

## Post-merge validation follow-up, iteration 5

Initial delivery PR2 merged as 28064e9e5494049ef8689db214ca96a04fcaea1a after 4 PR and 4 main matrix jobs passed. Exact remote/tested tree equality and all 74 owned blobs were verified. The synchronized primary validator then failed source parity. Its exact diff was `Only in skills: .DS_Store`. The initial bytecode hypothesis was not confirmed by that diff and was corrected immediately in the continuation record.

**Medium — C1/S2, scripts/validate-agent-surface.sh:65 and scripts/build-agent-plugin.sh:** recursive diff and copy treated ignored filesystem artifacts as maintained skill source. Source parity now excludes exactly `.DS_Store`, `__pycache__`, `*.pyc` and `*.pyo`. The builder strips them only inside its owned staging copy. It never cleans canonical or primary files. Three regressions verify canonical artifact preservation, artifact-only parity and continued rejection of an unexpected source file. Two red cases produced 5 failing assertions before correction.

The follow-up aligns 5 version surfaces at 3.13.2 and extends the suite to 63 tests. Directed fresh per-file diagnostics reviewed both helpers with no additional Medium+ findings; a directed test review covers the new regressions. These are iteration diagnostics, not a third blind exit gate. The exit remains **BLIND-AUDIT-DISSENT**. No corroborated Medium+ finding remains after directed repairs, with the independent-gate limit unchanged. Final remote checks and the primary artifact hash are recorded in the delivery receipt.

Follow-up rollback (isolated follow-up checkout only):

```bash
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.claude-plugin/plugin.json.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/.claude-plugin/plugin.json"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/.cursor-plugin/plugin.json.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/.cursor-plugin/plugin.json"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/CHANGELOG.md.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/CHANGELOG.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/COG-VERSION.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/COG-VERSION"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/docs/COMPONENTS.md.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/docs/COMPONENTS.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/docs/TESTING.md.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/docs/TESTING.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/docs/code-deep-optimizer-2026-11-12.md.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/docs/code-deep-optimizer-2026-11-12.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/docs/known-issues.md.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/docs/known-issues.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/docs/maintenance-coverage-2026-11-12.json.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/docs/maintenance-coverage-2026-11-12.json"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/docs/repo-bootstrap-audit-2026-11-12.md.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/docs/repo-bootstrap-audit-2026-11-12.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/marketplace-entry.json.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/marketplace-entry.json"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/memory.md.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/memory.md"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/plugin.json.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/plugin.json"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/scripts/build-agent-plugin.sh.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/scripts/build-agent-plugin.sh"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/scripts/validate-agent-surface.sh.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/scripts/validate-agent-surface.sh"
cp "/Users/mitch.hudson/.claude/skill-consolidation/backups/COG-second-brain-20261112T085029Z/tests/test_maintenance.py.iter5" "/Users/mitch.hudson/dev/.repo-maintenance/20261112T081335Z/app-worktrees/COG-bytecode-parity/tests/test_maintenance.py"
```

The directed test audit also found a Medium T1 coverage gap: placing the only `.pyc` file below `__pycache__` masked an independent exclusion rule. Standalone `.pyc` and `.pyo` cases plus an explicit directory-absence assertion now cover each rule independently. This is repaired within iteration 5. A 63rd hostile-template/global-hook test proves that fixture initialization strips inherited Git overrides, uses its own empty template, verifies actual hook configuration before committing, and never runs the sentinel hook.

The final local 63-test run uses the task-local `mdbx-egress-runner.py` process-tree guard, with all outbound networking (including loopback) denied. COG has no model/provider inference path. Earlier runs used isolated Git templates/global config but did not use this later egress helper; historical dispatch is therefore unverified until the separate task-specific redacted metadata audit resolves it. Real repository commits had no active hooks; this does not by itself prove fixture isolation in past runs.

Controlled mutation checks removed each of the four exclusion rules independently in disposable helper copies. Both regression targets detected every removed rule with assertion failures and zero test errors. These checks ran under the same process-tree outbound deny guard and never modified the repository helpers.
