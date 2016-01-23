package main

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

//export TableColumnAppendInt
func TableColumnAppendInt(table *uint64, i, value int) {
	tables[table].columns[i].Append(interface{}(value))
}

//export TableColumnAppendString
func TableColumnAppendString(table *uint64, i int, value *C.char) {
	tables[table].columns[i].Append(interface{}(C.GoString(value)))
}

//export TableColumnGetInt
func TableColumnGetInt(table *uint64, col, row int) int {
	if element, ok := tables[table].columns[col].GetItem(row).(int); ok {
		return element
	}
	return -1
}

//export TableColumnGetString
func TableColumnGetString(table *uint64, col, row int) *C.char {
	if element, ok := tables[table].columns[col].GetItem(row).(string); ok {
		return C.CString(element)
	}
	return C.CString("")
}

//export TableRowInc
func TableRowInc(table *uint64) {
	tables[table].size++
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
