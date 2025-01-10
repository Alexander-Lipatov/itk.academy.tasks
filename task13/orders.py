import uuid
import json
from confluent_kafka import Producer


KAFKA_TOPICS = {
    "new_orders": "new_orders",
    "payed_orders": "payed_orders",
    "sent_orders": "sent_orders",
}

config = {
    'bootstrap.servers': "localhost:64250",
}

producer = Producer(config)

def create_order():
    order = {
        'order_id': str(uuid.uuid4()),
        'status': 'created',
    }
    producer.produce(KAFKA_TOPICS['new_orders'], value=json.dumps(order))
    producer.flush()

create_order()