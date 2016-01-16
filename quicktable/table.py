from quicktable.utils import free_c_string
from quicktable.binding import table_new, table_name, table_free


class Table:
    def __init__(self):
        self._table_ptr = table_new()

    @property
    def name(self):
        with free_c_string(table_name(self._table_ptr)) as string:
            return string

    def __del__(self):
        table_free(self._table_ptr)
