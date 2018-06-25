import pyembroidery.EmbPattern as EmbPattern


class PatternReader():
    def __init__(self):
        self.pattern = EmbPattern.EmbPattern()

    def move(self, dx: float, dy: float):
        self.pattern.addStitchRel(dx, dy, EmbPattern.JUMP)

    def stitch(self, dx: float, dy: float):
        self.pattern.addStitchRel(dx, dy, EmbPattern.STITCH)

    def stop(self, dx: float, dy: float):
        self.pattern.addStitchRel(dx, dy, EmbPattern.STOP)

    def trim(self, dx: float, dy: float):
        self.pattern.addStitchRel(dx, dy, EmbPattern.TRIM)

    def colorChange(self, dx: float, dy: float):
        self.pattern.addStitchRel(dx, dy, EmbPattern.COLOR_CHANGE)

    def sequin(self, dx: float, dy: float):
        self.pattern.addStitchRel(dx, dy, EmbPattern.SEQUIN)

    def count(self):
        return len(self.pattern.stitches)