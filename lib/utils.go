package main

//#include <stdlib.h>
import "C"
import "unsafe"

//export StringFree
func StringFree(ptr *C.char) {
	C.free(unsafe.Pointer(ptr))
}
