import asyncio
import logging
from xecution.models.order import ActiveOrder
from xecution.models.config import RuntimeConfig, OrderConfig
from xecution.models.topic import KlineTopic
from xecution.services.connection.base_websockets import WebSocketService
from xecution.services.exchange.binance_helper import BinanceHelper
from xecution.common.enums import Mode, Symbol
from xecution.services.exchange.exchange_order_manager import BinanceOrderManager

class BinanceService:
    
    def __init__(self, config: RuntimeConfig, data_map: dict):
        """
        Service for managing Binance WebSocket subscriptions and REST API calls.
        """
        self.config = config
        self.ws_service = WebSocketService()
        self.data_map = data_map  # Shared reference for storing market data
        self.binanceHelper = BinanceHelper(self.config)
        self.manager = BinanceOrderManager(
            api_key=config.API_Key,
            api_secret=config.API_Secret,
            mode=config.mode
        )
        
    async def check_connection(self):
        account_info = await self.get_account_info()
        if not account_info or "code" in account_info:  # Binance error responses typically include "code"
            error_msg = account_info.get("msg", "Unknown error") if account_info else "No response"
            logging.error(f"[BinanceService] check_connection: API Key validation failed: {error_msg}")
            # Raise an exception to indicate connection failure
            raise ConnectionError(f"API Key validation failed: {error_msg}")
        logging.info("[BinanceService] check_connection: Successfully connected to Binance")
    
    async def get_klines(self, on_candle_closed):
        """
        Call Binance REST or WebSocket to retrieve kline (candlestick) data.
        """
        for kline_topic in self.config.kline_topic:
            if self.config.mode == Mode.Backtest:
                candles = await self.binanceHelper.getKlineRestAPI(kline_topic)
                self.data_map[kline_topic] = candles
                await on_candle_closed(kline_topic)
            elif self.config.mode in (Mode.Live, Mode.Testnet):
                await self.listen_kline(on_candle_closed, kline_topic)

    async def listen_kline(self, on_candle_closed, kline_topic: KlineTopic):
        """Subscribe to Binance WebSocket for a given kline topic and handle closed candles."""
        try:
            ws_url = (
                self.binanceHelper.get_websocket_base_url(kline_topic, self.config.mode)
                + f"/{kline_topic.symbol.value.lower()}@kline_{kline_topic.timeframe.lower()}"
            )
            # Initialize data storage for this kline topic
            self.data_map[kline_topic] = []

            async def message_handler(exchange, message):
                """Process incoming WebSocket kline messages and trigger the candle-closed callback."""
                try:
                    kline = message.get("k", {})
                    if not kline or not kline.get("x", False):
                        return  # Ignore incomplete or invalid candles

                    # Wait until REST API confirms the same candle
                    while True:
                        recent = await self.binanceHelper.getLatestKline(kline_topic)
                        converted = self.binanceHelper.convert_ws_kline(kline)
                        start_ts = converted.get("start_time")
                        end_ts = converted.get("end_time")
                        if any(c["start_time"] == start_ts for c in recent):
                            self.data_map[kline_topic] = await self.binanceHelper.getKlineRestAPI(kline_topic, end_ts)
                            break

                    logging.debug(
                        f"[{exchange}] Candle closed | "
                        f"{kline_topic.klineType.name}-{kline_topic.symbol}-{kline_topic.timeframe} | "
                        f"Close: {kline.get('c')}"
                    )
                    await on_candle_closed(kline_topic)

                except Exception as e:
                    logging.error(f"[BinanceService] on_candle_closed failed: {e}")

            # Subscribe to the kline stream
            logging.debug(f"[BinanceService] Connecting to WebSocket: {ws_url}")
            await self.ws_service.subscribe(ws_url, ws_url, None, message_handler)
            logging.info(f"[BinanceService] Subscribed to {kline_topic.klineType.name}-{kline_topic.symbol}-{kline_topic.timeframe}")

        except Exception as e:
            logging.error(f"[BinanceService] listen_kline failed: {e}")
            
    async def listen_order_status(self, on_order_update):
        """
        Subscribe to Binance User Data Stream WebSocket to receive order update events,
        and call `on_order_update(order)` when an order status changes.
        """
        try:
            # Retrieve the listenKey for the user data stream
            res = await self.manager.get_listen_key()
            listen_key = res.get("listenKey")
            if not listen_key:
                logging.error("[BinanceService] Failed to obtain listenKey.")
                return

            # Launch background task to keep the listenKey alive
            asyncio.create_task(self._keepalive_listen_key(listen_key))

            # Build the WebSocket URL for order updates
            ws_url = (
                self.binanceHelper.get_websocket_user_data_base_url(self.config.mode)
                + f"/{listen_key}"
            )
            logging.debug(f"[BinanceService] Connecting to order update stream at {ws_url}")

            async def message_handler(_, message):
                """Handle incoming messages; parse and forward order updates."""
                if message.get("e") == "ORDER_TRADE_UPDATE":
                    try:
                        order = self.binanceHelper.parse_order_update(message, self.config.exchange)
                        await on_order_update(order)
                    except Exception as e:
                        logging.error(f"[BinanceService] listen_order_status error: {e}")

            # Subscribe to the user data stream
            await self.ws_service.subscribe("binance_futures_order", ws_url, None, message_handler)

        except Exception as e:
            logging.error(f"[BinanceService] listen_order_status failed: {e}")


    async def _keepalive_listen_key(self, listen_key):
        """
        Periodically call keepalive to maintain the listenKey's validity (every 30 minutes).
        """
        while True:
            try:
                await self.manager.keepalive_listen_key(listen_key)
            except Exception as e:
                logging.error(f"[BinanceService] keepalive_listen_key error: {e}")
            await asyncio.sleep(30 * 60)

    async def place_order(self, order_config: OrderConfig):
        # (Optional) Check for existing open orders to avoid duplicate submissions
        resp = await self.manager.place_order(order_config)
        return self.binanceHelper.parse_order_response(resp)
        
    async def get_account_info(self):
        """Fetch account information via REST API."""
        return await self.manager.get_account_info()
    
    async def get_wallet_balance(self):
        """Fetch current wallet balances."""
        return await self.manager.get_wallet_balance()
    
    async def set_hedge_mode(self, is_hedge_mode: bool):
        """Enable or disable hedge mode."""
        await self.manager.set_hedge_mode(is_hedge_mode)
        
    async def set_leverage(self, symbol: Symbol, leverage: int):
        """Set position leverage for a given symbol."""
        await self.manager.set_leverage(symbol, leverage)
    
    async def get_position_info(self, symbol: Symbol):
        """Retrieve current position details for a symbol."""
        return await self.manager.get_position_info(symbol)

    async def get_current_price(self, symbol: Symbol):
        """Get the latest market price for a symbol."""
        return await self.manager.get_current_price(symbol)
    
    async def get_order_book(self, symbol: Symbol):
        """Fetch and parse the current order book snapshot."""
        ob = await self.manager.get_order_book(symbol)
        snapshot = self.binanceHelper.parse_order_book(ob)
        logging.debug(f"[BinanceService] get_order_book: {snapshot}")
        return snapshot
    
    async def get_open_orders(self, on_active_order_interval):
        """Fetch all open orders and forward ActiveOrder list to the provided callback."""
        orders = await self.manager.get_open_orders()
        active_orders = [self.binanceHelper.convert_order_to_active_order(o) for o in orders]
        return await on_active_order_interval(active_orders)

    async def cancel_order(self, symbol: Symbol, client_order_id: str):
        """Cancel an existing order by its client order ID."""
        return await self.manager.cancel_order(symbol, client_order_id)
