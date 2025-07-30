import time
from .consts import *
from functools import wraps


def get_time(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        s = time.perf_counter()
        r = func(*args, **kwargs)
        e = time.perf_counter()

        if PRINT_TIME:
            LOGGER.debug(f"run func: {func.__name__} costs {(e-s):3f}s")

        return r

    return wrap
