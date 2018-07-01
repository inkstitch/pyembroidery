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


def vp3_patch_byte_count(stream, offset, adjustment):
    currentPos = stream.tell();
    stream.seek(offset, 0)  # Absolute position seek.
    # helper.write_int_32be(stream, currentPos - offset + adjustment);
    helper.write_int_32be(stream, currentPos + 1 + adjustment);
    stream.seek(currentPos, 0)  # Absolute position seek.


def vp3_patch_byte_offset(stream, offset, adjustment):
    currentPos = stream.tell();
    stream.seek(offset, 0)  # Absolute position seek.
    helper.write_int_32be(stream, currentPos - offset + adjustment);
    stream.seek(currentPos, 0)  # Absolute position seek.


# calculated extends[2]: 1560
# calculated extends[1]: -119
# calculated extends[0]: -730
# calculated extends[3]: 1094

# Wilcom extends 1
# 00 02 61 60 ==  156_000
# 00 00 2E 7C ==   11_900
# FF FE E2 D8 ==  -73_000
# FF FE 54 A8 == -109_400

# Note: ((156 + 73) / 2) = 114.5
# Note: ((11.9 + 109.4) / 2) = 60.65

# Note: 156 - 114.5 = 41.5 (initial x)
# Note: 11.9 - 60.65 = -48.75 (initial y)

# Wilcom extends 2
# FF FE 40 BC == -114_500
# 00 01 BF 44 ==  114_500
# FF FF 13 48 ==  -60_600
# 00 00 EC B8 ==   60_600

def write(pattern, f):
    pattern.fix_color_count();

    helper.write(f, "%vsm%")
    helper.write_int_8(f, 0)
    # vp3_write_string_16(f, "PyEmboridery");
    vp3_write_string_16(f, "Produced by     Software Ltd");

    f.write(b'\x00\x02\x00')
    placeholder_distance_end_of_file_020 = f.tell()
    helper.write_int_32le(f, 0)  # placeholder
    # This refers to the end of the final block, not entire bytes.

    vp3_write_string_16(f, "");

    # vp3_write_string_16(f, "PyEmboridery");
    count_stitches = len(pattern.stitches)
    colorblocks = [i for i in get_as_colorblocks(pattern)]

    count_threads = len(colorblocks)

    extends = pattern.extends()
    width = extends[2] - extends[0]
    height = extends[3] - extends[1]
    half_width = width / 2
    half_height = height / 2
    center_x = extends[2] - half_width
    center_y = extends[3] - half_height

    # Check this on review of embroidermodder
    # extends 1
    helper.write_int_32be(f, int(extends[2] * 100))  # right
    helper.write_int_32be(f, int(extends[1] * -100))  # -top
    helper.write_int_32be(f, int(extends[0] * 100))  # left
    helper.write_int_32be(f, int(extends[3] * -100))  # -bottom

    # EmbroiderModder Comment:
    # "this would be some(unknown) function of thread length"
    # Wilcom: 0C 54 == 3156
    # Note, this is the total stitch count, sans end.
    ends = pattern.count_stitch_commands(EmbPattern.END);
    count_just_stitches = count_stitches - ends
    helper.write_int_32be(f, count_just_stitches);

    helper.write_int_8(f, 0);
    # Embroidermodder loops here to count colors.

    helper.write_int_8(f, count_threads)

    helper.write_int_8(f, 12)
    helper.write_int_8(f, 0)
    helper.write_int_8(f, 1)

    f.write(b'\x00\x03\x00')
    placeholder_distance_end_of_file_030 = f.tell()
    helper.write_int_32be(f, 0)  # placeholder2
    # This is length to end of file.

    # Generated:
    # Centerx, centery: 00 00 D0 FC 00 00 A5 A0 == 53500, 42400

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
    vp3_write_string_16(f, "");

    f.write(b'\x64\x64')  # helper.write_int_16be(f, 25700)
    # maybe b'dd'
    helper.write_int_32be(f, 4096)  # b'\x00\x00\x10\x00'
    helper.write_int_32be(f, 0)  # b'\x00\x00\x00\x00'
    helper.write_int_32be(f, 0)  # b'\x00\x00\x10\x00'
    helper.write_int_32be(f, 4096)  # b'\x00\x00\x10\x00'

    f.write(b'xxPP\x01\x00')

    vp3_write_string_16(f, "Produced by     Software Ltd");

    helper.write_int_16be(f, count_threads)

    first = True;
    for colorblock in colorblocks:
        stitches = colorblock[0]
        thread = colorblock[1]
        write_vp3_block(f, first, center_x, center_y, stitches, thread)
        first = False;
    vp3_patch_byte_offset(f, placeholder_distance_end_of_file_030, -4)
    vp3_patch_byte_offset(f, placeholder_distance_end_of_file_020, -4)


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


def write_vp3_block(f, first, center_x, center_y, stitches, thread):
    f.write(b'\x00\x05\x00')
    placeholder_distance_to_next_block_050 = f.tell();
    helper.write_int_32be(f, 0)

    first_pos_x = stitches[0][0]
    first_pos_y = stitches[0][1]
    if first:
        first_pos_x = 0
        first_pos_y = 0
    last_pos_x = stitches[-1][0]
    last_pos_y = stitches[-1][1]

    # Centerx, centery: 00 00 D0 FC 00 00 A5 A0 == 53500, 42400

    # BLOCK 1: FF FF 2F 04 FF FF 5A 60. -53500, -42400
    # BLOCK 2: FF FF 59 FC FF FF 38 64. -42500, -51100
    # BLOCK 3: 00 00 E0 9C FF FF FC E0. 57500, -800
    start_position_from_center_x = first_pos_x - center_x
    start_position_from_center_y = -(first_pos_y - center_y)
    helper.write_int_32be(f, int(start_position_from_center_x) * 100)
    helper.write_int_32be(f, int(start_position_from_center_y) * 100)

    # blockshift - centerx; 00 00 AD D4 00 00 C7 9C, 44500, 51100

    vp3_write_thread(f, thread);
    # Block 1: 00 00 2A F8 FF FF DE 04. 11000, -8700
    # Block 2: 00 01 86 A0 00 00 C4 7C. 100000, 50300
    # Block 3: FF FF A6 28 00 00 DF 0C. -23000, 57100

    #first-last1: 00 00 2A F8 FF FF DE 04
    #first-last2: 00 01 86 A0 00 00 C4 7C
    #first-last3: FF FF A6 28 00 00 DF 0C

    block_shift_x = last_pos_x - first_pos_x
    block_shift_y = -(last_pos_y - first_pos_y)

    helper.write_int_32be(f, int(block_shift_x) * 100)
    helper.write_int_32be(f, int(block_shift_y) * 100)

    #Firstgen = 00 00 23 28 FF FF DE 04,9000,

    # Embroidermodder code has
    # vp3_write_string(f, "\x00");
    # The 0, x, 0 bytes come before placeholders
    # 0, 5, 0
    # 0, 2, 0
    # Given this consisistency, it's doubtful this is a string.
    # Those aren't
    f.write(b'\x00\x01\x00')
    placeholder_distance_to_block_end_010 = f.tell()
    helper.write_int_32be(f, 0)  # placeholder

    f.write(b'\x0A\xF6\x00')
    last_x = first_pos_x
    last_y = first_pos_y

    # stitches cut at 255, -465,355
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
            #f.write(b'\x80\x04')
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
    vp3_patch_byte_offset(f, placeholder_distance_to_block_end_010, -4)
    helper.write_int_8(f, 0)
    vp3_patch_byte_offset(f, placeholder_distance_to_next_block_050, -4)


def vp3_write_thread(f, thread):
    f.write(b'\x01\x00')
    helper.write_int_24be(f,thread.color)
    f.write(b'\x00\x00\x00\x05\x28')

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
