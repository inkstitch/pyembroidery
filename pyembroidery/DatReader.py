from .EmbConstant import *
from .ReadHelper import read_int_16le, read_int_8, signed8


# This code proved to be utterly untestable as I never found a copy of the filetype

def read(f, out, settings=None):
    f.seek(0x02, 0)
    stitches = read_int_16le(f)
    f.seek(0x100, 0)
    while True:
        b1 = read_int_8(f)
        b2 = read_int_8(f)
        b0 = read_int_8(f)
        if b0 is None:
            break
        stitch_type = STITCH
        if (b0 & 0x02) == 0:
            stitch_type = TRIM
        if b0 == 0xF8:
            break
        x = signed8(b1)
        y = -signed8(b2)
        out.add_stitch_relative(stitch_type, x, y)
    out.end()
