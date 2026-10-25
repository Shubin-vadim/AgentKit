---
name: langgraph-fundamentals
description: >-
  LangGraph patterns for StateGraph, nodes, edges, tools, checkpointer, streaming,
  and error handling. Use when creating or modifying LangGraph orchestrators, graphs,
  tools, or state models.
license: MIT
metadata:
  source: https://github.com/langchain-ai/langchain-skills
---

<overview>
LangGraph models agent workflows as **directed graphs**:

- **StateGraph**: Main class for building stateful graphs
- **Nodes**: Functions that perform work and update state
- **Edges**: Define execution order (static or conditional)
- **START/END**: Special nodes marking entry and exit points
- **State with Reducers**: Control how state updates are merged

Graphs must be `compile()`d before execution.
</overview>

<design-methodology>

### Designing a LangGraph application

Follow these 5 steps when building a new graph:

1. **Map out discrete steps** — sketch a flowchart of your workflow. Each step becomes a node.
2. **Identify what each step does** — categorize nodes: LLM step, data step, action step, or user input step. For each, determine static context (prompt), dynamic context (from state), retry strategy, and desired outcome.
3. **Design your state** — state is shared memory for all nodes. Store raw data, format prompts on-demand inside nodes.
4. **Build your nodes** — implement each step as a function that takes state and returns partial updates.
5. **Wire it together** — connect nodes with edges, add conditional routing, compile with a checkpointer if needed.

</design-methodology>

<when-to-use-langgraph>

| Use LangGraph When | Use Alternatives When |
|-------------------|----------------------|
| Need fine-grained control over agent orchestration | Quick prototyping → LangChain agents |
| Building complex workflows with branching/loops | Simple stateless workflows → LangChain direct |
| Require human-in-the-loop, persistence | Batteries-included features → Deep Agents |

</when-to-use-langgraph>

<references>
Code for every section lives in `references/`; open only the file you need:

| File | Contents |
|------|----------|
| [state.md](references/state.md) | Reducers, partial updates |
| [nodes-and-edges.md](references/nodes-and-edges.md) | Node signatures, basic graph, conditional edges |
| [command-and-send.md](references/command-and-send.md) | `Command`, `Send`, orchestrator-worker |
| [running-and-streaming.md](references/running-and-streaming.md) | `invoke`, stream modes |
| [errors-and-fixes.md](references/errors-and-fixes.md) | Retry policy, tool errors, common fixes |
</references>

---

## State Management

<state-update-strategies>

| Need | Solution | Example |
|------|----------|---------|
| Overwrite value | No reducer (default) | Simple fields like counters |
| Append to list | Reducer (operator.add / concat) | Message history, logs |
| Custom logic | Custom reducer function | Complex merging |

</state-update-strategies>

Examples: [references/state.md](references/state.md) — reducer state, missing list reducer, returning partial dicts.

---

## Nodes

Node signatures (Python; TypeScript in the reference):

| Signature | When to Use |
|-----------|-------------|
| `def node(state: State)` | Simple nodes that only need state |
| `def node(state: State, config: RunnableConfig)` | Need thread_id, tags, or configurable values |
| `def node(state: State, runtime: Runtime[Context])` | Need runtime context, store, or stream_writer |

Examples: [references/nodes-and-edges.md](references/nodes-and-edges.md).

---

## Edges

<edge-type-selection>

| Need | Edge Type | When to Use |
|------|-----------|-------------|
| Always go to same node | `add_edge()` | Fixed, deterministic flow |
| Route based on state | `add_conditional_edges()` | Dynamic branching |
| Update state AND route | `Command` | Combine logic in single node |
| Fan-out to multiple nodes | `Send` | Parallel processing with dynamic inputs |

</edge-type-selection>

Examples: [references/nodes-and-edges.md](references/nodes-and-edges.md) — basic graph, conditional edges.

---

## Command

Command combines state updates and routing in a single return value. Fields:
- **`update`**: State updates to apply (like returning a dict from a node)
- **`goto`**: Node name(s) to navigate to next
- **`resume`**: Value to resume after `interrupt()` — see human-in-the-loop skill

Example: [references/command-and-send.md](references/command-and-send.md).

<command-return-type-annotations>

**Python**: Use `Command[Literal["node_a", "node_b"]]` as the return type annotation to declare valid goto destinations.

**TypeScript**: Pass `{ ends: ["node_a", "node_b"] }` as the third argument to `addNode` to declare valid goto destinations.

</command-return-type-annotations>

<warning-command-static-edges>

**Warning**: `Command` only adds **dynamic** edges — static edges defined with `add_edge` / `addEdge` still execute. If `node_a` returns `Command(goto="node_c")` and you also have `graph.add_edge("node_a", "node_b")`, **both** `node_b` and `node_c` will run.

</warning-command-static-edges>

---

## Send API

Fan-out with `Send`: return `[Send("worker", {...})]` from a conditional edge to spawn parallel workers. Requires a reducer on the results field.

Examples: [references/command-and-send.md](references/command-and-send.md) — orchestrator-worker, Send accumulator.

---

## Running Graphs: Invoke and Stream

Call `graph.invoke(input, config)` to run a graph to completion and return the final state. Examples: [references/running-and-streaming.md](references/running-and-streaming.md).

<stream-mode-selection>

| Mode | What it Streams | Use Case |
|------|----------------|----------|
| `values` | Full state after each step | Monitor complete state |
| `updates` | State deltas | Track incremental updates |
| `messages` | LLM tokens + metadata | Chat UIs |
| `custom` | User-defined data | Progress indicators |

</stream-mode-selection>

Examples: [references/running-and-streaming.md](references/running-and-streaming.md) — LLM tokens, custom data.

---

## Error Handling

Match the error type to the right handler:

<error-handling-table>

| Error Type | Who Fixes | Strategy | Example |
|---|---|---|---|
| Transient (network, rate limits) | System | `RetryPolicy(max_attempts=3)` | `add_node(..., retry_policy=...)` |
| LLM-recoverable (tool failures) | LLM | `ToolNode(tools, handle_tool_errors=True)` | Error returned as ToolMessage |
| User-fixable (missing info) | Human | `interrupt({"message": ...})` | Collect missing data (see HITL skill) |
| Unexpected | Developer | Let bubble up | `raise` |

</error-handling-table>

Examples: [references/errors-and-fixes.md](references/errors-and-fixes.md) — retry policy, tool-node errors.

---

## Common Fixes

- Compile before running: `builder.compile()` returns the executable graph.
- Every loop needs a conditional path to `END`.
- Routers and `Command` may only name nodes already added to the graph.
- Python `Command` nodes declare destinations with `Command[Literal[...]]`; TypeScript passes `{ ends: [...] }` to `addNode`.
- `START` is entry-only; route to a named entry node instead.
- Reducer updates must match the field type (a list for a list reducer).
- TypeScript: always `await graph.invoke()`.

Examples: [references/errors-and-fixes.md](references/errors-and-fixes.md).

<boundaries>
### What You Should NOT Do

- Mutate state directly — always return partial update dicts from nodes
- Route back to START — it's entry-only; use a named node instead
- Forget reducers on list fields — without one, last write wins
- Mix static edges with Command goto without understanding both will execute
</boundaries>
