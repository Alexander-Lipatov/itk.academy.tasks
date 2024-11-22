import time
import uuid
from datetime import timedelta
from redis import Redis, exceptions


redis_client = Redis('redis-18750.c92.us-east-1-3.ec2.redns.redis-cloud.com',
                     18750, password='ZhGSoO5yah5xlifyAP5QgN8qYylhxmi2')


def single(max_processing_time: timedelta):
    def decorator(func):
        def wrap(*args, **kwargs):
            lock_key = f"lock:{func.__name__}"
            lock_id = str(uuid.uuid4())
            lock_timeout = max_processing_time.total_seconds()
            try:
                if redis_client.set(lock_key, lock_id, nx=True, ex=int(lock_timeout)):
                    try:
                        func(*args, **kwargs)
                    finally:
                        redis_client.delete(lock_key)
                else:
                    raise exceptions.LockError('Функция запущена')
            except exceptions.LockError as e:
                print(e)

        return wrap
    return decorator

#


@single(max_processing_time=timedelta(seconds=15))
def process_transaction():
    time.sleep(10)


process_transaction()
