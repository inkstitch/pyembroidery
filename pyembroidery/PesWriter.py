import math
import io
import pyembroidery.PecWriter as writer
import pyembroidery.EmbPattern as EmbPattern

maxJumpDistance = 2047
maxStitchDistance = 2047


def write(pattern: EmbPattern, file):
    with open(file, "wb") as f:
        f.write(bytes("#PES0001", 'utf8'))
        f.write(b'\x16\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        writer.writePecStitches(pattern, f)
