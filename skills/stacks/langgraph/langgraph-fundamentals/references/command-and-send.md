# Command and Send

Update-and-route in one return; fan-out to parallel workers. Python and TypeScript. Rules and tables are in [../SKILL.md](../SKILL.md).

<ex-command-state-and-routing>
<python>
Command lets you update state AND choose next node in one return.

```python
from langgraph.types import Command
from typing import Literal

class State(TypedDict):
    count: int
    result: str

def node_a(state: State) -> Command[Literal["node_b", "node_c"]]:
    """Update state AND decide next node in one return."""
    new_count = state["count"] + 1
    if new_count > 5:
        return Command(update={"count": new_count}, goto="node_c")
    return Command(update={"count": new_count}, goto="node_b")

graph = (
    StateGraph(State)
    .add_node("node_a", node_a)
    .add_node("node_b", lambda s: {"result": "B"})
    .add_node("node_c", lambda s: {"result": "C"})
    .add_edge(START, "node_a")
    .add_edge("node_b", END)
    .add_edge("node_c", END)
    .compile()
)
```
</python>
<typescript>
Return Command with update and goto to combine state change with routing.

```typescript
import { StateGraph, StateSchema, START, END, Command } from "@langchain/langgraph";
import { z } from "zod";

const State = new StateSchema({
  count: z.number().default(0),
  result: z.string().default(""),
});

const nodeA = async (state: typeof State.State) => {
  const newCount = state.count + 1;
  if (newCount > 5) {
    return new Command({ update: { count: newCount }, goto: "node_c" });
  }
  return new Command({ update: { count: newCount }, goto: "node_b" });
};

const graph = new StateGraph(State)
  .addNode("node_a", nodeA, { ends: ["node_b", "node_c"] })
  .addNode("node_b", async () => ({ result: "B" }))
  .addNode("node_c", async () => ({ result: "C" }))
  .addEdge(START, "node_a")
  .addEdge("node_b", END)
  .addEdge("node_c", END)
  .compile();
```
</typescript>
</ex-command-state-and-routing>

<ex-orchestrator-worker>
<python>
Fan out tasks to parallel workers using the Send API and aggregate results.

```python
from langgraph.types import Send
from typing import Annotated
import operator

class OrchestratorState(TypedDict):
    tasks: list[str]
    results: Annotated[list, operator.add]
    summary: str

def orchestrator(state: OrchestratorState):
    """Fan out tasks to workers."""
    return [Send("worker", {"task": task}) for task in state["tasks"]]

def worker(state: dict) -> dict:
    return {"results": [f"Completed: {state['task']}"]}

def synthesize(state: OrchestratorState) -> dict:
    return {"summary": f"Processed {len(state['results'])} tasks"}

graph = (
    StateGraph(OrchestratorState)
    .add_node("worker", worker)
    .add_node("synthesize", synthesize)
    .add_conditional_edges(START, orchestrator, ["worker"])
    .add_edge("worker", "synthesize")
    .add_edge("synthesize", END)
    .compile()
)

result = graph.invoke({"tasks": ["Task A", "Task B", "Task C"]})
```
</python>
<typescript>
Fan out tasks to parallel workers using the Send API and aggregate results.

```typescript
import { Send, StateGraph, StateSchema, ReducedValue, START, END } from "@langchain/langgraph";
import { z } from "zod";

const State = new StateSchema({
  tasks: z.array(z.string()),
  results: new ReducedValue(
    z.array(z.string()).default(() => []),
    { reducer: (curr, upd) => curr.concat(upd) }
  ),
  summary: z.string().default(""),
});

const orchestrator = (state: typeof State.State) => {
  return state.tasks.map((task) => new Send("worker", { task }));
};

const worker = async (state: { task: string }) => {
  return { results: [`Completed: ${state.task}`] };
};

const synthesize = async (state: typeof State.State) => {
  return { summary: `Processed ${state.results.length} tasks` };
};

const graph = new StateGraph(State)
  .addNode("worker", worker)
  .addNode("synthesize", synthesize)
  .addConditionalEdges(START, orchestrator, ["worker"])
  .addEdge("worker", "synthesize")
  .addEdge("synthesize", END)
  .compile();
```
</typescript>
</ex-orchestrator-worker>

<fix-send-accumulator>
<python>
Use a reducer to accumulate parallel worker results (otherwise last worker overwrites).

```python
# WRONG: No reducer - last worker overwrites
class State(TypedDict):
    results: list

# CORRECT
class State(TypedDict):
    results: Annotated[list, operator.add]  # Accumulates
```
</python>
<typescript>
Use ReducedValue to accumulate parallel worker results.

```typescript
// WRONG: No reducer
const State = new StateSchema({ results: z.array(z.string()) });

// CORRECT
const State = new StateSchema({
  results: new ReducedValue(z.array(z.string()).default(() => []), { reducer: (curr, upd) => curr.concat(upd) }),
});
```
</typescript>
</fix-send-accumulator>
