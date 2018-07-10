from .DszReader import z_stitch_encoding_read


# I found no copies of this file.

def read(f, out, settings=None):
    f.seek(0x100)
    z_stitch_encoding_read(f, out)
