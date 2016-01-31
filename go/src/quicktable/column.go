package main

//Column is an interface describing each typed column
type Column interface {
	Name() string
	Type() string
	Append(interface{})
	GetItem(int) interface{}
}

//ColumnString is a named slice of strings
type ColumnString struct {
	name string
	data []string
}

//Name is the name used to initialise the column
func (column *ColumnString) Name() string {
	return column.name
}

//Type is the corresponding Python type of the column - `string`
func (column *ColumnString) Type() string {
	return "string"
}

//Append adds appends a string to the typed column
func (column *ColumnString) Append(element interface{}) {
	if e, ok := element.(string); ok {
		column.data = append(column.data, e)
	}
}

//GetItem returns the string at index i
func (column *ColumnString) GetItem(i int) interface{} {
	return interface{}(column.data[i])
}

//ColumnInt is a named slice of strings
type ColumnInt struct {
	name string
	data []int
}

//Name is the name used to initialise the column
func (column *ColumnInt) Name() string {
	return column.name
}

//Type is the corresponding Python type of the column - `int`
func (column *ColumnInt) Type() string {
	return "int"
}

//Append adds appends an int to the typed column
func (column *ColumnInt) Append(element interface{}) {
	if e, ok := element.(int); ok {
		column.data = append(column.data, e)
	}
}

//GetItem returns the int at index i
func (column *ColumnInt) GetItem(i int) interface{} {
	return interface{}(column.data[i])
}
