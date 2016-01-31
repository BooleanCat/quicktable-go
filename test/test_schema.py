from quicktable import Table
from unittest import TestCase


class TestSchema(TestCase):
    def test_empty_schema(self):
        """An empty schema is valid."""
        Table([])

    def test_empty_schema_width(self):
        """An empty schema has a width of 0"""
        self.assertEqual(Table([]).width, 0)

    def test_width(self):
        """A table's width is the number of columns."""
        self.assertEqual(Table([('Name', 'string')]).width, 1)
        self.assertEqual(
            Table([('Name', 'string'), ('EyeColour', 'string')]).width,
            2
        )

    def test_validate_schema_pairs_of_items(self):
        """A schema must contain (name, type) column specifications."""
        Table([('Name', 'string')])

    def test_validate_schema_invalid_column(self):
        """A TypeError is raised if a column description doesn't contain 2 items."""
        self.assertRaises(TypeError, Table, [('Name',)])

    def test_validate_column_name(self):
        """A column name must only contain letters or numbers."""
        self.assertRaises(ValueError, Table, [('-', 'string')])

    def test_validate_column_types(self):
        """A column type must be of the valid types."""
        self.assertRaises(TypeError, Table, [('Name', 'Foo')])

    def test_column_names(self):
        """Column names can be retrived from table."""
        table = Table([('Name', 'string'), ('EyeColour', 'string')])
        self.assertEqual(table.column_names, ['Name', 'EyeColour'])

    def test_column_types(self):
        """Column types can be retrieved from table."""
        table = Table([('Name', 'string'), ('EyeColour', 'string')])
        self.assertEqual(table.column_types, ['string', 'string'])

    def test_schema(self):
        """Schema can be retrived from table."""
        table = Table([('Name', 'string'), ('EyeColour', 'string')])
        self.assertEqual(table.schema, [('Name', 'string'), ('EyeColour', 'string')])
