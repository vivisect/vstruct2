import unittest

from vstruct2.bases import *
from vstruct2.types import *

class SizesTest(unittest.TestCase):

    def test_int8(self):
        i = int8()
        self.assertEqual(len(i.vsEmit()), 1)
        i.vsParse(b"\x00" * 8)
        self.assertEqual(len(i.vsEmit()), 1)

    def test_int16(self):
        i = int16()
        self.assertEqual(len(i.vsEmit()), 2)
        i.vsParse(b"\x00" * 8)
        self.assertEqual(len(i.vsEmit()), 2)

    def test_int32(self):
        i = int32()
        self.assertEqual(len(i.vsEmit()), 4)
        i.vsParse(b"\x00" * 8)
        self.assertEqual(len(i.vsEmit()), 4)

    def test_int64(self):
        i = int64()
        self.assertEqual(len(i.vsEmit()), 8)
        i.vsParse(b"\x00" * 8)
        self.assertEqual(len(i.vsEmit()), 8)

    def test_vbytes(self):
        i = vbytes(size=4)
        self.assertEqual(len(i.vsEmit()), 4)
        i.vsParse(b"\x00" * 8)
        self.assertEqual(len(i.vsEmit()), 4)

    def test_cstr(self):
        i = cstr(size=4)
        self.assertEqual(len(i.vsEmit()), 4)
        i.vsParse(b"\x00" * 8)
        self.assertEqual(len(i.vsEmit()), 4)

    def test_zstr(self):
        # zstr automatic resizing is documented,
        # so we'll allow it to not emit `size` bytes
        i = zstr(size=4)
        self.assertEqual(len(i.vsEmit()), 1)
        i.vsParse(b"\x00" * 8)
        self.assertEqual(len(i.vsEmit()), 1)

    def test_varray_int8(self):
        i = varray(4, int8)()
        self.assertEqual(len(i.vsEmit()), 4)
        i.vsParse(b"\x00" * 8)
        self.assertEqual(len(i.vsEmit()), 4)

    def test_varray_vbytes(self):
        i = VArray(fields=[vbytes(size=1) for _ in range(4)])
        self.assertEqual(len(i.vsEmit()), 4)
        i.vsParse(b"\x00" * 8)
        self.assertEqual(len(i.vsEmit()), 4)


def test():
    try:
        unittest.main()
    except SystemExit:
        pass


if __name__ == '__main__':
    test()
