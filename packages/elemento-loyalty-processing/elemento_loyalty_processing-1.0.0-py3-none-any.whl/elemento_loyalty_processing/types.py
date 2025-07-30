from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, NewType, TypedDict

from msgspec import Struct


__all__ = [
    "DATE_MAXVALUE",
    "ListId",
    "CustomerId",
    "ItemList",
    "ItemListType",
    "EventTypeId",
    "BalanceStatus",
    "Balance",
    "TransactionType",
    "OrderItem",
    "TransactionId",
    "CustomerId",
    "Transaction",
    "EventTypeId",
    "Item",
    "Cart",
    "BalanceAction",
    "Customer",
    "StoredTransaction",
    "OfferId",
    "GroupId",
    "OfferEventTypes",
    "ConditionId",
    "LifetimeId",
    "ActionId",
    "Points",
]

DATE_MAXVALUE = date.fromisoformat("3000-01-01")

TransactionId = NewType("TransactionId", str)
EventTypeId = NewType("EventTypeId", str)
ListId = NewType("ListId", str)
CustomerId = NewType("CustomerId", int)
OfferId = NewType("OfferId", int)
LifetimeId = NewType("LifetimeId", int)
GroupId = NewType("GroupId", int)
ConditionId = NewType("ConditionId", int)
ActionId = NewType("ActionId", int)
Points = NewType("Points", int)


class OfferEventTypes(Enum):
    PointsAdd = "PointsAdd"
    PointsUse = "PointsUse"
    Purchase = "Purchase"
    Return = "Return"
    Birthday = "Birthday"
    RegistrationDone = "RegistrationDone"


class Customer(TypedDict):
    id: CustomerId
    profile: dict[str, Any]


class ItemListType(Enum):
    STORE = "STORE"
    PRODUCT = "PRODUCT"
    TERMINAL = "TERMINAL"


class ItemList(Struct):
    type: ItemListType
    id: ListId
    items: frozenset[str]


class BalanceStatus(Enum):
    FUTURE = "FUTURE"
    HOLD = "HOLD"
    ACTIVE = "ACTIVE"


class Balance(Struct):
    customer_id: CustomerId
    active_from: date
    active_to: date
    status: BalanceStatus
    amount: int
    transaction_id: TransactionId | None = None


class OrderItem(Struct):
    product_id: str
    quantity: int
    price: Decimal
    balance: Points
    active: bool


class TransactionType(Enum):
    ORDER = "ORDER"
    SCRIPT = "SCRIPT"


class StoredTransaction(Struct):
    created: datetime
    customer_id: CustomerId
    type: TransactionType
    ext_id: TransactionId | None = None
    order_id: str | None = None
    active: bool = True
    meta: dict[str, Any] | None = None
    items: list[OrderItem] | None = None
    id: int = None


class BalanceAction(Enum):
    CALC = "CALC"
    SUB = "SUB"
    ADD = "ADD"


class Item(Struct):
    pos: int
    product_id: str
    quantity: int
    total: Decimal
    price: Decimal
    cashback: Points = 0
    discount: Decimal = Decimal("0.00")
    points_add: Points = 0
    points_sub: Points = 0
    points_sub_max: Points = 0


class Cart(Struct):
    points_add: Points
    points_sub: Points
    points_sub_max: Points
    items: list[Item]
    cashier_message: str | None = None
    customer_message: str | None = None


class Transaction(Struct):
    id: TransactionId = None
    order_id: str = None
    customer_id: CustomerId = None
    timestamp: datetime = None
    cart: Cart = None
    confirmed: bool = False
