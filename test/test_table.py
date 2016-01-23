from quicktable import Table
from unittest import TestCase


class TestTable(TestCase):
    def setUp(self):
        self.table = Table([('Name', 'string'), ('Age', 'int')])

    def test_width_no_columns(self):
        self.assertEqual(Table([]).width, 0)

    def test_width(self):
        self.assertEqual(self.table.width, 2)

    def test_table_empty(self):
        """A new table will have a length of 0."""
        self.assertEqual(len(self.table), 0)

    def test_append(self):
        """I can append a row to a table."""
        self.table.append(['Tom', 26])

    def test_append_len(self):
        """Appending to a table should increment it's len."""
        self.table.append(['Tom', 26])
        self.assertEqual(len(self.table), 1)

        self.table.append(['Chantelle', 24])
        self.table.append(['Deccy', 8])
        self.assertEqual(len(self.table), 3)

    def test_slice_single_first(self):
        """Slicing a table returns the row at 0 index."""
        self.table.append(['Tom', 26])
        self.assertEqual(self.table[0], ['Tom', 26])

    def test_slice_second(self):
        """Slicing a table returns the row at that index."""
        self.table.append(['Tom', 26])
        self.table.append(['Chantelle', 24])
        self.assertEqual(self.table[1], ['Chantelle', 24])

    def test_slice_last(self):
        """Slicing a table with -1 returns the last row."""
        self.table.append(['Tom', 26])
        self.table.append(['Chantelle', 24])
        self.assertEqual(self.table[-1], ['Chantelle', 24])

    def test_slice_second_last(self):
        """Slicing a table with a negative number returns the row at that negative index from the last."""
        self.table.append(['Tom', 26])
        self.table.append(['Chantelle', 24])
        self.assertEqual(self.table[-2], ['Tom', 26])

    def test_slice_index_error(self):
        """Slicing a table to a row that doesn't exist raises an IndexError."""
        self.assertRaises(IndexError, lambda: self.table[0])

    def test_slice_negative_index_error(self):
        """Slicing a table with a negative index to a row that doesn't exist raises an IndexError."""
        self.assertRaises(IndexError, lambda: self.table[-1])
