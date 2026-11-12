# COG Agent Support Matrix

COG intentionally ships **multiple agent surfaces**. They are not all identical.

This document is the packaging contract: it tells contributors and maintainers which surfaces are first-class today, which ones are partial, and what must stay in sync before publishing a release.

## Current Support Matrix

| Surface | Shipped format | Coverage | Status |
|---|---|---:|---|
| Claude Code | `.claude/skills/*/SKILL.md` | 35 skills | Full native surface |
| Antigravity | `.agents/skills/*/SKILL.md` + `.agents/agents/*.md` | 35 skills + 10 agents | Full surface (pointer-stub format — delegates to `.claude/`, which stays authoritative) |
| [Agent Plugins](https://agent-plugins.org) standard | Root `plugin.json` + `skills/` (generated mirror) | 35 skills | Spec 1.0.0 conformant; rebuild with `scripts/build-agent-plugin.sh` |
| Universal agent docs | `AGENTS.md` | 35 commands | Full documented fallback |
| Kiro | `.kiro/powers/*/POWER.md` | 7 powers | Core workflows only |
| Gemini CLI | `.gemini/commands/*.toml` + `.gemini/skills/*.md` | 7 commands | Core workflows only |

## What “Full” vs “Core” Means

### Full surfaces
These surfaces expose the complete public COG command set:
- `auto-research`
- `braindump`
- `closed-loop`
- `comprehensive-analysis`
- `content-factory`
- `create-user-story`
- `daily-brief`
- `daily-journal`
- `data-forms`
- `editorial-illustrations`
- `export-open-issues`
- `generate-prd`
- `generate-release-notes`
- `harvest`
- `knowledge-consolidation`
- `loop-engineering`
- `meeting-transcript`
- `memory-hygiene`
- `museum-art`
- `no-ai-slop`
- `onboarding`
- `product-ui-taste`
- `publish-to-confluence`
- `retro`
- `review-cockpit`
- `scout`
- `slop-gate`
- `taste-skill`
- `team-brief`
- `ultragoal`
- `update-cog`
- `update-knowledge-base`
- `url-dump`
- `voice-baseline`
- `weekly-checkin`

Today, **Claude Code**, **Antigravity**, **Agent Plugins**, **Cursor packaging**, and **`AGENTS.md`** carry all 35 skills. Static packaging consistency does not certify live client interpretation.

### Core surfaces
These surfaces intentionally cover the most common personal workflows first:
- `onboarding`
- `braindump`
- `daily-brief`
- `weekly-checkin`
- `knowledge-consolidation`
- `url-dump`
- `update-cog`

Today, **Kiro** and **Gemini CLI** are core surfaces.

## Packaging Rules

If you add, remove, rename, or materially change a public COG skill:

1. Update the **Claude skill** in `.claude/skills/`
2. Update the matching **Antigravity pointer stub** in `.agents/skills/<name>/SKILL.md` (same template as the existing stubs — `name` + `description` only change, the body always points back at `.claude/skills/<name>/SKILL.md` as authoritative)
3. Update **`AGENTS.md`** for the universal surface
4. Update **`.claude-plugin/plugin.json`** and **`.cursor-plugin/plugin.json`** so packaged skill/agent inventories stay truthful
5. Update **README / SETUP / this file** if counts or support levels change
6. If the skill is supported natively in Kiro or Gemini, update those files too
7. Add new framework files to `FRAMEWORK_FILES` in `cog-update.sh`
8. Run `./scripts/validate-agent-surface.sh`

## Validation

Run this before tagging a release, opening a packaging PR, or after using `./cog-update.sh`:

```bash
./scripts/validate-agent-surface.sh
```

The validator checks:
- manifest JSON validity and unique, complete canonical skill paths
- Cursor version, skill entries and exact agent inventory
- all five version surfaces and generated skill mirror equality
- declared skill paths in `.claude-plugin/plugin.json`
- plugin skill count vs actual shipped Claude skills
- `AGENTS.md` coverage for all manifest skills
- common packaging drift like `agents.md` vs `AGENTS.md`

## Safe Update Workflow

Recommended maintainer flow:

```bash
./cog-update.sh --check
./cog-update.sh
./scripts/validate-agent-surface.sh
```

If you have local framework customizations, prefer interactive update mode so you can backup per-file before replacing anything.
