from dataclasses import dataclass
from typing import Optional
from xecution.models.topic import DataTopic, KlineTopic
from xecution.common.enums import Exchange, Mode, OrderSide, OrderType, Symbol, TimeInForce

@dataclass
class RuntimeConfig:
    mode: Mode
    kline_topic: list[KlineTopic]
    data_count: int
    API_Key: Optional[str] = None
    API_Secret: Optional[str] = None
    is_hedge_mode: bool = False
    datasource_topic: Optional[list[DataTopic]] = None
    leverage: Optional[int] = None
    exchange: Optional[Exchange] = None
    cryptoquant_api_key: Optional[str] = None

@dataclass
class OrderConfig:
    market_type: KlineTopic      # "spot" 或 "futures"
    symbol: Symbol
    side: OrderSide             # "BUY" 或 "SELL"
    order_type: OrderType       # "LIMIT" 或 "MARKET"
    quantity: float
    price: Optional[float] = None
    time_in_force: Optional[TimeInForce] = None