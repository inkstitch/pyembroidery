from DstReader import dst_read_header


def read(f, out, settings=None):
    dst_read_header(f, out)

    count = 0
    while True:
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        x = byte[2]
        y = -byte[1]
        ctrl = byte[0]
        if ctrl & 0b01000000 != 0:
            y = -y
        if ctrl & 0b00100000 != 0:
            x = -x
        ctrl &= ~0b11100000
        if ctrl & 0b00010000 != 0:
            out.end()
            return
        elif ctrl & 0b00001000 != 0:
            # Set needle. Needle is: ctrl & 0b111
            if count > 0:
                out.color_change()
            continue
        elif ctrl & 0b00000001 != 0:
            out.move(x, y)
        elif ctrl == 0:
            out.stitch(x, y)
        count += 1

    out.end()
