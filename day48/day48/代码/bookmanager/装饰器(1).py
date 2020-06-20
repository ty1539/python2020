import time
from functools import wraps


def timer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        """
        inner
        :param args:
        :param kwargs:
        :return:
        """
        start = time.time()
        ret = func(*args, **kwargs)
        print('执行的时间是：{}'.format(time.time() - start))
        return ret

    return inner


@timer
def func():
    """
    func的相关信息
    :return:
    """
    time.sleep(0.5)
    print('func')

@timer
def func1():
    """
    func1的相关信息
    :return:
    """
    time.sleep(0.5)
    print('func')

func()  # inner
print(func.__name__)
print(func1.__name__)
print(func.__doc__)
print(func1.__doc__)
