from .ReadHelper import read_int_8, read_int_24be, read_int_24le, read_int_16le, signed24
from .EmbThread import EmbThread


def read_pc_file(f, out, settings=None):
    version = read_int_8(f)
    hoop_size = read_int_8(f)
    # 0 for PCD,
    # 1 for PCQ (MAXI),
    # 2 for PCS small hoop(80x80),
    # 3 for PCS with large hoop.
    color_count = read_int_16le(f)
    for i in range(0, color_count):
        thread = EmbThread()
        thread.color = read_int_24be(f)
        out.add_thread(thread)
        f.seek(1, 1)

    stitch_count = read_int_16le(f)
    for i in range(0, stitch_count):
        c0 = read_int_8(f)
        x = read_int_24le(f)
        c1 = read_int_8(f)
        y = read_int_24le(f)
        c2 = read_int_8(f)
        if c2 is None:
            break
        x = signed24(x)
        y = -signed24(y)
        if c2 & 0x01:
            out.color_change()
            continue
        if c2 & 0x04:
            out.move_abs(x, y)
            continue
        out.stitch_abs(x, y)
    out.end()


def read(f, out, settings=None):
    read_pc_file(f, out)
