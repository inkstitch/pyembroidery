def read(f, out, settings=None):
    f.seek(0x80, 1)  # first block of hell if I know
    f.seek(0x80, 1)  # 2nd block of hell if I know
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        ctrl = byte[0]
        dy = -byte[1]
        dx = byte[2]
        if (ctrl & 0x20) != 0:
            dx = -dx
        if (ctrl & 0x40) != 0:
            dy = -dy
        if (ctrl & 0b00011111) == 0x0:
            out.stitch(dx, dy)
            continue
        if (ctrl & 0b00011111) == 0x1:
            out.move(dx, dy)
            continue
        if ctrl == 0xE7:
            out.trim(dx, dy)
            continue
        if ctrl == 0xE8:
            out.stop()
            continue
        if 0xE9 <= ctrl <= 0xEF:
            if count > 1:
                out.color_change(dx, dy)
            continue
        # print(str(count), " ", str("{0:b}").format(ctrl), " 0x%0.2X " % ctrl, dx, " ", dy)
    out.end()
