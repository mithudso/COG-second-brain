# Maintainer wiki

This wiki is local Markdown navigation. It has no remote publishing or synchronization step.

| Need | Reference |
|---|---|
| Install or start contributing | [Installation](../INSTALLATION.md), [onboarding](../onboarding.md), [development](../DEVELOPMENT.md) |
| Understand files and flows | [Architecture](../ARCHITECTURE.md), [components](../COMPONENTS.md), [requirements](../requirements.md) |
| Check a change | [Testing](../TESTING.md), [validation runbook](../runbooks/validation.md) |
| Update framework files | [Framework update runbook](../runbooks/framework-update.md) |
| Review security and integrations | [Security](../SECURITY.md), [MCP](../MCP.md), [integrations and assumptions](../integrations-and-assumptions.md), [external calls](../external-calls.md) |
| Understand maintenance state | [Maintenance](maintenance.md), [known issues](../known-issues.md), [bootstrap audit](../repo-bootstrap-audit-2026-11-12.md) |
| Inspect logging and derived state | [Logging](../logging.md), [caching and optimization](../caching-and-optimization.md), [archive policy](../archive/README.md) |
| Check host packaging | [Agent support](../AGENT-SUPPORT.md), [skill distillation](../SKILL-DISTILLATION.md) |

The generated repository map is maintained by `scripts/doc_indexes.py`. It lists reviewed tracked/staged paths, reads no vault bodies, and runs offline. The delivery owner refreshes it after staging intended public paths.
