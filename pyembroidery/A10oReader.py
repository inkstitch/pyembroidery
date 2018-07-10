def read(f, out, settings=None):
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        ctrl = byte[0]
        y = -byte[1]
        x = byte[2]
        if ctrl & 0b00100000 != 0:
            x = -x
        if ctrl & 0b01000000 != 0:
            y = -y
        ctrl &= 0b00011111
        if ctrl == 0:
            out.stitch(x, y)
            continue
        if ctrl == 0x0A:
            # Start.
            continue
        if ctrl == 0x10:
            out.move(x, y)
            continue
        if ctrl == 0x05:
            out.color_change()
            continue
        if ctrl == 0x01:
            out.trim()
            continue
        if ctrl == 0x07:
            out.end()
            return
        # We shouldn't get here.
        break

    out.end()
