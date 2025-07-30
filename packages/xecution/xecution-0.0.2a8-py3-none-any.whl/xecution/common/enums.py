from enum import Enum

class KlineType(Enum):
    Binance_Spot = 1
    Binance_Futures = 2
    Bybit_Spot = 3
    Bybit_Futures = 4
    OKX_Spot = 5
    OKX_Futures = 6

class Mode(Enum):
    Live = 1
    Backtest = 2
    Testnet = 3
    
class ConcurrentRequest(Enum):
    Max = 3
    Chunk_Size = 5
    
class Exchange(Enum):
    Binance = 1
    Bybit = 2
    Okx = 3    
    
class Symbol(Enum):
    BTCUSDT = "BTCUSDT"
    ETHUSDT = "ETHUSDT"
    SOLUSDT = "SOLUSDT"
    
class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    
class TimeInForce(str, Enum):
    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"
    GTX = "GTX"

class OrderStatus(str, Enum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"

class OrderType(str, Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP = "STOP"
    TAKE_PROFIT = "TAKE_PROFIT"
    TRAILING_STOP_MARKET = "TRAILING_STOP_MARKET"
    
class TimeInForce(str, Enum):
    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"
    GTX = "GTX"
    
class DataProvider(str, Enum):
    CRYPTOQUANT = "CRYPTOQUANT"
    