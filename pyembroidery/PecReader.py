import pyembroidery.EmbThreadPec as PecThread
import pyembroidery.ReadHelper as helper

JUMP_CODE = 0x10
TRIM_CODE = 0x20
FLAG_LONG = 0x80


def read(f, read_object):
    pec_string = helper.read_string_8(f, 8)
    # pec_string must equal #PEC0001
    read_pec(f, read_object, None);


def read_pec(f, read_object, threadlist):
    f.seek(0x30, 1)
    color_changes = helper.read_int_8(f);
    count_colors = color_changes + 1  # PEC uses cc - 1, 0xFF means 0.

    color_bytes = f.read(count_colors)
    map_pec_colors(color_bytes, read_object, threadlist)

    f.seek(0x200 - (0x30 + color_changes), 1)
    f.seek(0x13, 1)  # 2 bytes size, 17 bytes cruft
    read_pec_stitches(f, read_object)


def process_pec_colors(colorbytes, read_object):
    thread_set = PecThread.get_thread_set()
    max_value = len(thread_set)
    for byte in colorbytes:
        thread_value = thread_set[byte % max_value]
        read_object.add_thread(thread_value)


def process_pec_table(colorbytes, read_object, threadlist):
    # This is how PEC actually allocates pre-defined threads to blocks.
    thread_set = PecThread.get_thread_set()
    max_value = len(thread_set)
    thread_map = {}
    queue = []
    for i in range(0, len(colorbytes)):
        color_index = int(colorbytes[i] % max_value)
        thread_value = thread_map.get(color_index, None);
        if thread_value == None:
            thread_value = thread_set[color_index]
            if len(threadlist) > 0:
                thread_value = threadlist.pop(0);
            else:
                thread_value = thread_set[color_index]
            thread_map[color_index] = thread_value
        read_object.add_thread(thread_value)


def map_pec_colors(colorbytes, read_object, threadlist):
    current_index = 0
    if threadlist == None or len(threadlist) == 0:
        # Reading pec colors.
        process_pec_colors(colorbytes, read_object)

    elif len(threadlist) >= len(colorbytes):
        # Reading threads in 1 : 1 mode.
        for threads in threadlist:
            read_object.add_thread(thread)
    else:
        # Reading tabled mode threads.
        process_pec_table(colorbytes, read_object, threadlist)


def signed12(b):
    b = b & 0xFFF;
    if b > 0x7FF:
        return - 0x1000 + b;
    else:
        return b


def signed7(b):
    if b > 63:
        return - 128 + b
    else:
        return b


def read_pec_stitches(f, read_object):
    while True:
        val1 = helper.read_int_8(f)
        val2 = helper.read_int_8(f)
        code = (val1 << 8) | val2
        if val1 == 0xFF:
            read_object.end(0, 0)
            return;
        if val1 == 0xFE and val2 == 0xB0:
            f.seek(1, 1)
            read_object.color_change(0, 0)
            continue
        x = 0;
        y = 0;
        jump = False
        trim = False
        if val1 & FLAG_LONG != 0:
            if val1 & TRIM_CODE != 0:
                trim = True
            if val1 & JUMP_CODE != 0:
                jump = True
            x = signed12(code);
            val2 = helper.read_int_8(f)
        else:
            x = signed7(val1)

        if val2 & FLAG_LONG != 0:
            if val2 & TRIM_CODE != 0:
                trim = True
            if val2 & JUMP_CODE != 0:
                jump = True
            val3 = helper.read_int_8(f)
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
