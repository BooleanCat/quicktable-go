from quicktable import binding


class Table:
    def __init__(self):
        self._table_ptr = binding.table_new()

    @property
    def name(self):
        return binding.table_name(self._table_ptr)

    def append(self):
        binding.table_append(self._table_ptr)

    def __len__(self):
        return binding.table_len(self._table_ptr)

    def __del__(self):
        binding.table_free(self._table_ptr)
