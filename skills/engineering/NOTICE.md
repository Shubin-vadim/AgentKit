These skills are copied from
https://github.com/mattpocock/skills/tree/main/skills/engineering

- research
- codebase-design
- code-review
- domain-modeling
- improve-codebase-architecture
- grill-with-docs
- wayfinder
- to-spec
- to-tickets
- triage
- implement
- tdd
- prototype
- diagnosing-bugs
- resolving-merge-conflicts
- wizard

`code-review` is adapted: it no longer requires `/setup-matt-pocock-skills`. If `docs/agents/issue-tracker.md` is missing, it uses `gh` / GitLab CLI or asks where the spec lives.

`grill-with-docs` and `improve-codebase-architecture` are adapted: Claude Code Skill tool calls are replaced with local paths to `grilling`, `domain-modeling`, and `codebase-design`.

`wayfinder` is adapted: it no longer requires `/setup-matt-pocock-skills`. Tracker lookup follows `code-review` (`docs/agents/issue-tracker.md`, then `gh` / GitLab CLI, then a local-markdown fallback); Skill tool calls are replaced with local paths to `grilling`, `domain-modeling`, `research`, and `prototype`.

`to-spec`, `to-tickets`, and `triage` are adapted the same way: no `/setup-matt-pocock-skills`; tracker via `docs/agents/issue-tracker.md` → `gh` / GitLab CLI → `.scratch/` markdown; triage labels via `docs/agents/triage-labels.md` or the canonical names. `tdd`, `implement`, and `triage` reference `codebase-design`, `code-review`, `tdd`, `grilling`, and `domain-modeling` by local path.

Not included: `ask-matt` (router over the upstream repo) and `setup-matt-pocock-skills` (replaced by the conventions above).

MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
