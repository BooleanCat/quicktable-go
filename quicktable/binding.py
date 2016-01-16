import os
import ctypes
from ctypes import cdll

FILE_PATH = os.path.abspath(os.path.dirname(__file__))
LIB_PATH = os.path.join(FILE_PATH, 'libadd.so')


_lib = cdll.LoadLibrary(LIB_PATH)

# sum
_lib.sum.argtypes = [ctypes.c_int, ctypes.c_int]
_lib.sum.restypes = ctypes.c_int

add = _lib.sum
