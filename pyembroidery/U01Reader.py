from .EmbConstant import *


def read_u01_stitches(f, out):
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        ctrl = byte[0]
        dy = -byte[1]
        dx = byte[2]
        if (ctrl & 0x20) != 0:
            dx = -dx
        if (ctrl & 0x40) != 0:
            dy = -dy
        command = ctrl & 0b11111
        #print(str(count), " ", str("{0:b}").format(ctrl), " 0x%0.2X " % ctrl, str(command), " " + str(dx), " ", str(dy))
        if command == 0x0:
            out.stitch(dx, dy)
            continue
        if command == 0x1:
            out.move(dx, dy)
            continue
        if command == 0x2:
            out.add_stitch_relative(FAST)
            if dx != 0 or dy != 0:
                out.stitch(dx, dy)
            continue
        if command == 0x4:
            out.add_stitch_relative(SLOW)
            if dx != 0 or dy != 0:
                out.stitch(dx, dy)
            continue
        if command == 0x7:
            out.trim(dx, dy)
            continue
        if command == 0x8:  # ww, stop file had proper A8 rather than E8 and displacement
            out.stop(dx, dy)
            continue
        if 0xE9 <= ctrl <= 0xEF:
            if count > 1:
                out.color_change(dx, dy)
            continue
        if ctrl == 0xF8:
            break
        break  # Uncaught Command
    out.end()


def read(f, out, settings=None):
    f.seek(0x80, 1)
    f.seek(0x80, 1)
    read_u01_stitches(f, out)
