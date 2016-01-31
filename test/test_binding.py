import ctypes
from unittest import TestCase
# noinspection PyProtectedMember
from quicktable.binding import _lib, Binding

try:
    from unittest import mock
except ImportError:
    import mock


class TestBinding(TestCase):
    def test_table_new(self):
        assert _lib.TableNew.argtypes is None
        self.assertEqual(_lib.TableNew.restype, ctypes.POINTER(ctypes.c_ulonglong))

    def test_free_string(self):
        self.assertEqual(_lib.StringFree.argtypes, [ctypes.POINTER(ctypes.c_char)])
        assert _lib.StringFree.restype is None

    def test_table_column_name(self):
        self.assertEqual(
            _lib.TableColumnName.argtypes,
            [ctypes.POINTER(ctypes.c_ulonglong), ctypes.c_longlong]
        )
        self.assertEqual(_lib.TableColumnName.restype, ctypes.POINTER(ctypes.c_char))

    def test_table_column_type(self):
        self.assertEqual(
            _lib.TableColumnType.argtypes,
            [ctypes.POINTER(ctypes.c_ulonglong), ctypes.c_longlong]
        )
        self.assertEqual(_lib.TableColumnType.restype, ctypes.POINTER(ctypes.c_char))

    def test_new_column(self):
        self.assertEqual(
            _lib.TableNewColumn.argtypes,
            [ctypes.POINTER(ctypes.c_ulonglong), ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char)]
        )
        assert _lib.TableNewColumn.restype is None

    def test_table_len(self):
        self.assertEqual(_lib.TableLen.argtypes, [ctypes.POINTER(ctypes.c_ulonglong)])
        self.assertEqual(_lib.TableLen.restype, ctypes.c_longlong)

    def test_table_width(self):
        self.assertEqual(_lib.TableWidth.argtypes, [ctypes.POINTER(ctypes.c_ulonglong)])
        self.assertEqual(_lib.TableWidth.restype, ctypes.c_longlong)

    def test_table_column_append_int(self):
        self.assertEqual(_lib.TableColumnAppendInt.argtypes, [
            ctypes.POINTER(ctypes.c_ulonglong),
            ctypes.c_longlong,
            ctypes.c_longlong
        ])
        assert _lib.TableColumnAppendInt.restype is None

    def test_table_column_append_string(self):
        self.assertEqual(_lib.TableColumnAppendString.argtypes, [
            ctypes.POINTER(ctypes.c_ulonglong),
            ctypes.c_longlong,
            ctypes.POINTER(ctypes.c_char),
        ])
        assert _lib.TableColumnAppendString.restype is None

    def test_table_free(self):
        self.assertEqual(_lib.TableFree.argtypes, [ctypes.POINTER(ctypes.c_ulonglong)])
        assert _lib.TableFree.restype is None

    def test_py_str(self):
        c_string = ctypes.create_string_buffer(b'Foo!')
        self.assertEqual(Binding.py_str(c_string), 'Foo!')

    # noinspection PyUnresolvedReferences
    @mock.patch.object(_lib, 'StringFree', mock.Mock())
    def test_table_column_name_freed(self):
        c_string = ctypes.create_string_buffer(b'Foo!')
        with mock.patch.object(_lib, 'TableColumnName', return_value=c_string):
            table = _lib.TableNew()
            binding = Binding(table)

            self.assertEqual(binding.table_column_name(0), 'Foo!')
            _lib.StringFree.assert_called_once_with(c_string)
