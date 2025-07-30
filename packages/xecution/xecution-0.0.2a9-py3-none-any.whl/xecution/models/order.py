from dataclasses import dataclass
from datetime import datetime
from typing import List
from xecution.common.enums import (
    Exchange,
    OrderSide,
    OrderStatus,
    OrderType,
    Symbol,
    TimeInForce
)
from xecution.models.position import Position

@dataclass
class ActiveOrder:
    symbol: Symbol
    exchange: Exchange
    updated_time: int
    created_time: int
    exchange_order_id: str
    client_order_id: str
    position: Position

@dataclass
class Level:
    price: float
    quantity: float

@dataclass
class OrderBookSnapshot:
    bids: List[Level]
    asks: List[Level]

@dataclass
class OrderUpdate:
    symbol: Symbol
    order_type: OrderType
    side: OrderSide
    time_in_force: TimeInForce
    exchange_order_id: str
    order_time: datetime
    updated_time: datetime
    size: float
    filled_size: float
    remain_size: float
    price: float
    client_order_id: str
    status: OrderStatus
    exchange: Exchange = Exchange.Binance
    is_reduce_only: bool = False
    is_hedge_mode: bool = False

@dataclass
class OrderResponse:
    exchange_order_id: str
    client_order_id: str
