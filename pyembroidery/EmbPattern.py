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

class EmbPattern():
    def __init__(self):
        self.stitches = [] #type: list
        self.threadlist = [] #type: list
        self.filename = None #type: str
        self.name = None #type: str
        self.category = None  # type: str
        self.author = None  # type: str
        self.keywords = None  # type: str
        self.comments = None  # type: str
        self._previousX = 0  # type: float
        self._previousY = 0 # type: float
        # filename, name, category, author, keywords, comments, are typical metadata.

    def add(self, x, y, cmd):
        self.stitches.append([x, y, cmd]);

    def addThread(self, thread):
        self.threadlist.append(self, thread)

    def getRandomThread(self):
        return EmbThread(0xFF000000, "Random")

    def getThreadOrFiller(self, index):
        if (len(self.threadlist) <= index):
            return self.getRandomThread()
        else:
            return self.threadlist[index]

    def getThreadCount(self):
        return len(self.threadlist)

    def getAsEmbObject(self):
        pass  # This should generate, stitchblocks

    def getAsColorObject(self):
        pass  # This should generate, colorblocks

    def getUniqueThreadList(self):
        return set(self.threadlist)

    def getSingletonThreadList(self):
        singleton = []
        lastthread = null
        for thread in self.threadlist:
            if thread != lastthread:
                singleton.append(thread)
            lastthread = thread
        return singleton;

    def translate(self, dx, dy):
        for stitch in self.command:
            stitch[0] += dx;
            stitch[1] += dy;

    def fixColorCount(self):
        threadIndex = 0;
        starting = True;
        for stitch in self.command:
            data = stitch[2] & COMMAND_MASK
            if data == STITCH:
                if starting:
                    threadIndex += 1
                starting = false
            elif data == self.commands['COLOR_CHANGE']:
                if starting:
                    continue
                threadIndex += 1
        while len(self.threadlist) < threadIndex:
            self.addThread(self.getThreadOrFiller(len(self.threadlist)))

    def addStitchAbs(self, x, y, cmd):
        self.add(x, y, cmd)
        self._previousX = x;
        self._previousY = y;

    def addStitchRel(self, dx, dy, cmd):
        x = self._previousX + dx;
        y = self._previousY + dy;
        self.addStitchAbs(x, y, cmd)
