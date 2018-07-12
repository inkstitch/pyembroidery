from .EmbThreadJef import get_thread_set
from .ReadHelper import read_signed, read_int_32le, signed8


def read(f, out, settings=None):
    jef_threads = get_thread_set()
    stitch_offset = read_int_32le(f)
    f.seek(20, 1)
    count_colors = read_int_32le(f)
    f.seek(88, 1)

    for i in range(0, count_colors):
        index = abs(read_int_32le(f))
        out.add_thread(jef_threads[index % len(jef_threads)])

    f.seek(stitch_offset, 0)
    while True:
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        if b[0] != 0x80:
            out.stitch(signed8(b[0]), -signed8(b[1]))
            continue
        control = b[1]
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        elif control == 0x02:
            out.move(signed8(b[0]), -signed8(b[1]))
            continue
        elif control == 0x01:
            out.color_change(0, 0)
            continue
        elif control == 0x10:
            break
    out.end(0, 0)
