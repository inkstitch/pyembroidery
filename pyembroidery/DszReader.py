from DstReader import dst_read_header


def process_header_info(out, prefix, value):
    if prefix == "LA":
        out.metadata("name", value)
    else:
        out.metadata(prefix, value)


def read(f, out, settings=None):
    dst_read_header(f, out)
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break

        x = byte[1]
        y = -byte[0]
        ctrl = byte[2]
        if ctrl & 0b01000000 != 0:
            x = -x
        if ctrl & 0b00100000 != 0:
            y = -y
        ctrl &= ~0b11100000
        if ctrl & 0b00010000 != 0:
            out.end()
            return
        if ctrl & 0b00011110 != 0:
            # Set needle = color - (ctrl >> 1)
            out.color_change()
        elif ctrl & 0b00000001 != 0:
            out.move(x, y)
        elif ctrl == 0:
            out.stitch(x, y)
