import json
from confluent_kafka import Consumer, TopicPartition
from multiprocessing import Process

KAFKA_TOPIC = 'web_log'
NUM_PARTITIONS = 10

consumer_config = {
    'bootstrap.servers': 'localhost:64250',
    'group.id': 'web_logs_consumer',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
}

def list_partitions():
    consumer = Consumer(consumer_config)
    topic_metadata = consumer.list_topics(timeout=10)
    if KAFKA_TOPIC in topic_metadata.topics:
        partitions = topic_metadata.topics[KAFKA_TOPIC].partitions
        for partition_id, partition_metadata in partitions.items():
            print(f"Partition ID: {partition_id}, Leader: {partition_metadata.leader}, Replicas: {partition_metadata.replicas}, In-Sync Replicas: {partition_metadata.isrs}")
    else:
        print(f"Topic {KAFKA_TOPIC} does not exist")
    consumer.close()


def event_consumer(partition: str):
    consumer = Consumer(consumer_config)
    consumer.assign([TopicPartition(KAFKA_TOPIC, int(partition))])
    try:
        while True:

            msg = consumer.poll(1)
            if msg is None:
                continue
            if msg.error():
                print(f"Error: {msg.error()}")
                continue
            
            event = json.loads(msg.value().decode("utf-8"))
            
            print(f"Partition {partition} received event: {event}")
            consumer.commit()
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == '__main__':
    processes = []
    for i in range(NUM_PARTITIONS):
        print(i)
        p = Process(target=event_consumer, args=(str(i),))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()