def read(f, out, settings=None):
    f.seek(0x200)
    while True:
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
        if ctrl == 0x11:
            break
        if (ctrl & 0x02) == 0x02:
            out.color_change()
            continue
        if (ctrl & 0x01) == 0x01:
            out.move(x, y)
            continue
    out.end()
