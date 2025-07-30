"""RPC client services for customer app."""

import datetime
from typing import Any

from kaiju_tools.http import RPCClientService
from kaiju_tools.services import SERVICE_CLASS_REGISTRY

from .types import *


class ElementoLoyaltyProcessingClient(RPCClientService):
    """Auto-generated ElementoCustomers RPC client."""

    async def lists_set_product_list(
        self, id: ListId, items: list[str], _max_timeout: int = None, _nowait: bool = False
    ):
        """Call Lists.products.set."""
        return await self.call(
            method="Lists.products.set", params=dict(id=id, items=items), max_timeout=_max_timeout, nowait=_nowait
        )

    async def lists_get_product_list(self, id: ListId, _max_timeout: int = None, _nowait: bool = False):
        """Call Lists.products.get."""
        return await self.call(
            method="Lists.products.get", params=dict(id=id), max_timeout=_max_timeout, nowait=_nowait
        )

    async def lists_set_store_list(self, id: ListId, items: list[str], _max_timeout: int = None, _nowait: bool = False):
        """Call Lists.stores.set."""
        return await self.call(
            method="Lists.stores.set", params=dict(id=id, items=items), max_timeout=_max_timeout, nowait=_nowait
        )

    async def lists_get_store_list(self, id: ListId, _max_timeout: int = None, _nowait: bool = False):
        """Call Lists.stores.get."""
        return await self.call(method="Lists.stores.get", params=dict(id=id), max_timeout=_max_timeout, nowait=_nowait)

    async def balance_get_balance(
        self, customer_id: CustomerId, _max_timeout: int = None, _nowait: bool = False
    ) -> Points:
        """Call Balance.get."""
        return await self.call(
            method="Balance.get", params=dict(customer_id=customer_id), max_timeout=_max_timeout, nowait=_nowait
        )

    async def balance_calculate(
        self,
        customer: dict[str, Any],
        items: list[Item],
        custom_attributes: dict[str, Any] = None,
        points_sub: int = 0,
        transaction_id: TransactionId = None,
        order_id: str = None,
        timestamp: datetime.datetime = None,
        actions: list[BalanceAction | str] = None,
        meta: dict[str, Any] = None,
        _max_timeout: int = None,
        _nowait: bool = False,
    ) -> Cart:
        """Call Balance.calculate_cart."""
        return await self.call(
            method="Balance.calculate_cart",
            params=dict(
                customer=customer,
                items=items,
                custom_attributes=custom_attributes,
                points_sub=points_sub,
                transaction_id=transaction_id,
                order_id=order_id,
                timestamp=timestamp,
                actions=actions,
                meta=meta,
            ),
            max_timeout=_max_timeout,
            nowait=_nowait,
        )

    async def balance_confirm_transaction(
        self, transaction_id: TransactionId, _max_timeout: int = None, _nowait: bool = False
    ) -> None:
        """Call Balance.transaction.confirm."""
        return await self.call(
            method="Balance.transaction.confirm",
            params=dict(transaction_id=transaction_id),
            max_timeout=_max_timeout,
            nowait=_nowait,
        )

    async def balance_revert_transaction(
        self, transaction_id: TransactionId, _max_timeout: int = None, _nowait: bool = False
    ) -> None:
        """Call Balance.transaction.revert."""
        return await self.call(
            method="Balance.transaction.revert",
            params=dict(transaction_id=transaction_id),
            max_timeout=_max_timeout,
            nowait=_nowait,
        )

    async def balance_commit_transaction(
        self, transaction_id: TransactionId, _max_timeout: int = None, _nowait: bool = False
    ) -> None:
        """Call Balance.transaction.commit."""
        return await self.call(
            method="Balance.transaction.commit",
            params=dict(transaction_id=transaction_id),
            max_timeout=_max_timeout,
            nowait=_nowait,
        )

    async def balance_create_event(
        self,
        customer: dict[str, Any],
        event_type: EventTypeId,
        meta: dict[str, Any] = None,
        _max_timeout: int = None,
        _nowait: bool = False,
    ) -> bool:
        """Call Balance.create_event."""
        return await self.call(
            method="Balance.create_event",
            params=dict(customer=customer, event_type=event_type, meta=meta),
            max_timeout=_max_timeout,
            nowait=_nowait,
        )


SERVICE_CLASS_REGISTRY.register(ElementoLoyaltyProcessingClient)
