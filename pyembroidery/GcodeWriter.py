import math

from .EmbConstant import *
from .WriteHelper import write_string_utf8


STRIP_SPEEDS = True
SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_STITCH
MAX_JUMP_DISTANCE = float('inf')
MAX_STITCH_DISTANCE = float('inf')


def write(pattern, f, settings=None):
    if settings is None:
        settings = {}

    laser_mode = settings.get('laser_mode', False)
    flip_x = settings.get('flip_x', True)
    flip_y = settings.get('flip_y', True)
    stitch_z_travel = settings.get('stitch_z_travel', 5)
    spindle_speed = settings.get('spindle_speed', -1)
    max_spindle_speed = settings.get('max_spindle_speed', -1)
    min_spindle_speed = settings.get('min_spindle_speed', -1)
    feed_rate = settings.get('feed_rate', -1)

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

    init(f, laser_mode, max_spindle_speed, min_spindle_speed, spindle_speed, feed_rate)

    write_string_utf8(f, "G0 X0.0 Y0.0\r\n")

    z = 0
    stitching = False
    for x, y, command in pattern.stitches:
        # embroidery G-code discussion: https://github.com/inkstitch/inkstitch/issues/335
        if command == STITCH:
            if flip_x:
                x = -x
            if flip_y:
                y = -y

            # pyembroidery natively uses tenths of a millimeter
            x /= 10.0
            y /= 10.0

            if stitching and spindle_speed >= 0 and feed_rate >= 0:
                command = "G1"
            else:
                # If we're in laser mode, G0 automatically turns off the laser for the move.
                command = "G0"

            write_string_utf8(f, "%s X%.3f Y%.3f\r\n" % (command, x, y))

            if stitch_z_travel > 0:
                # For DIY embroidery machines, stitching is modeled as continuous
                # travel on the Z axis.  The Z motor is hooked up to the hand wheel
                # of the sewing machine.  For each stitch, we "move" in the Z
                # direction, which turns the wheel and causes the machine to
                # stitch.
                z += stitch_z_travel
                write_string_utf8(f, "G0 Z%.1f\r\n" % z)

            stitching = True
        else:
            stitching = False

    write_string_utf8(f, "\r\n")
    write_string_utf8(f, "G0 X0.0 Y0.0\r\n")
    write_string_utf8(f, "M30\r\n")


def init(f, laser_mode, max_spindle_speed, min_spindle_speed, spindle_speed, feed_rate):
    write_string_utf8(f, "G90 (use absolute coordinates)\r\n")
    write_string_utf8(f, "G21 (coordinates will be specified in millimeters)\r\n")

    if max_spindle_speed >= 0:
        write_string_utf8(f, "$30=%d (S value used for maximum spindle speed or laser power)\r\n" % max_spindle_speed)

    if min_spindle_speed >= 0:
        write_string_utf8(f, "$31=%d (S value used for minimum spindle speed or laser power)\r\n" % min_spindle_speed)

    if laser_mode:
        write_string_utf8(f, "$32=1 (enable grbl laser mode)\r\n")
        write_string_utf8(f, "M4 (use dynamic laser power)\r\n")

    if spindle_speed > 0 and feed_rate > 0:
        write_string_utf8(f, "G1 X0 Y0 S%d F%d\r\n" % (spindle_speed, feed_rate))

    write_string_utf8(f, "\r\n")
