import time
from xecution.common.enums import Symbol
from xecution.models.position import Position, PositionData

class Standardize:
    @staticmethod
    def parse_binance_position(raw_data) -> Position:
        """
        Parse Binance Futures position data in Hedge Mode.

        `raw_data` is expected to be a list of entries, each containing:
          - symbol: e.g. "BTCUSDT"
          - positionSide: "LONG" or "SHORT"
          - positionAmt: string number (positive for LONG, negative for SHORT)
          - entryPrice: string number
          - updateTime: integer timestamp

        This method aggregates all LONG and SHORT entries separately to compute
        total quantity and weighted average entry price for each side.
        """
        total_long_qty = 0.0
        total_long_value = 0.0
        total_short_qty = 0.0
        total_short_value = 0.0
        updated_time = 0
        symbol_str = None

        for item in raw_data:
            if not symbol_str:
                symbol_str = item.get("symbol")
            ts = int(item.get("updateTime", time.time() * 1000))
            updated_time = max(updated_time, ts)

            qty = float(item.get("positionAmt", "0"))
            entry = float(item.get("entryPrice", "0"))

            if qty > 0:
                total_long_qty += qty
                total_long_value += entry * qty
            elif qty < 0:
                # positionAmt is negative for SHORT, take absolute value
                total_short_qty += abs(qty)
                total_short_value += entry * abs(qty)

        if total_long_qty > 0:
            avg_long = total_long_value / total_long_qty
            long_data = PositionData(quantity=total_long_qty, avg_price=avg_long)
        else:
            long_data = PositionData(quantity=0.0, avg_price=0.0)

        if total_short_qty > 0:
            avg_short = total_short_value / total_short_qty
            short_data = PositionData(quantity=total_short_qty, avg_price=avg_short)
        else:
            short_data = PositionData(quantity=0.0, avg_price=0.0)

        if symbol_str not in Symbol._value2member_map_:
            raise ValueError(f"Unknown symbol from Binance data: {symbol_str}")

        return Position(
            symbol=Symbol(symbol_str),
            long=long_data,
            short=short_data,
            updated_time=updated_time or int(time.time() * 1000)
        )

    @staticmethod
    def parse_bybit_position(raw_data) -> Position:
        """
        Parse Bybit position data.

        `raw_data` is expected to be a list of entries, each containing:
          - symbol: e.g. "BTCUSDT"
          - side: "Buy" for long, "Sell" for short
          - size: string number representing quantity
          - avgEntryPrice: string number
          - updateTime: optional timestamp

        Aggregates entries by side to compute total quantity and weighted average price.
        """
        total_long_qty = 0.0
        total_long_value = 0.0
        total_short_qty = 0.0
        total_short_value = 0.0
        updated_time = 0
        symbol_str = None

        for item in raw_data:
            if not symbol_str:
                symbol_str = item.get("symbol")
            if "updateTime" in item:
                ts = int(item.get("updateTime"))
                updated_time = max(updated_time, ts)
            side = item.get("side", "").upper()
            qty = float(item.get("size", "0"))
            entry = float(item.get("avgEntryPrice", "0"))
            if side == "BUY":
                total_long_qty += qty
                total_long_value += entry * qty
            elif side == "SELL":
                total_short_qty += qty
                total_short_value += entry * qty

        if total_long_qty > 0:
            avg_long = total_long_value / total_long_qty
            long_data = PositionData(quantity=total_long_qty, avg_price=avg_long)
        else:
            long_data = PositionData(quantity=0.0, avg_price=0.0)

        if total_short_qty > 0:
            avg_short = total_short_value / total_short_qty
            short_data = PositionData(quantity=total_short_qty, avg_price=avg_short)
        else:
            short_data = PositionData(quantity=0.0, avg_price=0.0)

        if symbol_str not in Symbol._value2member_map_:
            raise ValueError(f"Unknown symbol from Bybit data: {symbol_str}")

        return Position(
            symbol=Symbol(symbol_str),
            long=long_data,
            short=short_data,
            updated_time=updated_time or int(time.time() * 1000)
        )

    @staticmethod
    def parse_okx_position(raw_data) -> Position:
        """
        Parse OKX position data.

        `raw_data` is expected to be a dict containing:
          - instId: e.g. "BTC-USDT" (converted to "BTCUSDT")
          - longQty: string number for long quantity
          - longAvgPx: string number for long average price
          - shortQty: string number for short quantity
          - shortAvgPx: string number for short average price
          - ts: timestamp (string or numeric)

        Returns a Position with separate long and short data.
        """
        inst_id = raw_data.get("instId", "")
        symbol_str = inst_id.replace("-", "")
        updated_time = int(raw_data.get("ts", time.time() * 1000))
        long_qty = float(raw_data.get("longQty", "0"))
        long_avg = float(raw_data.get("longAvgPx", "0"))
        short_qty = float(raw_data.get("shortQty", "0"))
        short_avg = float(raw_data.get("shortAvgPx", "0"))

        if symbol_str not in Symbol._value2member_map_:
            raise ValueError(f"Unknown symbol from OKX data: {symbol_str}")

        return Position(
            symbol=Symbol(symbol_str),
            long=PositionData(quantity=long_qty, avg_price=long_avg),
            short=PositionData(quantity=short_qty, avg_price=short_avg),
            updated_time=updated_time
        )
