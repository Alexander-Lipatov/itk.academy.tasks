import json
from confluent_kafka import Consumer, Producer

KAFKA_TOPICS = {
    "new_orders": "new_orders",
    "payed_orders": "payed_orders",
    "sent_orders": "sent_orders",
}


config = {
    'bootstrap.servers': 'localhost:64250',
    'group.id':          'payment_service',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
}

consumer = Consumer(config)
producer = Producer(config)


def process_payment(order):
    order['status'] = 'payed'
    producer.produce(
        topic=KAFKA_TOPICS['payed_orders'], value=json.dumps(order))
    producer.flush()


if __name__ == '__main__':

    consumer.subscribe([KAFKA_TOPICS["new_orders"]])

    try:
        while True:
            msg = consumer.poll(1.0)
            msg_text = None if msg is None else msg.value().decode('utf-8')
            print(msg_text)
            if msg is None:
                continue
            elif msg.error():
                print("ERROR: %s".format(msg.error()))
                continue
            try:
                order = json.loads(msg.value().decode('utf-8'))
                process_payment(order)
                consumer.commit()
            except Exception as e:
                print(e)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
