from .EmbConstant import *
from .ReadHelper import read_int_16le, read_int_8


def read(f, out, settings=None):
    f.seek(0x100, 0)
    while True:
        stitch_type = STITCH
        b1 = read_int_8(f)
        b2 = read_int_8(f)
        if b2 is None:
            break
        if b1 == 0x80:
            b_code = read_int_8(f)
            b1 = read_int_16le(f)
            b2 = read_int_16le(f)
            if b_code == 2:
                stitch_type = COLOR_CHANGE
            if b_code == 3:
                stitch_type = TRIM
            if b_code == 0x7E:
                out.end()
                return
        out.add_stitch_relative(stitch_type, b1, b2)
    out.end()
