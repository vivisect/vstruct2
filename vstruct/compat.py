'''
A place to isolate the py27 compat filth.
'''
import sys

major = sys.version_info.major
minor = sys.version_info.minor
micro = sys.version_info.micro

version = (major,minor,micro)

if version < (3,0,0):

    import struct
    fmtchars = {
        (1,'big',False):'B',
        (1,'little',False):'B',

        (2,'big',False):'>H',
        (2,'little',False):'<H',

        (4,'big',False):'>I',
        (4,'little',False):'<I',

        (8,'big',False):'>Q',
        (8,'little',False):'<Q',

        (1,'big',True):'b',
        (1,'little',True):'b',

        (2,'big',True):'>h',
        (2,'little',True):'<h',

        (4,'big',True):'>i',
        (4,'little',True):'<i',

        (8,'big',True):'>q',
        (8,'little',True):'<q',
    }

    def bytes2int(byts, size, off=0, byteorder='little', signed=False):
        """
        Mostly for pulling immediates out of strings...
        """
        if size > 8:
            return slowparsebytes(bytes, offset, size, sign=sign, bigend=bigend)

        fmt = fmtchars.get( (size,byteorder,signed) )
        if fmt != None:
            return struct.unpack(fmt, byts[off:off+size])[0]

        valu = 0
        vals = [ ord(c) for c in byts[off:off+size] ]

        if byteorder == 'little':
            vals.reverse()

        for i in range(size):
            valu <<= 8
            valu += vals[i]

        return valu

    def int2bytes(valu, size, byteorder='little', signed=False):
        fmt = fmtchars.get( (size,byteorder,signed) )
        if fmt != None:
            return struct.pack(fmt, valu)

        ords = []
        for i in range(size):
            ords.append( (valu >> (8*i) ) & 0xff )

        if byteorder == 'big':
            ords.reverse()

        return ''.join([ chr(o) for o in ords ])

else:

    def int2bytes(valu, size, byteorder='little', signed=False):
        return valu.to_bytes(size, byteorder=byteorder, signed=signed)

    def bytes2int(byts, size, byteorder='little', signed=False, off=0):
        return int.from_bytes(byts[off:off+size], byteorder=byteorder, signed=signed)
