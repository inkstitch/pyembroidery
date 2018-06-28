import math
import io
import pyembroidery.EmbPattern as EmbPattern
import pyembroidery.EmbThread as EmbThread
import pyembroidery.WriteHelper as helper

# Vp3 can encode signed 16 bit deltas.
MAX_JUMP_DISTANCE = 3200
MAX_STITCH_DISTANCE = 3200


def vp3_write_string_8(stream, string):
    bytestring = bytes(string, "utf-8")
    vp3_write_length_and_bytes(stream, bytestring)


def vp3_write_string_16(stream, string):
    bytestring = bytes(string, "UTF-16BE")
    vp3_write_length_and_bytes(stream, bytestring)


def vp3_write_length_and_bytes(stream, bytestring):
    helper.write_int_16be(stream, len(bytestring))
    stream.write(bytestring)


def vp3_patch_byte_count(stream, offset):
    currentPos = stream.tell();
    stream.seek(offset, 0)  # Absolute position seek.
    # helper.write_int_32be(stream, currentPos - offset + adjustment);
    helper.write_int_32be(stream, currentPos + 1);
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
    placeholder_position_end_final_block = f.tell()
    helper.write_int_32le(f, 0)  # placeholder
    # This refers to the end of the final block, not entire bytes.

    vp3_write_string_16(f, "");
    # vp3_write_string_16(f, "PyEmboridery");

    count_stitches = len(pattern.stitches)
    count_threads = len(pattern.threadlist)

    extends = pattern.extends()
    width = extends[2] - extends[0]
    height = extends[3] - extends[1]
    half_width = width / 2
    half_height = height / 2
    initial_x = extends[2] - half_width
    initial_y = extends[3] - half_height

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
    placeholder_length_to_end_of_file = f.tell()
    helper.write_int_32be(f, 0)  # placeholder2
    # This is length to end of file.

    # 00 00 A2 1C == 41500
    # FF FF 41 C4 == -48700
    helper.write_int_32be(f, int(initial_x) * 100)  # initial x
    helper.write_int_32be(f, int(initial_y) * -100)  # initial y

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

    thread_index = 0

    current_thread = None
    stitch_index = 0
    first_stitch_block = True
    last_x = 0;
    last_y = 0;
    block_shift_x = 0
    block_shift_y = 0
    while stitch_index < count_stitches:
        # skip non-stitch elements.
        # calculate frame shift.
        frame_x_initial = last_x
        frame_y_initial = last_y
        while stitch_index < count_stitches:
            stitch = pattern.stitches[stitch_index]
            if stitch[2] != EmbPattern.STITCH:
                stitch_index += 1
            else:
                break;

        # break if we ran out of elements
        if stitch_index == count_stitches:
            break;

        seek_index = stitch_index + 1;
        while seek_index < count_stitches:
            stitch = pattern.stitches[seek_index]
            if stitch[2] == EmbPattern.STITCH:
                seek_index += 1
            else:
                break;
        seek_index -= 1;
        block_end_stitch = pattern.stitches[seek_index]
        block_shift_x = block_end_stitch[0] - block_shift_x
        block_shift_y = block_end_stitch[1] - block_shift_y

        # this element goes between stitch blocks.
        if not first_stitch_block:
            helper.write_int_8(f, 0)

        # position of the end of this block.
        f.write(b'\x00\x05\x00')
        placeholder_jump_to_next_block = f.tell();
        helper.write_int_32be(f, 0)  # placeholder

        current_thread = pattern.get_thread_or_filler(thread_index)
        # current_thread = pattern.threadlist[thread_index]
        thread_index += 1;

        # In embroidermodder this is wrong.
        # It gets the dx value and feeds that into that value
        # and iterates the stitch, but that value is simply
        # frameshift to center.

        # stitch = pattern.stitches[stitch_index]
        # x = round(stitch[0])
        # y = round(stitch[1])

        # Wilcom FF FF 5D E4 == -41500
        # Wilcom 00 00 BE 3C == 48700
        # Note: flipped values of the earlier initial_x, initial_y
        # 41500, -48700

        # This needs to be recalculated. It's the difference between layers, as well.
        # between 1st and 2nd it's: -18.5 -48.6
        helper.write_int_32be(f, int(initial_x) * -100)
        helper.write_int_32be(f, int(initial_y) * 100)

        # Embroidermodder incremented here, however I didn't
        # use that stitch.

        # is this position actually stitched? or the start position?
        # stitch = pattern.stitches[stitch_index]
        # last_x = stitch[0];
        # last_y = stitch[1];
        # stitch_index += 1
        # last_color = current_thread;

        # b'\x01\x00'
        helper.write_int_8(f, 1)
        helper.write_int_8(f, 0)

        helper.write_int_8(f, current_thread.get_red())
        helper.write_int_8(f, current_thread.get_green())
        helper.write_int_8(f, current_thread.get_blue())

        # b'\x00\x00\x00\x05\x28
        helper.write_int_8(f, 0)
        helper.write_int_8(f, 0)
        helper.write_int_8(f, 0)
        helper.write_int_8(f, 5)
        helper.write_int_8(f, 40)

        # vp3_write_string_8(f, "1")
        # vp3_write_string_8(f, "Blue")
        # vp3_write_string_8(f, "Wilcom")

        if current_thread.catalog_number != None:
            vp3_write_string_8(f, current_thread.catalog_number)
        else:
            vp3_write_string_8(f, "")
        if current_thread.description != None:
            vp3_write_string_8(f, current_thread.description)
        else:
            vp3_write_string_8(f, current_thread.hex_color())
        if current_thread.brand != None:
            vp3_write_string_8(f, current_thread.brand)
        else:
            vp3_write_string_8(f, "")

        # First iteration
        # Wilcom: 00 00 59 D8 == 23_000
        # Wilcom: FF FE 83 EC == -97_300
        # Second layer
        # Wilcom: 00 02 07 88 == 133_000
        # Wilcom: 00 00 00 00 == 0
        # Note 23_000 + 133_000 = 156_000 the max_x value.
        # Note the y shift between block ends (layer 2) is actually 0.

        # Shift from first to last position.
        helper.write_int_32be(f, int(block_shift_x) * 100)
        # wilcom has position data here.
        helper.write_int_32be(f, int(block_shift_y) * -100)
        # wilcom has position data here.

        # Embroidermodder code has
        # vp3_write_string(f, "\x00");
        # The 0, x, 0 bytes come before placeholders
        # 0, 5, 0
        # 0, 2, 0
        # Given this consisistency, it's doubtful this is a string.
        # Those aren't
        f.write(b'\x00\x01\x00')
        placeholder_next_block_seek_distance = f.tell()
        helper.write_int_32be(f, 0)  # placeholder
        # Place holder differs by 6, 3 is missing count.

        f.write(b'\x0A\xF6\x00')
        # helper.write_int_8(f, 10)
        # helper.write_int_8(f, 246)
        # helper.write_int_8(f, 0)
        # This zero is not static. It's part of frame shift.

        # Wilcom here reads 00 00 14 00
        # 00 32 00 00
        # Frame shift distance. I specifically adjusted by x+50.
        # 0 32, 00 00  == 50,0
        # So it's likely a frameshift.

        # helper.write_int_16be(f, frameshift_x)
        # helper.write_int_16be(f, frameshift_y)

        initializing_block = True
        while stitch_index < count_stitches:
            stitch = pattern.stitches[stitch_index]
            x = stitch[0]
            y = stitch[1]
            flags = stitch[2]
            if flags != EmbPattern.STITCH:
                break;
            dx = round(x - last_x)
            dy = round(y - last_y)
            last_x = x
            last_y = y

            if -127 <= dx <= 127 and -127 <= dy <= 127:
                helper.write_int_8(f, dx)
                helper.write_int_8(f, dy)
            else:
                f.write(b'\x80\x01')
                helper.write_int_16be(f, dx)
                helper.write_int_16be(f, dy)
                f.write(b'\x80\x02')
            if initializing_block:
                helper.write_int_8(f, 0)
                helper.write_int_8(f, 0)
                initializing_block = False
            stitch_index += 1
        vp3_patch_byte_offset(f, placeholder_next_block_seek_distance, -4)
        vp3_patch_byte_offset(f, placeholder_jump_to_next_block, -4)
        first_stitch_block = False
    f.write(b'\x80\x03\x00')
    vp3_patch_byte_offset(f, placeholder_length_to_end_of_file, 0)
    vp3_patch_byte_count(f, placeholder_position_end_final_block)
