import unittest

from vstruct2.compat import *

class CompatTest(unittest.TestCase):

    def test_compat_b2i(self):

        self.assertEqual( bytes2int(b'\xff\x56', 2, byteorder='big'), 0xff56 )
        self.assertEqual( bytes2int(b'\xff\x56', 2, byteorder='little'), 0x56ff )

        self.assertEqual( bytes2int(b'\xff\xff\xff\xff', 4, signed=True), -1 )
        self.assertEqual( bytes2int(b'\xff\xff\xff\xff', 4, signed=False), 0xffffffff )
        
        self.assertEqual( bytes2int(b'\xff\xff\xff\xff\xff\xff\xff\xff', 8, signed=True), -1 )
        self.assertEqual( bytes2int(b'\xff\xff\xff\xff\xff\xff\xff\xff', 8, signed=False), 0xffffffffffffffff )
        
        bytes16 = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
        self.assertEqual( bytes2int(bytes16, 16, signed=True), -1 )
        self.assertEqual( bytes2int(bytes16, 16, byteorder='big', signed=True), -1 )
        self.assertEqual( bytes2int(bytes16, 16), 0xffffffffffffffffffffffffffffffff )
        
        bytes16_2 = b'\xff\xff\xff\xff\xff\xff\xff\xff\xf0\xf0\xf0\xf0\xf0\xf0\xf0\xf0'
        self.assertEqual( bytes2int(bytes16_2, 16, byteorder='big'), 0xfffffffffffffffff0f0f0f0f0f0f0f0 )
        self.assertEqual( bytes2int(bytes16_2, 16), 0xf0f0f0f0f0f0f0f0ffffffffffffffff )

    def test_compat_i2b(self):

        self.assertEqual( int2bytes(-1, 2, signed=True), b'\xff\xff' )

        self.assertEqual( int2bytes(0x102030, 3, byteorder='big'), b'\x10\x20\x30')
        self.assertEqual( int2bytes(0x102030, 3, byteorder='little'), b'\x30\x20\x10')

        self.assertEqual( int2bytes(0x0080, 2, byteorder='big'), b'\x00\x80' )
        self.assertEqual( int2bytes(0x0080, 2, byteorder='little'), b'\x80\x00' )

        self.assertEqual( int2bytes(0x008000800080008000800080, 12, byteorder='big'), b'\x00\x80\x00\x80\x00\x80\x00\x80\x00\x80\x00\x80' )
        self.assertEqual( int2bytes(0x008000800080008000800080, 12, byteorder='little'), b'\x80\x00\x80\x00\x80\x00\x80\x00\x80\x00\x80\x00' )
