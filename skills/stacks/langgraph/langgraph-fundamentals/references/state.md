# State

Reducers and partial updates. Python and TypeScript. Rules and tables are in [../SKILL.md](../SKILL.md).

<ex-state-with-reducer>
<python>
Define state schema with reducers for accumulating lists and summing integers.

```python
from typing_extensions import TypedDict, Annotated
import operator

class State(TypedDict):
    name: str  # Default: overwrites on update
    messages: Annotated[list, operator.add]  # Appends to list
    total: Annotated[int, operator.add]  # Sums integers
```
</python>
<typescript>
Use StateSchema with ReducedValue for accumulating arrays.

```typescript
import { StateSchema, ReducedValue, MessagesValue } from "@langchain/langgraph";
import { z } from "zod";

const State = new StateSchema({
  name: z.string(),  // Default: overwrites
  messages: MessagesValue,  // Built-in for messages
  items: new ReducedValue(
    z.array(z.string()).default(() => []),
    { reducer: (current, update) => current.concat(update) }
  ),
});
```
</typescript>
</ex-state-with-reducer>

<fix-forgot-reducer-for-list>
<python>
Without a reducer, returning a list overwrites previous values.

```python
# WRONG: List will be OVERWRITTEN
class State(TypedDict):
    messages: list  # No reducer!

# Node 1 returns: {"messages": ["A"]}
# Node 2 returns: {"messages": ["B"]}
# Final: {"messages": ["B"]}  # "A" is LOST!

# CORRECT: Use Annotated with operator.add
from typing import Annotated
import operator

class State(TypedDict):
    messages: Annotated[list, operator.add]
# Final: {"messages": ["A", "B"]}
```
</python>
<typescript>
Without ReducedValue, arrays are overwritten not appended.

```typescript
// WRONG: Array will be overwritten
const State = new StateSchema({
  items: z.array(z.string()),  // No reducer!
});
// Node 1: { items: ["A"] }, Node 2: { items: ["B"] }
// Final: { items: ["B"] }  // A is lost!

// CORRECT: Use ReducedValue
const State = new StateSchema({
  items: new ReducedValue(
    z.array(z.string()).default(() => []),
    { reducer: (current, update) => current.concat(update) }
  ),
});
// Final: { items: ["A", "B"] }
```
</typescript>
</fix-forgot-reducer-for-list>

<fix-state-must-return-dict>
<python>
Nodes must return partial updates, not mutate and return full state.

```python
# WRONG: Returning entire state object
def my_node(state: State) -> State:
    state["field"] = "updated"
    return state  # Don't mutate and return!

# CORRECT: Return dict with only the updates
def my_node(state: State) -> dict:
    return {"field": "updated"}
```
</python>
<typescript>
Return partial updates only, not the full state object.

```typescript
// WRONG: Returning entire state
const myNode = async (state: typeof State.State) => {
  state.field = "updated";
  return state;  // Don't do this!
};

// CORRECT: Return partial updates
const myNode = async (state: typeof State.State) => {
  return { field: "updated" };
};
```
</typescript>
</fix-state-must-return-dict>
