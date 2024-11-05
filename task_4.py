
import datetime



class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['create_at'] = datetime.datetime.now()
        return super().__new__(cls, name, bases, attrs)
    

class A(metaclass=MyMeta):
    pass

print(A().create_at)
