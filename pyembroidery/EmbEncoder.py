import math

from .EmbConstant import *


class Transcoder:
    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        self.translate_x = settings.get("translate_x", 0)
        self.translate_y = settings.get("translate_y", 0)
        self.has_tie_on = settings.get("tie_on", False)
        self.has_tie_off = settings.get("tie_off", False)
        self.max_stitch = settings.get("max_stitch", float('inf'))
        self.max_jump = settings.get("max_jump", float('inf'))
        self.jump_threshold = settings.get("jump_threshold", self.max_jump)
        self.source_pattern = None
        self.dest_pattern = None
        self.position = 0
        self.color_index = -1
        self.stitch = None
        self.state_trimmed = True
        self.needle_x = 0
        self.needle_y = 0
        self.subdivide_long_stitches = self.max_stitch < self.jump_threshold

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
        Converts middle-level commands and potentially incompatible
        commands into a format friendly low level commands."""
        source = self.source_pattern.stitches
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

            elif flags == STITCH:
                if self.state_trimmed:
                    self.jump_to(x, y)
                    if self.has_tie_on:
                        self.tie_on()
                    self.stitch_at(x, y)
                else:
                    if self.subdivide_long_stitches:
                        self.sew_to(x, y)
                    else:
                        self.needle_to(x, y)
            elif flags == NEEDLE_AT:
                if self.state_trimmed:
                    self.jump_to(x, y)
                    if self.has_tie_on:
                        self.tie_on()
                    self.stitch_at(x, y)
                else:
                    self.needle_to(x, y)
            elif flags == SEW_TO:
                if self.state_trimmed:
                    self.jump_to(x, y)
                    if self.has_tie_on:
                        self.tie_on()
                    self.stitch_at(x, y)
                else:
                    self.sew_to(x, y)

            # Middle Level Commands.
            elif flags == FRAME_EJECT:
                self.tie_off_and_trim_if_needed()
                self.jump_to(x, y)
                self.stop_here()
            elif flags == SEQUENCE_BREAK:
                self.tie_off_and_trim_if_needed()
            elif flags == COLOR_BREAK:
                self.tie_off_and_trim_if_needed()
                self.color_change_here_if_needed()
            elif flags == TIE_OFF:
                self.tie_off()
            elif flags == TIE_ON:
                self.tie_on()

            # Core Commands.
            elif flags == TRIM:
                self.tie_off_and_trim_if_needed()
            elif flags == JUMP:
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
                    self.sew_to(x, y)
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

            # On-the-fly Settings Commands.
            elif flags == ENABLE_TIE_ON:
                self.has_tie_on = True
            elif flags == ENABLE_TIE_OFF:
                self.has_tie_off = True
            elif flags == DISABLE_TIE_ON:
                self.has_tie_on = False
            elif flags == DISABLE_TIE_OFF:
                self.has_tie_off = False
            elif flags == TRANSLATE:
                x = self.stitch[0]
                y = self.stitch[1]
                self.translate_x += x
                self.translate_y += y
            elif flags == JUMP_THRESHOLD:
                x = self.stitch[0]
                self.jump_threshold = x
                self.subdivide_long_stitches = self.max_stitch < self.jump_threshold
            elif flags == MAX_JUMP_LENGTH:
                x = self.stitch[0]
                self.max_jump = x
            elif flags == MAX_STITCH_LENGTH:
                x = self.stitch[0]
                self.max_stitch = x
                self.subdivide_long_stitches = self.max_stitch < self.jump_threshold
        if flags != END:
            self.end_here()

    def update_needle_position(self, x, y):
        self.needle_x = x
        self.needle_y = y

    def declare_not_trimmed(self):
        if self.state_trimmed:
            self.state_trimmed = False
            if self.color_index == -1:
                self.color_index = 0

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
            x = round(b[0] + self.translate_x)
            y = round(b[1] + self.translate_y)
            flags = self.stitch[2]
            if flags == STITCH or flags == NEEDLE_AT or flags == SEW_TO:
                self.lock_stitch(self.needle_x, self.needle_y,
                                 x, y, self.max_stitch)
        except IndexError:
            pass  # must be an island stitch. jump-stitch-jump

    def tie_on(self):
        try:
            b = self.source_pattern.stitches[self.position + 1]
            x = round(b[0] + self.translate_x)
            y = round(b[1] + self.translate_y)
            flags = self.stitch[2]
            if flags == STITCH or flags == NEEDLE_AT or flags == SEW_TO:
                self.lock_stitch(self.needle_x, self.needle_y,
                                 x, y, self.max_stitch)
        except IndexError:
            pass  # must be an island stitch. jump-stitch-jump

    def trim_here(self):
        self.add(TRIM)
        self.state_trimmed = True

    def jump_to(self, new_x, new_y):
        x0 = self.needle_x
        y0 = self.needle_y
        max_length = self.max_jump
        self.constrained_step_to(x0, y0, new_x, new_y, max_length, JUMP)
        self.add(JUMP, new_x, new_y)
        self.update_needle_position(new_x, new_y)

    def sew_to(self, new_x, new_y):
        """Stitches to a specific location, with the emphasis on sewing.
         Subdivides long stitches into additional stitches.
        """
        x0 = self.needle_x
        y0 = self.needle_y
        max_length = self.max_stitch
        self.constrained_step_to(x0, y0, new_x, new_y, max_length, STITCH)
        self.stitch_at(new_x, new_y)

    def needle_to(self, new_x, new_y):
        """Insert needle at specific location, emphasis on the needle.
        Uses jumps to avoid needle penetrations where possible.

        The limit here is the max stitch limit or jump threshold.
        If jump threshold is set low, it will insert jumps even
        between stitches it could have technically encoded values for.

        Stitches to the new location, adding jumps if needed.
        """
        x0 = self.needle_x
        y0 = self.needle_y
        max_length = min(self.jump_threshold, self.max_stitch)
        if self.position_will_exceed_constraint(max_length):
            pass
        self.constrained_step_to(x0, y0, new_x, new_y, max_length, JUMP)
        self.stitch_at(new_x, new_y)

    def stitch_at(self, new_x, new_y):
        """Inserts a stitch at the specific location.
        Should have already been checked for constraints."""
        self.add(STITCH, new_x, new_y)
        self.update_needle_position(new_x, new_y)
        self.declare_not_trimmed()

    def sequin_at(self, new_x, new_y):
        # TODO: There might be other middle-level commands needed here.
        self.add(SEQUIN)
        self.update_needle_position(new_x, new_y)
        self.declare_not_trimmed()

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
            # post-stitch color-changes are pointless.

    def color_change_here(self):
        self.add(COLOR_CHANGE)
        self.color_index += 1
        self.state_trimmed = True

    def position_will_exceed_constraint(self, length=None, new_x=None, new_y=None):
        """Check if the stitch is too long before trying to deal with it."""
        if length is None:
            length = self.max_stitch
        if new_x is None or new_y is None:
            new_x = round(self.stitch[0] + self.translate_x)
            new_y = round(self.stitch[1] + self.translate_y)
        distance_x = new_x - self.needle_x
        distance_y = new_y - self.needle_y
        return abs(distance_x) > length or abs(distance_y) > length

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
