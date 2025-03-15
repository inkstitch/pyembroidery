import struct

from .EmbThread import EmbThread

# TODO: verify this number. Tested on multiple files, sample file in
# https://github.com/inkstitch/inkstitch/issues/2107
MULTIPLIER = 253.8


def read(f, out, settings=None):
    # Read and verify the magic header
    magic = f.read(8).decode("ascii")
    expected_magic = "StitchV2"
    if magic != expected_magic:
        raise ValueError("Invalid file format")

    # Skip 8 times 0x20 and 8 times 0x00
    f.read(8)  # 8x 0x20
    f.read(8)  # 8x 0x00

    # Set thread (black)
    thread = EmbThread()
    thread.set_color(0, 0, 0)
    out.add_thread(thread)

    while True:
        # Read the type (i32 LE)
        type_id_data = f.read(4)
        if len(type_id_data) < 4:
            break  # Unexpected end of file
        type_id = struct.unpack("<i", type_id_data)[0]

        # Type 2 indicates end of file
        if type_id == 2:
            break

        # Read length (i32 LE)
        length_data = f.read(4)
        if len(length_data) < 4:
            raise ValueError("Unexpected end of file while reading length")
        length = struct.unpack("<i", length_data)[0]

        if type_id in [4, 8]:  # String
            f.read(length)  # Skip string data

        elif type_id == 7:  # Coordinate list
            coord_data = f.read(length * 2)  # Read all floats
            if len(coord_data) < length * 2:
                raise ValueError("Unexpected end of file while reading coordinates")

            coords = list(struct.unpack(f"<{length // 2}f", coord_data))
            for stitch in zip(coords[::2], coords[1::2]):
                x = stitch[0] * MULTIPLIER
                y = stitch[1] * -MULTIPLIER
                out.stitch_abs(x, y)
    out.end()
