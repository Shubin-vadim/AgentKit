---
name: visitor-pattern
description: >-
  Generic Visitor pattern: add new operations to a class hierarchy without
  modifying the classes in it. Use when operations change often but the
  class hierarchy is stable — compilers, AST passes, report generators over
  a fixed node set — in any language or project.
---

# Visitor Pattern (Portable Template)

## When to Use

Activate when:
- You have a stable hierarchy of node/element types (AST nodes, document elements, shape types) and need to add new operations over them regularly
- Each new operation (pretty-print, evaluate, type-check, serialize) would otherwise require adding a method to every node class, scattering that operation's logic across many files
- The hierarchy itself is closed or rarely changes — adding a new node type is much rarer than adding a new operation

Do **not** use when:
- The class hierarchy changes more often than the operations do — every new node type then requires a new method on *every* existing visitor, which is worse than just adding a method to each node class directly
- There's only one or two operations ever needed — the double-dispatch machinery isn't worth it yet

## Template

```python
from typing import Protocol

class Node(Protocol):
    def accept(self, visitor: "Visitor") -> None: ...

class NumberNode:
    def __init__(self, value: float) -> None:
        self.value = value

    def accept(self, visitor: "Visitor") -> None:
        visitor.visit_number(self)

class AddNode:
    def __init__(self, left: Node, right: Node) -> None:
        self.left, self.right = left, right

    def accept(self, visitor: "Visitor") -> None:
        visitor.visit_add(self)

class Visitor(Protocol):
    def visit_number(self, node: NumberNode) -> None: ...
    def visit_add(self, node: AddNode) -> None: ...

class EvalVisitor:
    def visit_number(self, node: NumberNode) -> float:
        return node.value

    def visit_add(self, node: AddNode) -> float:
        return node.left.accept(self) + node.right.accept(self)
```

A new operation (pretty-printer, type-checker) is a new `Visitor` implementation — `NumberNode`/`AddNode` are never touched again.

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Node interface | `Node`, with `accept(visitor)` |
| Concrete nodes | Named for the domain concept (`NumberNode`, `AddNode`) |
| Visitor interface | `Visitor`, one `visit_xxx(node)` method per concrete node type |
| Concrete visitors | Named for the operation (`EvalVisitor`, `PrettyPrintVisitor`) |

## Anti-Patterns

- Adding Visitor when the node hierarchy is still actively growing — you'll be updating every visitor every time, which is the exact cost this pattern is meant to avoid
- A visitor that mutates the nodes it visits when callers expect a pure read-only traversal — document mutation clearly if it happens
- Fat `Visitor` interfaces where most concrete visitors only care about 2 of 10 node types and implement the other 8 as no-ops — consider splitting by node category if this becomes common

## Related Skills

- `design-patterns-catalog` — choosing Visitor vs. adding methods directly to node classes
- `composite-pattern` — Visitor is most often applied over a Composite tree structure
