def signed(b):
    if b > 127:
        return -256 + b
    else:
        return b


def read_signed(stream, n):
    byte = stream.read(n);
    signed_bytes = []
    for b in byte:
        signed_bytes.append(signed(b))
    return signed_bytes;


def read_sint_8(stream):
    byte = stream.read(1)
    if len(byte) is 1:
        return signed(byte[0]);
    return None


def read_int_8(stream):
    byte = stream.read(1)
    if len(byte) is 1:
        return byte[0];
    return None


def read_int_16le(stream):
    byte = stream.read(2)
    if len(byte) is 2:
        return (byte[0] & 0xFF) + ((byte[1] & 0xFF) << 8)
    return None


def read_int_16be(stream):
    byte = stream.read(2)
    if len(byte) is 2:
        return ((byte[1] & 0xFF) << 8) + (byte[0] & 0xFF);
    return None


def read_int_24le(stream):
    byte = stream.read(3)
    if len(byte) is 3:
        return (byte[0] & 0xFF) + ((byte[1] & 0xFF) << 8) + \
               ((byte[2] & 0xFF) << 16)
    return None


def read_int_24be(stream):
    byte = stream.read(3)
    if len(byte) is 3:
        return (byte[2] & 0xFF) + ((byte[1] & 0xFF) << 8) + \
               ((byte[0] & 0xFF) << 16)
    return None


def read_int_32le(stream):
    byte = stream.read(4)
    if len(byte) is 4:
        return (byte[0] & 0xFF) + ((byte[1] & 0xFF) << 8) + \
               ((byte[2] & 0xFF) << 16) + ((byte[3] & 0xFF) << 24)
    return None


def read_int_32be(stream):
    byte = stream.read(4)
    if len(byte) is 4:
        return (byte[3] & 0xFF) + ((byte[2] & 0xFF) << 8) + \
               ((byte[1] & 0xFF) << 16) + ((byte[0] & 0xFF) << 24);
    return None

def read_string_8(stream,length):
    byte = stream.read(length);
    return byte.decode('utf8');


def read_string_16(stream,length):
    byte = stream.read(length);
    return byte.decode('utf16');
