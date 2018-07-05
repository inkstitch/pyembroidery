import math

from .EmbConstant import *


class Transcoder:
    def __init__(self, encode_settings=None):
        if encode_settings is None:
            encode_settings = {}
        self.translate_x = encode_settings.get("translate_x", 0)
        self.translate_y = encode_settings.get("translate_y", 0)
        self.has_tie_on = encode_settings.get("tie_on", False)
        self.has_tie_off = encode_settings.get("tie_off", False)
        self.max_stitch = encode_settings.get("max_stitch", float('inf'))
        self.max_jump = encode_settings.get("max_jump", float('inf'))
        self.source_pattern = None
        self.dest_pattern = None
        self.position = 0
        self.color_index = -1
        self.stitch = None
        self.state_trimmed = True
        self.needle_x = 0
        self.needle_y = 0

    def transcode(self, source_pattern, destination_pattern):
        self.source_pattern = source_pattern
        self.dest_pattern = destination_pattern
        self.transcode_metadata()
        self.transcode_threads()
        self.transcode_stitches()
        return destination_pattern

    def transcode_metadata(self):
        """Transcodes metadata, (just moves)"""
        source = self.source_pattern
        dest = self.dest_pattern
        self.dest_pattern.extras = self.source_pattern.extras.copy()

    def transcode_threads(self):
        """Transcodes threads, (just moves)"""
        source = self.source_pattern.threadlist
        dest = self.dest_pattern.threadlist
        dest.extend(source)

    def transcode_stitches(self):
        """Transcodes stitches.
        Converts middle-level commands and potentially incompatable
        commands into a format friendly low level commands."""
        source = self.source_pattern.stitches
        dest = self.dest_pattern.stitches
        self.state_trimmed = True
        self.needle_x = 0
        self.needle_y = 0
        self.position = 0
        self.color_index = -1
        flags = NO_COMMAND

        for self.position, self.stitch in enumerate(source):
            x = round(self.stitch[0] + self.translate_x)
            y = round(self.stitch[1] + self.translate_y)
            flags = self.stitch[2]
            if flags == NO_COMMAND:
                continue
            elif flags == ENABLE_TIE_ON:
                self.has_tie_on = True
            elif flags == ENABLE_TIE_OFF:
                self.has_tie_off = True
            elif flags == DISABLE_TIE_ON:
                self.has_tie_on = False
            elif flags == DISABLE_TIE_OFF:
                self.has_tie_off = False
            elif flags == TRANSLATE:
                self.translate_x += x
                self.translate_y += y
            elif flags == FRAME_EJECT:
                self.tie_off_and_trim_if_needed()
                self.jump_to(x, y)
                self.stop_here()
            elif flags == SEQUENCE_BREAK:
                self.tie_off_and_trim_if_needed()
            elif flags == COLOR_BREAK:
                self.tie_off_and_trim_if_needed()
                self.color_change_here_if_needed()
            elif flags == STITCH:
                if self.state_trimmed:
                    self.jump_to(x, y)
                    if self.has_tie_on:
                        self.tie_on()
                    self.stitch_at(x, y)
                else:
                    self.stitch_to(x, y)
            elif flags == TRIM:
                self.tie_off_and_trim_if_needed()
            elif flags == JUMP:
                self.tie_off_and_trim_if_needed()
                self.jump_to(x, y)
            elif flags == SEQUIN:
                # While DST are the only files with this there are some
                # chances that we might need to further alter the routines
                # built here by the format. For example dst calls a sequin
                # command out of jumps and toggles that on and off. Other
                # formats might use a different paradigm.
                if self.state_trimmed:
                    self.jump_to(x, y)
                    if self.has_tie_on:
                        self.tie_on()
                else:
                    self.stitch_to(x, y)
                self.sequin_at(x, y)
            elif flags == COLOR_CHANGE:
                self.tie_off_and_trim_if_needed()
                self.color_change_here()
                # If we are told to do something we do it.
                # Even if it's the first command and makes no sense.
            elif flags == STOP:
                self.stop_here()
            elif flags == END:
                self.end_here()
                break
        if flags != END:
            self.end_here()

    def needle(self, x, y):
        self.needle_x = x
        self.needle_y = y

    def add(self, flags, x=None, y=None):
        if x is None:
            x = self.needle_x
        if y is None:
            y = self.needle_y
        self.dest_pattern.stitches.append([x, y, flags])

    def tie_off_and_trim_if_needed(self):
        if not self.state_trimmed:
            self.tie_off_and_trim()

    def tie_off_and_trim(self):
        if self.has_tie_off:
            self.tie_off()
        self.trim_here()

    def tie_off(self):
        try:
            b = self.source_pattern.stitches[self.position - 1]
            if b[2] == STITCH:
                self.lock_stitch(self.needle_x, self.needle_y,
                                 b[0], b[1], self.max_stitch)
        except IndexError:
            pass  # must be an island stitch. jump-stitch-jump

    def tie_on(self):
        try:
            b = self.source_pattern.stitches[self.position + 1]
            if b[2] == STITCH:
                self.lock_stitch(self.needle_x, self.needle_y,
                                 b[0], b[1], self.max_stitch)
        except IndexError:
            pass  # must be an island stitch. jump-stitch-jump

    def trim_here(self):
        self.add(TRIM)
        self.state_trimmed = True

    def jump_to(self, new_x, new_y):
        self.constrained_jump_to(self.needle_x, self.needle_y,
                                 new_x, new_y, self.max_jump)
        self.needle(new_x, new_y)

    def stitch_to(self, new_x, new_y):
        self.constrained_stitch_to(self.needle_x, self.needle_y,
                                   new_x, new_y, self.max_stitch)
        self.needle(new_x, new_y)
        if self.state_trimmed:
            self.state_trimmed = False
            if self.color_index == -1:
                self.color_index = 0

    def stitch_at(self, new_x, new_y):
        self.add(STITCH, new_x, new_y)
        self.needle(new_x, new_y)
        if self.state_trimmed:
            self.state_trimmed = False
            if self.color_index == -1:
                self.color_index = 0

    def sequin_at(self, new_x, new_y):
        # TODO: There might be other middle-level commands needed here.
        self.add(SEQUIN)
        self.needle(new_x, new_y)
        if self.state_trimmed:
            self.state_trimmed = False
            if self.color_index == -1:
                self.color_index = 0

    def stop_here(self):
        self.add(STOP)
        self.state_trimmed = True

    def end_here(self):
        self.add(END)
        self.state_trimmed = True

    def color_change_here_if_needed(self):
        if self.color_index >= 0:  # Have we stitched anything yet?
            self.color_change_here()
            # We should actually look ahead and ensure
            # there are no more objects that will become stitches.

    def color_change_here(self):
        self.add(COLOR_CHANGE)
        self.color_index += 1
        self.state_trimmed = True

    def constrained_jump_to(self, x0, y0, x1, y1, max_length=None):
        """Jumps from x0, y1 to x1, y1, respecting max length"""
        if max_length is None:
            max_length = self.max_jump
        self.constrained_step_to(x0, y0, x1, y1, max_length, JUMP)
        self.add(JUMP, x1, y1)

    def constrained_stitch_to(self, x0, y0, x1, y1, max_length=None):
        """Stitches from x0, y1 to x1, y1, respecting max length"""
        if max_length is None:
            max_length = self.max_stitch
        self.constrained_step_to(x0, y0, x1, y1, max_length, STITCH)
        self.add(STITCH, x1, y1)

    def constrained_step_to(self, x0, y0, x1, y1, max_length, data):
        """Command sequence line to x, y, respecting length as maximum.
        This does not arrive_at, it steps to within striking distance.
        The next step can arrive at (x, y) without violating constraint.
        If these are already in range, this command will do nothing.
        """
        transcode = self.dest_pattern.stitches
        distance_x = x1 - x0
        distance_y = y1 - y0
        if abs(distance_x) > max_length or abs(distance_y) > max_length:
            steps_x = math.ceil(abs(distance_x / max_length))
            steps_y = math.ceil(abs(distance_y / max_length))
            if steps_x > steps_y:
                steps = steps_x
            else:
                steps = steps_y
            step_size_x = distance_x / steps
            step_size_y = distance_y / steps

            q = 0
            qe = steps
            qx = x0
            qy = y0
            while q < qe:
                transcode.append([round(qx), round(qy), data])
                q += 1
                qx += step_size_x
                qy += step_size_y

    def lock_stitch(self, x, y, anchor_x, anchor_y, max_length=None):
        """Tie-on, Tie-off. Lock stitch from current location towards
        anchor location.Ends again at lock location. May not exceed
        max_length in the process."""
        if max_length is None:
            max_length = self.max_stitch
        transcode = self.dest_pattern.stitches
        dist = distance(x, y, anchor_x, anchor_y)
        if dist > max_length:
            p = oriented(x, y, anchor_x, anchor_y, max_length)
            anchor_x = p[0]
            anchor_y = p[1]
        for amount in (0, .33, .66, .33, 0):
            transcode.append([
                towards(x, anchor_x, amount),
                towards(y, anchor_y, amount),
                STITCH])


def distance_squared(x0, y0, x1, y1):
    """squared of distance between x0,y0 and x1,y1"""
    dx = x1 - x0
    dy = y1 - y0
    dx *= dx
    dy *= dy
    return dx + dy


def distance(x0, y0, x1, y1):
    """distance between x0,y0 and x1,y1"""
    return math.sqrt(distance_squared(x0, y0, x1, y1))


def towards(a, b, amount):
    """amount between [0,1] -> [a,b]"""
    return (amount * (b - a)) + a


def angle_radians(x0, y0, x1, y1):
    """Angle in radians between x0,y0 and x1,y1"""
    return math.atan2(y1 - y0, x1 - x0)


def oriented(x0, y0, x1, y1, r):
    """from x0,y0 in the direction of x1,y1 in the distance of r"""
    radians = angle_radians(x0, y0, x1, y1)
    return x0 + (r * math.cos(radians)), y0 + (r * math.sin(radians))
