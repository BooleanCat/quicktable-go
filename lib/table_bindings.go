package main

//#include <stdlib.h>
import "C"
import "unsafe"

var tables = make(map[*uint64]*Table)

//export TableLen
func TableLen(table *uint64) int {
	return tables[table].Len()
}

//export TableAppend
func TableAppend(table *uint64) {
	tables[table].Append()
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

//export TableName
func TableName(table *uint64) *C.char {
	return C.CString(tables[table].name)
}
