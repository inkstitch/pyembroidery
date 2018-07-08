from .EmbConstant import *


def read(f, out, settings=None):
    while True:
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        x = byte[2]
        y = -byte[1]
        ctrl = byte[0]
        stitch_type = STITCH
        if ctrl & 0x01 != 0:
            stitch_type = TRIM
        if ctrl & 0x20 != 0:
            x = -x
        if ctrl & 0x40 != 0:
            y = -y
        if ctrl & 0x05 == 0x05:
            stitch_type = COLOR_CHANGE
        if ctrl == 0xF8 or ctrl == 0x91 or ctrl == 0x87:
            out.end()
            return
        out.add_stitch_relative(x, y, stitch_type)

    out.end()
