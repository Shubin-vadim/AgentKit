---
name: composite-pattern
description: >-
  Generic Composite pattern: treat individual objects and groups of them
  uniformly through one shared interface. Use for recursive tree structures
  (file systems, UI widgets, org charts, nested menus) where callers
  shouldn't have to special-case leaf vs. branch, in any language or project.
---

# Composite Pattern (Portable Template)

## When to Use

Activate when:
- The domain is genuinely a recursive tree (folders containing files and folders, widgets containing widgets, categories containing items and sub-categories)
- Client code currently branches on "is this a leaf or a group" and that branching is duplicated at every call site
- Operations (size, render, total price) need to aggregate naturally from leaves up through the tree

Do **not** use when:
- The structure is always exactly one level deep — plain iteration over a list is clearer and needs no shared interface
- Leaves and composites have fundamentally different operations with little overlap — forcing a shared interface would make it lie about what's common

## Template

```python
from typing import Protocol

class FileSystemNode(Protocol):
    def size(self) -> int: ...

class File:
    def __init__(self, bytes_size: int) -> None:
        self._bytes_size = bytes_size

    def size(self) -> int:
        return self._bytes_size

class Folder:
    def __init__(self) -> None:
        self._children: list[FileSystemNode] = []

    def add(self, node: FileSystemNode) -> None:
        self._children.append(node)

    def size(self) -> int:
        return sum(child.size() for child in self._children)

root = Folder()
root.add(File(100))
sub = Folder()
sub.add(File(50))
root.add(sub)
root.size()  # 150 — caller never checks "is this a File or a Folder"
```

## Naming Conventions

| Artifact | Pattern |
|---|---|
| Shared interface | Named for the tree's domain concept (`FileSystemNode`, `UiComponent`) |
| Leaf | The base case with no children (`File`) |
| Composite | The recursive case holding children (`Folder`) |

## Anti-Patterns

- Client code that still does `isinstance(node, File)` checks instead of trusting the shared interface — defeats the point
- A composite whose leaf and branch behaviors diverge so much that half the shared interface throws `NotImplementedError` on one side
- Unbounded recursion with no cycle protection when the tree is built from external/untrusted data

## Related Skills

- `design-patterns-catalog` — choosing Composite vs. plain recursion
- `iterator-pattern` — often paired with Composite to traverse the tree without exposing its structure
- `visitor-pattern` — adding new operations over a Composite tree without modifying every node class
