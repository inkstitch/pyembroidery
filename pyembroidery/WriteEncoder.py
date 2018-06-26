import pyembroidery.EmbPattern as EmbPattern
import math


def distance_squared(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    dx *= dx
    dy *= dy
    return dx + dy


def distance(x0, y0, x1, y1):
    return math.sqrt(distance_squared(x0, y0, x1, y1))


def towards(a, b, amount):
    return (amount * (b - a)) + a


def angleR(x0, y0, x1, y1):
    return math.atan2(y1 - y0, x1 - x0)


def oriented(x0, y0, x1, y1, r):
    radians = angleR(x0, y0, x1, y1)
    return (x0 + (r * math.cos(radians)), y0 + (r * math.sin(radians)))

class WriteEncoder():
    def __init__(self):
        self.max_jump_length = float('inf')  # type: float
        self.max_stitch_length = float('inf')  # type: float
        self.tie_on = False  # type: bool
        self.tie_off = False  # type: bool
        self.needle_x = 0  # type: float
        self.needle_y = 0  # type: float
        self.translate_X = 0  # type: float
        self.translate_Y = 0  # type: float

    def set_translation(self, x, y):
        self.translate_X = x
        self.translate_Y = y

    def jumpTo(self, transcode, x, y):
        self.step_to_range(transcode, x, y, self.max_jump_length, EmbPattern.JUMP)
        transcode.append([x, y, EmbPattern.JUMP])

    def stitchTo(self, transcode, x, y):
        self.step_to_range(
            transcode,
            x,
            y,
            self.max_stitch_length,
            EmbPattern.STITCH)
        transcode.append([x, y, EmbPattern.STITCH])

    def step_to_range(
            self,
            transcode,
            x,
            y,
            length,
            data):
        distance_x = x - self.needle_x
        distance_y = y - self.needle_y
        if abs(distance_x) > length or abs(distance_y) > length:
            stepsX = math.ceil(abs(distance_x / length))
            stepsY = math.ceil(abs(distance_y / length))
            if (stepsX > stepsY):
                steps = stepsX
            else:
                steps = stepsY
            stepSizeX = distance_x / steps
            stepSizeY = distance_y / steps

            q = 0
            qe = steps
            qx = self.needle_x
            qy = self.needle_y
            while q < qe:
                transcode.append([round(qx), round(qy), data])
                q += 1
                qx += stepSizeX
                qy += stepSizeY

    def lock_stitch(
            self,
            transcode,
            lockposition_x,
            lockposition_y,
            towards_x,
            towards_y):
        if distance(
                lockposition_x,
                lockposition_y,
                towards_x,
                towards_y) > self.max_stitch_length:
            polar = oriented(
                lockposition_x,
                lockposition_y,
                towards_x,
                towards_y,
                self.max_stitch_length)
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

    def process(self, p):
        copy = EmbPattern.EmbPattern()
        EmbPattern.set(p, copy)
        layer = copy.stitches
        for stitch in layer:
            stitch[0] = round(stitch[0] - self.translate_X)
            stitch[1] = round(stitch[1] - self.translate_Y)
        p.stitches = []
        p.threadlist = []
        self.write_code(copy, p)
        self.write_thread(copy, p)
        return p

    def write_thread(self, pattern_from, pattern_to):
        threads_to = pattern_to.threadlist
        threads_to.extend(pattern_to.threadlist)

    def write_code(self, pattern_from, pattern_to):
        from_stitches = pattern_from.stitches
        to_stitches = pattern_to.stitches
        current_index_end = len(from_stitches)
        current_index = 0
        while current_index < current_index_end:
            current = from_stitches[current_index]
            current_x = current[0]
            current_y = current[1]
            current_command = current[2]
            if current_command is EmbPattern.STITCH:
                self.stitchTo(to_stitches, current_x, current_y)
            elif current_command is EmbPattern.STITCH_FINAL_LOCATION:
                if self.tie_off:
                    bi = current_index - 1
                    b = from_stitches[bi]
                    bx = b[0]
                    by = b[1]
                    self.lock_stitch(to_stitches, current_x, current_y, bx, by)
                self.stitchTo(to_stitches, current_x, current_y)
                to_stitches.append([current_x, current_y, EmbPattern.TRIM])
            elif current_command is EmbPattern.STITCH_FINAL_COLOR:
                if self.tie_off:
                    bi = current_index - 1
                    b = from_stitches[bi]
                    bx = b[0]
                    by = b[1]
                    self.lock_stitch(to_stitches, current_x, current_y, bx, by)
                self.stitchTo(to_stitches, current_x, current_y)
                to_stitches.append([current_x, current_y, EmbPattern.TRIM])
                to_stitches.append(
                    [current_x, current_y, EmbPattern.COLOR_CHANGE])
            elif current_command is EmbPattern.STITCH_NEW_LOCATION or current_command is EmbPattern.STITCH_NEW_COLOR:
                self.jumpTo(to_stitches, current_x, current_y)
                self.needle_x = current_x
                self.needle_y = current_y
                if self.tie_on:
                    bi = current_index + 1
                    b = from_stitches[bi]
                    bx = b[0]
                    by = b[1]
                    self.lock_stitch(to_stitches, current_x, current_y, bx, by)
                to_stitches.append([current_x, current_y, EmbPattern.STITCH])
            else:
                to_stitches.append(current)
            self.needle_x = current_x
            self.needle_y = current_y
            current_index += 1
        to_stitches.append([self.needle_x, self.needle_y, EmbPattern.END])
