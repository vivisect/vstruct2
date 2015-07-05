# vstruct
Vivisect Structure Definition/Parsing Library
[![Build Status](https://travis-ci.org/vivisect/vstruct.svg)](https://travis-ci.org/vivisect/vstruct)

# Examples

## Basic Parsing
Simple vstruct byte parsing:

```
from vstruct.types import *

class Foo(VStruct):

    def __init__(self):
        VStruct.__init__(self)
        self.bar    = uint32()
        self.baz    = vbytes(20)


foo = Foo()

# read in byts from somewhere...
foo.vsParse(byts)

# access struct fields by name
if foo.bar == 30:
    print('bar == 30!')

# assign fields by name
foo.bar = 90

# emit modified bytes back out
byts = bytes(foo) # same as foo.vsEmit()

```

## Parser Callbacks

## WriteBack Bytes/Files
vstruct supports "writeback" functionality for both files and mutable
bytearray types, allowing field assignments to change the underlying file
or bytearray immediately.

```
class Foo(VStruct):

    def __init__(self):
        VStruct.__init__(self)
        self.bar    = uint32()
        self.baz    = uint32()


foo = Foo()

# ba is a bytearray
foo.vsParse(ba, writeback=True)

# if bar is 30, set baz to 99
if foo.bar == 30:
    foo.baz = 99

# ba bytearray has now been modified

```

## Enum Types

