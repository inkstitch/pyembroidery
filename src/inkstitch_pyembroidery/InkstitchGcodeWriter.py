import math
from itertools import cycle

from .EmbFunctions import *
from .WriteHelper import write_string_utf8

# This writer is in a different file because our version is substantially
# different from upstream's.  This way we make merge conflicts less likely.

STRIP_SPEEDS = True
SEQUIN_CONTINGENCY = CONTINGENCY_SEQUIN_STITCH
MAX_JUMP_DISTANCE = float('inf')
MAX_STITCH_DISTANCE = float('inf')


def write(pattern, f, settings=None):
    if settings is None:
        settings = {}

    flip_x = settings.get('flip_x', True)
    flip_y = settings.get('flip_y', True)
    alternate_z_value = settings.get('alternate_z', True)
    stitch_z_travel = settings.get('stitch_z_travel', 5)

    custom_stitch = settings.get('custom_stitch', '')
    custom_color_change = settings.get('custom_color_change', '')
    custom_frameout = settings.get('custom_frameout', '')
    custom_stop = settings.get('custom_stop', '')
    custom_start = settings.get('custom_start', '')
    custom_end = settings.get('custom_end', '')

    threadlist = pattern.threadlist
    current_thread = 0

    laser_mode = settings.get('laser_mode', False)
    dynamic_laser_power = settings.get('dynamic_laser_power', True)
    laser_warm_up_time = settings.get('laser_warm_up_time', 0)
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

    if custom_start == '' or laser_mode:
        init(f, laser_mode, dynamic_laser_power, max_spindle_speed, min_spindle_speed, spindle_speed, feed_rate)
    else:
        # They may want to set the inital thread color
        thread = threadlist[current_thread]
        custom_start = custom_start.replace(
            "%R", str("%.0f" % thread.get_red())
        ).replace(
            "%G", str("%.0f" % thread.get_green())
        ).replace(
            "%B", str("%.0f" % thread.get_blue())
        ).split('\\n')
        for value in custom_start:
            write_string_utf8(f, "%s\r\n" % value.strip())
        write_string_utf8(f, "\r\n")

    z = 0
    alternate_z = cycle(list(range(2)))
    stitching = False
    for x, y, command in pattern.stitches:
        command = command & COMMAND_MASK

        # embroidery G-code discussion: https://github.com/inkstitch/inkstitch/issues/335
        if command == STITCH:
            if flip_x:
                x = -x
            if flip_y:
                y = -y

            # pyembroidery natively uses tenths of a millimeter
            x /= 10.0
            y /= 10.0

            if alternate_z_value:
                # alternates the z value between 0 and 1
                z = next(alternate_z)
            elif stitch_z_travel > 0.0001:
                # For DIY embroidery machines, stitching is modeled as continuous
                # travel on the Z axis.  The Z motor is hooked up to the hand wheel
                # of the sewing machine.  For each stitch, we "move" in the Z
                # direction, which turns the wheel and causes the machine to
                # stitch.
                z += stitch_z_travel

            # custom stitch
            if custom_stitch != '' and not laser_mode:
                custom_stitch_value = custom_stitch.replace("%X", str("%.3f" % x)).replace("%Y", str("%.3f" % y)).replace("%Z", str("%.1f" % z)).split('\\n')
                for value in custom_stitch_value:
                    write_string_utf8(f, "%s\r\n" % (value.strip()))
                continue

            # default stitch
            if stitching and spindle_speed >= 0 and feed_rate >= 0:
                command = "G1"
            else:
                # G0 automatically turns off the laser for the move.
                command = "G0"

            write_string_utf8(f, "%s X%.3f Y%.3f\r\n" % (command, x, y))
            if alternate_z_value or stitch_z_travel > 0.0001:
                write_string_utf8(f, "G0 Z%.1f\r\n" % z)

            # If we're about to cut, wait and let the laser warm up.
            if not stitching and laser_mode and laser_warm_up_time > 0:
                write_string_utf8(f, "G1 G4 P%.2f (wait for laser to warm up)\r\n" % laser_warm_up_time)

            stitching = True
        elif command == COLOR_CHANGE and not laser_mode:
            current_thread += 1
            thread = threadlist[current_thread]
            if custom_color_change == '':
                color_change = ['M00']
            else:
                color_change = custom_color_change.replace(
                    "%R", str("%.0f" % thread.get_red())
                ).replace(
                    "%G", str("%.0f" % thread.get_green())
                ).replace(
                    "%B", str("%.0f" % thread.get_blue())
                ).split('\\n')
            if custom_color_change not in ['None', 'none']:
                for value in color_change:
                    write_string_utf8(f, "%s\r\n" % value.strip())
        elif command == STOP and not laser_mode:
            if custom_stop != '':
                stop = custom_stop.replace('%X', str(x)).replace('%Y', str(y)).split('\\n')
            else:
                # Move to frame out position
                stop = ['G0 X%.3f Y%.3f' % (x, y)]
                # and stop
                stop.append('M00')
            if custom_stop not in ['None', 'none']:
                for value in stop:
                    write_string_utf8(f, "%s\r\n" % value.strip())
        else:
            stitching = False

    write_string_utf8(f, "\r\n")
    if custom_end == '':
        write_string_utf8(f, "G0 X0.0 Y0.0\r\n")
        write_string_utf8(f, "M30\r\n")
    else:
        for value in custom_end.strip().split('\\n'):
            write_string_utf8(f, "%s\r\n" % value.strip())


def init(f, laser_mode, dynamic_laser_power, max_spindle_speed, min_spindle_speed, spindle_speed, feed_rate):
    write_string_utf8(f, "G90 (use absolute coordinates)\r\n")
    write_string_utf8(f, "G21 (coordinates will be specified in millimeters)\r\n")

    if max_spindle_speed >= 0:
        write_string_utf8(f, "$30=%d (S value used for maximum spindle speed or laser power)\r\n" % max_spindle_speed)

    if min_spindle_speed >= 0:
        write_string_utf8(f, "$31=%d (S value used for minimum spindle speed or laser power)\r\n" % min_spindle_speed)

    if laser_mode:
        write_string_utf8(f, "$32=1 (enable grbl laser mode)\r\n")

        if dynamic_laser_power:
            write_string_utf8(f, "M4 (use dynamic laser power)\r\n")
        else:
            write_string_utf8(f, "M3 (use constant laser power)\r\n")

    write_string_utf8(f, "G0 X0.0 Y0.0\r\n")

    if spindle_speed > 0 and feed_rate > 0:
        write_string_utf8(f, "G1 X0 Y0 S%d F%d\r\n" % (spindle_speed, feed_rate))

    write_string_utf8(f, "\r\n")
