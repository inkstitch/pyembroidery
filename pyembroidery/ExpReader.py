def signed(b: int) -> int:
    if b > 127:
        return -256 + b
    else:
        return b


def read(file: str, read_object):
    with open(file, "rb") as f:
        while True:
            b = f.read(2)
            if len(b) != 2:
                break
            if ((b[0] & 0xFF) == 0x80):
                if (b[1] == 0x80):
                    b = f.read(2)
                    if len(b) != 2:
                        break
                    read_object.stop()
                elif b[1] == 0x02:
                    read_object.stitch(signed(b[0]), -(signed(b[1])))
                elif b[1] == 0x04:
                    b = f.read(2)
                    if len(b) != 2:
                        break
                    read_object.move(signed(b[0]), signed(b[1]))
                else:
                    if ((b[1] & 1) != 0):
                        b = f.read(2)
                        if len(b) != 2:
                            break
                        read_object.color_change()
                        read_object.move(signed(b[0]), signed(b[1]))
                    else:
                        b = f.read(2)
                        if len(b) != 2:
                            break
                        read_object.stop()
                        read_object.move(signed(b[0]), signed(b[1]))
            else:
                read_object.stitch(signed(b[0]), -signed(b[1]))
