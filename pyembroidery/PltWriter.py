"""
This is code based on an unfinished pull request from https://github.com/EmbroidePy/pyembroidery/pull/174 (May 24, 2024)

HPGL2 Plot vector graphics are used commonly in pen plotters and vinyl cutters and have been a pretty mature language
since the 1970s. Here we are using a subset of the main language and commands to work with somewhat common form of
quilting machine. While this will process a lot of the more complex methods simple quilting stitches are expected to
work and are the typical goal product.
The standard step size of 1 unit in HPGL is 1/40 mm. As opposed to 1/10 mm which is standard for embroidery. HPGL is
increasing Y is downwards, which is contrary to most embroidery.
"""

from .WriteHelper import write_string_utf8

from .EmbFunctions import *
import sys


def write(pattern, f, settings=None):
    write_string_utf8(f, "IN;\n")
    write_string_utf8(f, "IP;\n")
    write_string_utf8(f, "SP1;\n")
    write_string_utf8(f, "WD\n")

    trimmed = True

    stitches = pattern.stitches
    xx = 0
    yy = 0

    # Start point = (0, 0)
    pattern.translate(-pattern.stitches[0][0], -pattern.stitches[0][1])

    pen_id = 1

    for stitch in stitches:
        # 4 to convert 1/10mm to 1/40mm.
        x = stitch[0] * 4.0
        y = stitch[1] * 4.0
        data = stitch[2] & COMMAND_MASK
        dx = int(round(x - xx))
        dy = int(round(y - yy))
        xx += dx
        yy += dy
        if data == STITCH:
            if trimmed:
                write_string_utf8(f, f"PU{int(xx)},{-int(yy)};\n")
            else:
                write_string_utf8(f, f"PD{int(xx)},{-int(yy)};\n")
            trimmed = False
        elif data == COLOR_CHANGE:
            pen_id += 1
            write_string_utf8(f, f"SP{pen_id};\n")
            trimmed = True
        elif data == JUMP:
            trimmed = True
        elif data == STOP:
            trimmed = True
        elif data == TRIM:
            trimmed = True
        elif data == END:
            write_string_utf8(f, "EN;\n")
            break
