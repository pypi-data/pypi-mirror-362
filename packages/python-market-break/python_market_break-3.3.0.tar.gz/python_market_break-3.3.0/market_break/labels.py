# labels

__all__ = [
    "OHLCV_COLUMNS",
    "OHLC_COLUMNS",
    "ORDERBOOK_COLUMNS",
    "OPEN",
    "CLOSE",
    "HIGH",
    "LOW",
    "VOLUME",
    "DATETIME",
    "BID",
    "ASK",
    "BID_VOLUME",
    "ASK_VOLUME",
    "EXCHANGE",
    "SELL",
    "SIDE",
    "SYMBOL",
    "BUY",
    "TIMESTAMP",
    "RECEIVED_DATETIME",
    "ENTRY",
    "EXIT",
    "TYPE",
    "SHORT",
    "LONG",
    "RETURNS",
]

DATETIME = 'datetime'
RECEIVED_DATETIME = 'received_datetime'
TIMESTAMP = 'timestamp'

OPEN = "open"
CLOSE = "close"
HIGH = "high"
LOW = "low"
VOLUME = "volume"

BID = "bid"
ASK = "ask"
BID_VOLUME = "bid_volume"
ASK_VOLUME = "ask_volume"

SIDE = "side"
BUY = "buy"
SELL = "sell"

EXCHANGE = "exchange"
SYMBOL = "symbol"

ENTRY = 'entry'
EXIT = 'exit'
TYPE = 'type'
LONG = 'long'
SHORT = 'short'
RETURNS = 'returns'

OHLC_COLUMNS = (OPEN, HIGH, LOW, CLOSE)
OHLCV_COLUMNS = (*OHLC_COLUMNS, VOLUME)
ORDERBOOK_COLUMNS = (BID, ASK, BID_VOLUME, ASK_VOLUME)