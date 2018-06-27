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
STITCH_NEW_LOCATION = 0xF0
STITCH_NEW_COLOR = 0xF1
STITCH_FINAL_LOCATION = 0xF2
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
        pass  # This should generate, stitchblocks

    def get_as_colorblock(self):
        pass  # This should generate, colorblocks

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

    def list_commands(self, read_object):
        last_x = 0
        last_y = 0
        for thread in self.threadlist:
            read_object.add_thread(thread)
        stitch_position = 0;
        for stitch in self.stitches:
            x = stitch[0]
            y = stitch[1]
            flags = stitch[2]
            dx = x - last_x
            dy = y - last_y
            if flags == STITCH:
                read_object.stitch(dx, dy);
            elif flags == JUMP:
                read_object.move(dx, dy);
            elif flags == COLOR_CHANGE:
                read_object.color_change(dx, dy);
            elif flags == STOP:
                read_object.stop(dx, dy);
            elif flags == TRIM:
                read_object.trim(dx, dy);
            elif flags == SEQUIN:
                read_object.sequin(dx, dy);
            elif flags == END:
                read_object.end(dx, dy)
            else:
                pass
            stitch_position += 1

