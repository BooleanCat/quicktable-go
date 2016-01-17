package main

type Table struct {
	size int
	name string
}

//NewTable creates a new instance of Table
func NewTable() *Table {
	return &Table{name: "Foo"}
}

//Len returns the number of rows in the Table.
func (table *Table) Len() int {
	return table.size
}

//Append increments the row count by 1
func (table *Table) Append() {
	table.size++
}

func main() {}
