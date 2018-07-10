from .ReadHelper import signed8


# This code doesn't work. I am unsure how to decode the format.

def read(f, out, settings=None):
    while True:
        b = bytearray(f.read(4))
        if len(b) != 4:
            break
        x = b[2]
        y = b[3]
        if x > 0x80:
            x -= 0x80
            x = -x
        if y > 0x80:  # because 2s complement is for chumps?
            y -= 0x80
            y = -y

        if b[0] == 0x61:
            out.stitch(x, -y)
        elif (b[0] & 0x01) != 0:
            out.move(x, -y)
        else:
            out.color_change()
    out.end()
