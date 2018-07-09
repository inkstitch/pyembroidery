from .EmbConstant import *
from .ReadHelper import signed8


def read(f, out, settings=None):

    while True:
        byte = bytearray(f.read(4))
        if len(byte) != 4:
            break
        stitch_type = STITCH
        x = signed8(byte[2])
        y = signed8(byte[3])
        if (byte[0] & 0x01) != 0:
            stitch_type = COLOR_CHANGE
        if byte[0] == 0x1F:
            break
        out.add_stitch_relative(stitch_type, x, y)
    out.end()
