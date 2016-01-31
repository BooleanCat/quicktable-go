import re
from quicktable.binding import Binding


class Table:
    VALID_COLUMN_NAME = re.compile(r'^[A-Za-z\d]+$')
    VALID_COLUMN_TYPES = {'string': str, 'int': int}

    def __init__(self, schema):
        schema = self.validate_schema(schema)
        self._table_ptr = Binding.table_new()
        self.binding = Binding(self._table_ptr)
        self._init_columns(schema)
        self._len_changed = True

    @classmethod
    def validate_schema(cls, schema):
        for column in schema:
            if len(column) != 2:
                raise TypeError('Expected schema format is [(name, type), (name, type) ...]')

            if not cls.VALID_COLUMN_NAME.match(column[0]):
                raise ValueError('Invalid column name %s: it must only contain letters and numbers.' % column[0])

            if column[1] not in cls.VALID_COLUMN_TYPES:
                raise TypeError('Invalid column type: %s: it must be one of %s' % (column[1], cls.VALID_COLUMN_TYPES))

        return schema

    def _init_columns(self, schema):
        self.binding.init_columns(schema)

    @property
    def width(self):
        return self.binding.table_width()

    @property
    def column_names(self):
        """An list of column names in the schema."""
        return [self.binding.table_column_name(i) for i in range(self.width)]

    @property
    def column_types(self):
        """An list of column types in the schema."""
        return [self.binding.table_column_type(i) for i in range(self.width)]

    @property
    def schema(self):
        """Return the schema of the table."""
        return list(zip(self.column_names, self.column_types))

    def append(self, row):
        for (name, typ), element in zip(self.schema, row):
            if not isinstance(element, self.VALID_COLUMN_TYPES[typ]):
                raise TypeError('Column %s expects %s, got %s.' % (
                    name,
                    self.VALID_COLUMN_TYPES[typ],
                    type(element)
                ))

        self.binding.table_append(row)
        self._len_changed = True

    def extend(self, rows):
        for row in rows:
            self.append(row)

    def __len__(self):
        if self._len_changed:
            self._len = self.binding.table_len()
            self._len_changed = False
        return self._len

    def __getitem__(self, row_index):
        if row_index < 0:
            row_index = abs(row_index + len(self))

        if row_index > len(self) - 1:
            raise IndexError('Table index out of range')

        return self.binding.table_row(row_index)

    def __del__(self):
        """Free the underlying table.

        In case Table instatiation failing, then there is nothing to free.

        """
        try:
            self.binding.table_free()
        except AttributeError:
            pass
