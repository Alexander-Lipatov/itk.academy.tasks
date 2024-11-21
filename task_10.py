import time
import uuid
from datetime import timedelta
from redis import Redis


redis_client = Redis('redis-18750.c92.us-east-1-3.ec2.redns.redis-cloud.com', 18750, password='ZhGSoO5yah5xlifyAP5QgN8qYylhxmi2')




def single(max_processing_time:timedelta):
    def decorator(func):
        def wrap(*args, **kwargs):
            lock_key = f"lock:{func.__name__}"
            lock_id = str(uuid.uuid4())
            lock_timeout = max_processing_time.total_seconds()

            if redis_client.set(lock_key, lock_id, nx=True, ex=int(lock_timeout)):
                try:
                    func(*args, **kwargs)
                finally:
                    if redis_client.get(lock_key) == lock_key:
                        redis_client.delete(lock_key)
            else:
                cur_lock_id = redis_client.get(lock_key)
                if cur_lock_id and redis_client.ttl(lock_key)<=0:
                    redis_client.set(lock_key,lock_id, ex=int(lock_timeout))
                    try:
                        func(*args, **kwargs)
                    finally:
                        if redis_client.get(lock_key) == lock_id:
                            redis_client.delete(lock_key)
                else:
                    raise Exception("Another instance is processing the function.")
        return wrap
    return decorator

@single(max_processing_time=timedelta(seconds=15))
def process_transaction():
    time.sleep(2)


process_transaction()