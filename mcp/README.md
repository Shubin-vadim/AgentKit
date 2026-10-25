# MCP

Portable MCP definitions, not vendor checkouts of MCP servers: a stdio launch
(`command` + `args`) or a remote endpoint (`url` + `headers`).
Each file is one server: the JSON object key is the server name.

`scripts/kit.py install` translates these definitions into each client's
configuration (`.cursor/mcp.json`, `.mcp.json`, `opencode.json`,
`.codex/config.toml`); existing entries are skipped unless `--force`. Write
secrets as `${env:NAME}`: the installer rewrites that per client. Tokens stay
out of git; set them as environment variables the client can see.

| Fragment | Profile | Package |
|----------|---------|---------|
| [context7/context7.json](./context7/context7.json) | `core` | [`@upstash/context7-mcp@4.4.4`](https://www.npmjs.com/package/@upstash/context7-mcp) |
| [codegraph/codegraph.json](./codegraph/codegraph.json) | `core` | [`@colbymchenry/codegraph@1.6.2`](https://www.npmjs.com/package/@colbymchenry/codegraph) ([colbymchenry/codegraph](https://github.com/colbymchenry/codegraph)) |
| [drawio/drawio.json](./drawio/drawio.json) | `architecture` | [`@drawio/mcp@1.10.0`](https://www.npmjs.com/package/@drawio/mcp) ([jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp)) |
| [github/github.json](./github/github.json) | `github` | Remote [GitHub MCP server](https://github.com/github/github-mcp-server) (`https://api.githubcopilot.com/mcp/`) |
| [playwright/playwright.json](./playwright/playwright.json) | `playwright` | [`@playwright/mcp@0.0.83`](https://www.npmjs.com/package/@playwright/mcp) ([microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)) |
| [reverse-engineering/rea.json](./reverse-engineering/rea.json) | `reverse-engineering` | [`rea-agents@6.7.0`](https://www.npmjs.com/package/rea-agents) ([morluto/rea](https://github.com/morluto/rea)) |

Context7 4.x needs Node.js 20.18.1+. Every fragment pins its package version so
a new release cannot silently change tool names; bump versions deliberately.

Optional Context7 API key: configure it in the client or through
`CONTEXT7_API_KEY`. Do not commit the key.

draw.io opens diagrams from Mermaid, CSV, or draw.io XML in the browser
editor (`app.diagrams.net` by default; set `DRAWIO_BASE_URL` for a self-hosted
instance). It can also read and rewrite pages of a local `.drawio` file and
search about 10,000 cloud and network shapes. Keep Mermaid in the repo as the
source of truth; use draw.io when a diagram needs precise layout or icons.

GitHub reads a personal access token from the environment variable
`GITHUB_PERSONAL_ACCESS_TOKEN` (written as `${env:...}` and translated per
client); the variable must be visible to the client process, not only to a
shell. Scope the
token to what the agent needs. For read-only use, change the URL to
`https://api.githubcopilot.com/mcp/readonly`; `X-MCP-Toolsets` (for example
`repos,issues,pull_requests,actions`) narrows the tool list.

Playwright needs Node.js 18+ and downloads a browser on first use. The version
is pinned because tool names change between releases; bump it deliberately.

REA needs Node.js 22.19+, 24.11+, or 26+, plus npm. The supplied Windows
launch definition uses `cmd.exe /d /c npx` to run npm's command shim. It
performs local analysis; optional native-analysis providers such as Ghidra,
IDA, and JADX are bring-your-own and are not installed by this kit.

## References

- [webmachinelearning/webmcp](https://github.com/webmachinelearning/webmcp): draft web standard (not an MCP server, nothing to install). Pages expose tools to agents via `document.modelContext.registerTool()`. Only npm artifact: [`webmcp-types`](https://www.npmjs.com/package/webmcp-types) (TypeScript types). Related: MCP-B.

codegraph needs a per-project index: run `npx -y @colbymchenry/codegraph@1.6.2 init -y` once in the target root. It
writes `.codegraph/` (ignored by its own `.gitignore`) and keeps the index in
sync while the server runs. By default the server exposes one tool,
`codegraph_explore`; `CODEGRAPH_MCP_TOOLS` enables the others. The fragment sets
`CODEGRAPH_TELEMETRY=0` to turn off its anonymous usage stats.
