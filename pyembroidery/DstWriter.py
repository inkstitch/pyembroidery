import math
import pyembroidery.EmbPattern as EmbPattern

MAX_JUMP_DISTANCE = 121
MAX_STITCH_DISTANCE = 121
PPMM = 10
DSTHEADERSIZE = 512

extended_header = False


def bit(b: int) -> int:
    return 1 << b


def encode_record(x: int, y: int, flags: int):
    y = -y  # flips the coordinate y space.
    b0 = 0
    b1 = 0
    b2 = 0
    if flags is EmbPattern.JUMP:
        b2 += bit(7)  # jumpstitch 10xxxx11
    if flags is EmbPattern.STITCH or flags is EmbPattern.JUMP:
        b2 += bit(0)
        b2 += bit(1)
        if x > 40:
            b2 += bit(2)
            x -= 81
        if x < -40:
            b2 += bit(3)
            x += 81
        if x > 13:
            b1 += bit(2)
            x -= 27
        if x < -13:
            b1 += bit(3)
            x += 27
        if x > 4:
            b0 += bit(2)
            x -= 9
        if x < -4:
            b0 += bit(3)
            x += 9
        if x > 1:
            b1 += bit(0)
            x -= 3
        if x < -1:
            b1 += bit(1)
            x += 3
        if x > 0:
            b0 += bit(0)
            x -= 1
        if x < 0:
            b0 += bit(1)
            x += 1
        if x != 0:
            pass  # this might actually want to raise an error, if true, x was > 121 to start
        if y > 40:
            b2 += bit(5)
            y -= 81
        if y < -40:
            b2 += bit(4)
            y += 81
        if y > 13:
            b1 += bit(5)
            y -= 27
        if y < -13:
            b1 += bit(4)
            y += 27
        if y > 4:
            b0 += bit(5)
            y -= 9
        if y < -4:
            b0 += bit(4)
            y += 9
        if y > 1:
            b1 += bit(7)
            y -= 3
        if y < -1:
            b1 += bit(6)
            y += 3
        if y > 0:
            b0 += bit(7)
            y -= 1
        if y < 0:
            b0 += bit(6)
            y += 1
        if y != 0:
            pass  # Fail. y > 121
    elif flags is EmbPattern.COLOR_CHANGE:
        b2 = 0b11000011
    elif flags is EmbPattern.STOP:
        b2 = 0b11110011
    elif flags is EmbPattern.END:
        b2 = 0b11110011
    elif flags is EmbPattern.SEQUIN:
        b2 = 0b01000011
    return bytes([b0, b1, b2])


def write(pattern: EmbPattern, file):
    with open(file, "wb") as f:
        extends = pattern.extends()
        width = extends[2] - extends[0]
        height = extends[3] - extends[1]

        name = pattern.name
        if name is None:
            name = "Untitled"
        f.write(bytes("LA:%-16s\r" % (name), 'utf8'))
        f.write(bytes("ST:%7d\r" % (pattern.count_stitches()), 'utf8'))
        f.write(bytes("CO:%3d\r" % (pattern.count_color_changes()), 'utf8'))
        x_extend = math.ceil(PPMM * width / 2)
        y_extend = math.ceil(PPMM * height / 2)
        f.write(bytes("+X:%5d\r" % (x_extend), 'utf8'))
        f.write(bytes("-X:%5d\r" % (x_extend), 'utf8'))
        f.write(bytes("+Y:%5d\r" % (y_extend), 'utf8'))
        f.write(bytes("-Y:%5d\r" % (y_extend), 'utf8'))
        f.write(bytes("AX:+%5d\r" % (0), 'utf8'))
        f.write(bytes("AY:+%5d\r" % (0), 'utf8'))
        f.write(bytes("MX:+%5d\r" % (0), 'utf8'))
        f.write(bytes("AY:+%5d\r" % (0), 'utf8'))
        f.write(bytes("PD:%6s\r" % ("******"), 'utf8'))
        if extended_header:
            if pattern.author is not None:
                f.write(bytes("AU:%s\r" % (pattern.author), 'utf8'))
            if pattern.copyright is not None:
                f.write(bytes("CP:%s\r" % (pattern.copyright), 'utf8'))
            if len(pattern.threadlist) > 0:
                for thread in pattern.threadlist:
                    f.write(
                        bytes(
                            "TC:%s,%s,%s\r" %
                            (thread.hex_color(),
                             thread.description,
                             thread.catalog_number),
                            'utf8'))
        f.write(b'\x1a')
        for i in range(f.tell(), DSTHEADERSIZE):
            f.write(b'\x20')  # space

        stitches = pattern.stitches
        xx = 0
        yy = 0
        for stitch in stitches:
            x = stitch[0]
            y = stitch[1]
            data = stitch[2]
            dx = x - xx
            dy = y - yy
            if (data is EmbPattern.TRIM):
                f.write(encode_record(2, 2, EmbPattern.JUMP))
                f.write(encode_record(-4, -4, EmbPattern.JUMP))
                f.write(encode_record(2, 2, EmbPattern.JUMP))
            else:
                f.write(encode_record(round(dx), round(dy), data))
            xx = x
            yy = y
