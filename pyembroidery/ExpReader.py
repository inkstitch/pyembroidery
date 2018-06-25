def signed(b: int) -> int:
    if b > 127:
        return -256 + b
    else:
        return b


def read(file: str, readObject):
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
                    readObject.stop()
                elif b[1] == 0x02:
                    readObject.stitch(signed(b[0]), -(signed(b[1])))
                elif b[1] == 0x04:
                    b = f.read(2)
                    if len(b) != 2:
                        break
                    readObject.move(signed(b[0]), signed(b[1]))
                else:
                    if ((b[1] & 1) != 0):
                        b = f.read(2)
                        if len(b) != 2:
                            break
                        readObject.colorChange()
                        readObject.move(signed(b[0]), signed(b[1]))
                    else:
                        b = f.read(2)
                        if len(b) != 2:
                            break
                        readObject.stop()
                        readObject.move(signed(b[0]), signed(b[1]))
            else:
                readObject.stitch(signed(b[0]), -signed(b[1]))
