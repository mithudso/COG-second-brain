# Logging

Maintenance helpers print human-readable diagnostics to stdout/stderr. There is no centralized logger, telemetry collector, remote log sink, or common JSON event schema.

| Producer | Output | Contract |
|---|---|---|
| Updater and validator | Console info/success/warning/error messages | Nonzero failures matter; retain sanitized command output with the maintenance review |
| Mirror builder | Console count or failure/lock/recovery message | Inspect staged recovery location if recovery fails; do not delete another writer's lock |
| Scanner | File label, tell snippets, or host hook JSON decision | Snippets may contain source text; do not publish output from sensitive inputs |
| Census | Baseline report, draft comparison, or stderr failure | Corpus names and phrases can be sensitive; keep private reports local |
| Checkpoint helper | Per-run `evidence/checkpoints.tsv` and `.claude/logs/checkpoint-ledger.tsv` | Append-only timestamped TSV; fields escape backslashes, tabs, CR, and LF |
| Documentation indexer | Success message or stale/error diagnostic | Paths only; no source-body logging |
| Agent workflows | Skill-specific notes and optional harness ledgers | Not every workflow produces a log; no remote collection is bundled |

`info`, `ok`, `warn`, and `err` are presentation labels in shell helpers, with no central severity filter. Most helpers do not write log files. Checkpoint status reads existing records and does not create a log directory.

For new diagnostics, identify the operation and outcome, use stderr for failures, and preserve a useful exit code. Test error paths and observable preservation effects. Do not claim request/outcome instrumentation for every external integration; [external-call coverage](external-calls.md) is partial.

Do not log tokens, credential-bearing URLs, private vault bodies, customer data, or reversible maps. Checkpoint notes are arbitrary caller text, so callers must sanitize them. TSV escaping protects field formatting. It does not redact or encrypt text.

[memory.md](../memory.md) and [prompts.md](../prompts.md) are append-only workflow logs. They start small. Automatic size-based rotation is a declared gap; use [archive guidance](archive/README.md) before either approaches 200 KB. No rotation script or scheduled job is shipped by this update.

Checkpoint record commands fail explicitly while the shared ledger lock is busy. Retry after the current writer finishes; never remove an active lock. TSV fields escape backslashes, tabs, CR and newlines so one observation stays one physical row.
