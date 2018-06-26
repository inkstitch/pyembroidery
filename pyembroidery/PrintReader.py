from __future__ import print_function

class PrintReader():
    def move(self, dx, dy):
        print("JUMP ", dx, dy)

    def stitch(self, dx, dy):
        print("STITCH", dx, dy)

    def stop(self, dx, dy):
        print("STOP")

    def trim(self, dx, dy):
        print("TRIM")

    def color_change(self, dx, dy):
        print("COLOR_CHANGE")

    def sequin(self, dx, dy):
        print("SEQUIN")
