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

        y = -byte[0]
        x = byte[1]
        ctrl = byte[2]

        if ctrl & 0b01000000 != 0:
            x = -x
        if ctrl & 0b00100000 != 0:
            y = -y
        ctrl &= ~0b11100000

        if trimmed:  # any x, y gets executed regardless.
            out.move(x, y)
        else:
            out.stitch(x, y)

        if ctrl == 0:
            continue
        if ctrl == 0b00000111:  # 0x07, Initialize stitch
            continue
        if ctrl == 0b00011001:  # 0x19, start sewing again.
            trimmed = False
            continue
        trimmed = True
        if ctrl == 0b00010011:  # 0x13 trim, no color change.
            continue
        if previous_needle != ctrl:
            out.color_change()
        else:
            out.stop()
        previous_needle = ctrl
