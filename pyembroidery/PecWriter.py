import math
import io
import pyembroidery.EmbPattern as EmbPattern
import pyembroidery.EmbThread as EmbThread
import pyembroidery.EmbThreadPec as EmbThreadPec
import pyembroidery.WriteHelper as helper
import pyembroidery.PecGraphics as PecGraphics

MAX_JUMP_DISTANCE = 2047
MAX_STITCH_DISTANCE = 2047

MASK_07_BIT = 0b01111111
JUMP_CODE = 0b00010000
TRIM_CODE = 0b00100000
FLAG_LONG = 0b10000000
PEC_ICON_WIDTH = 48
PEC_ICON_HEIGHT = 38


def write(pattern, f):
    f.write(bytes("#PEC0001", 'utf8'))
    write_pec_stitches(pattern, f)


def encode_long_form(value):
    value &= 0b0000111111111111
    value |= 0b1000000000000000
    return value


def flag_jump(longForm):
    return longForm | (JUMP_CODE << 8)


def flag_trim(longForm):
    return longForm | (TRIM_CODE << 8)


def pec_encode(pattern, f):
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
        elif data == EmbPattern.JUMP:
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
        elif data == EmbPattern.COLOR_CHANGE:
            if jumping:
                f.write(b'\x00\x00')
                jumping = False
            f.write(b'\xfe\xb0')
            if color_two:
                f.write(b'\x02')
            else:
                f.write(b'\x01')
        elif data == EmbPattern.STOP:
            if jumping:
                f.write(b'\x00\x00')
                jumping = False
            f.write(b'\x80\x01\x00\x00')
        elif data == EmbPattern.END:
            if jumping:
                f.write(b'\x00\x00')
                jumping = False
            f.write(b'\xff')
        xx = x
        yy = y


def write_pec_stitches(pattern, f):
    extends = pattern.extends()
    width = extends[2] - extends[0]
    height = extends[3] - extends[1]

    name = pattern.name
    if name == None:
        name = "Untitled"
    name = name[:8]
    f.write(bytes("LA:%-16s\r" % (name), 'utf8'))
    f.write(b'\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\xFF\x00\x06\x26')

    pattern.fix_color_count()
    thread_set = EmbThreadPec.get_thread_set()
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
