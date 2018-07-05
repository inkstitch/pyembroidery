import math
import io
import pyembroidery.EmbThread as EmbThread;
import pyembroidery.PecWriter as writer
import pyembroidery.EmbPattern as EmbPattern
import pyembroidery.WriteHelper as helper
import pyembroidery.EmbThreadPec as EmbThreadPec
from pyembroidery.EmbConstant import *

MAX_JUMP_DISTANCE = 2047
MAX_STITCH_DISTANCE = 2047

VERSION_1 = 1
VERSION_6 = 6
VERSION_1_TRUNCATED = 0x101
VERSION_6_TRUNCATED = 0x106

PES_VERSION_1_SIGNATURE = "#PES0001"
PES_VERSION_6_SIGNATURE = "#PES0060"

EMB_ONE = "CEmbOne";
EMB_SEG = "CSewSeg";

def write(pattern, f, settings=None):
    version = VERSION_6
    if settings != None:
        version = settings.get("pes version", version)

    if version == VERSION_1:
        write_version_1(pattern, f)
    elif version == VERSION_6:
        write_version_6(pattern, f)
    elif version == VERSION_1_TRUNCATED:
        write_truncated_version_1(pattern, f)
    elif version == VERSION_6_TRUNCATED:
        write_truncated_version_6(pattern, f)


def write_truncated_version_1(pattern, f):
    f.write(bytes(PES_VERSION_1_SIGNATURE, 'utf8'))
    f.write(b'\x16\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    writer.write_pec(pattern, f)


def write_truncated_version_6(pattern, f):
    chart = pattern.threadlist
    helper.write(f, PES_VERSION_6_SIGNATURE)
    placeholder_pec_block = f.tell();
    helper.write_int_32le(f, 0)  # Placeholder for PEC BLOCK
    write_pes_header_v6(pattern, f, 0)
    helper.write_int_16le(f, 0x0000);
    helper.write_int_16le(f, 0x0000);
    current_position = f.tell();
    f.seek(placeholder_pec_block, 0)
    helper.write_int_32le(f, current_position)
    f.seek(current_position, 0);
    writer.write_pec(pattern, f);


def write_version_1(pattern, f):
    chart = EmbThreadPec.get_thread_set()
    helper.write(f, PES_VERSION_1_SIGNATURE)

    pattern.move_center_to_origin();

    extends = pattern.extends()

    left = extends[0]
    top = extends[1]
    right = extends[2]
    bottom = extends[3]

    width = round(right - left)
    height = round(bottom - top)

    placeholder_pec_block = f.tell();
    helper.write_int_32le(f, 0)  # Placeholder for PEC BLOCK

    if len(pattern.stitches) == 0:
        write_pes_header_v1(f, 0)
        helper.write_int_16le(f, 0x0000);
        helper.write_int_16le(f, 0x0000);
    else:
        write_pes_header_v1(f, 1)
        helper.write_int_16le(f, 0xFFFF)
        helper.write_int_16le(f, 0x0000);
        write_pes_blocks(f, pattern, chart, left, top, right, bottom)

    current_position = f.tell();
    f.seek(placeholder_pec_block, 0)
    helper.write_int_32le(f, current_position)
    f.seek(current_position, 0);

    writer.write_pec(pattern, f);


def write_version_6(pattern, f):
    chart = set(pattern.threadlist)
    helper.write(f, PES_VERSION_6_SIGNATURE)

    pattern.move_center_to_origin();

    extends = pattern.extends()

    left = extends[0]
    top = extends[1]
    right = extends[2]
    bottom = extends[3]

    width = round(right - left)
    height = round(bottom - top)

    placeholder_pec_block = f.tell();
    helper.write_int_32le(f, 0)  # Placeholder for PEC BLOCK

    if len(pattern.stitches) == 0:
        write_pes_header_v6(pattern, f, 0)
        helper.write_int_16le(f, 0x0000);
        helper.write_int_16le(f, 0x0000);
    else:
        write_pes_header_v6(pattern, f, 1)
        helper.write_int_16le(f, 0xFFFF)
        helper.write_int_16le(f, 0x0000);
        log = write_pes_blocks(f, pattern, chart, left, top, right, bottom)
        # In version 6 there is some node, tree, order thing.
        helper.write_int_32le(f, 0)
        helper.write_int_32le(f, 0)
        for i in range(0, len(log)):
            helper.write_int_32le(f, i)
            helper.write_int_32le(f, 0)

    current_position = f.tell();
    f.seek(placeholder_pec_block, 0)
    helper.write_int_32le(f, current_position)
    f.seek(current_position, 0);
    writer.write_pec(pattern, f);


def write_pes_header_v1(f, distinct_block_objects):
    helper.write_int_16le(f, 0x01)  # scale to fit
    helper.write_int_16le(f, 0x01)  # 0 = 100x100, 130x180 hoop
    helper.write_int_16le(f, distinct_block_objects)


def write_pes_header_v6(pattern, f, distinct_block_objects):
    helper.write_int_16le(f, 0x01)  # 0 = 100x100, 130x180 hoop
    f.write(b'02')  # This is an 2-digit ascii number.
    write_pes_string_8(f, pattern.get_metadata("name", None));
    write_pes_string_8(f, pattern.get_metadata("category", None));
    write_pes_string_8(f, pattern.get_metadata("author", None));
    write_pes_string_8(f, pattern.get_metadata("keywords", None));
    write_pes_string_8(f, pattern.get_metadata("comments", None));
    helper.write_int_16le(f, 0)  # OptimizeHoopChange = False
    helper.write_int_16le(f, 0)  # Design Page Is Custom = False
    helper.write_int_16le(f, 0x64)  # Hoop Width
    helper.write_int_16le(f, 0x64)  # Hoop Height
    helper.write_int_16le(f, 0)  # Use Existing Design Area = False
    helper.write_int_16le(f, 0xC8);  # designWidth
    helper.write_int_16le(f, 0xC8);  # designHeight
    helper.write_int_16le(f, 0x64);  # designPageSectionWidth
    helper.write_int_16le(f, 0x64);  # designPageSectionHeight
    helper.write_int_16le(f, 0x64);  # p6 # 100
    helper.write_int_16le(f, 0x07);  # designPageBackgroundColor
    helper.write_int_16le(f, 0x13);  # designPageForegroundColor
    helper.write_int_16le(f, 0x01);  # ShowGrid
    helper.write_int_16le(f, 0x01);  # WithAxes
    helper.write_int_16le(f, 0x00);  # SnapToGrid
    helper.write_int_16le(f, 100);  # GridInterval
    helper.write_int_16le(f, 0x01);  # p9 curves?
    helper.write_int_16le(f, 0x00);  # OptimizeEntryExitPoints
    helper.write_int_8(f, 0);  # fromImageStringLength
    #  String FromImageFilename
    helper.write_float_32le(f, float(1))
    helper.write_float_32le(f, float(0))
    helper.write_float_32le(f, float(0))
    helper.write_float_32le(f, float(1))
    helper.write_float_32le(f, float(0))
    helper.write_float_32le(f, float(0))
    helper.write_int_16le(f, 0);  # numberOfProgrammableFillPatterns
    helper.write_int_16le(f, 0);  # numberOfMotifPatterns
    helper.write_int_16le(f, 0);  # featherPatternCount
    count_thread = pattern.count_threads()
    helper.write_int_16le(f, count_thread);  # numberOfColors
    for thread in pattern.threadlist:
        write_pes_thread(f, thread);
    helper.write_int_16le(f, distinct_block_objects);  # number ofdistinct blocks


def write_pes_string_8(f, string):
    if string == None:
        helper.write_int_8(f, 0)
        return
    if len(string) > 255:
        string = string[:255]
    helper.write_int_8(f, len(string))
    f.write(bytes(string, 'utf8'))


def write_pes_string_16(f, string):
    if string == None:
        helper.write_int_16le(f, 0)
        return
    helper.write_int_16le(f, len(string))
    # 16 refers to the size write not the string encoding.
    f.write(bytes(string, 'utf8'))


def write_pes_thread(f, thread):
    write_pes_string_8(f, thread.catalog_number)
    helper.write_int_8(f, thread.get_red())
    helper.write_int_8(f, thread.get_green())
    helper.write_int_8(f, thread.get_blue())
    helper.write_int_8(f, 0)  # unknown
    helper.write_int_32le(f, 0xA)  # A is custom color
    write_pes_string_8(f, thread.description)
    write_pes_string_8(f, thread.brand)
    write_pes_string_8(f, thread.chart)


def write_pes_blocks(f, pattern, chart, left, top, right, bottom):
    if len(pattern.stitches) == 0:
        return

    write_pes_string_16(f, EMB_ONE)
    placeholder = write_pes_sewsegheader(f, pattern, left, top, right, bottom)
    helper.write_int_16le(f, 0xFFFF);
    helper.write_int_16le(f, 0x0000);  # FFFF0000 means more blocks exist

    write_pes_string_16(f, EMB_SEG)
    data = write_pes_embsewseg_segments(f, pattern, chart, left, bottom)

    sections = data[0]
    colorlog = data[1]

    current_position = f.tell()
    f.seek(placeholder, 0)
    helper.write_int_16le(f, sections)
    f.seek(current_position, 0)  # patch final section count.

    # If there were addition embsewsegheaders or segments they would go here.

    helper.write_int_16le(f, 0x0000)
    helper.write_int_16le(f, 0x0000)  # 00000000 means no more blocks.

    return colorlog


def write_pes_sewsegheader(f, pattern, left, top, right, bottom):
    width = right - left
    height = bottom - top
    hoop_height = 1800
    hoop_width = 1300
    helper.write_int_16le(f, 0)  # left
    helper.write_int_16le(f, 0)  # top
    helper.write_int_16le(f, 0)  # right
    helper.write_int_16le(f, 0)  # bottom
    helper.write_int_16le(f, 0)  # left
    helper.write_int_16le(f, 0)  # top
    helper.write_int_16le(f, 0)  # right
    helper.write_int_16le(f, 0)  # bottom
    trans_x = 0
    trans_y = 0
    trans_x += float(350)
    trans_y += float(100) + height
    trans_x += hoop_width / 2
    trans_y += hoop_height / 2
    trans_x += -width / 2
    trans_y += -height / 2
    helper.write_float_32le(f, float(1))
    helper.write_float_32le(f, float(0))
    helper.write_float_32le(f, float(0))
    helper.write_float_32le(f, float(1))
    helper.write_float_32le(f, float(trans_x))
    helper.write_float_32le(f, float(trans_y))

    helper.write_int_16le(f, 1);
    helper.write_int_16le(f, 0);
    helper.write_int_16le(f, 0);
    helper.write_int_16le(f, int(width))
    helper.write_int_16le(f, int(height))
    f.write(b'\x00\x00\x00\x00\x00\x00\x00\x00')

    placeholder_needs_section_data = f.tell()
    # sections
    helper.write_int_16le(f, 0);
    return placeholder_needs_section_data


def get_as_segments_blocks(pattern, chart, left, bottom):
    color_index = 0;
    current_thread = pattern.get_thread_or_filler(color_index)
    color_index += 1
    color_code = current_thread.find_nearest_color_index(chart)
    stitched_x = 0
    stitched_y = 0
    for command_block in pattern.get_as_command_blocks():
        block = []
        command = command_block[0][2]
        if command == JUMP:
            block.append([stitched_x - left, stitched_y - bottom])
            last_pos = command_block[-1]
            block.append([last_pos[0] - left, last_pos[1] - bottom])
            flag = 1
        elif command == COLOR_CHANGE:
            current_thread = pattern.get_thread_or_filler(color_index)
            color_index += 1
            color_code = current_thread.find_nearest_color_index(chart)
            flag = 1
            continue
        elif command == STITCH:
            for stitch in command_block:
                stitched_x = stitch[0]
                stitched_y = stitch[1]
                block.append([stitched_x - left, stitched_y - bottom])
            flag = 0
        else:
            continue
        yield (block, color_code, flag)


def write_pes_embsewseg_segments(f, pattern, chart, left, bottom):
    section = 0
    colorlog = []

    previous_color_code = -1
    flag = -1;
    for segs in get_as_segments_blocks(pattern, chart, left, bottom):
        if flag != -1:
            helper.write_int_16le(f, 0x8003)  # section end.
        segments = segs[0]
        color_code = segs[1]
        flag = segs[2]

        if previous_color_code != color_code:
            colorlog.append([section, color_code])
            previous_color_code = color_code
            # This must trigger first segment.
        helper.write_int_16le(f, flag)
        helper.write_int_16le(f, color_code)
        helper.write_int_16le(f, len(segments))
        for segs in segments:
            helper.write_int_16le(f, int(segs[0]))
            helper.write_int_16le(f, int(segs[1]))
        section += 1;

    helper.write_int_16le(f, len(colorlog))
    for log_item in colorlog:
        helper.write_int_16le(f, log_item[0])
        helper.write_int_16le(f, log_item[1])

    return (section, colorlog)  # how many sections, how color transitions.
