from .ReadHelper import read_int_16le, read_int_8, signed8, signed16


# Do you even embroider .bro?

def read(f, out, settings=None):
    f.seek(0x100, 0)
    count = 0
    while True:
        count += 1
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        if b[0] != 0x80:
            out.stitch(signed8(b[0]), -signed8(b[1]))
            continue
        control = read_int_8(f)
        if control == 0x00:
            continue
        elif control == 0x02:
            break
        if control != 0x03:
            needle = control - 0xE0
            out.color_change()
        x = signed16(read_int_16le(f))
        y = signed16(read_int_16le(f))
        out.move(x, -y)
    out.end()
