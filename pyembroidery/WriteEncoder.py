import pyembroidery.EmbPattern as EmbPattern
import math


def distanceSq(x0: float, y0: float, x1: float, y1: float) -> float:
    dx = x1 - x0
    dy = y1 - y0
    dx *= dx
    dy *= dy
    return dx + dy


def distance(x0: float, y0: float, x1: float, y1: float) -> float:
    return math.sqrt(distanceSq(x0, y0, x1, y1))


def towards(a: float, b: float, amount: float) -> float:
    return (amount * (b - a)) + a


def angleR(x0: float, y0: float, x1: float, y1: float) -> float:
    return math.atan2(y1 - y0, x1 - x0)


def oriented(x0: float, y0: float, x1: float, y1: float, r: float):
    radians = angleR(x0, y0, x1, y1)
    return (x0 + (r * math.cos(radians)), y0 + (r * math.sin(radians)))


def rint(v: float) -> int:
    return round(v)
    # This should actually perform a proper rint.


class WriteEncoder():
    def __init__(self):
        self.maxJumpLength = float('inf')  # type: float
        self.maxStitchLength = float('inf')  # type: float
        self.tie_on = False  # type: bool
        self.tie_off = False  # type: bool
        self.needle_X = 0  # type: float
        self.needle_Y = 0  # type: float
        self.translate_X = 0  # type: float
        self.translate_Y = 0  # type: float

    def setTranslation(self, x: float, y: float):
        self.translate_X = x
        self.translate_Y = y

    def jumpTo(self, transcode, x: float, y: float):
        self.stepToRange(transcode, x, y, self.maxJumpLength, EmbPattern.JUMP)
        transcode.append([x, y, EmbPattern.JUMP])

    def stitchTo(self, transcode, x: float, y: float):
        self.stepToRange(
            transcode,
            x,
            y,
            self.maxStitchLength,
            EmbPattern.STITCH)
        transcode.append([x, y, EmbPattern.STITCH])

    def stepToRange(
            self,
            transcode,
            x: float,
            y: float,
            length: float,
            data: int):
        distanceX = x - self.needle_X
        distanceY = y - self.needle_Y
        if abs(distanceX) > length or abs(distanceY) > length:
            stepsX = math.ceil(abs(distanceX / length))
            stepsY = math.ceil(abs(distanceY / length))
            if (stepsX > stepsY):
                steps = stepsX
            else:
                steps = stepsY
            stepSizeX = distanceX / steps
            stepSizeY = distanceY / steps

            q = 0
            qe = steps
            qx = self.needle_X
            qy = self.needle_Y
            while q < qe:
                transcode.append([rint(qx), rint(qy), data])
                q += 1
                qx += stepSizeX
                qy += stepSizeY

    def lockStitch(
            self,
            transcode,
            lockposition_x: float,
            lockposition_y: float,
            towards_x: float,
            towards_y: float):
        if distance(
                lockposition_x,
                lockposition_y,
                towards_x,
                towards_y) > self.maxStitchLength:
            polar = oriented(
                lockposition_x,
                lockposition_y,
                towards_x,
                towards_y,
                self.maxStitchLength)
            towards_x = polar[0]
            towards_y = polar[1]
        self.stitchTo(transcode, lockposition_x, lockposition_y)
        self.stitchTo(
            transcode, towards(
                lockposition_x, towards_x, .33), towards(
                lockposition_y, towards_y, .33))
        self.stitchTo(
            transcode, towards(
                lockposition_x, towards_x, .66), towards(
                lockposition_y, towards_y, .66))
        self.stitchTo(
            transcode, towards(
                lockposition_x, towards_x, .33), towards(
                lockposition_y, towards_y, .33))

    def process(self, p: EmbPattern) -> EmbPattern:
        copy = EmbPattern.EmbPattern()
        EmbPattern.set(p, copy)
        layer = copy.stitches
        for stitch in layer:
            stitch[0] = rint(stitch[0] - self.translate_X)
            stitch[1] = rint(stitch[1] - self.translate_Y)
        p.stitches = []
        p.threadlist = []
        self.writeCode(copy, p)
        self.writeThread(copy, p)
        return p

    def writeThread(self, pattern_from, pattern_to):
        threads_to = pattern_to.threadlist
        threads_to.extend(pattern_to.threadlist)

    def writeCode(self, pattern_from, pattern_to):
        fromPoints = pattern_from.stitches
        toPoints = pattern_to.stitches
        currentIndexEnd = len(fromPoints)
        currentIndex = 0
        while currentIndex < currentIndexEnd:
            current = fromPoints[currentIndex]
            current_x = current[0]
            current_y = current[1]
            processingCommand = current[2]
            if processingCommand is EmbPattern.STITCH:
                self.stitchTo(toPoints, current_x, current_y)
            elif processingCommand is EmbPattern.STITCH_FINAL_LOCATION:
                if self.tie_off:
                    bi = currentIndex - 1
                    b = fromPoints[bi]
                    bx = b[0]
                    by = b[1]
                    self.lockStitch(toPoints, current_x, current_y, bx, by)
                self.stitchTo(toPoints, current_x, current_y)
                toPoints.append([current_x, current_y, EmbPattern.TRIM])
            elif processingCommand is EmbPattern.STITCH_FINAL_COLOR:
                if self.tie_off:
                    bi = currentIndex - 1
                    b = fromPoints[bi]
                    bx = b[0]
                    by = b[1]
                    self.lockStitch(toPoints, current_x, current_y, bx, by)
                self.stitchTo(toPoints, current_x, current_y)
                toPoints.append([current_x, current_y, EmbPattern.TRIM])
                toPoints.append(
                    [current_x, current_y, EmbPattern.COLOR_CHANGE])
            elif processingCommand is EmbPattern.STITCH_NEW_LOCATION or processingCommand is EmbPattern.STITCH_NEW_COLOR:
                self.jumpTo(toPoints, current_x, current_y)
                self.needle_X = current_x
                self.needle_Y = current_y
                if self.tie_on:
                    bi = currentIndex + 1
                    b = fromPoints[bi]
                    bx = b[0]
                    by = b[1]
                    self.lockStitch(toPoints, current_x, current_y, bx, by)
                toPoints.append([current_x, current_y, EmbPattern.STITCH])
            else:
                toPoints.append(current)
            self.needle_X = current_x
            self.needle_Y = current_y
            currentIndex += 1
        toPoints.append([self.needle_X, self.needle_Y, EmbPattern.END])
