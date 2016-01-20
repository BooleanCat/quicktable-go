import os
import ctypes
from ctypes import cdll
from contextlib import contextmanager

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
    def py_str(cstring_ptr, encoding='UTF-8'):
        """Create a Python string from a null-terminated C string.

        :param cstring_ptr: pointer to a null-terminated C string
        :param encoding: encoding of the C String

        """
        return ctypes.cast(cstring_ptr, ctypes.c_char_p).value.decode(encoding)

    @staticmethod
    def free_string(cstring_ptr):
        """Free the C string created by the shared library.

        :param cstring_ptr: pointer to a null-terminated C string

        """
        return _lib.StringFree(cstring_ptr)

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
        """The number of rows within self.table."""
        return _lib.TableLen(self.table)

    def table_width(self):
        """The number of columns within self.table."""
        return _lib.TableWidth(self.table)

    @contextmanager
    def free_cstring(self, cstring):
        """Context manager to free a cstring after converting to a Python string.

        :param cstring: a pointer to a cstring

        """
        try:
            yield self.py_str(cstring)
        finally:
            self.free_string(cstring)

    def table_column_name(self, i):
        """Return the name of the column at index i within self.table.

        :param i: integer corresponding to the column's index

        """
        with self.free_cstring(_lib.TableColumnName(self.table, i)) as name:
            return name

    def table_column_type(self, i):
        """Return the name of the column at index i within self.table.

        :param i: integer corresponding to the column's index

        """
        with self.free_cstring(_lib.TableColumnType(self.table, i)) as typ:
            return typ
