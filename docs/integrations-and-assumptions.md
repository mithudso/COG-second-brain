# Integrations and assumptions

## Shipped executable boundary

The updater's configured official source is `https://github.com/huytieu/COG-second-brain.git`, remote name `cog-upstream`, branch `main`. The personal fork is `https://github.com/mithudso/COG-second-brain`. The updater accepts the source-coded HTTPS/SSH forms for that official repository; it refuses a foreign identity. It uses Git's existing transport authentication and performs no GitHub API login.

The network operation is `git fetch`. `git remote get-url`, `remote add`, `rev-parse`, `show`, and `ls-tree` are local operations. Check/dry-run modes still fetch and can create remote configuration. See the [call inventory](external-calls.md).

## Optional workflow services

Playbooks describe GitHub CLI, Linear, Slack, Jira, PostHog, HackMD, Confluence, Notion, web search/fetch, and other host-provided capabilities. The user selects active integrations. This list describes workflow surfaces, not installed or healthy connections.

| Surface | Source example | Target/auth/data boundary |
|---|---|---|
| GitHub and team tools | `.claude/skills/team-brief/SKILL.md` | User-selected repositories, work items, analytics, and messages; host/CLI credentials |
| HackMD | Same playbook, publishing phases | `https://api.hackmd.io/v1`; user token and workspace; brief body and returned note link |
| Confluence | `.claude/skills/publish-to-confluence/SKILL.md` | User-supplied site URL and space; host/provider auth; document body and page metadata |
| Slack, Notion, webhooks | `.claude/agents/worker-publisher.md` | User-selected target; credential mechanism and returned artifact depend on host |
| Web research | Research/brief playbooks | URLs and query content chosen for authorized research; provider access varies |

No shared service base URL, account ID, token environment variable, retry library, or permission model can be inferred for every host. Configure and test each connection only when authorized. No integration was probed in this documentation task.

## Environment assumptions

Helpers expect a Git checkout, readable canonical files, writable temporary storage for write operations, and standard Unix commands. Updater resolves the checkout containing its script and rejects linked framework paths. The seven native Kiro/Gemini workflows are deliberate subsets; `.agents/` stubs and `skills/` are derived surfaces.

CI has a fresh checkout and no private vault contents. Local worktrees can contain unrelated edits and sensitive ignored content. Review intended paths before staging or generating maps. There is no dev/prod deployment split, mandatory server environment, or datastore to configure. GitHub-hosted CI downloads actions and Python as infrastructure, separate from helper network behavior.
