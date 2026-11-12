# MCP boundary

COG does not implement or ship an MCP server. The maintenance helpers expose no MCP tools, authentication endpoints, or ports. There is no required repository `.mcp.json` or editor MCP configuration.

Some playbooks can use host-provided MCP integrations, such as Slack, Linear, PostHog, or Confluence. Availability, tool names, server commands, credentials, and scopes depend on the user's agent installation. This repository cannot supply a universal tool inventory or certify those connections offline.

Before an integration-backed workflow, inspect the user's integration preferences, confirm that the host exposes the required tools, and use the skill's approval and post-condition rules. Do not probe disabled integrations. A file describing an integration is not evidence of a working connection.

For example, the team brief playbook can gather GitHub evidence and optionally use active team integrations; the Confluence publishing playbook requires a configured target and its own preview/approval step. These are workflow examples, with no bundled server invocation.

To add a connection, the user configures it in the chosen host using that provider's instructions and private credential store. Keep secrets out of Git. Test only the authorized read or mutation and observe its result. See [integrations and assumptions](integrations-and-assumptions.md) and [external calls](external-calls.md).
