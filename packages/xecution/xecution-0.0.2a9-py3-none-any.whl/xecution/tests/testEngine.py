import asyncio
import sys

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    sys.path.append("/Users/kaihock/Desktop/All In/Xecution")
import asyncio
from pathlib import Path
from urllib.parse import parse_qs
import pandas as pd
import logging
from xecution.core.engine import BaseEngine
from xecution.common.enums import DataProvider, KlineType, Mode, Symbol
from xecution.models.config import RuntimeConfig
from xecution.models.topic import DataTopic, KlineTopic
from xecution.utils.logger import Logger

# --------------------------------------------------------------------
candle_path1 = Path("data/candle/binance_kline_btc_1h.csv") # candle data file path
# --------------------------------------------------------------------

BASE_PATH = Path("data/datasource")
candle_path1.parent.mkdir(parents=True, exist_ok=True)
KLINE_FUTURES = KlineTopic(klineType=KlineType.Binance_Futures, symbol=Symbol.BTCUSDT, timeframe="1h")
Data1  = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/market-data/coinbase-premium-index?window=hour&exchange=binance')
Data2  = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/market-data/funding-rates?window=hour&exchange=binance')
Data3  = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/exchange-flows/reserve?exchange=binance&window=hour')
Data4  = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/exchange-flows/netflow?window=hour&exchange=binance')
Data5  = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/exchange-flows/transactions-count?window=hour&exchange=binance')
Data6  = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/exchange-flows/in-house-flow?exchange=binance&window=hour')
Data7  = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/flow-indicator/exchange-shutdown-index?exchange=binance&window=hour')
Data8  = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/flow-indicator/exchange-inflow-age-distribution?exchange=binance&window=hour')
Data9  = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/flow-indicator/exchange-inflow-cdd?window=hour&exchange=binance')
Data10 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/flow-indicator/exchange-supply-ratio?window=hour&exchange=binance')
Data11 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/flow-indicator/miner-supply-ratio?miner=f2pool&window=hour')
Data12 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/market-indicator/utxo-realized-price-age-distribution?window=hour&exchange=binance')
Data13 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-indicator/stock-to-flow?window=hour')
Data14 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-indicator/nrpl?window=hour')
Data15 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-indicator/utxo-age-distribution?window=hour')
Data16 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-indicator/spent-output-age-distribution?window=hour')
Data17 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-indicator/utxo-supply-distribution?window=hour')
Data18 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-indicator/utxo-realized-supply-distribution?window=hour')
Data19 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-indicator/utxo-count-supply-distribution?window=hour')
Data20 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-indicator/spent-output-supply-distribution?window=hour')
Data21 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/miner-flows/reserve?miner=f2pool&window=hour')
Data22 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/miner-flows/netflow?miner=f2pool&window=hour')
Data23 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/miner-flows/transactions-count?miner=f2pool&window=hour')
Data24 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/miner-flows/addresses-count?miner=f2pool&window=hour')
Data25 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/miner-flows/in-house-flow?miner=f2pool&window=hour')
Data26 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/inter-entity-flows/exchange-to-exchange?from_exchange=binance&to_exchange=bithumb&window=hour')
Data27 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/inter-entity-flows/miner-to-exchange?from_miner=f2pool&to_exchange=binance&window=hour')
Data28 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/inter-entity-flows/bank-to-exchange?from_bank=blockfi&to_exchange=binance&window=hour')
Data29 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/inter-entity-flows/exchange-to-miner?from_exchange=binance&to_miner=f2pool&window=hour')
Data30 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/inter-entity-flows/miner-to-miner?from_miner=f2pool&to_miner=antpool&window=hour')
Data31 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/inter-entity-flows/bank-to-miner?from_bank=blockfi&to_miner=f2pool&window=hour')
Data32 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/inter-entity-flows/exchange-to-bank?from_exchange=binance&to_bank=blockfi&window=hour')
Data33 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/market-data/taker-buy-sell-stats?window=hour&exchange=binance')
Data34 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/market-data/liquidations?window=hour&exchange=binance')
Data35 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-data/supply?window=hour')
Data36 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-data/velocity?window=hour')
Data37 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-data/transactions-count?window=hour')
Data38 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-data/addresses-count?window=hour')
Data39 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-data/tokens-transferred?window=hour')
Data40 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-data/block-bytes?window=hour')
Data41 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-data/block-count?window=hour')
Data42 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-data/block-interval?window=hour')
Data43 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-data/utxo-count?window=hour')
Data44 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-data/fees?window=hour')
Data45 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-data/fees-transaction?window=hour')
Data46 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-data/blockreward?window=hour')
Data47 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-data/difficulty?window=hour')
Data48 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/network-data/hashrate?window=hour')
Data49 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/flow-indicator/stablecoins-ratio?exchange=binance&window=hour')
Data50 = DataTopic(provider=DataProvider.CRYPTOQUANT, url='btc/flow-indicator/exchange-whale-ratio?exchange=binance&window=hour')

# Enable logging to see real-time data
class Engine(BaseEngine):
    """Base engine that initializes BinanceService and processes on_candle_closed and on_datasource_update."""
    def __init__(self, config):
        Logger(log_file="data_retrieval.log", log_level=logging.DEBUG)
        super().__init__(config)

    async def on_candle_closed(self, kline_topic: KlineTopic):
        """Handles closed candle data using `self.data_map[kline_topic]`."""
        candles = self.data_map[kline_topic]
        logging.info(f"Candle Incoming: {kline_topic} and length of {len(candles)}")
        pd.DataFrame(candles).to_csv(candle_path1)

    async def on_datasource_update(self, datasource_topic):
        data = self.data_map[datasource_topic]
        logging.info(f"Data Incoming: {datasource_topic} (len={len(data)})")

        # strip any leading slash, split off params
        path, _, query = datasource_topic.url.lstrip("/").partition("?")

        # 1) symbol is the first segment of the path, upper-cased
        symbol = path.split("/", 1)[0].upper()          # e.g. "BTC"

        # 2) endpoint slug is the last segment of the path
        endpoint = path.rsplit("/", 1)[-1]               # e.g. "coinbase-premium-index"

        # 3) CamelCase the slug
        camel = "".join(part.title() for part in endpoint.split("-"))

        # 4) derive interval (e.g. "hour" → "1h")
        params = parse_qs(query)
        window = params.get("window", ["hour"])[0]
        interval = {"hour": "1h", "day": "1d"}.get(window, window)

        # — new: extract the category segment and CamelCase it —
        #    path looks like "btc/market-data/coinbase-premium-index"
        category_slug = path.split("/", 2)[1]            # e.g. "market-data"
        category_camel = "".join(part.title() for part in category_slug.split("-"))

        # 5) build filename dynamically (now including category)
        filename = f"{symbol}_Cryptoquant-{category_camel}-{camel}-{interval}.csv"
        out_path = BASE_PATH / filename

        # ensure dir exists & write
        out_path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(data).to_csv(out_path, index=False)

        logging.info(f"Saved {datasource_topic.url} → {out_path}")

engine = Engine(
    RuntimeConfig(
        mode= Mode.Backtest,
        kline_topic=[
            KLINE_FUTURES
        ],
        datasource_topic=[
        # Data1,Data2,Data3,Data4,Data5,Data6,Data7,Data8,Data9,Data10,
        # Data11,Data12,Data13,Data14,Data15,Data16,Data17,Data18,Data19,Data20,
        # Data21,Data22,Data23,Data24,Data25,Data26,Data27,Data28,Data29,Data30,
        # Data31,Data32,Data33,Data34,Data35,Data36,Data37,Data38,Data39,Data40,       
        # Data41,Data42,Data43,Data44,Data45,Data46,Data47,Data48,Data49,Data50,
        ],
        data_count=31000,
        exchange="",
        API_Key="" ,  # Replace with your API Key if needed
        API_Secret="", # Replace with your API Secret if needed
        cryptoquant_api_key="iG48lac3kRFcFq0q5WMm0BpnTt1XYMvRB6yz63OP"
    )
)

asyncio.run(engine.start())

