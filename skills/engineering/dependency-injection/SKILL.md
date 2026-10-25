---
name: dependency-injection
description: >-
  Correct Dependency Injection for this codebase: constructor injection
  against `Protocol` abstractions, FastAPI `Depends()` as the DI mechanism,
  a single composition root, and testability via injected fakes. Use when
  wiring a new service/repository's dependencies, deciding how a class
  should obtain its collaborators, or reviewing code for hidden/global
  dependencies. Pair with `singleton-pattern`/`factory-pattern` for lifecycle
  scope and `design-patterns-catalog` for Dependency Inversion.
metadata:
  version: '1.0.0'
paths:
  - src/**
allowed-tools: Read Edit Write
context: fork
---

# Dependency Injection

A class never constructs its own collaborators and never reaches into a global registry to fetch them. It declares what it needs, and something outside — a constructor call, or FastAPI's `Depends()` — provides it. This is Dependency Inversion (SOLID's "D", see `python-code-style` rule 7) put into practice at every service/repository boundary.

## The Core Rule

```python
# Wrong — the class builds its own dependency
class OrderService:
    def __init__(self) -> None:
        self._repository = OrderRepository()  # hardcoded, untestable, hidden coupling

# Right — the dependency is injected
class OrderService:
    def __init__(self, repository: OrderRepositoryProtocol) -> None:
        self._repository = repository
```

`OrderService` now depends on `OrderRepositoryProtocol`, not on `OrderRepository` — swap in a fake for tests, or a different implementation later, without touching `OrderService` at all.

## When to Use

Activate when:
- Writing a new service, repository, or orchestrator class that needs collaborators (another service, a repository, an HTTP client, a config object)
- A class is currently importing and instantiating its own dependencies inline instead of receiving them
- Wiring a FastAPI route/service to the resources it needs (DB session, cache, another service)
- Reviewing code for testability — if a class can't be unit-tested without hitting a real database/network, it's probably not receiving its dependencies through injection

Do **not** use when:
- The "dependency" is a cheap, pure value object (a `Pydantic` DTO, a plain computation) — inject actual collaborators (services, repositories, clients), not every value that happens to be a parameter
- A local helper function has no state and no side effects — see `python-code-style` rule 9, it belongs in `utils.py`, not behind an injected interface

## Constructor Injection (primary mechanism)

Every service/repository class takes its dependencies as `__init__` parameters, typed against the narrowest `Protocol` that satisfies its needs — not the concrete class.

```python
from typing import Protocol

class NotifierProtocol(Protocol):
    def send(self, message: str) -> None: ...

class OrderRepositoryProtocol(Protocol):
    def get(self, order_id: int) -> Order: ...
    def save(self, order: Order) -> None: ...

class OrderService:
    """Coordinates order creation and confirmation notifications."""

    def __init__(
        self,
        repository: OrderRepositoryProtocol,
        notifier: NotifierProtocol,
    ) -> None:
        self._repository = repository
        self._notifier = notifier

    def confirm(self, order_id: int) -> None:
        """Confirm an order and notify the customer.

        :param order_id: Numeric order identifier.
        :return: None.
        """
        order = self._repository.get(order_id)
        order.confirm()
        self._repository.save(order)
        self._notifier.send(f"Order {order_id} confirmed")
```

`OrderService` never imports `OrderRepository` or `EmailNotifier` — it only knows the `Protocol`s. Interface Segregation (SOLID's "I") applies here too: keep each `Protocol` to the methods the consumer actually calls, not the full surface of the concrete implementation.

## FastAPI `Depends()` Is This Project's DI Container

`Depends()` is how constructor-injected dependencies actually get resolved at request time. Every provider function returns something that satisfies the `Protocol` the service was typed against; routes never construct services directly.

```python
from typing import Annotated
from fastapi import Depends

def get_order_repository(session: AsyncSessionDep) -> OrderRepositoryProtocol:
    return OrderRepository(session)

def get_notifier() -> NotifierProtocol:
    return EmailNotifier()

def get_order_service(
    repository: Annotated[OrderRepositoryProtocol, Depends(get_order_repository)],
    notifier: Annotated[NotifierProtocol, Depends(get_notifier)],
) -> OrderService:
    return OrderService(repository=repository, notifier=notifier)

OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]

@router.post("/orders/{order_id}/confirm")
async def confirm_order(order_id: int, service: OrderServiceDep) -> None:
    service.confirm(order_id)
```

The route depends on `OrderServiceDep`, never on `OrderService(...)` built inline. Choose the dependency's **scope** — per-request construction here, vs. a process-wide singleton — using `singleton-pattern`'s three variants and `factory-pattern`'s wiring checklist; this skill covers *how the dependency reaches the consumer*, those two cover *how long it lives*.

## One Composition Root

All wiring — which concrete class satisfies which `Protocol` — happens in exactly one place per dependency: either a `get_xxx()` provider function (request-scoped) or `src/main.py`'s lifespan via the relevant `XxxFactory.init(...)` (process-wide, see `factory-pattern`). Business logic never picks its own implementation.

```python
# src/main.py — composition root for process-wide singletons
@asynccontextmanager
async def lifespan(app: FastAPI):
    RedisFactory.init(settings.redis_url)
    NotifierFactory.init()
    yield
```

If you find yourself writing `if env == "prod": self._client = RealClient() else: self._client = FakeClient()` inside a service, that decision belongs in the composition root (a provider function or `main.py`), not inside the class that uses the client.

## Testability: Inject Fakes, Don't Monkeypatch

Because dependencies arrive through the constructor, tests substitute them directly — no `mock.patch` on import paths required.

```python
def test_confirm_sends_notification() -> None:
    repository = FakeOrderRepository(orders={1: Order(id=1)})
    notifier = FakeNotifier()
    service = OrderService(repository=repository, notifier=notifier)

    service.confirm(order_id=1)

    assert notifier.sent_messages == ["Order 1 confirmed"]
```

For endpoint-level tests, override the FastAPI provider instead of the service:

```python
app.dependency_overrides[get_order_service] = lambda: OrderService(
    repository=FakeOrderRepository(), notifier=FakeNotifier()
)
```

See `tdd` for the full testing workflow this supports.

## Anti-Patterns

- **Service Locator** — pulling a dependency from a global registry/container *inside a method body* (`def confirm(self): repo = ServiceRegistry.get("order_repository")`) instead of receiving it in `__init__`. This hides the real dependency graph and makes the class untestable without the global registry set up. Constructor injection only.
- **Concrete-type injection** — typing a constructor parameter as `OrderRepository` (the concrete class) instead of `OrderRepositoryProtocol`. Works today, but re-couples the consumer to one implementation and defeats the point of injecting anything.
- **Injecting everything** — wrapping plain values (a `str`, a `float`, a Pydantic DTO) behind a `Protocol` "just in case." Inject actual collaborators with behavior; pass plain data as plain arguments (see `python-code-style` rules 6 and 10 — YAGNI applies to DI too).
- **Building dependencies inline mid-method** — `notifier = EmailNotifier()` constructed on the fly inside a service method instead of received at construction time. Even if it's only used once, this is exactly the hardcoded coupling injection exists to remove.
- **Circular dependencies** — `ServiceA` depends on `ServiceB` and `ServiceB` depends on `ServiceA`. Break the cycle by extracting the shared piece into a third collaborator both depend on, or invert one side to depend on an event/callback instead of the other service directly.

## Review Checklist

- [ ] Every service/repository receives its collaborators via `__init__`, never constructs them inline
- [ ] Constructor parameters are typed against `Protocol`s, not concrete classes
- [ ] FastAPI routes depend on a `XxxDep`/provider, never build a service inline
- [ ] Exactly one composition root per dependency (a provider function, or `main.py` lifespan via a `Factory`) — no scattered `if env == ...` construction logic inside business classes
- [ ] Unit tests inject fakes through the constructor; endpoint tests use `app.dependency_overrides` — no `mock.patch` on import paths as a substitute for DI
- [ ] No Service Locator calls inside method bodies
- [ ] No circular dependency between two services

## Related Skills

- `python-code-style` — rule 7 (SOLID, especially Dependency Inversion and Interface Segregation) and rule 20 (services must not hold request-scoped state)
- `singleton-pattern`, `factory-pattern` — deciding a dependency's lifecycle/scope once it's being injected
- `design-patterns-catalog` — `Protocol`-based abstraction is the same seam `adapter-pattern`/`strategy-pattern` rely on
- `tdd` — writing the unit tests that injected fakes make possible
