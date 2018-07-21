from .EmbConstant import *
from .WriteHelper import write_int_16le, write_int_32le

STRIP_SEQUINS = False
FULL_JUMP = False
MAX_JUMP_DISTANCE = 127
MAX_STITCH_DISTANCE = 127


def write(pattern, f, settings=None):
    stitches = pattern.stitches
    stitch_count = len(stitches)
    for i in range(0, 0x80):
        f.write(b'0')
    if stitch_count == 0:
        return
    extends = pattern.extends()
    write_int_16le(f, int(extends[0]))
    write_int_16le(f, -int(extends[3]))
    write_int_16le(f, int(extends[2]))
    write_int_16le(f, -int(extends[1]))
    write_int_32le(f, 0)  # Dunno.

    write_int_32le(f, stitch_count + 1)  # force write first needle position
    last_stitch = stitches[stitch_count - 1]
    write_int_16le(f, int(last_stitch[0]))
    write_int_16le(f, -int(last_stitch[1]))
    for i in range(f.tell(), 0x100):
        f.write(b'\x00')
    sequin_mode = False
    xx = 0
    yy = 0
    needle = 1
    f.write(b'\xE9\x00\x00')  # Needle to C1
    for stitch in stitches:
        x = stitch[0]
        y = stitch[1]
        data = stitch[2]
        dx = int(round(x - xx))
        dy = int(round(y - yy))
        xx += dx
        yy += dy
        cmd = 0x80
        if dy >= 0:
            cmd |= 0x40
        if dx <= 0:
            cmd |= 0x20
        delta_x = abs(dx)
        delta_y = abs(dy)
        if data == STITCH:
            f.write(bytes(bytearray([cmd, delta_y, delta_x])))
        elif data == JUMP:
            cmd |= 0x01
            f.write(bytes(bytearray([cmd, delta_y, delta_x])))
        elif data == STOP:
            f.write(b'\xE8\x00\x00')  # C0 Stop
        elif data == COLOR_CHANGE:
            needle %= 7
            needle += 1
            cmd = 0xE8 + needle
            f.write(bytes(bytearray([cmd, delta_y, delta_x])))
        elif data == SEQUIN_MODE:
            if sequin_mode:
                f.write(b'\xE8\x00\x00')  # Need to know this command. S2
            else:
                f.write(b'\xE8\x00\x00')  # Need to know this command. S1
            sequin_mode = not sequin_mode
        elif data == TRIM:
            f.write(b'\xE7\x00\x00')  # Trim
        elif data == SEQUIN_EJECT:
            cmd = 0xE8  # I don't know the command for this.
            f.write(bytes(bytearray([cmd, delta_y, delta_x])))
        elif data == END:
            f.write(b'\xF8\x00\x00')
            break
