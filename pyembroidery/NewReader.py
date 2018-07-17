# I found no copies of this file.


def new_stitch_encoding_read(f, out):
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break

        y = -byte[0]
        x = byte[1]
        ctrl = byte[2]

        if ctrl & 0b01000000 != 0:
            x = -x
        if ctrl & 0b00100000 != 0:
            y = -y

        ctrl &= ~0b11100000
        if ctrl == 0:
            out.stitch(x, y)
            continue
        if ctrl & 0b00010000 != 0:
            out.trim(x, y)
            continue
        if ctrl & 0b00000001 != 0:
            out.move(x, y)
            continue
        if ctrl & 0b00011110 != 0:
            out.color_change()
            continue
    out.end()


def read(f, out, settings=None):
    f.seek(4, 1)  # stitchcount.
    new_stitch_encoding_read(f, out)
