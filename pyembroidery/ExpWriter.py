from .EmbConstant import *

STRIP_SEQUINS = True
FULL_JUMP = True
MAX_JUMP_DISTANCE = 127
MAX_STITCH_DISTANCE = 127


def write(pattern, f, settings=None):
    stitches = pattern.stitches
    xx = 0
    yy = 0
    for stitch in stitches:
        x = stitch[0]
        y = stitch[1]
        data = stitch[2]
        dx = x - xx
        dy = y - yy
        if data is STITCH:
            # consider bounds checking the delta_x, delta_y and raising ValueError if exceeds.
            delta_x = int(round(dx)) & 0xFF
            delta_y = -int(round(dy)) & 0xFF
            f.write(bytes(bytearray([delta_x, delta_y])))
        elif data == JUMP:
            delta_x = int(round(dx)) & 0xFF
            delta_y = -int(round(dy)) & 0xFF
            f.write(b'\x80\x04')
            f.write(bytes(bytearray([delta_x, delta_y])))
        elif data == TRIM:
            f.write(b'\x80\x80\x07\x00')
            continue
        elif data == COLOR_CHANGE:
            f.write(b'\x80\x01\x00\x00')
            continue
        elif data == STOP:
            f.write(b'\x80\x01\x00\x00')
            continue
        elif data == END:
            pass
        xx = x
        yy = y
