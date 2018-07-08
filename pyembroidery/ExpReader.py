def signed(b):
    if b > 127:
        return -256 + b
    else:
        return b


def read(f, out, settings=None):
    while True:
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        if b[0] & 0xFF == 0x80:
            if b[1] == 0x80:  # Trim
                b = bytearray(f.read(2))  # 07 00
                if len(b) != 2:
                    break
                out.trim(0, 0)
            elif b[1] == 0x02:
                out.stitch(signed(b[0]), -(signed(b[1])))
                # This shouldn't exist.
            elif b[1] == 0x04:  # Jump
                b = bytearray(f.read(2))
                if len(b) != 2:
                    break
                out.move(signed(b[0]), -signed(b[1]))
            elif b[1] == 0x01:  # Colorchange
                b = bytearray(f.read(2))  # 00 00
                if len(b) != 2:
                    break
                out.color_change(0, 0)
                out.move(signed(b[0]), -signed(b[1]))
        else:
            out.stitch(signed(b[0]), -signed(b[1]))
