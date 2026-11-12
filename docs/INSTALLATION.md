# Installation

COG is a directory of playbooks, Markdown templates, and maintenance helpers. There is no mandatory package install, server deployment, database migration, or model download.

## Prerequisites

Use a Markdown-capable agent host. Obsidian and Git sync are optional for everyday note use. Maintainers need Git, Bash, Python 3, and Unix tools; supported CI combinations are Ubuntu/macOS with Python 3.11/3.13. No hardware minimum has been measured. Windows-native helper execution is not covered by CI.

## Get the files

```bash
git clone https://github.com/mithudso/COG-second-brain.git
cd COG-second-brain
./scripts/validate-agent-surface.sh
```

This URL is the personal fork. The original project is [Huy Tieu's COG](https://github.com/huytieu/COG-second-brain), licensed under [MIT](../LICENSE). Existing upstream installation links in [SETUP](../SETUP.md) continue to identify that project.

Open the folder in the selected agent. Canonical skills live in `.claude/skills/`; `AGENTS.md` supplies universal documentation. Gemini and Kiro ship seven native core workflows each. Consult [components](COMPONENTS.md) for packaging boundaries. Invoke personal onboarding only when the user requests personalization; it is unnecessary for maintenance validation.

## Verify and upgrade

Run the [offline validation procedure](runbooks/validation.md). It verifies packaging and helper behavior, without testing a live app or integration. Choose optional connections only through the user's host configuration.

For upstream changes, follow the [framework update runbook](runbooks/framework-update.md). Both `--check` and `--dry-run` fetch Git metadata and may add the official upstream remote. They are not offline commands.

## Remove

Back up personal notes and user-owned host configuration first. Close applications using the checkout, then remove only the intended clone or disable its plugin in the host that installed it. No repository-owned service, daemon, or datastore needs removal. Do not delete a shared vault to uninstall framework files.
