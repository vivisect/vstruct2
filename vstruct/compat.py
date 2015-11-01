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
    
    ''' Stolen from vivisect/envi/bits.py to keep vstruct dependency free. '''
    MAX_WORD = 32 # usually no more than 8, 16 is for SIMD register support

    # Masks to use for unsigned anding to size
    u_maxes = [ (2 ** (8*i)) - 1 for i in range(MAX_WORD+1) ]
    u_maxes[0] = 0 # powers of 0 are 1, but we need 0

    # Masks of just the sign bit for different sizes
    sign_bits = [ (2 ** (8*i)) >> 1 for i in range(MAX_WORD+1) ]
    sign_bits[0] = 0 # powers of 0 are 1, but we need 0

    def unsigned(value, size):
        ''' Stolen from vivisect/envi/bits.py to keep vstruct dependency free. '''
        return value & u_maxes[size]

    def signed(value, size):
        ''' Stolen from vivisect/envi/bits.py to keep vstruct dependency free. '''
        x = unsigned(value, size)
        if x & sign_bits[size]:
            x = (x - u_maxes[size]) - 1
        return x
    
    def slowparsebytes(byts, offset, size, sign=False, byteorder='little'):
        ''' Stolen from vivisect/envi/bits.py to keep vstruct dependency free. '''
        if byteorder == 'big':
            begin = offset
            inc = 1
        else:
            begin = offset + (size-1)
            inc = -1

        ret = 0
        ioff = 0
        for x in range(size):
            ret = ret << 8
            ret |= ord(byts[begin+ioff])
            ioff += inc
        if sign:
            ret = signed(ret, size)
        return ret

    def bytes2int(byts, size, off=0, byteorder='little', signed=False):
        """
        Mostly for pulling immediates out of strings...
        """
        if size > 8:
            return slowparsebytes(byts, off, size, sign=signed, byteorder=byteorder)

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
