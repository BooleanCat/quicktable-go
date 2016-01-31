package main

//Table TODO Write docstring
type Table struct {
	size    int
	columns []Column
}

//NewTable creates a new instance of Table
func NewTable() *Table {
	return new(Table)
}

//NewColumn appends a new column to Table.data
func (table *Table) NewColumn(name, kind string) {
	switch kind {
	case "string":
		table.columns = append(table.columns, &ColumnString{name: name})
	case "int":
		table.columns = append(table.columns, &ColumnInt{name: name})
	}
}

//Len returns the number of rows in the Table.
func (table *Table) Len() int {
	return table.size
}

//Width returns the number of columns
func (table *Table) Width() int {
	return len(table.columns)
}

//ColumnName returns the column name at index i
func (table *Table) ColumnName(i int) string {
	return table.columns[i].Name()
}

//ColumnType returns the column type at index i
func (table *Table) ColumnType(i int) string {
	return table.columns[i].Type()
}

func main() {}
