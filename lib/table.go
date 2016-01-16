package main

//#include <stdlib.h>
import "C"
import "unsafe"

type Table struct {
	name string
}

var tables = make(map[*uint64]*Table)

//export TableNew
func TableNew() *uint64 {
	table := &Table{ "Foo" }
	ptr := (*uint64)(unsafe.Pointer(table))

	tables[ptr] = table

	return ptr
}

//export TableFree
func TableFree(ptr *uint64) {
	delete(tables, ptr)
}

//export TableName
func TableName(ptr *uint64) *C.char {
	return C.CString(tables[ptr].name)
}

func main() {}
