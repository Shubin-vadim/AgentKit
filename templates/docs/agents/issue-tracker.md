# Issue tracker

<!--
Tells agents where this project's specifications live, so `code-review` and
other skills can fetch the spec for a change. Fill the fields below and delete
the ones that do not apply. Do not put tokens or passwords here.
-->

- **Tracker:** <GitHub Issues | GitLab Issues | Jira | Linear | other | none>
- **Project or queue:** <owner/repo, project key, or queue name>
- **Issue key format:** <#123 | PROJ-123>
- **How to fetch an issue:** <MCP server name, `gh issue view <n>`, `glab issue view <n>`, or a URL pattern>
- **Where the key appears:** <branch name `feature/PROJ-123-slug`, commit message, PR title>
- **Other spec sources:** <PRD folder, OpenSpec changes under `openspec/changes/`>

## Until this file is filled in

1. If an OpenSpec change exists under `openspec/changes/`, use its proposal and specs.
2. Else, if an issue-tracker MCP is connected, fetch the issue from it.
3. Else, if the remote is GitHub, use `gh`; if GitLab, use `glab`.
4. Otherwise ask the user where the spec lives.

Do not invent issue keys.
