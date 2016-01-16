package main

import "C"

//export sum
func sum(a, b int) int {
	return a + b
}

func main() {}
