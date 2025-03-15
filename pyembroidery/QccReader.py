import re

READ_FILE_IN_TEXT_MODE = True
TENTH_MM_PER_INCH = 254


def read(f, out, settings=None):
    for line in f.readlines():
        line = line.strip()
        if "M02" in line:
            break

        try:
            x, y = get_coords(line)
            x = float(x) * TENTH_MM_PER_INCH
            y = -float(y) * TENTH_MM_PER_INCH
            out.move_abs(x, y)
            out.stitch_abs(x, y)
        except ValueError:
            pass


def get_coords(line):
    return re.findall(r"[X,Y]([-+]?\d+\.\d*)", line)
