
from .EmbConstant import *
from .EmbThreadJef import get_thread_set
from .WriteHelper import write_string_utf8, write_int_32le, write_int_8, write_int_array_8

STRIP_SEQUINS = True
FULL_JUMP = True
MAX_JUMP_DISTANCE = 127
MAX_STITCH_DISTANCE = 127

# These are in mm, embroidery units are 1/10 mm
HOOP_110X110 = 0
HOOP_50X50 = 1
HOOP_140X200 = 2
HOOP_126X110 = 3
HOOP_200X200 = 4


def write(pattern, f, settings=None):
    pattern.fix_color_count()
    color_count = pattern.count_threads()
    point_count = pattern.count_stitches()
    offsets = 0x74 + (color_count * 8)
    write_int_32le(f, offsets)
    write_int_32le(f, 0x14)
    write_string_utf8(f, "20122017218088")
    write_int_8(f, 0)
    write_int_8(f, 0)
    write_int_32le(f, color_count)
    write_int_32le(f, point_count)
    extends = pattern.extends()
    design_width = int(round(extends[2] - extends[0]))
    design_height = int(round(extends[3] - extends[1]))
    write_int_32le(f, get_jef_hoop_size(design_width, design_width))
    half_width = int(round(design_width / 2))
    half_height = int(round(design_height / 2))

    # distance from center of hoop.
    write_int_32le(f, half_width)
    write_int_32le(f, half_height)
    write_int_32le(f, half_width)
    write_int_32le(f, half_height)

    # distance from default 110 x 110 hoop
    x_hoop_edge = 550 - half_width
    y_hoop_edge = 550 - half_height
    write_hoop_edge_distance(f, x_hoop_edge, y_hoop_edge)

    # distance from default 50 x 50 hoop
    x_hoop_edge = 250 - half_width
    y_hoop_edge = 250 - half_height
    write_hoop_edge_distance(f, x_hoop_edge, y_hoop_edge)

    # distance from default 140 x 200 hoop
    x_hoop_edge = 700 - half_width
    y_hoop_edge = 1000 - half_height
    write_hoop_edge_distance(f, x_hoop_edge, y_hoop_edge)

    # distance from default 126 x 50 hoop
    x_hoop_edge = 630 - half_width
    y_hoop_edge = 550 - half_height
    write_hoop_edge_distance(f, x_hoop_edge, y_hoop_edge)

    jef_threads = get_thread_set()
    for thread in pattern.threadlist:
        thread_index = thread.find_nearest_color_index(jef_threads)
        write_int_32le(f, thread_index)

    for i in range(0, color_count):
        write_int_32le(f, 0x0D)

    xx = 0
    yy = 0
    data = NO_COMMAND
    for stitch in pattern.stitches:
        x = stitch[0]
        y = stitch[1]
        data = stitch[2]
        dx = x - xx
        dy = y - yy
        encoded_bytes = jef_encode(dx, -dy, data)
        write_int_array_8(f, encoded_bytes)
        xx = x
        yy = y
    if data != END:
        f.write(b'\x80\x10')


def get_jef_hoop_size(width,height):
    if width < 500 and height < 500:
        return HOOP_50X50
    if width < 1100 and height < 1100:
        return HOOP_110X110
    if width < 1400 and height < 2000:
        return HOOP_140X200
    return HOOP_200X200


def jef_encode(dx, dy, data):
    if data == STITCH:
        return [int(dx), int(dy)]
    if data == COLOR_CHANGE:
        return [0x80, 0x01, int(dx), int(dy)]
    if data == STOP:
        return [0x80, 0x01, int(dx), int(dy)]
    if data == END:
        return [0x80, 0x10, int(dx), int(dy)]
    if data == JUMP:
        return [0x80, 0x02, int(dx), int(dy)]
    if data == TRIM:
        return [0x80, 0x02, int(dx), int(dy)]
    return [dx, dy]


def write_hoop_edge_distance(f, x_hoop_edge, y_hoop_edge):
    if min(x_hoop_edge, y_hoop_edge) >= 0:
        write_int_32le(f, x_hoop_edge)  # left
        write_int_32le(f, y_hoop_edge)  # top
        write_int_32le(f, x_hoop_edge)  # right
        write_int_32le(f, y_hoop_edge)  # bottom
    else:
        write_int_32le(f, -1)
        write_int_32le(f, -1)
        write_int_32le(f, -1)
        write_int_32le(f, -1)
