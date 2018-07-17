from .ReadHelper import signed8


# I found no copies of this file.

def read(f, out, settings=None):
    while True:
        byte = bytearray(f.read(2))
        if len(byte) != 2:
            break
        x = signed8(x)
        y = signed8(y)
        out.stitch(x, y)
    out.end()
