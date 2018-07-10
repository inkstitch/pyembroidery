from .ReadHelper import signed8


def read_exp_stitches(f, out):
    while True:
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        if b[0] == 0x80:
            control = b[1]
            b = bytearray(f.read(2))  # 07 00
            if len(b) != 2:
                break
            if control == 0x80:  # Trim
                out.trim()
            elif control == 0x02:
                out.stitch(signed8(b[0]), -(signed8(b[1])))
                # This shouldn't exist.
            elif control == 0x04:  # Jump
                out.move(signed8(b[0]), -signed8(b[1]))
            elif control == 0x01:  # Colorchange
                out.color_change()
                out.move(signed8(b[0]), -signed8(b[1]))
        else:
            out.stitch(signed8(b[0]), -signed8(b[1]))
    out.end()


def read(f, out, settings=None):
    read_exp_stitches(f, out)
