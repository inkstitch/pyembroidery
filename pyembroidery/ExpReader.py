
def signed(b):
    if b > 127:
        return -256 + b
    else:
        return b


def read(f, read_object):
    while True:
        b = bytearray(f.read(2))
        if len(b) != 2:
            break
        if b[0] & 0xFF == 0x80:
            if b[1] == 0x80:  # Trim
                b = bytearray(f.read(2))
                if len(b) != 2:
                    break
                read_object.trim(0, 0)
            elif b[1] == 0x02:
                read_object.stitch(signed(b[0]), -(signed(b[1])))
            elif b[1] == 0x04:  # Jump
                b = bytearray(f.read(2))
                if len(b) != 2:
                    break
                read_object.move(signed(b[0]), -signed(b[1]))
            elif b[1] == 0x01:  # Colorchange
                b = bytearray(f.read(2))
                if len(b) != 2:
                    break
                read_object.color_change(0, 0)
                read_object.move(signed(b[0]), -signed(b[1]))
        else:
            read_object.stitch(signed(b[0]), -signed(b[1]))
