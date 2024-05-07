import os
from copy import deepcopy


def delivery_reporter(err, _):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print(f'Message delivery failed: {err}')


CONTAINER_MODE = os.environ.get('CONTAINER_MODE')

CRYPTO_TOPIC = 'crypto_topic'
SECURITY_PROTOCOL = 'PLAINTEXT' if CONTAINER_MODE else 'SASL_PLAINTEXT'
SASL_MECHANISM = 'PLAIN'
KAFKA_CONFIG = {
    'bootstrap.servers': 'broker1:29092' if CONTAINER_MODE else 'localhost:9092',
    'security.protocol': SECURITY_PROTOCOL,
    'sasl.mechanism': SASL_MECHANISM,
    'sasl.username': os.environ.get('TEST_KAFKA_USER') if CONTAINER_MODE else 'user',
    'sasl.password': os.environ.get('TEST_KAFKA_PASS') if CONTAINER_MODE else 'user',
}

PRODUCER_CONFIG = deepcopy(KAFKA_CONFIG)
PRODUCER_CONFIG.update({
    'on_delivery': delivery_reporter,
})

CONSUMER_CONFIG = deepcopy(KAFKA_CONFIG)
CONSUMER_CONFIG.update({
    'session.timeout.ms': 60000,
    'auto.offset.reset': 'earliest',
    'client.id': 'crypto',
    'group.id': 'crypto_consumers',
})

SR_CONFIG = {
    'url': 'http://schemaregistry:8085' if CONTAINER_MODE else 'http://localhost:8085',
}


def delivery_callback(err, msg):
    if err:
        print(f'ERROR: Message failed delivery: {err}')
    else:
        key = msg.key().decode('utf-8')
        value = msg.value().decode('utf-8')
        print(f'Produced event to topic `{msg.topic()}`: key = {key:12} value = {value:12}')
