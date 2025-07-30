class LiveConstants:
   # Binance Endpoints
    class Binance:
        RESTAPI_SPOT_URL = "https://api.binance.com/api"
        RESTAPI_FUTURES_URL = "https://fapi.binance.com/fapi"
        WEBSOCKET_SPOT_URL = "wss://stream.binance.com:9443/ws"
        WEBSOCKET_FUTURES_URL = "wss://fstream.binance.com/ws"
        WEBSOCKET_SPOT_USER_DATA_URL = "wss://stream.binance.com/ws"
        WEBSOCKET_FUTURES_USER_DATA_URL = "wss://fstream.binance.com/ws"
        PUBLIC_CHANNELS = {
            "ticker": "!ticker@arr",
            "trade": "!trade@arr",
            "order_book": "!depth@100ms"
        }
        PRIVATE_CHANNELS = {
            "user_data": "listenKey"
        }
        
    # Bybit Endpoints
    class Bybit:
        RESTAPI_SPOT_URL = "https://api.bybit.com"
        RESTAPI_FUTURES_URL = "https://api.bybit.com"
        WEBSOCKET_SPOT_URL = "wss://stream.bybit.com/v5/public/spot"
        WEBSOCKET_FUTURES_URL = "wss://stream.bybit.com/v5/public/futures"
        PUBLIC_CHANNELS = {
            "ticker": "tickers",
            "trade": "publicTrade",
            "order_book": "orderbook.100"
        }
        PRIVATE_CHANNELS = {
            "execution": "execution",
            "order": "order",
            "wallet": "wallet"
        }

    # OKX Endpoints
    class OKX:
        RESTAPI_SPOT_URL = "https://www.okx.com"
        RESTAPI_FUTURES_URL = "https://www.okx.com"
        WEBSOCKET_SPOT_URL = "wss://ws.okx.com:8443/ws/v5/public"
        WEBSOCKET_FUTURES_URL = "wss://ws.okx.com:8443/ws/v5/public"
        PUBLIC_CHANNELS = {
            "ticker": "tickers",
            "trade": "trades",
            "order_book": "books"
        }
        PRIVATE_CHANNELS = {
            "order": "orders"
        }

    # Coinbase Endpoints
    class Coinbase:
        RESTAPI_SPOT_URL = "https://api.coinbase.com"
        RESTAPI_FUTURES_URL = "https://api.exchange.coinbase.com"
        WEBSOCKET_SPOT_URL = "wss://ws-feed.exchange.coinbase.com"
        WEBSOCKET_FUTURES_URL = "wss://ws-feed.exchange.coinbase.com"
        PUBLIC_CHANNELS = {
            "ticker": "ticker",
            "trade": "matches",
            "order_book": "level2"
        }
        PRIVATE_CHANNELS = {
            "user": "user"
        }