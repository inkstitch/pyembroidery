from .EmbConstant import *


def read(f, out, settings=None):
    f.seek(0x80, 1)  # first block of hell if I know
    f.seek(0x80, 1)  # 2nd block of hell if I know

    while True:
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        b0 = byte[0]
        if b0 == 0xF8 or b0 == 0x87 or b0 == 91:
            break
        flags = STITCH
        command_nibble = b0 & 0xF
        if command_nibble == 0:
            flags = STITCH
        elif command_nibble == 0x1:
            flags = JUMP
        elif command_nibble == 0x7:
            flags = TRIM
        elif command_nibble >= 0x8:
            flags = COLOR_CHANGE
        dx = byte[2]
        dy = -byte[1]
        if (b0 & 0x20) != 0:
            dx = -dx
        if (b0 & 0x40) != 0:
            dy = -dy
        out.add_stitch_relative(flags, dx, dy)
    out.end()
