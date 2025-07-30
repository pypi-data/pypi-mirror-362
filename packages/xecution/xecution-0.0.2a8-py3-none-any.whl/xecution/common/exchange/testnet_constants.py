class TestnetConstants:
    # Binance Endpoints
    class Binance:
        RESTAPI_SPOT_URL = "https://testnet.binance.vision/api"
        RESTAPI_FUTURES_URL = "https://testnet.binancefuture.com/fapi"
        WEBSOCKET_SPOT_URL = "wss://testnet.binance.vision/ws"
        WEBSOCKET_FUTURES_URL = "wss://stream.binancefuture.com/ws"
        WEBSOCKET_SPOT_USER_DATA_URL = "wss://testnet.binance.vision/ws"
        WEBSOCKET_FUTURES_USER_DATA_URL = "wss://fstream.binancefuture.com/ws"
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
        RESTAPI_SPOT_URL = "https://api-demo.bybit.com"
        RESTAPI_FUTURES_URL = "https://api-demo.bybit.com"
        WEBSOCKET_SPOT_URL = "wss://stream-demo.bybit.com/v5/public/spot"
        WEBSOCKET_FUTURES_URL = "wss://stream-demo.bybit.com/v5/public/futures"
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
        WEBSOCKET_SPOT_URL = "wss://wspap.okx.com:8443/ws/v5/public"
        WEBSOCKET_FUTURES_URL = "wss://wspap.okx.com:8443/ws/v5/public"
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
        RESTAPI_SPOT_URL = "https://api-public.sandbox.exchange.coinbase.com"
        RESTAPI_FUTURES_URL = "https://api-public.sandbox.exchange.coinbase.com"
        WEBSOCKET_SPOT_URL = "wss://ws-feed-public.sandbox.exchange.coinbase.com"
        WEBSOCKET_FUTURES_URL = "wss://ws-feed-public.sandbox.exchange.coinbase.com"
        PUBLIC_CHANNELS = {
            "ticker": "ticker",
            "trade": "matches",
            "order_book": "level2"
        }
        PRIVATE_CHANNELS = {
            "user": "user"
        }
