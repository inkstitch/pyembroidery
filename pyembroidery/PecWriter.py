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


def write(pattern, f, settings=None):
    f.write(bytes("#PEC0001", 'utf8'))
    write_pec(pattern, f)


def write_pec(pattern, f):
    extends = pattern.extends()
    pattern.fix_color_count()

    write_pec_header(pattern, f)
    write_pec_block(pattern, f, extends)
    write_pec_graphics(pattern, f, extends)


def write_pec_header(pattern, f):
    name = pattern.get_metadata("name", "Untitled")
    f.write(bytes("LA:%-16s\r" % (name[:8]), 'utf8'))
    f.write(b'\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\xFF\x00')
    helper.write_int_8(f, int(PEC_ICON_WIDTH / 8))  # PEC BYTE STRIDE
    helper.write_int_8(f, int(PEC_ICON_HEIGHT))  # PEC ICON HEIGHT

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


def write_pec_block(pattern, f, extends):
    width = extends[2] - extends[0]
    height = extends[3] - extends[1]

    stitch_block_start_position = f.tell();
    f.write(b'\x00\x00')
    helper.write_int_24le(f, 0)  # Space holder.
    f.write(b'\x31\xff\xf0')
    helper.write_int_16le(f, round(width))
    helper.write_int_16le(f, round(height))
    helper.write_int_16le(f, 0x1E0)
    helper.write_int_16le(f, 0x1B0)

    helper.write_int_16le(f, 0x9000 | -round(extends[0]))
    helper.write_int_16le(f, 0x9000 | -round(extends[1]))

    pec_encode(pattern, f)

    stitch_block_length = f.tell() - stitch_block_start_position

    current_position = f.tell();
    f.seek(stitch_block_start_position + 2, 0)
    helper.write_int_24le(f, stitch_block_length)
    f.seek(current_position, 0)


def write_pec_graphics(pattern, f, extends):
    blank = PecGraphics.get_blank()
    for block in pattern.get_as_stitchblock():
        stitches = block[0]
        PecGraphics.draw_scaled(extends, stitches, blank, 6, 4)
    f.write(bytes(blank))

    for block in pattern.get_as_colorblocks():
        stitches = [s for s in block[0] if s[2] == EmbPattern.STITCH]
        blank = PecGraphics.get_blank()  # [ 0 ] * 6 * 38
        PecGraphics.draw_scaled(extends, stitches, blank, 6)
        f.write(bytes(blank))


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
            color_two = not color_two
        elif data == EmbPattern.STOP:
            # if jumping:
            #     f.write(b'\x00\x00')
            #     jumping = False
            # f.write(b'\x80\x01\x00\x00')
            pass
        elif data == EmbPattern.END:
            if jumping:
                f.write(b'\x00\x00')
                jumping = False
            f.write(b'\xff')
        xx = x
        yy = y
