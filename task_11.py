

from redis import Redis


class RedisQueue:

    def __init__(self, name):
        self.name = name
        self.redis = Redis('redis-18750.c92.us-east-1-3.ec2.redns.redis-cloud.com',
                     18750, password='ZhGSoO5yah5xlifyAP5QgN8qYylhxmi2')

    def publish(self, msg: dict):
        self.redis.lpush(self.name, str(msg))
        
    def consume(self) -> dict:
        msg = self.redis.rpop(self.name)
        if msg:
            return eval(msg)
        raise Exception('Очередь пуста')
        


if __name__ == '__main__':
    q = RedisQueue('simple')

    q.publish({'a': 1})
    q.publish({'b': 2})
    q.publish({'c': 3})

    assert q.consume() == {'a': 1}
    assert q.consume() == {'b': 2}
    assert q.consume() == {'c': 3}






# publish
# consume
