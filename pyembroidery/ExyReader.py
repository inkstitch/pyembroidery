from .EmbConstant import *


def getbit(b, pos):
    return (b >> pos) & 1


def decode_dx(b0, b1, b2):
    x = 0
    x += getbit(b2, 2) * (+81)
    x += getbit(b2, 3) * (-81)
    x += getbit(b1, 2) * (+27)
    x += getbit(b1, 3) * (-27)
    x += getbit(b0, 2) * (+9)
    x += getbit(b0, 3) * (-9)
    x += getbit(b1, 0) * (+3)
    x += getbit(b1, 1) * (-3)
    x += getbit(b0, 0) * (+1)
    x += getbit(b0, 1) * (-1)
    return x


def decode_dy(b0, b1, b2):
    y = 0
    y += getbit(b2, 5) * (+81)
    y += getbit(b2, 4) * (-81)
    y += getbit(b1, 5) * (+27)
    y += getbit(b1, 4) * (-27)
    y += getbit(b0, 5) * (+9)
    y += getbit(b0, 4) * (-9)
    y += getbit(b1, 7) * (+3)
    y += getbit(b1, 6) * (-3)
    y += getbit(b0, 7) * (+1)
    y += getbit(b0, 6) * (-1)
    return -y


def exy_decode_flags(b):
    if b == 0xF3:
        return END
    if (b & 0xC3) == 0xC3:
        return COLOR_CHANGE  # TRIM | STOP
    if (b & 0x80) != 0:
        return TRIM
    if (b & 0x40) != 0:
        return COLOR_CHANGE


def read(f, out, settings=None):
    f.seek(0x100)
    while True:
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        dx = decode_dx(byte[0], byte[1], byte[2])
        dy = decode_dy(byte[0], byte[1], byte[2])
        flags = exy_decode_flags(byte[2])
        if flags == END:
            break
        out.add_stitch_relative(flags, dx, dy)
    out.end();
