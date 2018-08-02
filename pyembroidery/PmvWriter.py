from .EmbConstant import *
from .WriteHelper import write_string_utf8, write_int_8, write_int_16le

MAX_STITCH_DISTANCE = 32


def write(pattern, f, settings=None):
    extends = pattern.extends()
    if extends[1] < -16:
        return
    if extends[3] > +16:
        return
    point_count = 0
    for stitch in pattern.stitches:
        data = stitch[2]
        if data == STITCH or data == JUMP:
            point_count += 1
    if point_count > 64:
        return

    write_string_utf8(f, "#PMV0001")
    header = "...................................."
    write_string_utf8(f, header[0:36])
    f.write(b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00')

    write_int_16le(f, point_count)
    write_int_16le(f, point_count * 2)
    xx = 0
    for stitch in pattern.stitches:
        x = stitch[0]
        y = stitch[1]
        data = stitch[2]
        dx = int(round(x - xx))
        xx += dx
        if data == STITCH or data == JUMP:
            if dx < 0:
                dx += 64
            if y < 0:
                y += 32
            write_int_8(f, dx)
            write_int_8(f, y)
            continue
    write_int_16le(f, 0)
    write_int_16le(f, 256)
    f.write(b'\x00\x00\x00\x00\x05\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x02\x00')
    write_int_16le(f, 256)
    write_int_8(f, 0)
    write_int_8(f, 0)
    write_int_8(f, 12)
    max_f = 8192
    max_s = 1000
    write_steps(f, 1, max_f, max_s)
    write_int_8(f, 0)
    write_steps(f, 1, max_f, max_s)
    write_int_16le(f, 0x12)
    f.write(b'\x00\x00\x00\x00\x00\x00\x00\x00'
            b'\x00\x00\x00\x00\x00\x00\x00\x00')


def write_steps(f, steps, max_first, max_second):
    write_int_8(f, steps)
    for i in range(0, steps - 1):
        f_val = int(round(i * max_first / float(steps)))
        s_val = int(round(i * max_second / float(steps)))
        write_int_16le(f, f_val)
        write_int_16le(f, s_val)
    f_val = max_first
    s_val = max_second
    write_int_16le(f, f_val)
    write_int_16le(f, s_val)
