from .EmbConstant import *
from .WriteHelper import write_string_utf8
import math

STRIP_SPEEDS = True
SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_STITCH
MAX_JUMP_DISTANCE = float('inf')
MAX_STITCH_DISTANCE = float('inf')


def write(pattern, f, settings=None):
    if settings is None:
        settings = {}

    flip_x = settings.get('flip_x', True)
    flip_y = settings.get('flip_y', True)
    stitch_z_travel = settings.get('stitch_z_travel', 5)

    # pyembroidery natively uses tenths of a millimeter
    extents = [extent / 10.0 for extent in pattern.extents()]
    width = extents[2] - extents[0]
    height = extents[3] - extents[1]

    write_string_utf8(f, '(STITCH_COUNT:%d)\r\n' % pattern.count_stitches())
    write_string_utf8(f, '(EXTENTS_LEFT:%.3f)\r\n' % extents[0])
    write_string_utf8(f, '(EXTENTS_TOP:%.3f)\r\n' % extents[1])
    write_string_utf8(f, '(EXTENTS_RIGHT:%.3f)\r\n' % extents[2])
    write_string_utf8(f, '(EXTENTS_BOTTOM:%.3f)\r\n' % extents[3])
    write_string_utf8(f, '(EXTENTS_WIDTH:%.3f)\r\n' % width)
    write_string_utf8(f, '(EXTENTS_HEIGHT:%.3f)\r\n' % height)
    write_string_utf8(f, "\r\n")
    write_string_utf8(f, "G0 X0.0 Y0.0\r\n")

    z = 0
    for i, (x, y, command) in enumerate(pattern.stitches):
        # embroidery G-code discussion: https://github.com/inkstitch/inkstitch/issues/335
        if command == STITCH:
            if flip_x:
                x = -x
            if flip_y:
                y = -y

            # pyembroidery natively uses tenths of a millimeter
            x /= 10.0
            y /= 10.0

            write_string_utf8(f, "G0 X%.3f Y%.3f\r\n" % (x, y))

            # Stitching is modelled as continuous travel on the Z axis.  The
            # Z motor is hooked up to the hand wheel of the sewing machine.
            z += stitch_z_travel
            write_string_utf8(f, "G0 Z%.1f\r\n" % z)

    write_string_utf8(f, "\r\n")
    write_string_utf8(f, "G0 X0.0 Y0.0\r\n")
    write_string_utf8(f, "M30\r\n")
