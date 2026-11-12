# Caching and optimization

COG has no repository-owned CDN, database query cache, in-memory application cache, semantic vector cache, or running indexing watcher.

| Derived state | Refresh/invalidation | Limits |
|---|---|---|
| Root `skills/` mirror | Rebuild from `.claude/skills/` after canonical edits | Generated copy; writer lock protects competing builds; validator compares the directories |
| Retrieval maps | Regenerate from reviewed tracked/staged paths after path additions/removals | Path-only output; `--check` fails on stale output; no embeddings |
| Fetched upstream Git objects/refs | Explicit updater fetch | Git-managed state; not a background refresh or cache TTL |
| Optional host/editor caches | Host or Obsidian manages them | Outside this repository's maintenance contract |

The mirror builder copies to staging before replacing a valid mirror. Updater file replacements use same-directory temporary files. These patterns protect existing files on failures; they do not establish a transaction for a whole framework update.

The census processes selected corpus files and excludes its own output. The scanner uses regex rules and has a regression case for a whitespace-prefix input. Neither has a published scale benchmark or resource budget. Large corpora and recursive packaging comparisons can cost more time as the checkout grows.

For an authorized synthetic profiling task, use `python3 -m cProfile -s cumulative .claude/skills/voice-baseline/scripts/census.py <synthetic-corpus>` or time an isolated helper invocation. Do not profile real private notes for a public report. Preserve raw measurements before making performance claims.

The parent maintenance task owns the optimizer assessment. This reference records patterns and limits; it does not declare that assessment complete. See [known issues](known-issues.md).
