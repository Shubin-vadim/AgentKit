# Architecture: <system name>

<!--
System design spine in the arc42 structure (https://arc42.org/, CC BY-SA 4.0).
This file points at other documents instead of copying them:
diagrams in docs/C4.md, decisions in adr/, quality scenarios in docs/quality.md,
threats in docs/threat-model.md, glossary in CONTEXT.md.
Always fill sections 1, 3, 5, 9, and 12. Fill the others when there is
something real to say; otherwise replace the body with one line on why it is
skipped. Never invent numbers or history: write TODO and name who knows.
Agents fill this file with the `system-design` skill.
-->

## 1. Introduction and goals

### Requirements overview

<One paragraph: what the system does and for whom.> Specification: <link to PRD, issue, or OpenSpec change>.

### Quality goals

| Priority | Quality characteristic | Scenario |
|----------|------------------------|----------|
| 1 | <Reliability> | [Q-01](quality.md#q-01) |
| 2 | <...> | <...> |

### Stakeholders

| Role | Expectations from this document |
|------|---------------------------------|
| <Developer> | <...> |

## 2. Architecture constraints

| Type | Constraint | Why |
|------|------------|-----|
| Technical | <must run on X, must use Y> | <...> |
| Organizational | <team, compliance, deadline> | <...> |
| Convention | <repository layout, documentation> | <...> |

## 3. Context and scope

Diagram: [C1](C4.md#c1-system-context).

| Partner | Input | Output |
|---------|-------|--------|
| <User> | <...> | <...> |
| <External system> | <...> | <...> |

Out of scope: <what this system deliberately does not do>.

## 4. Solution strategy

<!-- Five to ten bullets: architecture style, sync vs async, where state
lives, how modules are sliced. Link an ADR for each hard-to-reverse choice. -->

- <Approach>. See [ADR NNNN](../adr/NNNN-slug.md).

## 5. Building block view

Diagrams: [C2](C4.md#c2-containers), C3 where a boundary exists.

| Building block | Responsibility |
|----------------|----------------|
| <API> | <...> |

## 6. Runtime view

Key path: [sequence](C4.md#key-runtime-path). <One sentence on what it shows.>

## 7. Deployment view

See [Deployment](C4.md#deployment). <What runs where, instances, durable stores.>

## 8. Cross-cutting concepts

<!-- One heading per concept the system actually uses: authentication,
observability, error handling, multi-tenancy. Delete the example if none. -->

### <Concept>

<One paragraph and a pointer to the module or ADR.>

## 9. Architecture decisions

Bodies live in [adr/](../adr/README.md).

| ADR | Title | Status | Effect |
|-----|-------|--------|--------|
| [0001](../adr/0001-slug.md) | <...> | <Accepted> | <one line> |

## 10. Quality requirements

Scenarios: [quality.md](quality.md).

## 11. Risks and technical debt

| Risk or debt | Impact | Mitigation |
|--------------|--------|------------|
| <...> | <H/M/L> | <mitigation, or "accepted"> |

Security threats: [threat-model.md](threat-model.md).

## 12. Glossary

See [CONTEXT.md](../CONTEXT.md).
