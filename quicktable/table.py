import re
from quicktable import binding


class Table:
    VALID_COLUMN_NAME = re.compile(r'^[A-Za-z\d]+$')
    VALID_COLUMN_TYPES = ['string']

    def __init__(self, schema):
        schema = self.validate_schema(schema)
        self._table_ptr = binding.table_new()
        self._init_columns(schema)

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
        binding.new_columns(self._table_ptr, schema)

    @property
    def width(self):
        return binding.table_width(self._table_ptr)

    @property
    def column_names(self):
        """An list of column names in the schema."""
        return [binding.column_name(self._table_ptr, i) for i in range(self.width)]

    @property
    def column_types(self):
        """An list of column types in the schema."""
        return [binding.column_type(self._table_ptr, i) for i in range(self.width)]

    @property
    def schema(self):
        """Return the schema of the table."""
        return list(zip(self.column_names, self.column_types))

    def append(self):
        binding.table_append(self._table_ptr)

    def __len__(self):
        return binding.table_len(self._table_ptr)

    def __del__(self):
        """Free the underlying table.

        In case Table instatiation failing, then there is nothing to free.

        """
        try:
            binding.table_free(self._table_ptr)
        except AttributeError:
            pass
