from quicktable import Table
from unittest import TestCase


class TestTable(TestCase):
    def setUp(self):
        self.table = Table([])

    def test_table_empty(self):
        """A new table will have a length of 0."""
        self.assertEqual(len(self.table), 0)

    def test_append_len(self):
        """Appending to a table should increment it's len."""
        self.table.append()
        self.assertEqual(len(self.table), 1)

        self.table.append()
        self.table.append()
        self.assertEqual(len(self.table), 3)
