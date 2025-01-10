import json
from confluent_kafka import Consumer, Producer

KAFKA_TOPICS = {
    "new_orders": "new_orders",
    "payed_orders": "payed_orders",
    "sent_orders": "sent_orders",
}


config = {
    'bootstrap.servers': 'localhost:64250',
    'group.id':          'notifications_service',
    'auto.offset.reset': 'earliest'
}

producer = Producer(config)
consumer = Consumer(config)


def process_shipping(order):
    order['status'] = 'shipping'
    producer.produce(
        topic=KAFKA_TOPICS['sent_orders'], value=json.dumps(order))
    producer.flush()


if __name__ == '__main__':

    consumer.subscribe([KAFKA_TOPICS["sent_orders"]])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
                continue

            order = json.loads(msg.value().decode('utf-8'))
            order['status'] = 'complete'
            print('Order complete')

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
