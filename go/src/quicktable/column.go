package main

type Column interface {
	Name() string
	Type() string
	Append(interface{})
	GetItem(int) interface{}
}

type ColumnString struct {
	name string
	data []string
}

func (column *ColumnString) Name() string {
	return column.name
}

func (column *ColumnString) Type() string {
	return "string"
}

func (column *ColumnString) Append(element interface{}) {
	if e, ok := element.(string); ok {
		column.data = append(column.data, e)
	}
}

func (column *ColumnString) GetItem(i int) interface{} {
	return interface{}(column.data[i])
}

type ColumnInt struct {
	name string
	data []int
}

func (column *ColumnInt) Name() string {
	return column.name
}

func (column *ColumnInt) Type() string {
	return "int"
}

func (column *ColumnInt) Append(element interface{}) {
	if e, ok := element.(int); ok {
		column.data = append(column.data, e)
	}
}

func (column *ColumnInt) GetItem(i int) interface{} {
	return interface{}(column.data[i])
}
