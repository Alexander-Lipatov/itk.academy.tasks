import random
import json
from confluent_kafka import Producer
from confluent_kafka.admin import NewPartitions, NewTopic, AdminClient

KAFKA_TOPIC = 'web_log'
NUM_PARTITIONS = 3


def create_topic():
    admin_client = AdminClient({'bootstrap.servers': 'localhost:64250'})
    topic_metadata = admin_client.list_topics(timeout=10)
    
    if KAFKA_TOPIC not in topic_metadata.topics:
        topic = NewTopic(KAFKA_TOPIC, num_partitions=NUM_PARTITIONS)
        admin_client.create_topics([topic])
        print(f"Topic {KAFKA_TOPIC}. Partitions{NUM_PARTITIONS}")
    else:
        print(f"Topic {KAFKA_TOPIC} exists")

def event_produce():
    producer = Producer({'bootstrap.servers': 'localhost:64250'})
    events = [{
        'user_id': random.randint(100000, 1000000),
        'event_type': random.choice(['click', 'view', 'purchase']),
    } for _ in range(1000)]
    for event in events:
        key = event['user_id'] % NUM_PARTITIONS
        print(key, event['user_id'], event['event_type'])
        producer.produce(KAFKA_TOPIC, partition=key, value=json.dumps(event))
    producer.flush()


if __name__ == '__main__':
    create_topic()
    event_produce()
