package main

//#include <stdlib.h>
import "C"
import "unsafe"

type Table struct {
	size int
	name string
}

var tables = make(map[*uint64]*Table)

//Len returns the number of rows in the Table.
func (table *Table) Len() int {
	return table.size
}

//export TableLen
func TableLen(table *uint64) int {
	return tables[table].Len()
}

//Append increments the row count by 1
func (table *Table) Append() {
	table.size++
}

//export TableAppend
func TableAppend(table *uint64) {
	tables[table].Append()
}

//export TableNew
func TableNew() *uint64 {
	table := &Table{name: "Foo"}
	ptr := (*uint64)(unsafe.Pointer(table))

	tables[ptr] = table

	return ptr
}

//export TableFree
func TableFree(table *uint64) {
	delete(tables, table)
}

//export TableName
func TableName(table *uint64) *C.char {
	return C.CString(tables[table].name)
}

func main() {}
