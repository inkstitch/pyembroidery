def write_int_array_8(stream, int_array):
    for value in int_array:
        stream.write(bytes([int(value) & 0xFF]))

def write_int_8(stream, value: int):
    stream.write(bytes([value & 0xFF]))


def write_int_16le(stream, value: int):
    stream.write(bytes([value & 0xFF, (value >> 8) & 0xFF]))


def write_int_16be(stream, value: int):
    stream.write(bytes([(value >> 8) & 0xFF, value & 0xFF]))


def write_int_24le(stream, value: int):
    stream.write(
        bytes([value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF]))


def write_int_24be(stream, value: int):
    stream.write(
        bytes([(value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF]))


def write_int_32le(stream, value: int):
    stream.write(bytes([value & 0xFF, (value >> 8) & 0xFF,
                        (value >> 16) & 0xFF, (value >> 24) & 0xFF]))


def write_int_32be(stream, value: int):
    stream.write(bytes([(value >> 24) & 0xFF(value >> 16) & 0xFF,
                        (value >> 8) & 0xFF, value & 0xFF]))


def write(stream, string: str):
    stream.write(bytes(string, 'utf8'))
