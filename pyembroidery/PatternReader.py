import pyembroidery.EmbPattern as EmbPattern


class PatternReader():
    def __init__(self):
        self.pattern = EmbPattern.EmbPattern()

    def move(self, dx, dy):
        self.pattern.add_stitch_relative(dx, dy, EmbPattern.JUMP)

    def move_abs(self, x, y):
        self.pattern.add_stitch_absolute(x, y, EmbPattern.JUMP)

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

    def end(self, dx, dy):
        self.pattern.add_stitch_relative(dx, dy, EmbPattern.END)

    def add_thread(self, thread):
        self.pattern.add_thread(thread)

    def metadata(self, name, data):
        if name == "name":
            self.pattern.name = data
        elif name == "filename":
            self.pattern.filename = data
        elif name == "author":
            self.pattern.author = data
        elif name == "copyright":
            self.pattern.copyright = data
        elif name == "category":
            self.pattern.category = data
        elif name == "comment":
            self.pattern.comments = data
        elif name == "keywords":
            self.pattern.keywords = data
