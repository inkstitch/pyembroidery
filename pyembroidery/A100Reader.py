from .ReadHelper import signed8


def read(f, out, settings=None):
    while True:
        b = bytearray(f.read(4))
        if len(b) != 4:
            break
        x = b[2]
        y = b[3]
        if x > 0x80:
            x -= 0x80
        if y > 0x80:
            x -= 0x80
        if b[0] == 0x61:
            out.stitch(x, y)
        elif (b[0] & 0x01) != 0:
            out.move(b[2], b[3])
        else:
            out.color_change()
    out.end()
