import random
import time
from datetime import timedelta

from redis import Redis
import uuid

class RateLimitExceed(Exception):
    pass


class RateLimiter:

    def __init__(self, key='rate_limiter', limit: int=5, window: int=3) -> None:

        self.redis = Redis('redis-18750.c92.us-east-1-3.ec2.redns.redis-cloud.com',
                     18750, password='ZhGSoO5yah5xlifyAP5QgN8qYylhxmi2')
        
        self.key= key
        self.limit = limit
        self.window = window

    def test(self) -> bool:
        """
        Проверяет, достигнут ли лимит запросов за текущий временной интервал.

        :return: True, если лимит запросов не превышен; False, если превышен.
        """
        
        # Создаем ключ со значением 0
        # и время жизни (ex=self.window) в секундах.
        self.redis.set(self.key, 0, nx=True, ex=self.window)

        # Увеличиваем значение ключа на 1.
        current_count = self.redis.incr(self.key)
        

        return current_count <= self.limit


def make_api_request(rate_limiter: RateLimiter):
    if not rate_limiter.test():
        raise RateLimitExceed
    else:
        # какая-то бизнес логика
        pass


if __name__ == '__main__':
    rate_limiter = RateLimiter()

    for _ in range(50):
        
        time.sleep(random.randint(1, 3))

        try:
            make_api_request(rate_limiter)
        except RateLimitExceed:
            print("Rate limit exceed!")
        else:
            print("All good")





