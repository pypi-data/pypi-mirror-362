from errno import *
import warnings


def NotCompleted(*args: object):
    from functools import wraps

    def decorator(func):
        @wraps(func)
        def wrapper(*arg, **kwargs):
            raise NotImplementedError(*args)

        return wrapper

    return decorator

def assertTure(condition: bool, message: str = ""):
    if not condition:
        raise AssertionError(message)
    
def assertFalse(condition: bool, message: str = ""):
    if condition:
        raise AssertionError(message)