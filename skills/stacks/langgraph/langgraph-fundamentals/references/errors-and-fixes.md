# Errors and common fixes

Retry policy, tool errors, and frequent mistakes. Python and TypeScript. Rules and tables are in [../SKILL.md](../SKILL.md).

<ex-retry-policy>
<python>
Use RetryPolicy for transient errors (network issues, rate limits).

```python
from langgraph.types import RetryPolicy

workflow.add_node(
    "search_documentation",
    search_documentation,
    retry_policy=RetryPolicy(max_attempts=3, initial_interval=1.0)
)
```
</python>
<typescript>
Use retryPolicy for transient errors.

```typescript
workflow.addNode(
  "searchDocumentation",
  searchDocumentation,
  {
    retryPolicy: { maxAttempts: 3, initialInterval: 1.0 },
  },
);
```
</typescript>
</ex-retry-policy>

<ex-tool-node-error-handling>
<python>
Use ToolNode from langgraph.prebuilt to handle tool execution and errors. When handle_tool_errors=True, errors are returned as ToolMessages so the LLM can recover.

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode(tools, handle_tool_errors=True)

workflow.add_node("tools", tool_node)
```
</python>
<typescript>
Use ToolNode from @langchain/langgraph/prebuilt to handle tool execution and errors. When handleToolErrors is true, errors are returned as ToolMessages so the LLM can recover.

```typescript
import { ToolNode } from "@langchain/langgraph/prebuilt";

const toolNode = new ToolNode(tools, { handleToolErrors: true });

workflow.addNode("tools", toolNode);
```
</typescript>
</ex-tool-node-error-handling>

<fix-compile-before-execution>
<python>
Must compile() to get executable graph.

```python
# WRONG
builder.invoke({"input": "test"})  # AttributeError!

# CORRECT
graph = builder.compile()
graph.invoke({"input": "test"})
```
</python>
<typescript>
Must compile() to get executable graph.

```typescript
// WRONG
await builder.invoke({ input: "test" });

// CORRECT
const graph = builder.compile();
await graph.invoke({ input: "test" });
```
</typescript>
</fix-compile-before-execution>

<fix-infinite-loop-needs-exit>
<python>
Provide conditional path to END to avoid infinite loops.

```python
# WRONG: Loops forever
builder.add_edge("node_a", "node_b")
builder.add_edge("node_b", "node_a")

# CORRECT
def should_continue(state):
    return END if state["count"] > 10 else "node_b"
builder.add_conditional_edges("node_a", should_continue)
```
</python>
<typescript>
Use conditional edges with END return to break loops.

```typescript
// WRONG: Loops forever
builder.addEdge("node_a", "node_b").addEdge("node_b", "node_a");

// CORRECT
builder.addConditionalEdges("node_a", (state) => state.count > 10 ? END : "node_b");
```
</typescript>
</fix-infinite-loop-needs-exit>

<fix-common-mistakes>
Other common mistakes:

```python
# Router must return names of nodes that exist in the graph
builder.add_node("my_node", func)  # Add node BEFORE referencing in edges
builder.add_conditional_edges("node_a", router, ["my_node"])

# Command return type needs Literal for routing destinations (Python)
def node_a(state) -> Command[Literal["node_b", "node_c"]]:
    return Command(goto="node_b")

# START is entry-only - cannot route back to it
builder.add_edge("node_a", START)  # WRONG!
builder.add_edge("node_a", "entry")  # Use a named entry node instead

# Reducer expects matching types
return {"items": ["item"]}  # List for list reducer, not a string
```

```typescript
// Always await graph.invoke() - it returns a Promise
const result = await graph.invoke({ input: "test" });

// TS Command nodes need { ends } to declare routing destinations
builder.addNode("router", routerFn, { ends: ["node_b", "node_c"] });
```
</fix-common-mistakes>
