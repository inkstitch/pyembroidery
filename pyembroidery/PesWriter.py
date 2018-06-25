import math
import io
import pyembroidery.PecWriter as writer
import pyembroidery.EmbPattern as EmbPattern

MAX_JUMP_DISTANCE = 2047
MAX_STITCH_DISTANCE = 2047


def write(pattern: EmbPattern, file):
    with open(file, "wb") as f:
        f.write(bytes("#PES0001", 'utf8'))
        f.write(b'\x16\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        writer.write_pec_stitches(pattern, f)
