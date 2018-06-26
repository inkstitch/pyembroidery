import pyembroidery.EmbPattern as EmbPattern


class PatternReader():
    def __init__(self):
        self.pattern = EmbPattern.EmbPattern()

    def move(self, dx, dy):
        self.pattern.add_stitch_relative(dx, dy, EmbPattern.JUMP)

    def stitch(self, dx, dy):
        self.pattern.add_stitch_relative(dx, dy, EmbPattern.STITCH)

    def stop(self, dx, dy):
        self.pattern.add_stitch_relative(dx, dy, EmbPattern.STOP)

    def trim(self, dx, dy):
        self.pattern.add_stitch_relative(dx, dy, EmbPattern.TRIM)

    def color_change(self, dx, dy):
        self.pattern.add_stitch_relative(dx, dy, EmbPattern.COLOR_CHANGE)

    def sequin(self, dx, dy):
        self.pattern.add_stitch_relative(dx, dy, EmbPattern.SEQUIN)

    def stop(self,dx,dy):
        self.pattern.add_stitch_relative(dx,dy, EmbPattern.END)

    def add_thread(self, thread):
        self.pattern.add_thread(thread)
