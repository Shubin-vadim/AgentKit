---
name: design-patterns-catalog
description: >-
  Index of the classic GoF design patterns (Creational, Structural,
  Behavioral): which one fits a given problem, and a link to its own
  dedicated skill for templates and anti-patterns. Use when the user asks
  "which pattern fits this problem", wants to know Strategy vs. State,
  Decorator vs. Proxy, Adapter vs. Facade, or asks for a pattern by name. Not
  project-specific.
---

# Design Patterns Catalog

Reusable solutions to recurring design problems, from *Design Patterns: Elements of Reusable Object-Oriented Software* (Gamma, Helm, Johnson, Vlissides — "GoF"). Each pattern below is its own skill with a full template, naming conventions, and anti-patterns — this page only helps you pick the right one.

Pick a pattern because it names a shape you already need, not because it sounds sophisticated. A pattern is a cost (indirection, more types, more to read) paid for a benefit (flexibility at a specific point of change). If nothing is going to change at that point, skip it.

## How to choose

1. Name the actual force: what varies, what must stay stable, who depends on whom.
2. Find the pattern below whose "Use when" matches that force — not the one whose diagram looks similar.
3. Prefer the plainest tool that solves it: a plain function or a `switch` beats a pattern if there's no real variability yet. Introduce the pattern when the second variant shows up, not in anticipation of a first one.
4. Open the pattern's own skill for the "Don't use when" column and the full template before writing code.

## Creational — how objects get made

| Pattern | Intent | Use when | Don't use when |
|---|---|---|---|
| [Factory Method](../factory-method-pattern/SKILL.md) | Subclass/factory decides which concrete class to instantiate | A base class knows *that* an object is needed but not *which* concrete type | One concrete type ever exists — just construct it |
| [Abstract Factory](../abstract-factory-pattern/SKILL.md) | Family of related objects created together, consistently | You must swap an entire family (e.g. Windows/Mac widgets, Postgres/SQLite drivers) as one unit | Only one product type varies — use Factory Method instead |
| [Builder](../builder-pattern/SKILL.md) | Construct a complex object step by step, same construction process, different representations | Object has many optional/combinatorial parameters, or must be built over several steps | A plain constructor or keyword args already reads clearly |
| [Prototype](../prototype-pattern/SKILL.md) | Create new objects by cloning a prototypical instance | Construction is expensive or reflective, and you need many near-identical variants | Objects are cheap to construct normally |
| Singleton | Ensure exactly one instance, global access point | Truly one instance per process is a real invariant (connection pool, config) | Used as a substitute for dependency injection or global mutable state |

## Structural — how objects are composed

| Pattern | Intent | Use when | Don't use when |
|---|---|---|---|
| [Adapter](../adapter-pattern/SKILL.md) | Convert one interface into another the client expects | Integrating a third-party/legacy class whose interface you can't change | You own both sides — just change one interface |
| [Decorator](../decorator-pattern/SKILL.md) | Attach behavior to an object dynamically, same interface, stackable | Need to add responsibilities (logging, caching, retry) without subclass explosion | Only one variant ever needed — subclass is simpler |
| [Facade](../facade-pattern/SKILL.md) | Single simplified entry point over a complex subsystem | Callers only need a narrow slice of a big subsystem's API | The subsystem is already simple, or callers need full control |
| [Composite](../composite-pattern/SKILL.md) | Treat individual objects and groups uniformly via a shared interface | Recursive tree structures (UI widgets, file systems, org charts) | Structure is flat, no recursion |
| [Proxy](../proxy-pattern/SKILL.md) | Stand-in controlling access to a real object (lazy load, access control, remote call, caching) | Need to intercept access without changing the real object's interface | The extra indirection has no concrete job to do |
| [Bridge](../bridge-pattern/SKILL.md) | Decouple an abstraction from its implementation so both vary independently | Two dimensions of variation multiply (shape × renderer, device × OS) | Only one dimension varies |

## Behavioral — how objects communicate

| Pattern | Intent | Use when | Don't use when |
|---|---|---|---|
| [Strategy](../strategy-pattern/SKILL.md) | Encapsulate interchangeable algorithms behind one interface, swap at runtime | Several ways to do the same job (sort order, pricing rule, auth scheme) | One algorithm, or the "variants" are really just a couple of `if` branches |
| [Observer](../observer-pattern/SKILL.md) | One-to-many notification: subject changes, observers react | Decoupled event/pubsub, UI reacting to model changes | A single, fixed caller — just call the function |
| [Command](../command-pattern/SKILL.md) | Encapsulate a request as an object: execute, queue, log, undo | Need undo/redo, queuing, retry, or to pass "an action" as a value | Direct method call already expresses the intent |
| [State](../state-pattern/SKILL.md) | Object changes behavior when its internal state changes | Explicit state machine with state-specific behavior | A couple of boolean flags already model it clearly |
| [Template Method](../template-method-pattern/SKILL.md) | Fixed algorithm skeleton in a base class, subclasses override specific steps | Several classes share the same overall steps but differ in a few | The steps aren't actually shared, or there's only one implementation |
| [Chain of Responsibility](../chain-of-responsibility-pattern/SKILL.md) | Pass a request along a chain of handlers until one handles it | Middleware pipelines, validation chains, fallback resolution | Exactly one handler always applies — just call it |
| [Mediator](../mediator-pattern/SKILL.md) | Centralize how a set of objects interact instead of them referencing each other | Many objects with tangled peer-to-peer references | Only two objects interact — direct reference is fine |
| [Iterator](../iterator-pattern/SKILL.md) | Sequential access to elements without exposing the underlying structure | Custom traversal over a custom collection | The language's built-in iteration protocol already covers it |
| [Visitor](../visitor-pattern/SKILL.md) | Add new operations to a class hierarchy without modifying the classes | Operations change often, class hierarchy is stable (compilers, AST passes) | The class hierarchy changes more often than the operations |
| [Memento](../memento-pattern/SKILL.md) | Capture and restore an object's internal state without violating encapsulation | Undo/rollback/snapshot of state | Simple immutable value objects are already easy to snapshot |

## Anti-patterns

- Picking a pattern before there is a second real variant to justify it ("just in case" abstraction).
- Nesting Decorator/Proxy/Adapter so deep the actual call path is unreadable.
- Using Singleton where DI or a plain module-level constant would do, purely for the ceremony.
- Reaching for Visitor when the hierarchy itself is still churning — you'll rewrite both sides every time.
- A pattern name in a class name (`XxxStrategyImpl`) without the interchangeability the pattern implies.

## Related

- `codebase-design` — deep-module vocabulary (interface, seam, depth) for judging whether a pattern actually earns its interface
- `clean-code` — statement/function-level readability, one level below pattern-level design
- `api-design-patterns` — API-contract-level patterns (pagination, errors), distinct from GoF object patterns
