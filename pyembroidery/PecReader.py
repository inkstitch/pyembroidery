from .EmbThreadPec import get_thread_set
from .ReadHelper import read_string_8, read_int_8, read_int_24le

JUMP_CODE = 0x10
TRIM_CODE = 0x20
FLAG_LONG = 0x80


def read(f, read_object):
    pec_string = read_string_8(f, 8)
    # pec_string must equal #PEC0001
    read_pec(f, read_object)


def read_pec(f, read_object, pes_chart=None):
    f.seek(3, 1)  # LA:
    label = read_string_8(f, 16).strip()  # Label
    read_object.metadata("Label", label)
    f.seek(0xF, 1)  # Dunno, spaces then 0xFF 0x00
    pec_graphic_byte_stride = read_int_8(f)
    pec_graphic_icon_height = read_int_8(f)
    f.seek(0xC, 1)
    color_changes = read_int_8(f)
    count_colors = color_changes + 1  # PEC uses cc - 1, 0xFF means 0.
    color_bytes = bytearray(f.read(count_colors))
    threads = []
    map_pec_colors(color_bytes, read_object, pes_chart, threads)
    f.seek(0x1D0 - color_changes, 1)
    stitch_block_end = read_int_24le(f) - 5 + f.tell()
    # The end of this value is already 5 into the stitchblock.

    # 3 bytes, '\x31\xff\xf0', 6 2-byte shorts. 15 total.
    f.seek(0x0F, 1)
    read_pec_stitches(f, read_object)
    f.seek(stitch_block_end, 0)

    byte_size = pec_graphic_byte_stride * pec_graphic_icon_height

    read_pec_graphics(f,
                      read_object,
                      byte_size,
                      pec_graphic_byte_stride,
                      count_colors + 1,
                      threads
                      )


def read_pec_graphics(f, read_object, size, stride, count, values):
    values.insert(0,None)
    for i in range(0, count):
        graphic = bytearray(f.read(size))
        if f is not None:
            read_object.metadata(i, (graphic, stride, values[i]))


def process_pec_colors(colorbytes, read_object, values):
    thread_set = get_thread_set()
    max_value = len(thread_set)
    for byte in colorbytes:
        thread_value = thread_set[byte % max_value]
        read_object.add_thread(thread_value)
        values.append(thread_value)


def process_pec_table(colorbytes, read_object, chart, values):
    # This is how PEC actually allocates pre-defined threads to blocks.
    thread_set = get_thread_set()
    max_value = len(thread_set)
    thread_map = {}
    queue = []
    for i in range(0, len(colorbytes)):
        color_index = int(colorbytes[i] % max_value)
        thread_value = thread_map.get(color_index, None)
        if thread_value is None:
            thread_value = thread_set[color_index]
            if len(chart) > 0:
                thread_value = chart.pop(0)
            else:
                thread_value = thread_set[color_index]
            thread_map[color_index] = thread_value
        read_object.add_thread(thread_value)
        values.append(thread_value)


def map_pec_colors(colorbytes, read_object, chart, values):
    if chart is None or len(chart) == 0:
        # Reading pec colors.
        process_pec_colors(colorbytes, read_object, values)

    elif len(chart) >= len(colorbytes):
        # Reading threads in 1 : 1 mode.
        for thread in chart:
            read_object.add_thread(thread)
            values.append(thread)
    else:
        # Reading tabled mode threads.
        process_pec_table(colorbytes, read_object, chart,values)


def signed12(b):
    b = b & 0xFFF
    if b > 0x7FF:
        return - 0x1000 + b
    else:
        return b


def signed7(b):
    if b > 63:
        return - 128 + b
    else:
        return b


def read_pec_stitches(f, read_object):
    while True:
        val1 = read_int_8(f)
        val2 = read_int_8(f)
        if (val1 == 0xFF and val2 == 0x00) or val2 is None:
            read_object.end(0, 0)
            return
        if val1 == 0xFE and val2 == 0xB0:
            f.seek(1, 1)
            read_object.color_change(0, 0)
            continue
        x = 0
        y = 0
        jump = False
        trim = False
        if val1 & FLAG_LONG != 0:
            if val1 & TRIM_CODE != 0:
                trim = True
            if val1 & JUMP_CODE != 0:
                jump = True
            code = (val1 << 8) | val2
            x = signed12(code)
            val2 = read_int_8(f)
        else:
            x = signed7(val1)

        if val2 & FLAG_LONG != 0:
            if val2 & TRIM_CODE != 0:
                trim = True
            if val2 & JUMP_CODE != 0:
                jump = True
            val3 = read_int_8(f)
            code = val2 << 8 | val3
            y = signed12(code)
        else:
            y = signed7(val2)

        if jump:
            read_object.move(x, y)
        elif trim:
            read_object.trim(x, y)
        else:
            read_object.stitch(x, y)

    read_object.end(0, 0)
