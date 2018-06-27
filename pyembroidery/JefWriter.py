import math
import io
import pyembroidery.EmbPattern as EmbPattern
import pyembroidery.EmbThread as EmbThread
import pyembroidery.EmbThreadJef as JefThread
import pyembroidery.WriteHelper as helper

MAX_JUMP_DISTANCE = 127
MAX_STITCH_DISTANCE = 127

# These are in mm, embroidery units are 1/10 mm
HOOP_110X110 = 0
HOOP_50X50 = 1
HOOP_140X200 = 2
HOOP_126X110 = 3
HOOP_200X200 = 4


def write(pattern, file):
    with open(file, "wb") as f:
        pattern.fix_color_count();
        color_count = pattern.count_threads();
        point_count = pattern.count_stitches();
        offsets = 0x74 + (color_count * 8);
        helper.write_int_32le(f, offsets)
        helper.write_int_32le(f, 0x14)
        helper.write(f, "20122017218088")
        helper.write_int_8(f, 0);
        helper.write_int_8(f, 0);
        helper.write_int_32le(f, color_count);
        helper.write_int_32le(f, point_count);
        extends = pattern.extends();
        design_width = round(extends[2] - extends[0]);
        design_height = round(extends[3] - extends[1]);
        helper.write_int_32le(f, get_jef_hoop_size(design_width, design_width))
        half_width = round(design_width / 2)
        half_height = round(design_height / 2)

        # distance from center of hoop.
        helper.write_int_32le(f, half_width)
        helper.write_int_32le(f, half_height)
        helper.write_int_32le(f, half_width)
        helper.write_int_32le(f, half_height)

        # distance from default 110 x 110 hoop
        x_hoop_edge = 550 - half_width
        y_hoop_edge = 550 - half_height
        write_hoop_edge_distance(f,x_hoop_edge,y_hoop_edge)

        #distance from default 50 x 50 hoop
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

        jef_threads = JefThread.get_thread_set()
        for thread in pattern.threadlist:
            thread_index = thread.find_nearest_color_index(jef_threads)
            helper.write_int_32le(f, thread_index)

        for i in range(0,color_count):
            helper.write_int_32le(f, 0x0D)

        xx = 0
        yy = 0
        data = EmbPattern.NO_COMMAND
        for stitch in pattern.stitches:
            x = stitch[0]
            y = stitch[1]
            data = stitch[2]
            dx = x - xx
            dy = y - yy
            encoded_bytes = jef_encode(dx, -dy, data)
            helper.write_int_array_8(f, encoded_bytes)
            xx = x
            yy = y
        if data != EmbPattern.END:
            f.write(b'\x80\x10')


def get_jef_hoop_size(width: int, height: int) -> int:
    if width < 500 and height < 500:
        return HOOP_50X50
    if width < 1100 and height < 1100:
        return HOOP_110X110
    if width < 1400 and height < 2000:
        return HOOP_140X200
    return HOOP_200X200

def jef_encode(dx, dy, data):
    if data == EmbPattern.STITCH:
        return [dx, dy]
    if data == EmbPattern.COLOR_CHANGE:
        return [0x80, 0x01, dx, dy]
    if data == EmbPattern.STOP:
        return [0x80, 0x01, dx, dy]
    if data == EmbPattern.END:
        return [0x80, 0x10, dx, dy]
    if data == EmbPattern.JUMP:
        return [0x80, 0x02, dx, dy]
    if data == EmbPattern.TRIM:
        return [0x80, 0x02, dx, dy]
    return [dx, dy]


def write_hoop_edge_distance(f, x_hoop_edge, y_hoop_edge):
    if min(x_hoop_edge, y_hoop_edge) >= 0:
        helper.write_int_32le(f, x_hoop_edge)  # left
        helper.write_int_32le(f, y_hoop_edge)  # top
        helper.write_int_32le(f, x_hoop_edge)  # right
        helper.write_int_32le(f, y_hoop_edge)  # bottom
    else:
        helper.write_int_32le(f, -1);
        helper.write_int_32le(f, -1);
        helper.write_int_32le(f, -1);
        helper.write_int_32le(f, -1);