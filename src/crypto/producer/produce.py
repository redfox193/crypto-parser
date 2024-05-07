import os

import requests
import time

from confluent_kafka import Producer
from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONSerializer


if os.environ.get('CONTAINER_MODE'):
    from shared.schema import schema_crypto_str, CryptoCurrency
    from shared.kafka_utils import KAFKA_CONFIG, SR_CONFIG, CRYPTO_TOPIC, delivery_callback
else:
    from src.crypto.shared.schema import schema_crypto_str, CryptoCurrency
    from src.crypto.shared.kafka_utils import KAFKA_CONFIG, SR_CONFIG, CRYPTO_TOPIC, delivery_callback


API_CALL_DELAY_SEC = 2


def get_last_crypto_data(symbol: str) -> CryptoCurrency:
    response = requests.get(f'https://api.kucoin.com/api/v1/market/stats?symbol={symbol}-USDT')
    response.raise_for_status()
    crypto_data = response.json()['data']
    return CryptoCurrency(
        time=crypto_data['time'],
        symbol=crypto_data['symbol'],
        buy=crypto_data['buy'],
        sell=crypto_data['sell'],
        change_rate=crypto_data['changeRate'],
        change_price=crypto_data['changePrice'],
        high=crypto_data['high'],
        low=crypto_data['low'],
        vol=crypto_data['vol'],
        vol_value=crypto_data['volValue'],
        last=crypto_data['last'],
        average_price=crypto_data['averagePrice']
    )


def crypto_to_dict(crypto, ctx):
    return {
        "time": crypto.time,
        "symbol": crypto.symbol,
        "buy": crypto.buy,
        "sell": crypto.sell,
        "change_rate": crypto.change_rate,
        "change_price": crypto.change_price,
        "high": crypto.high,
        "low": crypto.low,
        "vol": crypto.vol,
        "vol_value": crypto.vol_value,
        "last": crypto.last,
        "average_price": crypto.average_price,
    }


if __name__ == '__main__':
    schema_registry_client = SchemaRegistryClient(SR_CONFIG)

    json_serializer = JSONSerializer(
        schema_crypto_str,
        schema_registry_client,
        crypto_to_dict,
    )

    producer = Producer(KAFKA_CONFIG)

    crypto_symbol = os.environ.get('SYMBOL')
    if crypto_symbol is None:
        crypto_symbol = "BTC"

    while True:
        crypto = get_last_crypto_data(crypto_symbol)

        producer.produce(
            topic=CRYPTO_TOPIC,
            key=crypto.symbol,
            value=json_serializer(
                crypto,
                SerializationContext(CRYPTO_TOPIC, MessageField.VALUE)
            ),
            on_delivery=delivery_callback
        )

        producer.flush()
        time.sleep(API_CALL_DELAY_SEC)
