from __future__ import print_function


class CountReader():
    def __init__(self):
        self.stitches = 0
        self.moves = 0
        self.stops = 0
        self.trims = 0
        self.color_changes = 0
        self.sequins = 0
        self.ends = 0
        self.threads = 0

    def move(self, dx, dy):
        self.moves += 1;

    def move_abs(self, x, y):
        self.moves += 1;

    def stitch(self, dx, dy):
        self.stitches += 1;

    def stop(self, dx, dy):
        self.stops += 1

    def trim(self, dx, dy):
        self.trims += 1

    def color_change(self, dx, dy):
        self.color_changes += 1

    def sequin(self, dx, dy):
        self.sequins += 1

    def end(self, dx, dy):
        self.ends += 1

    def add_thread(self, thread):
        self.threads += 1

    def print_counts(self):
        print("Stitches:      ", self.stitches)
        print("Jumps:         ", self.moves)
        print("Stops:         ", self.stops)
        print("Trims:         ", self.trims)
        print("Color Changes: ", self.color_changes)
        print("Sequins:       ", self.sequins)
        print("End:           ", self.ends)
        print("Threads:       ", self.threads)
