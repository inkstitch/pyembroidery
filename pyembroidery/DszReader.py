from .DstReader import dst_read_header


def z_stitch_encoding_read(f, out):
    count = 0
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
        if ctrl == 0:
            out.stitch(x, y)
            continue
        if ctrl & 0b00010000 != 0:
            out.end()
            return
        if ctrl & 0b00011110 != 0:
            # Set needle = color - (ctrl >> 1)
            # No initial call to this.
            out.color_change()
            continue
        if ctrl & 0b00000001 != 0:
            out.move(x, y)
    out.end()


def read(f, out, settings=None):
    dst_read_header(f, out)
    z_stitch_encoding_read(f, out)

# def alternative_read(f,out):
#     while True:
#         stitch_type = STITCH
#         b1 = read_int_8(f)
#         b2 = read_int_8(f)
#         command_byte = read_int_8(f)
#         if command_byte is None:
#             break
#         b1 = signed8(b1)
#         b2 = signed8(b2)
#         if command_byte == 0x91:
#             break
#         if (command_byte & 0x01) == 0x01:
#             stitch_type = TRIM
#         if (command_byte & 0x02) == 0x02:
#             stitch_type = COLOR_CHANGE
#         if (command_byte & 0x20) == 0x20:
#             b1 = -b1
#         if (command_byte & 0x40) == 0x40:
#             b2 = -b2
#         out.add_stitch_relative(stitch_type, b2, b1)
#     out.end()
