import ctypes
from contextlib import contextmanager
from quicktable.binding import free_string


def str_from_c(ptr, encoding='UTF-8'):
    return ctypes.cast(ptr, ctypes.c_char_p).value.decode(encoding)


@contextmanager
def free_c_string(ptr):
    try:
        yield str_from_c(ptr)
    finally:
        free_string(ptr)
