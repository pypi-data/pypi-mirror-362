from dataclasses import dataclass
from xecution.common.enums import Symbol

@dataclass
class PositionData:
    quantity: float
    avg_price: float

@dataclass
class Position:
    symbol: Symbol
    long: PositionData
    short: PositionData
    updated_time: int