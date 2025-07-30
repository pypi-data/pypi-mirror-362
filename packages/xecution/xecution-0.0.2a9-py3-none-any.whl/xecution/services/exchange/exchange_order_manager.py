import logging
from xecution.common.enums import KlineType, Mode, OrderType, Symbol
from xecution.common.exchange.live_constants import LiveConstants
from xecution.common.exchange.testnet_constants import TestnetConstants
from xecution.models.config import OrderConfig
from xecution.services.exchange.standardize import Standardize
from xecution.services.exchange.api.binanceapi import BinanceAPIClient
from xecution.services.exchange.api.bybitapi import BybitAPIClient
from xecution.services.exchange.api.okxapi import OkxAPIClient

# Implementation of BinanceOrderManager (supports spot and futures)
class BinanceOrderManager():
    def __init__(self, api_key: str, api_secret: str, market_type: KlineType = KlineType.Binance_Futures, mode: Mode = Mode.Live):
        self.api_key = api_key
        self.api_secret = api_secret
        self.market_type = market_type
        self.mode = mode
        # Select Live or Testnet
        base = LiveConstants.Binance if mode == Mode.Live else TestnetConstants.Binance
        self.binanceApiClient = BinanceAPIClient(api_key=api_key, api_secret=api_secret)
        # Choose Spot or Futures URL
        self.rest_url = (
            base.RESTAPI_SPOT_URL if self.market_type == KlineType.Binance_Spot
            else base.RESTAPI_FUTURES_URL
        )
    
    async def set_leverage(self, symbol: Symbol, leverage: int):
        if self.market_type == KlineType.Binance_Spot:
            return None
        endpoint = "/v1/leverage"
        url = self.rest_url + endpoint
        payload = {
            "symbol": symbol.value.lower(),
            "leverage": int(leverage),
        }
        try:
            response = await self.binanceApiClient.request(
                method="POST",
                url=url,
                params=payload,
                auth=True
            )
            logging.info(f"[BinanceOrderManager] set_leverage response: {response}")
            return response
        except Exception as e:
            logging.error(f"[BinanceOrderManager] set_leverage - Failed to set leverage for {symbol}: {e}")
            return None
        
    async def set_hedge_mode(self, is_hedge_mode: bool):
        if self.market_type == KlineType.Binance_Spot:
            return None
        endpoint = "/v1/positionSide/dual"
        url = self.rest_url + endpoint
        payload = {
            "dualSidePosition": bool(is_hedge_mode),
        }
        try:
            response = await self.binanceApiClient.request(
                method="POST",
                url=url,
                params=payload,
                auth=True
            )
            logging.info(f"[BinanceOrderManager] set_hedge_mode response: {response}")
            return response
        except Exception as e:
            logging.error(f"[BinanceOrderManager] set_hedge_mode - Failed to set hedge mode to {is_hedge_mode}: {e}")
            return None

    async def get_exchange_info(self):
        # Spot uses /api/v3/exchangeInfo; Futures uses /fapi/v1/exchangeInfo
        endpoint = "/v3/exchangeInfo" if self.market_type == KlineType.Binance_Spot else "/v1/exchangeInfo"
        url = self.rest_url + endpoint
        try:
            async with self.session.get(url) as response:
                data = await response.json()
                if response.status != 200:
                    raise Exception(f"Error getting exchange info: {data}")
                return data
        except Exception as e:
            logging.error(f"[BinanceOrderManager] get_exchange_info - Error fetching exchange info: {e}")
            return None

    async def get_open_orders(self):
        # Spot: /api/v3/openOrders; Futures: /fapi/v1/openOrders
        endpoint = "/v3/openOrders" if self.market_type == KlineType.Binance_Spot else "/v1/openOrders"
        url = self.rest_url + endpoint
        try:
            response = await self.binanceApiClient.request(
                method="GET",
                url=url,
                auth=True
            )
            return response
        except Exception as e:
            logging.error(f"[BinanceOrderManager] get_open_orders - Failed to fetch open orders: {e}")
            return None

    async def get_account_info(self):
        # Spot: /api/v3/account; Futures: /fapi/v2/account
        endpoint = "/v3/account" if self.market_type == KlineType.Binance_Spot else "/v2/account"
        url = self.rest_url + endpoint
        try:
            response = await self.binanceApiClient.request(
                method="GET",
                url=url,
                auth=True
            )
            return response
        except Exception as e:
            logging.error(f"[BinanceOrderManager] get_account_info - Failed to fetch account info: {e}")
            return None
        
    async def get_wallet_balance(self) -> float:
        """Return the available USDT balance for spot or futures account."""
        account_info = await self.get_account_info()
        if account_info is None:
            return None
        try:
            if self.market_type == KlineType.Binance_Spot:
                # Spot: find USDT entry in balances and return `free` field
                balances = account_info.get("balances", [])
                usdt_balance = next((b for b in balances if b.get("asset") == "USDT"), None)
                if usdt_balance:
                    available = usdt_balance.get("free", "0")
                    logging.info(f"[BinanceOrderManager] Spot USDT available balance: {available}")
                    return float(available)
                logging.info("[BinanceOrderManager] USDT not found in spot balances.")
                return 0.0
            else:
                # Futures: find USDT entry in assets and return `walletBalance`
                assets = account_info.get("assets", [])
                usdt_asset = next((a for a in assets if a.get("asset") == "USDT"), None)
                if usdt_asset:
                    available = usdt_asset.get("walletBalance")
                    logging.info(f"[BinanceOrderManager] Futures USDT available balance: {available}")
                    return float(available)
                logging.info("[BinanceOrderManager] USDT not found in futures assets.")
                return 0.0
        except Exception as e:
            logging.error(f"[BinanceOrderManager] get_wallet_balance - Error retrieving USDT balance: {e}")
            return 0.0

    async def get_position_info(self, symbol: Symbol):
        # Spot has no position info; Futures uses /fapi/v2/positionRisk
        if self.market_type == KlineType.Binance_Spot:
            return []
        else:
            endpoint = "/v2/positionRisk"
            url = self.rest_url + endpoint
            params = {"symbol": symbol.value}
            try:
                response = await self.binanceApiClient.request(
                    method="GET",
                    url=url,
                    params=params,
                    auth=True
                )
                logging.info(f"[BinanceOrderManager] get_position response: {response}")
                parsed = Standardize.parse_binance_position(response)
                logging.debug(f"[BinanceOrderManager] Parsed positions: {parsed}")
                return parsed
            except Exception as e:
                logging.error(f"[BinanceOrderManager] get_position_info - Error for {symbol}: {e}")
                return None
                
    async def get_current_price(self, symbol: Symbol) -> float:
        # Spot: /api/v3/ticker/price; Futures: /fapi/v1/ticker/price
        endpoint = "/v3/ticker/price" if self.market_type == KlineType.Binance_Spot else "/v1/ticker/price"
        url = self.rest_url + endpoint
        params = {"symbol": symbol.value.upper()}
        try:
            response = await self.binanceApiClient.request(
                method="GET",
                url=url,
                params=params,
                auth=True
            )
            # Expected response: {"symbol": "BTCUSDT", "price": "12345.67"}
            price = response.get("price")
            logging.info(f"[BinanceOrderManager] get_current_price: {price}")
            return float(price) if price is not None else 0.0
        except Exception as e:
            logging.error(f"[BinanceOrderManager] get_current_price - Error fetching price: {e}")
            return 0.0
            
    async def place_order(self, order_config: OrderConfig) -> dict:
        # Order endpoint: Spot /api/v3/order; Futures /fapi/v1/order
        endpoint = "/v3/order" if self.market_type == KlineType.Binance_Spot else "/v1/order"
        url = self.rest_url + endpoint
        params = {
            "symbol": order_config.symbol.value.upper(),
            "side": order_config.side.value.upper(),
            "type": order_config.order_type.value.upper(),
            "quantity": order_config.quantity,
        }
        if order_config.order_type == OrderType.LIMIT:
            params["price"] = order_config.price
            params["timeInForce"] = order_config.time_in_force.value.upper()
        try:
            response = await self.binanceApiClient.request(
                method="POST",
                url=url,
                params=params,
                auth=True
            )
            logging.info(f"[BinanceOrderManager] Order placed for {order_config.symbol}. Response: {response}")
            return response
        except Exception as e:
            logging.error(f"[BinanceOrderManager] place_order - Error: {e}")
            return None
    
    async def get_order_book(self, symbol: Symbol = Symbol.BTCUSDT, limit: int = 5):
        # Spot: /api/v3/depth; Futures: /fapi/v1/depth
        endpoint = "/v3/depth" if self.market_type == KlineType.Binance_Spot else "/v1/depth"
        url = self.rest_url + endpoint
        try:
            params = {'symbol': symbol.value, 'limit': limit}
            response = await self.binanceApiClient.request(
                method="GET",
                url=url,
                params=params,
                auth=True
            )
            return response
        except Exception as e:
            logging.error(f"[BinanceOrderManager] get_order_book - Error fetching order book: {e}")
            return None
    
    async def cancel_order(self, symbol: Symbol, client_order_id: str):
        endpoint = "/v3/order" if self.market_type == KlineType.Binance_Spot else "/v1/order"
        url = self.rest_url + endpoint
        params = {
            "symbol": symbol.value.upper(),
            "origClientOrderId": client_order_id
        }
        try:
            response = await self.binanceApiClient.request(
                method="DELETE",
                url=url,
                params=params,
                auth=True
            )
            return response
        except Exception as e:
            logging.error(f"[BinanceOrderManager] cancel_order - Error cancelling order: {e}")
            return None
    
    async def get_listen_key(self):
        # Spot: /api/v3/userDataStream; Futures: /fapi/v1/listenKey
        endpoint = "/v3/userDataStream" if self.market_type == KlineType.Binance_Spot else "/v1/listenKey"
        url = self.rest_url + endpoint
        try:
            response = await self.binanceApiClient.request(
                method="POST",
                url=url,
                auth=True
            )
            return response
        except Exception as e:
            logging.error(f"[BinanceOrderManager] get_listen_key - Error fetching listenKey: {e}")
            return None
        
    async def keepalive_listen_key(self, listen_key):
        # Spot: /api/v3/userDataStream; Futures: /fapi/v1/listenKey
        endpoint = "/v3/userDataStream" if self.market_type == KlineType.Binance_Spot else "/v1/listenKey"
        url = self.rest_url + endpoint
        params = {"listenKey": listen_key}
        try:
            response = await self.binanceApiClient.request(
                method="PUT",
                url=url,
                params=params,
                auth=True
            )
            logging.debug(f"[BinanceOrderManager] keepalive_listen_key response: {response}")
            return response
        except Exception as e:
            logging.error(f"[BinanceOrderManager] keepalive_listen_key - Error keeping listenKey alive: {e}")
            return None
    
    async def close(self):    
        await self.binanceApiClient.close()

# Skeleton implementations for other exchanges (implement as needed)
class BybitOrderManager():
    def __init__(self, api_key: str, api_secret: str, market_type: KlineType = KlineType.Bybit_Futures, mode: Mode = Mode.Live):
        self.api_key = api_key
        self.api_secret = api_secret
        self.market_type = market_type
        self.mode = mode
        # Select Live or Testnet
        base = LiveConstants.Bybit if mode == Mode.Live else TestnetConstants.Bybit
        self.bybitApiClient = BybitAPIClient(api_key=api_key, api_secret=api_secret)
        # Choose Spot or Futures URL
        self.rest_url = (
            base.RESTAPI_SPOT_URL if self.market_type == KlineType.Bybit_Spot
            else base.RESTAPI_FUTURES_URL
        )

    async def get_exchange_info(self):
        pass
    async def get_open_orders(self, symbol: str):
        pass
    async def get_account_info(self):
        pass
    async def get_position_info(self, symbol: str):
        pass
    async def place_order(self, order_config: OrderConfig):
        pass
    async def set_hedge_mode(self, is_hedge_mode):
        pass
    async def set_leverage(self, leverage):
        pass
    async def get_current_price(self, symbol: str):
        """
        Use Bybit's /v5/market/tickers API to fetch the current price.
        Returns `lastPrice` from the result as a float.
        """
        endpoint = "/v5/market/tickers"
        url = self.rest_url + endpoint
        params = (
            {"category": "spot", "symbol": symbol.upper()}
            if self.market_type == KlineType.Bybit_Spot
            else {"category": "linear", "symbol": symbol.upper()}
        )
        try:
            response = await self.bybitApiClient.request(
                method="GET",
                url=url,
                params=params,
                auth=False  # Public endpoint, no auth required
            )
            if response.get("retCode") == 0:
                tickers = response.get("result", {}).get("list", [])
                if tickers:
                    price = tickers[0].get("lastPrice")
                    logging.info(f"[BybitOrderManager] get_current_price: {price}")
                    return float(price) if price is not None else None
            return None
        except Exception as e:
            logging.error(f"[BybitOrderManager] get_current_price - Error fetching price for {symbol}: {e}")
            return None

class OKXOrderManager():
    def __init__(self, api_key: str, api_secret: str, market_type: KlineType = KlineType.OKX_Futures, mode: Mode = Mode.Live):
        self.api_key = api_key
        self.api_secret = api_secret
        self.market_type = market_type
        self.mode = mode
        # Select Live or Testnet
        base = LiveConstants.OKX if mode == Mode.Live else TestnetConstants.OKX
        self.okxApiClient = OkxAPIClient(api_key=api_key, api_secret=api_secret)
        # Choose Spot or Futures URL
        self.rest_url = (
            base.RESTAPI_SPOT_URL if self.market_type == KlineType.OKX_Spot
            else base.RESTAPI_FUTURES_URL
        )

    async def get_exchange_info(self):
        pass
    async def get_open_orders(self, symbol: str):
        pass
    async def get_account_info(self):
        pass
    async def get_position_info(self, symbol: str):
        pass
    async def place_order(self, order_config: OrderConfig):
        pass
    async def set_hedge_mode(self, is_hedge_mode):
        pass
    async def set_leverage(self, leverage):
        pass
    async def get_current_price(self, symbol: str):
        """
        Use OKX's /api/v5/market/ticker API to fetch the current price.
        Convert symbol (e.g. "BTCUSDT") to OKX format ("BTC-USDT") before requesting.
        Returns `data[0]['last']` as the current price.
        """
        endpoint = "/api/v5/market/ticker"
        url = self.rest_url + endpoint
        inst_id = symbol[:-4] + "-" + symbol[-4:]
        params = (
            {"instId": inst_id, "instType": "SPOT"}
            if self.market_type == KlineType.OKX_Spot
            else {"instId": inst_id + "-SWAP", "instType": "SWAP"}
        )
        try:
            response = await self.okxApiClient.request(
                method="GET",
                url=url,
                params=params,
                auth=False  # Public endpoint, no auth required
            )
            if response.get("code") == "0":
                data = response.get("data", [])
                if data:
                    price = data[0].get("last")
                    logging.info(f"[OKXOrderManager] get_current_price: {price}")
                    return float(price) if price is not None else None
            return None
        except Exception as e:
            logging.error(f"[OKXOrderManager] get_current_price - Error fetching price for {symbol}: {e}")
            return None
