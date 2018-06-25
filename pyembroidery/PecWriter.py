import math
import io
import pyembroidery.EmbPattern as EmbPattern
import pyembroidery.EmbThread as EmbThread
import pyembroidery.EmbThreadPec as EmbThreadPec
import pyembroidery.WriteHelper as helper
import pyembroidery.PecGraphics as PecGraphics

maxJumpDistance = 2047
maxStitchDistance = 2047

MASK_07_BIT = 0b01111111
JUMP_CODE = 0b00010000
TRIM_CODE = 0b00100000
FLAG_LONG = 0b10000000
PEC_ICON_WIDTH = 48
PEC_ICON_HEIGHT = 38


def write(pattern: EmbPattern, file):
    with open(file, "wb") as f:
        f.write(bytes("#PEC0001", 'utf8'))
        writePecStitches(pattern, f)


def encodeLongForm(value: int) -> int:
    value &= 0b00001111_11111111
    value |= 0b10000000_00000000
    return value


def flagJump(longForm: int) -> int:
    return longForm | (JUMP_CODE << 8)


def flagTrim(longForm: int) -> int:
    return longForm | (TRIM_CODE << 8)


def pecEncode(pattern: EmbPattern, f):
    colorchangeJump = False
    colorTwo = True
    jumping = False
    stitches = pattern.stitches
    xx = 0
    yy = 0
    for stitch in stitches:
        x = stitch[0]
        y = stitch[1]
        data = stitch[2]
        dx = x - xx
        dy = y - yy
        if data is EmbPattern.STITCH:
            deltaX = round(dx)
            deltaY = round(dy)
            if jumping and deltaX is not 0 and deltaY is not 0:
                f.write(b'\x00\x00')
                jumping = False
            if -64 < deltaX < 63 and -64 < deltaY < 63:
                f.write(bytes([deltaX & MASK_07_BIT, deltaY & MASK_07_BIT]))
            else:
                deltaX = encodeLongForm(deltaX)
                deltaY = encodeLongForm(deltaY)
                data = [
                    (deltaX >> 8) & 0xFF,
                    deltaX & 0xFF,
                    (deltaY >> 8) & 0xFF,
                    deltaY & 0xFF]
                f.write(bytes(data))
        elif data is EmbPattern.JUMP:
            jumping = True
            deltaX = round(dx)
            deltaX = encodeLongForm(deltaX)
            if colorchangeJump:
                deltaX = flagJump(deltaX)
            else:
                deltaX = flagTrim(deltaX)
            deltaY = round(dy)
            deltaY = encodeLongForm(deltaY)
            if colorchangeJump:
                deltaY = flagJump(deltaY)
            else:
                deltaY = flagTrim(deltaY)
            f.write(bytes([
                (deltaX >> 8) & 0xFF,
                deltaX & 0xFF,
                (deltaY >> 8) & 0xFF,
                deltaY & 0xFF
            ]))
            colorchangeJump = False
        elif data is EmbPattern.COLOR_CHANGE:
            if jumping:
                f.write(b'\x00\x00')
                jumping = False
            f.write(b'\xfe\xb0')
            if colorTwo:
                f.write(b'\x02')
            else:
                f.write(b'\x01')
        elif data is EmbPattern.STOP:
            if jumping:
                f.write(b'\x00\x00')
                jumping = False
            f.write(b'\x80\x01\x00\x00')
        elif data is EmbPattern.END:
            if jumping:
                f.write(b'\x00\x00')
                jumping = False
            f.write(b'\xff')
        xx = x
        yy = y


def writePecStitches(pattern: EmbPattern, f):
    extends = pattern.extends()
    width = extends[2] - extends[0]
    height = extends[3] - extends[1]

    name = pattern.name
    if name is None:
        name = "Untitled"
    name = name[:8]
    f.write(bytes("LA:%-16s\r" % (name), 'utf8'))
    f.write(b'\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\xFF\x00\x06\x26')

    pattern.fixColorCount()
    threadset = EmbThreadPec.getThreadSet()
    chart = [None] * len(threadset)
    for thread in set(pattern.threadlist):
        index = thread.findNearestIndex(threadset)
        threadset[index] = None
        chart[index] = thread

    colorlist = []
    for thread in pattern.threadlist:
        colorlist.append(thread.findNearestIndex(chart))
    currentThreadCount = len(colorlist)
    if currentThreadCount is not 0:
        f.write(b'\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20')
        colorlist.insert(0, currentThreadCount - 1)
        f.write(bytes(colorlist))
    else:
        f.write(b'\x20\x20\x20\x20\x64\x20\x00\x20\x00\x20\x20\x20\xFF')
    for i in range(currentThreadCount, 463):
        f.write(b'\x20')  # 520
    f.write(b'\x00\x00')
    encodef = io.BytesIO()
    pecEncode(pattern, encodef)
    graphicsOffsetValue = encodef.tell() + 20
    helper.writeInt24LE(f, graphicsOffsetValue)
    f.write(b'\x31\xff\xf0')
    helper.writeInt16LE(f, round(width))
    helper.writeInt16LE(f, round(height))
    helper.writeInt16LE(f, 0x1E0)
    helper.writeInt16LE(f, 0x1B0)

    helper.writeInt16LE(f, 0x9000 | -round(extends[0]))
    helper.writeInt16LE(f, 0x9000 | -round(extends[1]))
    pecEncode(pattern, f)
    # shutil.copyfileobj(encodef, f)

    blank = PecGraphics.blank

    f.write(bytes(blank))
    for i in range(0, currentThreadCount):
        f.write(bytes(blank))
