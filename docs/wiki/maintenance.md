# Maintenance reference

The [bootstrap audit](../repo-bootstrap-audit-2026-11-12.md) records file-by-file standards coverage. It distinguishes applicable additions, intentional exceptions, and unresolved gaps. It is not an optimizer completion report or live application certification.

Canonical skills are in `.claude/skills/`. Edit those files, rebuild `skills/`, and check packaging. `.agents/` files are pointer stubs; Kiro and Gemini each retain seven native core workflows. All 10 canonical agent roles are linked in [components](../COMPONENTS.md).

Use the [validation runbook](../runbooks/validation.md) for offline checks and the [framework update runbook](../runbooks/framework-update.md) for authorized upstream work. Check/dry-run update modes still fetch. Never use a real upstream update as a maintenance-test substitute.

Keep [memory](../../memory.md) and [prompts](../../prompts.md) append-only and sanitized. Review [archive guidance](../archive/README.md) near 200 KB. No automatic log rotation or semantic watcher is installed.

The parent maintenance task owns source fixes, generated maps, optimizer assessment, version changes, final verification, and delivery. This documentation package does not imply those steps are finished.
