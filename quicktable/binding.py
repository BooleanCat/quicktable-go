import os
import ctypes
from ctypes import cdll

p_c_char = ctypes.POINTER(ctypes.c_char)
p_c_ulonglong = ctypes.POINTER(ctypes.c_ulonglong)

FILE_PATH = os.path.abspath(os.path.dirname(__file__))
LIB_PATH = os.path.join(FILE_PATH, 'libquicktable.so')

_lib = cdll.LoadLibrary(LIB_PATH)


BINDING_PARAMS = {
    'StringFree': {
        'argtypes': [p_c_char],
    },
    'TableNew': {
        'restype': p_c_ulonglong,
    },
    'TableColumnName': {
        'argtypes': [p_c_ulonglong, ctypes.c_longlong],
        'restype': p_c_char,
    },
    'TableColumnType': {
        'argtypes': [p_c_ulonglong, ctypes.c_longlong],
        'restype': p_c_char,
    },
    'TableNewColumn': {
        'argtypes': [p_c_ulonglong, p_c_char, p_c_char],
    },
    'TableLen': {
        'argtypes': [p_c_ulonglong],
        'restype': ctypes.c_longlong,
    },
    'TableWidth': {
        'argtypes': [p_c_ulonglong],
        'restype': ctypes.c_longlong,
    },
    'TableAppend': {
        'argtypes': [p_c_ulonglong],
    },
    'TableFree': {
        'argtypes': [p_c_ulonglong],
    }
}


for lib_func, params in BINDING_PARAMS.items():
    getattr(_lib, lib_func).argtypes = params.get('argtypes')
    getattr(_lib, lib_func).restype = params.get('restype')


class Binding:
    @staticmethod
    def str_from_c(ptr, encoding='UTF-8'):
        return ctypes.cast(ptr, ctypes.c_char_p).value.decode(encoding)

    @staticmethod
    def free_string(string):
        return _lib.StringFree(string)

    @staticmethod
    def table_new():
        return _lib.TableNew()

    def __init__(self, table):
        self.table = table

    def table_free(self):
        return _lib.TableFree(self.table)

    def init_columns(self, schema):
        for name, kind in schema:
            _lib.TableNewColumn(
                self.table,
                ctypes.create_string_buffer(name.encode()),
                ctypes.create_string_buffer(kind.encode())
            )

    def table_append(self):
        return _lib.TableAppend(self.table)

    def table_len(self):
        return _lib.TableLen(self.table)

    def table_width(self):
        return _lib.TableWidth(self.table)

    def table_column_name(self, i):
        c_string = _lib.TableColumnName(self.table, i)
        py_string = self.str_from_c(c_string)
        self.free_string(c_string)
        return py_string

    def table_column_type(self, i):
        c_string = _lib.TableColumnType(self.table, i)
        py_string = self.str_from_c(c_string)
        self.free_string(c_string)
        return py_string
