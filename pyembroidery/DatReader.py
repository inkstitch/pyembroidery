from .ReadHelper import read_int_16le, read_int_8, signed8


def read_barudan_dat(f, out):
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break

        ctrl = byte[0]
        y = -byte[1]
        x = byte[2]

        if ctrl & 0b10000000 == 0:
            # This bit should always be set, must be other dat type.
            return False
        if ctrl & 0b01000000 != 0:
            y = -y
        if ctrl & 0b00100000 != 0:
            x = -x

        ctrl &= ~0b11100000
        if ctrl == 0:
            out.stitch(x, y)
            continue
        if ctrl & 0b00010000 != 0:
            break
        if ctrl & 0b00001000 != 0:
            # Set needle. Needle is: ctrl & 0b111
            if count > 1:
                out.color_change()
            continue
        if ctrl & 0b00000001 != 0:
            out.move(x, y)
    out.end()
    return True


def read_sunstar_dat(f, out):
    f.seek(0x02, 0)
    stitches = read_int_16le(f)
    f.seek(0x100, 0)
    count = 0
    while True:
        count += 1
        byte = bytearray(f.read(3))
        if len(byte) != 3:
            break
        x = byte[0] & 0x7F
        y = byte[1] & 0x7F
        if byte[0] & 0x80:
            x = -x
        if byte[1] & 0x80:
            y = -y
        y = -y
        ctrl = byte[2]
        if ctrl == 0x07:
            out.stitch(x, y)
            continue
        if ctrl == 0x04:
            out.move(x, y)
            continue
        if ctrl == 0x87:
            out.color_change()
            out.stitch(x, y)
            continue
        if ctrl == 0x84:
            out.stitch(x, y)
            continue
        elif ctrl == 0:
            break
        out.stitch(x, y)
    out.end()


def read(f, out, settings=None):
    if not read_barudan_dat(f, out):
        f.seek(0, 0)
        read_sunstar_dat(f, out)
