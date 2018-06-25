def getbit(b: int, pos: int) -> int:
    return (b >> pos) & 1


def decodedx(b0: int, b1: int, b2: int) -> int:
    x = 0
    x += getbit(b2, 2) * (+81)
    x += getbit(b2, 3) * (-81)
    x += getbit(b1, 2) * (+27)
    x += getbit(b1, 3) * (-27)
    x += getbit(b0, 2) * (+9)
    x += getbit(b0, 3) * (-9)
    x += getbit(b1, 0) * (+3)
    x += getbit(b1, 1) * (-3)
    x += getbit(b0, 0) * (+1)
    x += getbit(b0, 1) * (-1)
    return x


def decodedy(b0: int, b1: int, b2: int) -> int:
    y = 0
    y += getbit(b2, 5) * (+81)
    y += getbit(b2, 4) * (-81)
    y += getbit(b1, 5) * (+27)
    y += getbit(b1, 4) * (-27)
    y += getbit(b0, 5) * (+9)
    y += getbit(b0, 4) * (-9)
    y += getbit(b1, 7) * (+3)
    y += getbit(b1, 6) * (-3)
    y += getbit(b0, 7) * (+1)
    y += getbit(b0, 6) * (-1)
    return -y


def read(file: str, readObject):
    with open(file, "rb") as f:
        f.seek(512)
        sequinMode = False
        while True:
            byte = f.read(3)
            if len(byte) != 3:
                break
            dx = decodedx(byte[0], byte[1], byte[2])
            dy = decodedy(byte[0], byte[1], byte[2])
            if ((byte[2] & 0b11110011) == 0b11110011):
                readObject.stop(dx, dy)
            elif ((byte[2] & 0b11000011) == 0b11000011):
                readObject.colorChange(dx, dy)
            elif ((byte[2] & 0b01000011) == 0b01000011):
                sequinMode = not sequinMode
            elif ((byte[2] & 0b10000011) == 0b10000011):
                if sequinMode:
                    readObject.sequin(dx, dy)
                else:
                    readObject.move(dx, dy)
            else:
                readObject.stitch(dx, dy)
