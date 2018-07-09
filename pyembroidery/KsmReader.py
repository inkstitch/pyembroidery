def read(f, out, settings=None):
    f.seek(0x200, 0)
    count = 0
    trimmed = False
    previous_needle = -1
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
        if ctrl == 0:
            if trimmed:
                out.move(x, y)
            else:
                out.stitch(x, y)
            continue
        if ctrl == 0b00011001:  # 0x19
            trimmed = False
            continue
        trimmed = True
        if previous_needle != ctrl:
            out.color_change()
        else:
            out.trim()
        previous_needle = ctrl
