from .EmbConstant import *
from .ReadHelper import read_int_16le, read_int_8, signed8


def read(f, out, settings=None):
    magic_number = f.read(6)
    width = read_int_16le(f)
    height = read_int_16le(f)
    colors = read_int_16le(f)
    f.seek(0x30, 0)
    while True:
        stitch_type = STITCH
        b0 = read_int_8(f)
        b1 = read_int_8(f)
        if b0 == 0x80:
            if b1 == 0x2A:
                out.color_change()
                continue
            if b1 == 0x80:
                b0 = read_int_8(f)
                b1 = read_int_8(f)
                stitch_type = TRIM
            if b1 == 0xFD:
                break
            else:
                continue
        dx = signed8(b0)
        dy = signed8(b1)
        out.add_stitch_relative(dx, dy, stitch_type)
    out.end()
