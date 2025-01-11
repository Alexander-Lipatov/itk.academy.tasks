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
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False

}

producer = Producer(config)
consumer = Consumer(config)


def process_notification(order):
    order['status'] = 'complete'
    print(f'Order {order['order_id']} complete')


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
            try:

                order = json.loads(msg.value().decode('utf-8'))
                process_notification(order)
                consumer.commit()
            except Exception as e:
                print(e)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
