# Реализуйте паттерн синглтон тремя способами:

# с помощью метаклассов
# с помощью метода __new__ класса
# через механизм импортов

from module import singleton_instance



# Способ 1: с помощью метаклассов

class SingletonMETA(type):
    _instance:dict = {}

    def __call__(cls, *args, **kwds):
        if cls not in cls._instance:
            cls._instance[cls] = super(SingletonMETA, cls).__call__(*args, **kwds)
        return cls._instance[cls]


class A(metaclass=SingletonMETA):
    pass

# assert A() is A()

# Способ 2: с помощью метода __new__ класса


class SingletonNEW:

    _instance:"SingletonNEW"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls) 

        return cls._instance
    
    def __init__(self, val):
        if not hasattr(self, 'val'):
            self.val = val

# assert Singleton(2) is Singleton(10)


# через механизм импортов


assert singleton_instance == singleton_instance