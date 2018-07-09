from .EmbConstant import *
from .ReadHelper import read_int_8, signed8


def read(f, out, settings=None):
    f.seek(0x2000, 0)
    while True:
        stitch_type = STITCH

        x = read_int_8(f)
        y = read_int_8(f)
        command_byte = read_int_8(f)
        if command_byte is None:
            break
        x = signed8(x)
        y = -signed8(y)
        if (command_byte & 0x20) == 0x20:
            y = -y
        if (command_byte & 0x40) == 0x40:
            x = -x
        if (command_byte & 0x01) == 0x01:
            stitch_type = COLOR_CHANGE
        if (command_byte & 0x02) == 0x02:
            stitch_type = TRIM
        out.add_stitch_relative(stitch_type, x, y)
    out.end()
