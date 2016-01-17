import os
import ctypes
from ctypes import cdll
from functools import wraps

LP_c_char = ctypes.POINTER(ctypes.c_char)
LP_c_ulonglong = ctypes.POINTER(ctypes.c_ulonglong)

FILE_PATH = os.path.abspath(os.path.dirname(__file__))
LIB_PATH = os.path.join(FILE_PATH, 'libquicktable.so')

_lib = cdll.LoadLibrary(LIB_PATH)


# StringFree
_lib.StringFree.argtypes = [LP_c_char]
_lib.StringFree.restype = None
free_string = _lib.StringFree


def str_from_c(ptr, encoding='UTF-8'):
    return ctypes.cast(ptr, ctypes.c_char_p).value.decode(encoding)


def with_string_free(get_func):
    @wraps(get_func)
    def _wrapper(*args, **kwargs):
        ptr = get_func(*args, **kwargs)
        string = str_from_c(ptr)
        free_string(ptr)
        return string

    return _wrapper


# TableNew
_lib.TableNew.argtypes = None
_lib.TableNew.restype = LP_c_ulonglong
table_new = _lib.TableNew


# TableName
_lib.TableName.argtypes = [LP_c_ulonglong]
_lib.TableName.restype = LP_c_char
table_name = with_string_free(_lib.TableName)


# TableFree
_lib.TableFree.argtypes = [LP_c_ulonglong]
_lib.TableFree.restype = None
table_free = _lib.TableFree
