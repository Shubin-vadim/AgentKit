# Python code style: examples

Wrong/right code for the rules in [../SKILL.md](../SKILL.md). Section numbers match the rule numbers.

## 1. Pydantic models, never `dataclass`

```python
# Wrong
from dataclasses import dataclass

@dataclass
class Order:
    id: int
    total: float

# Right
from pydantic import BaseModel

class Order(BaseModel):
    id: int
    total: float
```

## 2. Docstrings: English only, Sphinx style for callables

```python
class PricingService:
    """Computes final prices after discounts and taxes."""

    def calculate_price(self, price: float, discount: float) -> float:
        """Calculate the final price.

        :param price: Original product price.
        :param discount: Discount percentage.
        :return: Final price.
        :raises ValueError: If discount is invalid.
        """
        if not 0 <= discount <= 1:
            raise ValueError("discount must be between 0 and 1")
        return price * (1 - discount)
```

## 3. One class per file (except cohesive Pydantic model groups)

```
# Wrong: three unrelated services in one file
services/misc.py  → EmailService, PdfService, PaymentService

# Right
services/email_service.py     → EmailService
services/pdf_service.py       → PdfService
services/payment_service.py   → PaymentService

# Right (cohesive model family, one file is fine)
schemas/order.py → OrderCreate, OrderUpdate, OrderResponse
```

## 6. Full type annotations everywhere

```python
# Wrong
def get_total(items, tax_rate=0.0):
    ...

# Right
def get_total(items: list[OrderItem], tax_rate: float = 0.0) -> float:
    ...
```

## 9. Standalone helper functions live in `utils.py`

```python
# services/orders/utils.py
def format_order_number(order_id: int) -> str:
    """Format an order id as a display order number.

    :param order_id: Numeric order identifier.
    :return: Zero-padded order number string.
    """
    return f"ORD-{order_id:06d}"
```

## 13. Exception handling policy

```python
class AppError(Exception):
    """Base class for all domain errors in this project."""

class OrderError(AppError):
    """Base class for order-domain errors."""

class OrderNotFoundError(OrderError):
    """Raised when an order id has no matching record."""

def get_order(order_id: int) -> Order:
    """Fetch an order by id.

    :param order_id: Numeric order identifier.
    :return: The matching order.
    :raises OrderNotFoundError: If no order matches ``order_id``.
    """
    order = repository.find(order_id)
    if order is None:
        logger.warning("order lookup failed: order_id=%s not found", order_id)
        raise OrderNotFoundError(f"order {order_id} does not exist")
    return order
```

## 14. Logging: one logger per module, no `print()`

```python
import logging

logger = logging.getLogger(__name__)
```

## 16. Async: mandatory for I/O, no blocking calls inside `async def`

```python
# Wrong — blocks the event loop
async def fetch_status(url: str) -> int:
    response = requests.get(url)
    return response.status_code

# Right
async def fetch_status(url: str) -> int:
    """Fetch the HTTP status code for a URL.

    :param url: Target URL.
    :return: HTTP status code.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.status_code
```

## 18. Function/method size and argument-count limits, enforced by the linter

```python
# Wrong — 5th parameter about to be added
def create_order(user_id: int, items: list[Item], currency: str, discount: float, notes: str) -> Order:
    ...

# Right
class CreateOrderRequest(BaseModel):
    user_id: int
    items: list[Item]
    currency: str
    discount: float = 0.0
    notes: str = ""

def create_order(request: CreateOrderRequest) -> Order:
    ...
```

## 20. Immutability and state

```python
# Wrong
def add_item(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items

# Right
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    """Append an item to a list, creating one if not provided.

    :param item: Item to append.
    :param items: Existing list, or ``None`` to start a new one.
    :return: The updated list.
    """
    items = items if items is not None else []
    items.append(item)
    return items
```
