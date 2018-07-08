from .ReadHelper import read_int_16le, read_int_32le, \
    read_int_8, read_int_24be, signed8, signed16
from .EmbThread import EmbThread
from .EmbConstant import *


def read(f, out, settings=None):
    f.seek(0x27, 1)
    num_of_colors = read_int_16le(f)
    f.seek(0xD3, 1)
    palette_offset = read_int_32le(f)
    is_jump_stitch = False

    while f.tell() < palette_offset:
        b1 = read_int_8(f)
        stitch_type = STITCH
        if is_jump_stitch:
            stitch_type = TRIM
        is_jump_stitch = False
        if b1 == 0x7E or b1 == 0x7D:
            dx = signed16(read_int_16le(f))
            dy = signed16(read_int_16le(f))
        elif b1 == 0x7F:
            b2 = read_int_8(f)
            if b2 != 0x17 and b2 != 0x46 and b2 >= 8:
                b1 = 0
                b2 = 0
                is_jump_stitch = True
                stitch_type = COLOR_CHANGE
            elif b2 == 1:
                b1 = read_int_8(f)
                b2 = read_int_8(f)
                stitch_type = TRIM
            dx = signed8(b1)
            dy = signed8(b2)
        else:
            b2 = read_int_8(f)
            dx = signed8(b1)
            dy = signed8(b2)
        out.add_stitch_relative(stitch_type, dx, -dy)
    f.seek(6, 1)
    for i in range(0, num_of_colors + 1):
        thread = EmbThread()
        read_int_8(f)
        thread.color = read_int_24be(f)
