def writeInt8(stream, value: int):
    stream.write(bytes([value & 0xFF]))


def writeInt16LE(stream, value: int):
    stream.write(bytes([value & 0xFF, (value >> 8) & 0xFF]))


def writeInt16BE(stream, value: int):
    stream.write(bytes(reversed([value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF])))


def writeInt24LE(stream, value: int):
    stream.write(bytes([value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF]))


def writeInt24BE(stream, value: int):
    stream.write(bytes(reversed([value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF, (value >> 24) & 0xFF])))


def writeInt32LE(stream, value: int):
    stream.write(bytes([value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF, (value >> 24) & 0xFF]))


def writeInt32BE(stream, value: int):
    stream.write(bytes(reversed([value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF, (value >> 24) & 0xFF])))


def write(stream, string: str):
    stream.write(bytes[string, 'utf8'])
