import traceback
from vstruct.compat import int2bytes, bytes2int

# This routine was coppied from vivisect to allow vstruct
# to be free from dependencies
MAX_WORD = 16
def initmask(bits):
    return (1<<bits)-1

bitmasks = [ initmask(i) for i in range(MAX_WORD*8) ]
def bitmask(value,bits):
    return value & bitmasks[bits]

class v_base:
    '''
    Base class for all VStruct types
    '''
    def __init__(self):
        self._vs_onset = []
        self._vs_isprim = True

    def __len__(self):
        return self.vsSize()

    def __bytes__(self):
        return self.vsEmit()

    def vsOnset(self, callback, *args, **kwargs):
        '''
        Trigger a callback when the fields value is updated.

        NOTE: this callback is triggered during parse() as well
              as during value updates.
        '''
        self._vs_onset.append( (callback,args,kwargs) )
        return self

    def _fire_onset(self):
        for cb,args,kwargs in self._vs_onset:
            try:
                cb(*args,**kwargs)
            except Exception as e:
                traceback.print_exc()

class v_prim(v_base):
    '''
    Base class for all vstruct primitive types
    '''
    def __init__(self, size=None, valu=None):
        v_base.__init__(self)
        self._vs_size = size
        self._vs_bits = size * 8
        self._vs_value = self._prim_norm(valu)
        self._vs_parent = None

        # on-demand field parsing
        self._vs_backfd = None
        self._vs_backoff = None
        self._vs_backbytes = None
        self._vs_writeback = False

    def __repr__(self):
        return repr(self._prim_getval())

    def vsParse(self, bytez, offset=0, writeback=False):
        '''
        Byte parsing method for VStruct primitives.
        '''
        self._vs_value = None
        self._vs_backoff = offset
        self._vs_backbytes = bytez
        self._vs_writeback = writeback
        retval = offset + self.vsSize()
        self._fire_onset()
        return retval

    def vsLoad(self, fd, offset=0, writeback=False):
        self._vs_value = None
        self._vs_backfd = fd
        self._vs_backoff = offset
        self._vs_writeback = writeback
        retval = offset + self.vsSize()
        self._fire_onset()
        return retval

    def vsSize(self):
        '''
        Return the size of the field.
        '''
        return self._vs_size

    def vsResize(self, size):
        '''
        Resizing callback which can dynamically change the size
        of a primitive.
        '''
        self._vs_size = size

    def _prim_setval(self, newval):
        valu = self._prim_norm(newval)
        self._vs_value = valu

        # if requested, write changes back to bytearray / fd
        if self._vs_writeback:
            byts = self._prim_emit(valu)
            if self._vs_backbytes != None:
                self._vs_backbytes[ self._vs_backoff:self._vs_backoff + len(byts) ] = byts

            if self._vs_backfd != None:
                self._vs_backfd.seek( self._vs_backoff )
                self._vs_backfd.write( byts )

        self._fire_onset()

    def _prim_getval(self):
        # trigger on-demand parsing if needed
        if self._vs_value == None:
            if self._vs_backfd:
                self._vs_value = self._prim_load(self._vs_backfd, self._vs_backoff)
            elif self._vs_backbytes:
                self._vs_value = self._prim_parse(self._vs_backbytes, self._vs_backoff)

        return self._vs_value

    def _prim_load(self, fd, offset):
        # easy base case...
        fd.seek(offset)
        byts = fd.read(self._vs_size)
        return self._prim_parse(byts, 0)

    def vsEmit(self):
        return self._prim_emit( self._prim_getval() )

    def _prim_norm(self, x):
        raise Exception('Implement Me')

    def _prim_emit(self, x):
        raise Exception('Implement Me')

    def _prim_parse(self, bytez, offset):
        raise Exception('Implement Me')

class v_int(v_prim):

    def __init__(self,valu=0,size=4,endian='little',signed=False,enum=None):
        v_prim.__init__(self,valu=valu,size=size)
        self._vs_enum = enum
        self._vs_endian = endian
        self._vs_signed = signed

    def __int__(self):
        return self._prim_getval()

    def __repr__(self):
        valu = self._prim_getval()
        if self._vs_enum != None:
            enum = self._vs_enum[valu]
            if enum != None:
                return enum
        return repr(valu)

    def vsResize(self, size):
        self._vs_bits = size * 8
        return v_prim.vsResize(self,size)

    def _prim_emit(self,x):
        return int2bytes(x, self._vs_size, byteorder=self._vs_endian, signed=self._vs_signed)

    def _prim_norm(self,x):
        return bitmask(x,self._vs_bits)

    def _prim_parse(self, byts, offset):
        return bytes2int(byts, self._vs_size, byteorder=self._vs_endian, signed=self._vs_signed, off=offset)
