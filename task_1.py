# Реализуйте lru_cache декоратор.

# Требования:

#   Декоратор должен кешировать результаты вызовов функции на 
# основе её аргументов.
#   Если функция вызывается с теми же аргументами, что и ранее, 
# возвращайте результат из кеша вместо повторного выполнения функции.
#   Декоратор должно быть возможно использовать двумя способами: 
# с указанием максимального кол-ва элементов и без.

import unittest.mock


def lru_cache(func=None, maxsize=None):
    def decorator(func):
        cache = dict()

        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            # Если ключ уже есть в кэше, перемещаем его в конец списка order
            if key in cache:
                return cache[key]
            
            # Вычисляем результат и добавляем его в кэш
            result = func(*args, **kwargs)
            cache[key] = result

            # Если cache переполнен, то удаляем самый старый элемент 
            if maxsize is not None and len(cache) > maxsize:
                old_key = list(cache.keys())[0]
                del cache[old_key]

            return result

        return wrapper

    if func:
        return decorator(func)

    return decorator


@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == '__main__':

    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4




n = 5