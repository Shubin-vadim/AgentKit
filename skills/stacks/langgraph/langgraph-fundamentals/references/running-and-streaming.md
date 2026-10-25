# Running and streaming

`invoke` and the `messages` / `custom` stream modes. Python and TypeScript. Rules and tables are in [../SKILL.md](../SKILL.md).

<invoke-basics>

Call `graph.invoke(input, config)` to run a graph to completion and return the final state.

<python>

```python
result = graph.invoke({"input": "hello"})
# With config (for persistence, tags, etc.)
result = graph.invoke({"input": "hello"}, {"configurable": {"thread_id": "1"}})
```
</python>
<typescript>

```typescript
const result = await graph.invoke({ input: "hello" });
// With config
const result = await graph.invoke({ input: "hello" }, { configurable: { thread_id: "1" } });
```
</typescript>

</invoke-basics>

<ex-stream-llm-tokens>
<python>
Stream LLM tokens in real-time for chat UI display.

```python
for chunk in graph.stream(
    {"messages": [HumanMessage("Hello")]},
    stream_mode="messages"
):
    token, metadata = chunk
    if hasattr(token, "content"):
        print(token.content, end="", flush=True)
```
</python>
<typescript>
Stream LLM tokens in real-time for chat UI display.

```typescript
for await (const chunk of graph.stream(
  { messages: [new HumanMessage("Hello")] },
  { streamMode: "messages" }
)) {
  const [token, metadata] = chunk;
  if (token.content) {
    process.stdout.write(token.content);
  }
}
```
</typescript>
</ex-stream-llm-tokens>

<ex-stream-custom-data>
<python>
Emit custom progress updates from within nodes using the stream writer.

```python
from langgraph.config import get_stream_writer

def my_node(state):
    writer = get_stream_writer()
    writer("Processing step 1...")
    # Do work
    writer("Complete!")
    return {"result": "done"}

for chunk in graph.stream({"data": "test"}, stream_mode="custom"):
    print(chunk)
```
</python>
<typescript>
Emit custom progress updates from within nodes using the stream writer.

```typescript
import { getWriter } from "@langchain/langgraph";

const myNode = async (state: typeof State.State) => {
  const writer = getWriter();
  writer("Processing step 1...");
  // Do work
  writer("Complete!");
  return { result: "done" };
};

for await (const chunk of graph.stream({ data: "test" }, { streamMode: "custom" })) {
  console.log(chunk);
}
```
</typescript>
</ex-stream-custom-data>
