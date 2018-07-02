import math
import io
import pyembroidery.EmbPattern as EmbPattern
import pyembroidery.EmbThread as EmbThread
import pyembroidery.WriteHelper as helper

# Vp3 can encode signed 16 bit deltas.
MAX_JUMP_DISTANCE = 3200
# coded beyond 255 tho, they count as jumps.
MAX_STITCH_DISTANCE = 255


def vp3_write_string_8(stream, string):
    bytestring = bytes(string, "utf-8")
    vp3_write_length_and_bytes(stream, bytestring)


def vp3_write_string_16(stream, string):
    bytestring = bytes(string, "UTF-16BE")
    vp3_write_length_and_bytes(stream, bytestring)


def vp3_write_length_and_bytes(stream, bytestring):
    helper.write_int_16be(stream, len(bytestring))
    stream.write(bytestring)


def vp3_patch_byte_offset(stream, offset):
    currentPos = stream.tell();
    stream.seek(offset, 0)  # Absolute position seek.
    position = currentPos - offset - 4  # 4 bytes int32
    helper.write_int_32be(stream, position);
    stream.seek(currentPos, 0)  # Absolute position seek.


def get_as_colorblocks(pattern):
    thread_index = 0;
    last_pos = 0;
    end = len(pattern.stitches)
    for pos, stitch in enumerate(pattern.stitches):
        if stitch[2] != EmbPattern.COLOR_CHANGE:
            continue
        thread = pattern.get_thread_or_filler(thread_index)
        thread_index += 1;
        yield (pattern.stitches[last_pos:pos], thread)
        last_pos = pos;
    thread = pattern.get_thread_or_filler(thread_index)
    thread_index += 1;
    yield (pattern.stitches[last_pos:end], thread)


def write(pattern, f):
    pattern.fix_color_count();

    helper.write(f, "%vsm%")
    helper.write_int_8(f, 0)
    # vp3_write_string_16(f, "PyEmboridery");
    vp3_write_string_16(f, "Produced by     Software Ltd");
    write_file(pattern, f)


def write_file(pattern, f):
    f.write(b'\x00\x02\x00')
    placeholder_distance_end_of_file_block_020 = f.tell()
    helper.write_int_32le(f, 0)  # placeholder
    # This refers to the end of the final block, not entire bytes.

    vp3_write_string_16(f, "");
    # This is global notes and settings string.
    # "Setting:" followed by settings text.

    # vp3_write_string_16(f, "PyEmboridery");
    count_stitches = len(pattern.stitches)
    colorblocks = [i for i in get_as_colorblocks(pattern)]

    count_colorblocks_total = len(colorblocks)

    extends = pattern.extends()
    helper.write_int_32be(f, int(extends[2] * 100))  # right
    helper.write_int_32be(f, int(extends[1] * -100))  # -top
    helper.write_int_32be(f, int(extends[0] * 100))  # left
    helper.write_int_32be(f, int(extends[3] * -100))  # -bottom

    # EmbroiderModder Comment:
    # "this would be some(unknown) function of thread length"
    # Wilcom: 0C 54 == 3156
    # Note, this is the total stitch count, sans end command.
    ends = pattern.count_stitch_commands(EmbPattern.END);
    count_just_stitches = count_stitches - ends

    helper.write_int_32be(f, count_just_stitches);
    helper.write_int_8(f, 0);
    helper.write_int_8(f, count_colorblocks_total)
    helper.write_int_8(f, 12)  # 0xC
    helper.write_int_8(f, 0)

    count_designs = 1
    helper.write_int_8(f, count_designs)  # Number of designs.
    for i in range(0, count_designs):
        write_design_block(f, extends, colorblocks)
    vp3_patch_byte_offset(f, placeholder_distance_end_of_file_block_020)


def write_design_block(f, extends, colorblocks):
    f.write(b'\x00\x03\x00')
    placeholder_distance_end_of_design_block_030 = f.tell()
    helper.write_int_32be(f, 0)

    count_colorblocks_total = len(colorblocks)

    width = extends[2] - extends[0]
    height = extends[3] - extends[1]
    half_width = width / 2
    half_height = height / 2
    center_x = extends[2] - half_width
    center_y = extends[3] - half_height

    helper.write_int_32be(f, int(center_x) * 100)  # initial x
    helper.write_int_32be(f, int(center_y) * -100)  # initial y
    helper.write_int_8(f, 0)
    helper.write_int_8(f, 0)
    helper.write_int_8(f, 0)

    # extends 2
    helper.write_int_32be(f, int(half_width) * -100)
    helper.write_int_32be(f, int(half_width) * 100)
    helper.write_int_32be(f, int(half_height) * -100)
    helper.write_int_32be(f, int(half_height) * 100)

    helper.write_int_32be(f, int(width) * 100)
    helper.write_int_32be(f, int(height) * 100)
    vp3_write_string_16(f, "")  # This is notes and settings string.

    f.write(b'\x64\x64')  # helper.write_int_16be(f, 25700)
    # maybe b'dd', maybe 100, 100
    helper.write_int_32be(f, 4096)  # b'\x00\x00\x10\x00'
    helper.write_int_32be(f, 0)  # b'\x00\x00\x00\x00'
    helper.write_int_32be(f, 0)  # b'\x00\x00\x10\x00'
    helper.write_int_32be(f, 4096)  # b'\x00\x00\x10\x00'

    f.write(b'xxPP\x01\x00')

    vp3_write_string_16(f, "Produced by     Software Ltd");

    helper.write_int_16be(f, count_colorblocks_total)

    first = True;
    for colorblock in colorblocks:
        stitches = colorblock[0]
        thread = colorblock[1]
        write_vp3_colorblock(f, first, center_x, center_y, stitches, thread)
        first = False;
    vp3_patch_byte_offset(f, placeholder_distance_end_of_design_block_030)


def write_vp3_colorblock(f, first, center_x, center_y, stitches, thread):
    f.write(b'\x00\x05\x00')
    placeholder_distance_end_of_color_block_050 = f.tell();
    helper.write_int_32be(f, 0)

    first_pos_x = stitches[0][0]
    first_pos_y = stitches[0][1]
    if first:
        first_pos_x = 0
        first_pos_y = 0
    last_pos_x = stitches[-1][0]
    last_pos_y = stitches[-1][1]

    start_position_from_center_x = first_pos_x - center_x
    start_position_from_center_y = -(first_pos_y - center_y)
    helper.write_int_32be(f, int(start_position_from_center_x) * 100)
    helper.write_int_32be(f, int(start_position_from_center_y) * 100)

    vp3_write_thread(f, thread);

    block_shift_x = last_pos_x - first_pos_x
    block_shift_y = -(last_pos_y - first_pos_y)

    helper.write_int_32be(f, int(block_shift_x) * 100)
    helper.write_int_32be(f, int(block_shift_y) * 100)

    write_stitches_block(f, stitches, first_pos_x, first_pos_y)

    helper.write_int_8(f, 0)
    vp3_patch_byte_offset(f, placeholder_distance_end_of_color_block_050)


def vp3_write_thread(f, thread):
    f.write(b'\x01\x00')  # Single color, no transition.
    helper.write_int_24be(f, thread.color)
    f.write(b'\x00\x00\x00\x05\x28')  # no parts, no length, Rayon 40-weight
    if thread.catalog_number != None:
        vp3_write_string_8(f, thread.catalog_number)
    else:
        vp3_write_string_8(f, "")
    if thread.description != None:
        vp3_write_string_8(f, thread.description)
    else:
        vp3_write_string_8(f, thread.hex_color())
    if thread.brand != None:
        vp3_write_string_8(f, thread.brand)
    else:
        vp3_write_string_8(f, "")


def write_stitches_block(f, stitches, first_pos_x, first_pos_y):
    # Embroidermodder code has
    # vp3_write_string(f, "\x00");
    # The 0, x, 0 bytes come before placeholders
    # Given this consisistency, it's doubtful this is a string.
    # Those aren't
    f.write(b'\x00\x01\x00')
    placeholder_distance_to_end_of_stitches_block_010 = f.tell()
    helper.write_int_32be(f, 0)  # placeholder

    f.write(b'\x0A\xF6\x00')
    last_x = first_pos_x
    last_y = first_pos_y

    for stitch in stitches:
        x = stitch[0]
        y = stitch[1]
        flags = stitch[2]
        if flags == EmbPattern.END:
            f.write(b'\x80\x03')
            break;
        elif flags == EmbPattern.COLOR_CHANGE:
            continue;
        elif flags == EmbPattern.TRIM:
            continue;
        elif flags == EmbPattern.SEQUIN:
            continue;
        elif flags == EmbPattern.STOP:
            # Not sure what to do here.
            # f.write(b'\x80\x04')
            continue;
        elif flags == EmbPattern.JUMP:
            # Since VP3.Jump == VP3.Stitch, we combine jumps.
            continue;
        dx = int(x - last_x)
        dy = int(y - last_y)
        last_x = last_x + dx;
        last_y = last_y + dy;
        if flags == EmbPattern.STITCH:
            trimmed = False;
            if -127 <= dx <= 127 and -127 <= dy <= 127:
                helper.write_int_8(f, dx)
                helper.write_int_8(f, dy)
            else:
                f.write(b'\x80\x01')
                helper.write_int_16be(f, dx)
                helper.write_int_16be(f, dy)
                f.write(b'\x80\x02')
    # VSM gave ending stitches as 80 03 35 A5, so, 80 03 isn't strictly end.
    vp3_patch_byte_offset(f, placeholder_distance_to_end_of_stitches_block_010)
