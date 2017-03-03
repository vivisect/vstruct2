vstruct2 ( Mark II )
===================

Vivisect Structure Definition/Parsing Library
|Build Status|

Installing
==========

.. code::

    python3.4 -m pip install vstruct2

vstruct2 can now be installed via pip!

Additionally, a repository of existing structure definitions
is available as a seperate package named fracture.

Examples
========

Basic Parsing
-------------

Simple vstruct2 byte parsing:

.. code:: python

    from vstruct2.types import *

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

Parser Callbacks
----------------

WriteBack Bytes/Files
---------------------

vstruct2 supports "writeback" functionality for both files and mutable
bytearray types, allowing field assignments to change the underlying file
or bytearray immediately.

.. code:: python

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

Enum Types
----------

.. |Build Status| image:: https://travis-ci.org/vivisect/vstruct2.svg
   :target: https://travis-ci.org/vivisect/vstruct2
