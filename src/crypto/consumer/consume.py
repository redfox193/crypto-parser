import os
import logging

from datetime import datetime

from confluent_kafka.serialization import SerializationContext, MessageField
from confluent_kafka.schema_registry.json_schema import JSONDeserializer
from confluent_kafka import Consumer, OFFSET_BEGINNING

from database.database import SessionLocal
from database import models


if os.environ.get('CONTAINER_MODE'):
    from shared.schema import CryptoCurrency, schema_crypto_str
    from shared.kafka_utils import CONSUMER_CONFIG, CRYPTO_TOPIC
else:
    from src.crypto.shared.schema import CryptoCurrency, schema_crypto_str
    from src.crypto.shared.kafka_utils import CONSUMER_CONFIG, CRYPTO_TOPIC


def dict_to_crypto(dict_: dict, ctx):
    return CryptoCurrency(
        dict_['time'],
        dict_['symbol'],
        dict_['buy'],
        dict_['sell'],
        dict_['change_rate'],
        dict_['change_price'],
        dict_['high'],
        dict_['low'],
        dict_['vol'],
        dict_['vol_value'],
        dict_['last'],
        dict_['average_price'],
    )


def save_crypto_info_to_db(crypto: CryptoCurrency):
    with SessionLocal() as session:
        existing_symbol = session.query(models.Symbol).filter_by(name=crypto.symbol).first()
        if not existing_symbol:
            session.add(models.Symbol(name=crypto.symbol))

        session.add(
            models.Statistic(
                symbol_name=crypto.symbol,
                time=datetime.fromtimestamp(float(crypto.time) / 1000),
                buy=crypto.buy,
                sell=crypto.sell,
                change_rate=crypto.change_rate,
                change_price=crypto.change_price,
                high=crypto.high,
                low=crypto.low,
                vol=crypto.vol,
                vol_value=crypto.vol_value,
                last=crypto.last,
                average_price=crypto.average_price
            )
        )
        session.commit()


def reset_offset(consumer_: Consumer, partitions, reset: bool = False):
    if reset:
        for p in partitions:
            p.offset = OFFSET_BEGINNING
        consumer_.assign(partitions)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="consumer.log", filemode="w")

    logging.info('json_deserializer')
    json_deserializer = JSONDeserializer(schema_crypto_str, from_dict=dict_to_crypto)

    logging.info('create consumer')
    consumer = Consumer(CONSUMER_CONFIG)

    logging.info('subscribe')
    consumer.subscribe([CRYPTO_TOPIC], on_assign=reset_offset)

    logging.info('start')
    try:
        while True:
            event = consumer.poll(1.0)
            if event is None:
                logging.info('Waiting...')
                continue
            elif event.error():
                logging.info(f'ERROR: {event.error()}')
                continue
            crypto = json_deserializer(
                event.value(),
                SerializationContext(CRYPTO_TOPIC, MessageField.VALUE)
            )
            if crypto is not None:
                timestamp = float(crypto.time) / 1000
                datetime_obj = datetime.fromtimestamp(timestamp)
                logging.info(f'Цена {crypto.symbol} на {datetime_obj}: {crypto.last}$.')

                save_crypto_info_to_db(crypto)

    except KeyboardInterrupt:
        ...
    finally:
        consumer.close()
