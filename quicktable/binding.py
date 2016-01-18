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


# TableColumnName
_lib.TableColumnName.argtypes = [LP_c_ulonglong, ctypes.c_longlong]
_lib.TableColumnName.restype = LP_c_char
column_name = with_string_free(_lib.TableColumnName)


# TableColumnType
_lib.TableColumnType.argtypes = [LP_c_ulonglong, ctypes.c_longlong]
_lib.TableColumnType.restype = LP_c_char
column_type = with_string_free(_lib.TableColumnType)


# TableCreateColumns
_lib.TableNewColumn.argtypes = [LP_c_ulonglong, LP_c_char, LP_c_char]
_lib.TableNewColumn.restype = None


def new_columns(table, schema):
    for name, kind in schema:
        _lib.TableNewColumn(
            table,
            ctypes.create_string_buffer(name.encode()),
            ctypes.create_string_buffer(kind.encode())
        )


# TableLen
_lib.TableLen.argtypes = [LP_c_ulonglong]
_lib.TableLen.restype = ctypes.c_longlong
table_len = _lib.TableLen


# TableWidth
_lib.TableWidth.argtypes = [LP_c_ulonglong]
_lib.TableWidth.restype = ctypes.c_longlong
table_width = _lib.TableWidth


# TableAppend
_lib.TableAppend.argtypes = [LP_c_ulonglong]
_lib.TableAppend.restype = None
table_append = _lib.TableAppend


# TableFree
_lib.TableFree.argtypes = [LP_c_ulonglong]
_lib.TableFree.restype = None
table_free = _lib.TableFree
