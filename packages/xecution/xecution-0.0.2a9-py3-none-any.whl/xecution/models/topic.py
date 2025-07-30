from dataclasses import dataclass
from xecution.common.enums import DataProvider, KlineType, Symbol

@dataclass(frozen=True)  
class KlineTopic:
    klineType: KlineType
    symbol: Symbol
    timeframe: str
    
@dataclass(frozen=True)
class DataTopic:
    provider: DataProvider
    url:str