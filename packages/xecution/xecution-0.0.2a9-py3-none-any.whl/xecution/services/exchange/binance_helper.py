import logging
import aiohttp
from typing import Optional
from datetime import datetime, timezone
from xecution.common.enums import Exchange, KlineType, Mode, Symbol
from xecution.common.exchange.live_constants import LiveConstants
from xecution.common.exchange.testnet_constants import TestnetConstants
from xecution.models.order import ActiveOrder, Level, OrderBookSnapshot, OrderResponse, OrderUpdate
from xecution.models.config import RuntimeConfig
from xecution.models.position import Position, PositionData
from xecution.models.topic import KlineTopic
from .safe_kline_downloader import SafeKlineDownloader

# Utility functions for the Binance service
class BinanceHelper:
    def __init__(self, config: RuntimeConfig):
        self.config = config
        
    # Mapping of interval strings to milliseconds
    interval_to_ms = {
        "1m": 60 * 1000,
        "3m": 3 * 60 * 1000,
        "5m": 5 * 60 * 1000,
        "15m": 15 * 60 * 1000,
        "30m": 30 * 60 * 1000,
        "1h": 60 * 60 * 1000,
        "2h": 2 * 60 * 60 * 1000,
        "4h": 4 * 60 * 60 * 1000,
        "6h": 6 * 60 * 60 * 1000,
        "8h": 8 * 60 * 60 * 1000,
        "12h": 12 * 60 * 60 * 1000,
        "1d": 24 * 60 * 60 * 1000,
    }
    
    @staticmethod
    def convert_ws_kline(k: dict) -> dict:
        """
        Convert a Binance WebSocket kline message to a simplified format.
        """
        try:
            return {
                "start_time": int(k.get("t")),
                "end_time":   int(k.get("T")),
                "open":       float(k.get("o")),
                "high":       float(k.get("h")),
                "low":        float(k.get("l")),
                "close":      float(k.get("c")),
                "volume":     float(k.get("v"))
            }
        except Exception:
            logging.exception(f"Failed to convert WebSocket kline: {k}")
            return {}

    @staticmethod
    def convert_rest_kline(kline: list) -> dict:
        """
        Convert a Binance REST API kline to a simplified format.
        """
        try:
            return {
                "start_time": int(kline[0]),
                "end_time":   int(kline[6]),
                "open":       float(kline[1]),
                "high":       float(kline[2]),
                "low":        float(kline[3]),
                "close":      float(kline[4]),
                "volume":     float(kline[5])
            }
        except Exception:
            logging.exception(f"Failed to convert REST kline: {kline}")
            return {}
    
    @staticmethod
    def get_restapi_base_url(kline_topic: KlineTopic, mode: Mode):
        """
        Determine the REST API base URL based on kline type (spot vs futures) and mode.
        """
        base = TestnetConstants.Binance if mode == Mode.Testnet else LiveConstants.Binance
        kline_type = kline_topic.klineType
        return (
            base.RESTAPI_SPOT_URL if kline_type == KlineType.Binance_Spot
            else base.RESTAPI_FUTURES_URL
        )
       
    @staticmethod
    def get_websocket_base_url(kline_topic: KlineTopic, mode: Mode):
        """
        Determine the WebSocket base URL based on kline type (spot vs futures) and mode.
        """
        base = LiveConstants.Binance if mode == Mode.Live else TestnetConstants.Binance
        kline_type = kline_topic.klineType
        return (
            base.WEBSOCKET_SPOT_URL if kline_type == KlineType.Binance_Spot
            else base.WEBSOCKET_FUTURES_URL
        )
       
    @staticmethod
    def get_websocket_user_data_base_url(mode: Mode):
        """
        Get the WebSocket user data URL for account/order events.
        """
        base = LiveConstants.Binance if mode == Mode.Live else TestnetConstants.Binance
        return base.WEBSOCKET_FUTURES_USER_DATA_URL
    
    async def fetch_kline(self, session, url, params):
        async with session.get(url, params=params) as response:
            return await response.json()  
        
    async def getKlineRestAPI(self, kline_topic: KlineTopic, end_time: Optional[int] = None):
        try:
            base_url = self.get_restapi_base_url(kline_topic, self.config.mode)
            endpoint = base_url + ("/v3/klines" if kline_topic.klineType == KlineType.Binance_Spot else "/v1/klines")
            symbol = kline_topic.symbol.value
            interval = kline_topic.timeframe.lower()
            async with aiohttp.ClientSession() as session:
                # If end_time isn't provided, default to current UTC timestamp in milliseconds
                if end_time is None:
                    end_time = int(datetime.now(timezone.utc).timestamp() * 1000)

                total_data = []
                total_needed = self.config.data_count
                time_increment = BinanceHelper.interval_to_ms.get(interval, 60 * 1000)

                downloader = SafeKlineDownloader(
                    session=session,
                    fetch_func=self.fetch_kline,
                    endpoint=endpoint,
                    symbol=symbol,
                    interval=interval,
                    max_limit=1000,
                    time_increment_ms=time_increment,
                    max_concurrent_requests=10,
                    chunk_sleep=0
                )

                total_data = await downloader.download_reverse(end_time=end_time, total_needed=total_needed)
                converted_data = [self.convert_rest_kline(k) for k in total_data]
                # Drop the first 5 bars as warm-up
                converted_data = converted_data[5:]
                return converted_data
        except Exception as e:
            logging.error(f"getKlineRestAPI: {e}")


    async def getLatestKline(self, kline_topic: KlineTopic):
        try:
            base_url = self.get_restapi_base_url(kline_topic, self.config.mode)
            endpoint = base_url + ("/v3/klines" if kline_topic.klineType == KlineType.Binance_Spot else "/v1/klines")
            symbol = kline_topic.symbol.value
            interval = kline_topic.timeframe.lower()

            params = {
                "symbol": symbol,
                "interval": interval,
                "limit": 2
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, params=params) as resp:
                    if resp.status != 200:
                        logging.error(f"Failed to fetch latest kline for {symbol}: HTTP {resp.status}")
                        return None

                    data = await resp.json()
                    if not data or not isinstance(data, list):
                        logging.warning(f"No kline data received for {symbol}")
                        return None

                    latest_kline = [self.convert_rest_kline(k) for k in data]
                    return latest_kline

        except Exception as e:
            logging.error(f"getKlineRestAPI (latest candle): {e}")
            return None
        
    def parse_order_book(self, data: dict) -> OrderBookSnapshot:
        """
        Convert Binance order book JSON into an OrderBookSnapshot.
        Data should contain 'bids' and 'asks' as lists of [price, quantity].
        """
        bids = [Level(price=float(price), quantity=float(qty)) for price, qty in data.get('bids', [])]
        asks = [Level(price=float(price), quantity=float(qty)) for price, qty in data.get('asks', [])]
        return OrderBookSnapshot(bids=bids, asks=asks)
    
    def parse_order_update(self, raw_event: dict, exchange: Exchange = Exchange.Binance) -> OrderUpdate:
        o = raw_event["o"]
        
        return OrderUpdate(
            symbol=o["s"],
            order_type=o["ot"],
            side=o["S"],
            time_in_force=o["f"],
            exchange_order_id=str(o["i"]),
            order_time=o["T"],
            updated_time=raw_event["E"],
            size=float(o["q"]),
            filled_size=float(o["z"]),
            remain_size=float(o["q"]) - float(o["z"]),
            price=float(o["ap"]),
            client_order_id=o["c"],
            status=o["X"],
            is_reduce_only=o.get("R", False),
            is_hedge_mode=o.get("ps", None) in ["LONG", "SHORT"],
            exchange=exchange
        )
    
    def convert_order_to_active_order(self, order: dict) -> ActiveOrder:
        """
        Convert a single order dict from Binance API into an ActiveOrder instance.
        """
        symbol = Symbol(order["symbol"])
        exchange = Exchange.Binance
        updated_time = order["updateTime"]
        created_time = order["time"]
        exchange_order_id = str(order["orderId"])
        client_order_id = order["clientOrderId"]
        
        # Determine long vs. short position based on side
        if order["side"] == "BUY":
            long_data = PositionData(quantity=float(order["origQty"]), avg_price=float(order["avgPrice"]))
            short_data = PositionData(quantity=0.0, avg_price=0.0)
        elif order["side"] == "SELL":
            long_data = PositionData(quantity=0.0, avg_price=0.0)
            short_data = PositionData(quantity=float(order["origQty"]), avg_price=float(order["avgPrice"]))
        else:
            long_data = PositionData(quantity=0.0, avg_price=0.0)
            short_data = PositionData(quantity=0.0, avg_price=0.0)
        
        position = Position(
            symbol=symbol,
            long=long_data,
            short=short_data,
            updated_time=order["updateTime"]
        )
        
        active_order = ActiveOrder(
            symbol=symbol,
            exchange=exchange,
            updated_time=updated_time,
            created_time=created_time,
            exchange_order_id=exchange_order_id,
            client_order_id=client_order_id,
            position=position
        )
        
        return active_order
    
    def parse_order_response(self, response: dict) -> OrderResponse:
        return OrderResponse(
            exchange_order_id=str(response.get("orderId")),
            client_order_id=response.get("clientOrderId")
        )
