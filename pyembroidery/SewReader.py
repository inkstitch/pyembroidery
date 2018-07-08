from .ReadHelper import read_signed, read_int_16le
from .EmbThreadSew import get_thread_set


def read(f, out, settings=None):
    threads = get_thread_set()
    colors = read_int_16le(f)
    for c in range(0, colors):
        index = read_int_16le(f)
        index %= len(threads)
        out.add_thread(threads[index])

    f.seek(0x1D78, 0)
    while True:
        b = read_signed(f, 2)
        if b is None:
            break
        if b[0] & 0xFF == 0x80:
            if b[1] & 1:
                b = read_signed(f, 2)
                out.color_change()
            elif b[1] == 0x04 or b[1] == 0x02:
                b = read_signed(f, 2)
                out.move(b[0], -b[1])
            elif b[1] == 0x10:
                out.stitch(b[0], -b[1])
                break
        else:
            out.stitch(b[0], -b[1])
    out.end()
