class CryptoCurrency(object):
    """represents statistics of the specified ticker in the last 24 hours"""
    def __init__(self, time, symbol, buy, sell, change_rate, change_price, high, low, vol, vol_value, last, average_price):
        self.time = time  # timestamp
        self.symbol = symbol  # Symbol
        self.buy = buy  # Best bid price
        self.sell = sell  # Best ask price
        self.change_rate = change_rate  # 24h change rate
        self.change_price = change_price  # 24h change price
        self.high = high  # Highest price in 24h
        self.low = low  # Lowest price in 24h
        self.vol = vol  # 24h volume, executed based on base currency
        self.vol_value = vol_value  # 24h traded amount
        self.last = last  # Last traded price
        self.average_price = average_price  # Average trading price in the last 24 hours


schema_crypto_str = """{
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "CryptoCurrency",
    "description": "Cryptocurrency statistics for the last 24 hours",
    "type": "object",
    "properties": {
        "time": {
            "description": "Time of statistics in ms since epoch",
            "type": "number"
        },
        "symbol": {
            "description": "Symbol of the cryptocurrency",
            "type": "string"
        },
        "buy": {
            "description": "Best bid price",
            "type": "string"
        },
        "sell": {
            "description": "Best ask price",
            "type": "string"
        },
        "change_rate": {
            "description": "24-hour change rate",
            "type": "string"
        },
        "change_price": {
            "description": "24-hour change price",
            "type": "string"
        },
        "high": {
            "description": "Highest price in 24 hours",
            "type": "string"
        },
        "low": {
            "description": "Lowest price in 24 hours",
            "type": "string"
        },
        "vol": {
            "description": "24-hour volume, executed based on base currency",
            "type": "string"
        },
        "vol_value": {
            "description": "24-hour traded amount",
            "type": "string"
        },
        "last": {
            "description": "Last traded price",
            "type": "string"
        },
        "average_price": {
            "description": "Average trading price in the last 24 hours",
            "type": "string"
        }
    }
}"""