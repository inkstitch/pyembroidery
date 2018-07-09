from ReadHelper import read_int_32le, read_int_16le, read_int_8, read_signed
from EmbThread import EmbThread


def signed(b):
    if b > 127:
        return -256 + b
    else:
        return b


def read_stx_thread(f, thread):
    pass


def read(f, out, settings=None):
    # File starts with STX
    f.seek(7 + 1)
    palette_length = read_int_32le(f)
    image_length = read_int_32le(f)
    something = read_int_32le(f)
    stitch_data_offset = read_int_32le(f)
    something3 = read_int_32le(f)
    thread_description_offset = read_int_32le(f)
    stitch_count = read_int_32le(f)
    colors = read_int_32le(f)
    right = read_int_16le(f)
    left = read_int_16le(f)
    bottom = read_int_16le(f)
    top = read_int_16le(f)
    gif = f.read(image_length)
    thread_count = read_int_16le(f)
    for i in range(0, thread_count):
        EmbThread
        t = EmbThread()
        read_stx_thread(f, t)
        out.add(t)
    read_int_32le(f)
    read_int_32le(f)
    read_int_32le(f)
    read_int_16le(f)
    read_int_8(f)

    val1 = read_int_16le(f)
    val2 = read_int_16le(f)
    val3 = read_int_16le(f)
    val4 = read_int_16le(f)

    val5 = read_int_16le(f)  # 0
    val6 = read_int_16le(f)  # 0

    vala1 = read_int_16le(f)
    vala2 = read_int_16le(f)
    vala3 = read_int_16le(f)
    vala4 = read_int_16le(f)
    vala5 = read_int_16le(f)  # 0
    vala6 = read_int_16le(f)  # 0

    read_int_32le(f)  # 0
    read_int_32le(f)  # 0

    return None  # Meh
    for i in range(1, stitch_count):
        b = read_signed(2)
        if len(b) != 2:
            break
        if b[0] & 0xFF == 0x80:
            if b[1] == 0x80:  # Trim
                b = bytearray(f.read(2))  # 07 00
                if len(b) != 2:
                    break
                out.trim(0, 0)
            elif b[1] == 0x02:
                out.stitch(signed(b[0]), -(signed(b[1])))
                # This shouldn't exist.
            elif b[1] == 0x04:  # Jump
                b = bytearray(f.read(2))
                if len(b) != 2:
                    break
                out.move(signed(b[0]), -signed(b[1]))
            elif b[1] == 0x01:  # Colorchange
                b = bytearray(f.read(2))  # 00 00
                if len(b) != 2:
                    break
                out.color_change(0, 0)
                out.move(signed(b[0]), -signed(b[1]))
        else:
            out.stitch(signed(b[0]), -signed(b[1]))
