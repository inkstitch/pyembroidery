import pyembroidery.EmbPattern as EmbPattern


class PatternReader():
    def __init__(self):
        self.pattern = EmbPattern.EmbPattern()

    def move(self, dx: float, dy: float):
        self.pattern.add_stitch_relative(dx, dy, EmbPattern.JUMP)

    def stitch(self, dx: float, dy: float):
        self.pattern.add_stitch_relative(dx, dy, EmbPattern.STITCH)

    def stop(self, dx: float, dy: float):
        self.pattern.add_stitch_relative(dx, dy, EmbPattern.STOP)

    def trim(self, dx: float, dy: float):
        self.pattern.add_stitch_relative(dx, dy, EmbPattern.TRIM)

    def color_change(self, dx: float, dy: float):
        self.pattern.add_stitch_relative(dx, dy, EmbPattern.COLOR_CHANGE)

    def sequin(self, dx: float, dy: float):
        self.pattern.add_stitch_relative(dx, dy, EmbPattern.SEQUIN)

    def count(self):
        return len(self.pattern.stitches)
