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


def write(pattern: EmbPattern, file):
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
        if data is not EmbPattern.END:
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
    if data is EmbPattern.STITCH:
        return [dx, dy]
    if data is EmbPattern.COLOR_CHANGE:
        return [0x80, 0x01, dx, dy]
    if data is EmbPattern.STOP:
        return [0x80, 0x01, dx, dy]
    if data is EmbPattern.END:
        return [0x80, 0x10, dx, dy]
    if data is EmbPattern.JUMP:
        return [0x80, 0x02, dx, dy]
    if data is EmbPattern.TRIM:
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

def encode_long_form(value: int) -> int:
    value &= 0b00001111_11111111
    value |= 0b10000000_00000000
    return value


def flag_jump(longForm: int) -> int:
    return longForm | (JUMP_CODE << 8)


def flag_trim(longForm: int) -> int:
    return longForm | (TRIM_CODE << 8)


def pec_encode(pattern: EmbPattern, f):
    color_change_jump = False
    color_two = True
    jumping = False
    stitches = pattern.stitches
    xx = 0
    yy = 0
    for stitch in stitches:
        x = stitch[0]
        y = stitch[1]
        data = stitch[2]
        dx = x - xx
        dy = y - yy
        if data is EmbPattern.STITCH:
            delta_x = round(dx)
            delta_y = round(dy)
            if jumping and delta_x is not 0 and delta_y is not 0:
                f.write(b'\x00\x00')
                jumping = False
            if -64 < delta_x < 63 and -64 < delta_y < 63:
                f.write(bytes([delta_x & MASK_07_BIT, delta_y & MASK_07_BIT]))
            else:
                delta_x = encode_long_form(delta_x)
                delta_y = encode_long_form(delta_y)
                data = [
                    (delta_x >> 8) & 0xFF,
                    delta_x & 0xFF,
                    (delta_y >> 8) & 0xFF,
                    delta_y & 0xFF]
                f.write(bytes(data))
        elif data is EmbPattern.JUMP:
            jumping = True
            delta_x = round(dx)
            delta_x = encode_long_form(delta_x)
            if color_change_jump:
                delta_x = flag_jump(delta_x)
            else:
                delta_x = flag_trim(delta_x)
            delta_y = round(dy)
            delta_y = encode_long_form(delta_y)
            if color_change_jump:
                delta_y = flag_jump(delta_y)
            else:
                delta_y = flag_trim(delta_y)
            f.write(bytes([
                (delta_x >> 8) & 0xFF,
                delta_x & 0xFF,
                (delta_y >> 8) & 0xFF,
                delta_y & 0xFF
            ]))
            color_change_jump = False
        elif data is EmbPattern.COLOR_CHANGE:
            if jumping:
                f.write(b'\x00\x00')
                jumping = False
            f.write(b'\xfe\xb0')
            if color_two:
                f.write(b'\x02')
            else:
                f.write(b'\x01')
        elif data is EmbPattern.STOP:
            if jumping:
                f.write(b'\x00\x00')
                jumping = False
            f.write(b'\x80\x01\x00\x00')
        elif data is EmbPattern.END:
            if jumping:
                f.write(b'\x00\x00')
                jumping = False
            f.write(b'\xff')
        xx = x
        yy = y


def write_pec_stitches(pattern: EmbPattern, f):
    extends = pattern.extends()
    width = extends[2] - extends[0]
    height = extends[3] - extends[1]

    name = pattern.name
    if name is None:
        name = "Untitled"
    name = name[:8]
    f.write(bytes("LA:%-16s\r" % (name), 'utf8'))
    f.write(b'\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\xFF\x00\x06\x26')

    pattern.fix_color_count()
    thread_set = EmbThreadPec.getThreadSet()
    chart = [None] * len(thread_set)
    for thread in set(pattern.threadlist):
        index = thread.find_nearest_color_index(thread_set)
        thread_set[index] = None
        chart[index] = thread

    colorlist = []
    for thread in pattern.threadlist:
        colorlist.append(thread.find_nearest_color_index(chart))
    current_thread_count = len(colorlist)
    if current_thread_count is not 0:
        f.write(b'\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20')
        colorlist.insert(0, current_thread_count - 1)
        f.write(bytes(colorlist))
    else:
        f.write(b'\x20\x20\x20\x20\x64\x20\x00\x20\x00\x20\x20\x20\xFF')
    for i in range(current_thread_count, 463):
        f.write(b'\x20')  # 520
    f.write(b'\x00\x00')
    stitch_encode = io.BytesIO()
    pec_encode(pattern, stitch_encode)
    graphics_offset_value = stitch_encode.tell() + 20
    helper.write_int_24le(f, graphics_offset_value)
    f.write(b'\x31\xff\xf0')
    helper.write_int_16le(f, round(width))
    helper.write_int_16le(f, round(height))
    helper.write_int_16le(f, 0x1E0)
    helper.write_int_16le(f, 0x1B0)

    helper.write_int_16le(f, 0x9000 | -round(extends[0]))
    helper.write_int_16le(f, 0x9000 | -round(extends[1]))
    pec_encode(pattern, f)
    # shutil.copyfileobj(encodef, f)

    blank = PecGraphics.blank

    f.write(bytes(blank))
    for i in range(0, current_thread_count):
        f.write(bytes(blank))
