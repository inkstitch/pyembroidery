from .ReadHelper import read_int_8, read_int_16le


def read_pmv_stitches(f, out, settings=None):
    """PMV files are stitch files, not embroidery."""
    px = 0
    # stitches = []
    while True:
        stitch_count = read_int_16le(f)
        block_length = read_int_16le(f)
        if block_length is None:
            return
        if block_length >= 256:
            break
        if stitch_count == 0:
            continue
        for i in range(0, stitch_count):
            x = read_int_8(f)
            y = read_int_8(f)
            if y > 16:
                y = -(32 - y)  # This is 5 bit signed number.
            if x > 32:
                x = -(64 - x)  # This is a 6 bit signed number.
            dx = x
            out.stitch_abs(px + x, y)  # This is a hybrid relative, absolute value.
            px += dx
            # stitches.append((x, y))
    out.end()
    # f.seek(0x10, 1)  # 16 bytes
    # block_end = read_int_16le(f)
    # if block_end != 256:
    #     return
    # steps = []
    # dunno0 = read_int_8(f)
    # dunno1 = read_int_8(f)
    # dunno2 = read_int_8(f)
    # steps_size = read_int_8(f)
    # for i in range(0, steps_size):
    #     x = read_int_16le(f)
    #     y = read_int_16le(f)
    #     if x is None or y is None:
    #         break
    #     steps.append((x, y))
    # dunno3 = read_int_8(f)
    # steps2_size = read_int_8(f)
    # steps2 = []
    # for i in range(0, steps2_size):
    #     x = read_int_16le(f)
    #     y = read_int_16le(f)
    #     if x is None or y is None:
    #         break
    #     steps2.append((x, y))
    # dunno4 = read_int_16le(f)  # seems to be 0x12.
    # f.seek(0x10, 1)  # 16 bytes
    # # EOF - This should be End of File.
    # none_bytes = read_int_8(f)
    # if none_bytes is None:
    #     pass
    # print(f)
    # print("Stitches: Total ", len(stitches), " : ", stitches)
    # print("Unknown0:", dunno0)
    # print("Unknown1:", dunno1)
    # print("Unknown2:", dunno2)
    # print("1st Steps: Total ", len(steps), " : ", steps)
    # print("Unknown3:", dunno3)
    # print("2nd Steps: Total ", len(steps2), " : ", steps2)
    # print("Unknown4:", dunno4)
    out.end()


def read(f, out, settings=None):
    f.seek(0x64, 0)
    read_pmv_stitches(f, out)
