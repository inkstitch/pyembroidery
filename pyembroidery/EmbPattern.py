import pyembroidery.EmbThread as EmbThread

NO_COMMAND = -1
STITCH = 0
JUMP = 1
TRIM = 2
STOP = 3
END = 4
COLOR_CHANGE = 5
INIT = 6
SEQUIN = 7


BREAK = 0xE1
BREAK_COLOR = 0xE2
FRAME_EJECT = 0xE9
STITCH_FINAL = 0xF2
STITCH_FINAL_COLOR = 0xF3
COMMAND_MASK = 0xFF


def set(p, copy):
    copy.stitches = p.stitches
    copy.threadlist = p.threadlist
    copy.filename = p.filename
    copy.name = p.name
    copy.category = p.category
    copy.author = p.author
    copy.keywords = p.keywords
    copy.comments = p.comments
    copy.copyright = p.copyright


class EmbPattern():
    def __init__(self):
        self.stitches = []  # type: list
        self.threadlist = []  # type: list
        self.filename = None  # type: str
        self.name = None  # type: str
        self.category = None  # type: str
        self.author = None  # type: str
        self.keywords = None  # type: str
        self.comments = None  # type: str
        self.copyright = None  # type: str
        self._previousX = 0  # type: float
        self._previousY = 0  # type: float
        # filename, name, category, author, keywords, comments, are typical
        # metadata.

    def extends(self):
        min_x = float('inf')
        min_y = float('inf')
        max_x = -float('inf')
        max_y = -float('inf')

        for stitch in self.stitches:
            if stitch[0] > max_x:
                max_x = stitch[0]
            if stitch[0] < min_x:
                min_x = stitch[0]
            if stitch[1] > max_y:
                max_y = stitch[1]
            if stitch[1] < min_y:
                min_y = stitch[1]
        return (min_x, min_y, max_x, max_y)

    def count_stitch_commands(self, command):
        count = 0
        for stitch in self.stitches:
            flags = stitch[2]
            if flags == command:
                count += 1
        return count

    def count_color_changes(self):
        return self.count_stitch_commands(COLOR_CHANGE)

    def count_stitches(self):
        return len(self.stitches)

    def count_threads(self):
        return len(self.threadlist)

    def add(self, x, y, cmd):
        self.stitches.append([x, y, cmd])

    def add_thread(self, thread):
        self.threadlist.append(thread)

    def get_random_thread(self):
        import random
        thread = EmbThread.EmbThread()
        thread.color = 0xFF000000 | random.randint(0, 0xFFFFFF)
        thread.description = "Random"
        return thread

    def get_thread_or_filler(self, index):
        if (len(self.threadlist) <= index):
            return self.get_random_thread()
        else:
            return self.threadlist[index]

    def get_as_stitchblock(self):
        stitchblock = []
        thread = self.get_thread_or_filler(0)
        thread_index = 1;
        for stitch in self.stitches:
            flags = stitch[2]
            if flags == STITCH:
                stitchblock.append(stitch);
            else:
                if len(stitchblock) > 0:
                    yield (stitchblock, thread)
                    stitchblock.clear()
                if flags == COLOR_CHANGE:
                    thread = self.get_thread_or_filler(thread_index)
                    thread_index += 1;
        if len(stitchblock) > 0:
            yield (stitchblock,thread)


    def get_unique_threadlist(self):
        return set(self.threadlist)

    def get_singleton_threadlist(self):
        singleton = []
        last_thread = null
        for thread in self.threadlist:
            if thread != last_thread:
                singleton.append(thread)
            last_thread = thread
        return singleton

    def translate(self, dx, dy):
        for stitch in self.stitches:
            stitch[0] += dx
            stitch[1] += dy

    def fix_color_count(self):
        thread_index = 0
        starting = True
        for stitch in self.stitches:
            data = stitch[2] & COMMAND_MASK
            if data == STITCH:
                if starting:
                    thread_index += 1
                    starting = False
            elif data == COLOR_CHANGE:
                if starting:
                    continue
                thread_index += 1
        while len(self.threadlist) < thread_index:
            self.add_thread(self.get_thread_or_filler(len(self.threadlist)))

    def add_stitch_absolute(self, x, y, cmd):
        self.add(x, y, cmd)
        self._previousX = x
        self._previousY = y

    def add_stitch_relative(self, dx, dy, cmd):
        x = self._previousX + dx
        y = self._previousY + dy
        self.add_stitch_absolute(x, y, cmd)
