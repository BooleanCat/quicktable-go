package main

type Table struct {
	size    int
	columns []*Column
}

//NewTable creates a new instance of Table
func NewTable() *Table {
	return new(Table)
}

func (table *Table) NewColumn(name, kind string) {
	table.columns = append(table.columns, &Column{name, kind})
}

//Len returns the number of rows in the Table.
func (table *Table) Len() int {
	return table.size
}

//Width returns the number of columns
func (table *Table) Width() int {
	return len(table.columns)
}

//Append increments the row count by 1
func (table *Table) Append() {
	table.size++
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
