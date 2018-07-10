from .ReadHelper import read_int_8, signed8


def read(f, out, settings=None):
    f.seek(0x30, 0)
    while True:
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        if b[0] == 0x80:
            control = b[1]
            b = bytearray(f.read(2))
            if len(b) != 2:
                break
            if control == 0x2A:
                out.color_change()
                continue
            elif control == 0x80:
                out.move(signed8(b[0]), -signed8(b[1]))
            elif control == 0xFD:
                break
        else:
            out.stitch(signed8(b[0]), -signed8(b[1]))
    out.end()
