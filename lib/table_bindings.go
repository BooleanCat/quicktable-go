package main

//#include <stdlib.h>
import "C"
import "unsafe"

var tables = make(map[*uint64]*Table)

//export TableLen
func TableLen(table *uint64) int {
	return tables[table].Len()
}

//export TableWidth
func TableWidth(table *uint64) int {
	return tables[table].Width()
}

//export TableAppend
func TableAppend(table *uint64) {
	tables[table].Append()
}

//export TableColumnName
func TableColumnName(table *uint64, i int) *C.char {
	return C.CString(tables[table].ColumnName(i))
}

//export TableColumnType
func TableColumnType(table *uint64, i int) *C.char {
	return C.CString(tables[table].ColumnType(i))
}

//export TableNewColumn
func TableNewColumn(table *uint64, name, kind *C.char) {
	tables[table].NewColumn(C.GoString(name), C.GoString(kind))
}

//export TableNew
func TableNew() *uint64 {
	table := NewTable()
	ptr := (*uint64)(unsafe.Pointer(table))
	tables[ptr] = table

	return ptr
}

//export TableFree
func TableFree(table *uint64) {
	delete(tables, table)
}
