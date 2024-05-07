# crypto-parser
An application, which collects crypto data via external API.
Producers sends data about cryptocurrency to [Kafka](https://kafka.apache.org/),
 consumers read it and save into database, from where data can be used for
analyzing or other things.

By using producers it's easy to scale our service to collect data
about more currencies. And you can add more consumers to proccess
data faster.

## Usage

#### Run
Before running, create ```.env``` file as ```.env.example```.

Tu run application use:
```shell
docker-compose up -d
```

Main endpoints:

http://localhost:9021/ - kafka control center where you can see
producers send messages into kafka broker.

http://localhost:5432/ - postgres database where consumers
save data.

If you want to see consumer's log:
```shell
docker-compose exec -ti <consumer service name> bash
```
Inside container:
```shell
cat consumer.log
```

#### Stop

```shell
docker-compose down
```

If you want to delete database volume:
```shell
docker volume rm crypto_pgdb_data
```

## Scaling

To add more producers and consumers, before starting go to ```docker-compose.yml```
and just add more services:

```yaml
# docker-compose.yml
services:
...
# producers
...
  <producer service name>:
    networks:
      - kafka_network
    extends:
      file: docker/producer/docker-compose.producer.yml
      service: producer
    environment:
      SYMBOL: <YOUR VALID CRYPTO CURRENCY SYMBOL>
    depends_on:
      broker1:
        condition: service_healthy
...
# consumers
...
  <consumer service name>:
    networks:
      - kafka_network
    extends:
      file: docker/consumer/docker-compose.consumer.yml
      service: consumer
    depends_on:
      broker1:
        condition: service_healthy
      initdb:
        condition: service_completed_successfully
```
