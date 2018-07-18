from .ReadHelper import signed8, read_int_32le


def read_jpx_stitches(f, out):
    while True:
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        if b[0] == 0x80:
            control = b[1]
            b = bytearray(f.read(2))
            if len(b) != 2:
                break
            if control == 0x02:
                out.move(signed8(b[0]), -(signed8(b[1])))
            elif control == 0x01:  # Colorchange
                out.color_change()
                if b[0] != 0 and b[1] != 0:
                    out.move(signed8(b[0]), -signed8(b[1]))
            elif control == 0x10:
                break
        else:
            out.stitch(signed8(b[0]), -signed8(b[1]))
    out.end()


def read(f, out, settings=None):
    stitch_start_position = read_int_32le(f)
    f.seek(0x1C, 1)
    colors = read_int_32le(f)
    f.seek(0x18, 1)
    for i in range(0, colors):
        color_index = read_int_32le(f)
        if color_index is None:
            break
        out.add_thread({
            "color": "random",
            "name": "JPX index " + str(color_index)
        })
    f.seek(stitch_start_position, 0)
    read_jpx_stitches(f, out)
