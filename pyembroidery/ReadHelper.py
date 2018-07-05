def signed(b):
    if b > 127:
        return -256 + b
    else:
        return b


def read_signed(stream, n):
    byte = bytearray(stream.read(n))
    signed_bytes = []
    for b in byte:
        signed_bytes.append(signed(b))
    return signed_bytes


def read_sint_8(stream):
    byte = bytearray(stream.read(1))
    if len(byte) is 1:
        return signed(byte[0])
    return None


def read_int_8(stream):
    byte = bytearray(stream.read(1))
    if len(byte) is 1:
        return byte[0]
    return None


def read_int_16le(stream):
    byte = bytearray(stream.read(2))
    if len(byte) is 2:
        return (byte[0] & 0xFF) + ((byte[1] & 0xFF) << 8)
    return None


def read_int_16be(stream):
    byte = bytearray(stream.read(2))
    if len(byte) is 2:
        return (byte[1] & 0xFF) + ((byte[0] & 0xFF) << 8)
    return None


def read_int_24le(stream):
    b = bytearray(stream.read(3))
    if len(b) is 3:
        return (b[0] & 0xFF) + ((b[1] & 0xFF) << 8) + \
               ((b[2] & 0xFF) << 16)
    return None


def read_int_24be(stream):
    b = bytearray(stream.read(3))
    if len(b) is 3:
        return (b[2] & 0xFF) + ((b[1] & 0xFF) << 8) + \
               ((b[0] & 0xFF) << 16)
    return None


def read_int_32le(stream):
    b = bytearray(stream.read(4))
    if len(b) is 4:
        return (b[0] & 0xFF) + ((b[1] & 0xFF) << 8) + \
               ((b[2] & 0xFF) << 16) + ((b[3] & 0xFF) << 24)
    return None


def read_int_32be(stream):
    b = bytearray(stream.read(4))
    if len(b) is 4:
        return (b[3] & 0xFF) + ((b[2] & 0xFF) << 8) + \
               ((b[1] & 0xFF) << 16) + ((b[0] & 0xFF) << 24)
    return None


def read_string_8(stream, length):
    byte = stream.read(length)
    return byte.decode('utf8')


def read_string_16(stream, length):
    byte = stream.read(length)
    return byte.decode('utf16')
