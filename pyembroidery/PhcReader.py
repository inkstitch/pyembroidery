from .PecReader import read_pec_stitches
from .EmbThreadPec import get_thread_set
from .ReadHelper import read_int_8, read_int_32le, read_int_16le


# I found no copies of this file.

def read(f, out, settings=None):
    f.seek(0x55, 0)
    color_count = read_int_16le(f)
    threadset = get_thread_set()
    for i in range(0, color_count):
        out.add_thread(threadset[read_int_8(f) % len(threadset)])

    f.seek(0x2B, 0)
    pec_add = read_int_8(f)
    f.seek(4, 1)
    pec_offset = read_int_16le(f)
    f.seek(pec_offset + pec_add, 0)
    bytes_in_section = read_int_16le(f)
    f.seek(bytes_in_section, 1)
    bytes_in_section2 = read_int_32le(f)
    f.seek(bytes_in_section2, 1)
    bytes_in_section3 = read_int_16le(f)
    f.seek(bytes_in_section3 + 0x12, 1)
    read_pec_stitches(f, out)
