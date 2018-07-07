from .EmbThreadJef import get_thread_set
from .ReadHelper import read_signed, read_int_32le, signed


def read(f, out, settings=None):
    jef_threads = get_thread_set()
    stitch_offset = read_int_32le(f)
    f.seek(20, 1)
    count_colors = read_int_32le(f)
    count_stitches = read_int_32le(f)
    f.seek(84, 1)
    for i in range(0, count_colors):
        index = abs(read_int_32le(f))
        out.add_thread(jef_threads[index % 79])

    f.seek(stitch_offset - 116 - (count_colors * 4), 1)
    for i in range(0, count_stitches + 100):
        b = read_signed(f, 2)
        if (b[0] & 0xFF) == 0x80:
            if (b[1] & 1) != 0:
                b = read_signed(f, 2)
                out.color_change(0, 0)
                out.move(b[0], -b[1])
            elif b[1] == 0x04 or b[1] == 0x02:  # trim
                b = read_signed(f, 2)
                out.trim(0, 0)
                out.move(b[0], -b[1])
            elif b[1] == 0x10:  # end
                break
        else:
            out.stitch(signed(b[0]),
                       -signed(b[1]))
    out.end(0, 0)
