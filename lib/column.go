package main

type Column struct {
	name string
	kind string
}

func (column *Column) Name() string {
	return column.name
}

func (column *Column) Type() string {
	return column.kind
}
