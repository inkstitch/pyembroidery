from .DstReader import dst_read_header


def b_stitch_encoding_read(f, out):
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break

        ctrl = byte[0]
        y = -byte[1]
        x = byte[2]

        if ctrl & 0b01000000 != 0:
            y = -y
        if ctrl & 0b00100000 != 0:
            x = -x

        ctrl &= ~0b11100000
        if ctrl == 0:
            out.stitch(x, y)
            continue
        if ctrl & 0b00010000 != 0:
            out.end()
            return
        if ctrl & 0b00001000 != 0:
            # Set needle. Needle is: ctrl & 0b111
            if count > 1:
                out.color_change()
            continue
        if ctrl & 0b00000001 != 0:
            out.move(x, y)
    out.end()


def read(f, out, settings=None):
    dst_read_header(f, out)
    b_stitch_encoding_read(f, out)
