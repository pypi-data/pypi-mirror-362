import asyncio
import logging
from typing import Dict
from datetime import datetime, timedelta, timezone
from xecution.common.enums import DataProvider, Exchange, Mode, Symbol
from xecution.models.order import ActiveOrder
from xecution.models.config import OrderConfig, RuntimeConfig
from xecution.models.topic import DataTopic, KlineTopic
from xecution.services.datasource.cryptoquant import CryptoQuantClient
from xecution.services.exchange.binance_service import BinanceService
from xecution.services.exchange.bybit_service import BybitService
from xecution.services.exchange.okx_service import OkxService


class BaseEngine:
    """Base engine that processes on_candle_closed and on_datasource_update."""
    def __init__(self, config: RuntimeConfig):
        self.config = config
        self.data_map = {}  # Local storage for kline and data source values
        self.binance_service = BinanceService(config, self.data_map)
        self.bybit_service = BybitService(config, self.data_map)
        self.okx_service = OkxService(config, self.data_map)
        self.cryptoquant_client = CryptoQuantClient(config, self.data_map)
        # Track last processed timestamp for each data topic
        self._last_timestamps: Dict[str, int] = {
            topic.url: None for topic in self.config.datasource_topic
        }

    async def on_candle_closed(self, kline_topic: KlineTopic):
        """Handle closed candle events from the exchange."""

    async def on_order_update(self, order):
        """Handle order status updates."""

    async def on_datasource_update(self, datasource_topic):
        """Handle updates from external data sources."""
        logging.info(f"on_datasource_update: {datasource_topic}")
    
    async def on_active_order_interval(self, activeOrders: list[ActiveOrder]):
        """Process the list of open orders from periodic checks."""

    async def start(self):
        """Start services and run the main event loop based on mode."""
        try:
            if self.config.mode == Mode.Backtest:
                logging.info("Backtest started.")
            elif self.config.mode == Mode.Live:
                logging.info("Live started.")
            elif self.config.mode == Mode.Testnet:
                logging.info("Testnet started.")

            # Begin fetching kline data and process closed candles
            await self.binance_service.get_klines(self.on_candle_closed)
            # Start listening to external data source updates
            if self.config.mode == Mode.Backtest:
                # Backtest: run the full history load, then exit
                await self.listen_data_source_update()
            # For live or testnet trading, set up real-time listeners
            if self.config.mode in (Mode.Live, Mode.Testnet):
                await self.binance_service.check_connection()
                asyncio.create_task(self.listen_data_source_update())
                await self.listen_order_status()
                asyncio.create_task(self.listen_open_orders_periodically())
                while True:
                    await asyncio.sleep(1)  # Keep the loop alive
            else:
                logging.info("Backtest completed. Exiting.")
                await self.on_backtest_completed()
        except ConnectionError as e:
            logging.error(f"Connection check failed: {e}")
        
    async def place_order(self, order_config: OrderConfig):
        return await self.binance_service.place_order(order_config)
        
    async def get_account_info(self):
        return await self.binance_service.get_account_info()

    async def set_hedge_mode(self, is_hedge_mode: bool):
        return await self.binance_service.set_hedge_mode(is_hedge_mode)

    async def set_leverage(self, symbol: Symbol, leverage: int):
        return await self.binance_service.set_leverage(symbol, leverage)
    
    async def get_position_info(self, symbol: Symbol):
        return await self.binance_service.get_position_info(symbol)
    
    async def get_wallet_balance(self):
        return await self.binance_service.get_wallet_balance()

    async def get_current_price(self, symbol: Symbol):
        if self.config.exchange == Exchange.Binance:
            return await self.binance_service.get_current_price(symbol)
        elif self.config.exchange == Exchange.Bybit:
            return await self.bybit_service.get_current_price(symbol)
        elif self.config.exchange == Exchange.Okx:
            return await self.okx_service.get_current_price(symbol)
        else:
            logging.error("Unknown exchange")
            return None
        
    async def get_order_book(self, symbol: Symbol):
        if self.config.exchange == Exchange.Binance:
            return await self.binance_service.get_order_book(symbol)
        else:
            logging.error("Unknown exchange")
            return None

    async def listen_order_status(self):
        if self.config.exchange == Exchange.Binance:
            return await self.binance_service.listen_order_status(self.on_order_update)
        else:
            logging.error("Unknown exchange")
            return None
        
    async def get_open_orders(self):
        if self.config.exchange == Exchange.Binance:
            # Call BinanceService and pass the on_active_order_interval callback
            return await self.binance_service.get_open_orders(self.on_active_order_interval)
        else:
            logging.error("Unknown exchange")
            
    async def cancel_order(self, symbol: Symbol, client_order_id: str):
        if self.config.exchange == Exchange.Binance:
            return await self.binance_service.cancel_order(symbol, client_order_id)
        else:
            logging.error("Unknown exchange")
    
    async def fetch_data_source(self, data_topic: DataTopic):
        if data_topic.provider == DataProvider.CRYPTOQUANT:
            return await self.cryptoquant_client.fetch_all_parallel(data_topic)

    async def listen_open_orders_periodically(self):
        """
        Every 60 seconds, call Binance's get_open_orders API, convert the
        returned open orders to ActiveOrder, and pass them to on_active_order_interval for processing.
        """
        while True:
            try:
                # Since get_open_orders internally uses on_active_order_interval,
                # we just await its completion here.
                await self.get_open_orders()
            except Exception as e:
                logging.error("Error retrieving open orders: %s", e)
            await asyncio.sleep(60)
            
    async def listen_data_source_update(self):
        """
        Backtest mode: Fetch full history once per topic, then invoke
        on_datasource_update(topic) so handlers can access data_map.

        Live/Testnet mode: Seed with the most recent bar, then every minute:
          - Re-fetch the most recent data (last_n=...),
          - Compare timestamps,
          - If there's new data, wait briefly to ensure it's complete,
          - Fetch full data batch, invoke on_datasource_update(topic),
          - Update last processed timestamp.
        """
        logging.info("Data source listening has started.")
        # Backtest: one-shot full history
        if self.config.mode == Mode.Backtest:
            for topic in self.config.datasource_topic:
                await self.cryptoquant_client.fetch_all_parallel(topic)
                await self.on_datasource_update(topic)
            return

        # Live/Testnet: initial seed with most recent bar
        for topic in self.config.datasource_topic:
            latest = await self.cryptoquant_client.fetch(topic, last_n=1)
            if latest:
                self._last_timestamps[topic] = latest[-1]["start_time"]

        # Align to the start of the next full minute
        now = datetime.now(timezone.utc)
        next_minute = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
        await asyncio.sleep((next_minute - now).total_seconds())

        # Periodic loop every 60 seconds
        while True:
            cycle_start = datetime.now(timezone.utc)

            for topic in self.config.datasource_topic:
                try:
                    latest = await self.cryptoquant_client.fetch(topic)
                    if latest is None or len(latest) == 0:
                        continue

                    ts = latest[-1]["start_time"]
                    last_ts = self._last_timestamps.get(topic) or 0

                    if ts > last_ts:
                        # Wait to ensure full data entry
                        await asyncio.sleep(10)
                        # Fetch the full data batch and invoke callback for new data
                        await self.fetch_data_source(topic)
                        await self.on_datasource_update(topic)
                        self._last_timestamps[topic] = ts

                except Exception as e:
                    logging.error("Error fetching %s: %s", topic.url, e)

            # Sleep until the next full minute
            elapsed = (datetime.now(timezone.utc) - cycle_start).total_seconds()
            await asyncio.sleep(max(0, 60 - elapsed))

    async def on_backtest_completed(self):
        """ Handling after all the data retrieving has done. """