import os
import ctypes
from ctypes import cdll
from contextlib import contextmanager

p_c_char = ctypes.POINTER(ctypes.c_char)
p_c_ulonglong = ctypes.POINTER(ctypes.c_ulonglong)

FILE_PATH = os.path.abspath(os.path.dirname(__file__))
LIB_PATH = os.path.join(FILE_PATH, 'libquicktable.so')

_lib = cdll.LoadLibrary(LIB_PATH)


_BINDING_PARAMS = {
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
    'TableColumnAppendInt': {
        'argtypes': [p_c_ulonglong, ctypes.c_longlong, ctypes.c_longlong],
    },
    'TableColumnAppendString': {
        'argtypes': [p_c_ulonglong, ctypes.c_longlong, p_c_char]
    },
    'TableColumnGetInt': {
        'argtypes': [p_c_ulonglong, ctypes.c_longlong, ctypes.c_longlong],
        'restype': ctypes.c_longlong,
    },
    'TableColumnGetString': {
        'argtypes': [p_c_ulonglong, ctypes.c_longlong, ctypes.c_longlong],
        'restype': p_c_char,
    },
    'TableFree': {
        'argtypes': [p_c_ulonglong],
    },
    'TableRowInc': {
        'argtypes': [p_c_ulonglong],
    },
}


for lib_func, params in _BINDING_PARAMS.items():
    getattr(_lib, lib_func).argtypes = params.get('argtypes')
    getattr(_lib, lib_func).restype = params.get('restype')


class Binding:
    """A Python wrapper around the quicktable shared library"""

    @staticmethod
    def py_str(cstring_ptr, encoding='UTF-8'):
        """Create a Python string from a null-terminated C string.

        :param cstring_ptr: pointer to a null-terminated C string
        :param encoding: encoding of the C String, defaults to UTF-8
        :returns: a Python string constructed by cstring_ptr

        """
        return ctypes.cast(cstring_ptr, ctypes.c_char_p).value.decode(encoding)

    @staticmethod
    def free_string(cstring_ptr):
        """Free the C string created by the shared library.

        :param cstring_ptr: pointer to a null-terminated C string

        """
        return _lib.StringFree(cstring_ptr)

    @contextmanager
    def free_cstring(self, cstring):
        """Context manager to free a cstring after converting to a Python string.

        :param cstring: a pointer to a cstring

        """
        try:
            yield self.py_str(cstring)
        finally:
            self.free_string(cstring)

    @staticmethod
    def table_new():
        """Create a new instance of a table within the shared library.

        :returns: An unsigned 64-bit integer pointer to the table.

        """
        return _lib.TableNew()

    def __init__(self, table):
        self.table = table

    def table_free(self):
        """Free the table within the shared library.

        Use of this table after calling this function will cause crashes.

        """
        return _lib.TableFree(self.table)

    def init_columns(self, schema):
        """Instantiate self.table with columns according to this schema.

        :param schema: a list of (Name, Type) column descriptions.

        """
        for name, kind in schema:
            _lib.TableNewColumn(
                self.table,
                ctypes.create_string_buffer(name.encode()),
                ctypes.create_string_buffer(kind.encode())
            )

    def table_append(self, row):
        for i, element in enumerate(row):
            if isinstance(element, int):
                _lib.TableColumnAppendInt(self.table, i, element)
            elif isinstance(element, str):
                _lib.TableColumnAppendString(self.table, i, ctypes.create_string_buffer(element.encode()))

        _lib.TableRowInc(self.table)

    def table_row(self, i):
        row = []
        for column_index in range(self.table_width()):
            column_type = self.table_column_type(column_index)

            if column_type == 'int':
                row.append(_lib.TableColumnGetInt(self.table, column_index, i))
            elif column_type == 'string':
                with self.free_cstring(_lib.TableColumnGetString(self.table, column_index, i)) as element:
                    row.append(element)
        return row

    def table_len(self):
        """The number of rows within self.table."""
        return _lib.TableLen(self.table)

    def table_width(self):
        """The number of columns within self.table."""
        return _lib.TableWidth(self.table)

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
