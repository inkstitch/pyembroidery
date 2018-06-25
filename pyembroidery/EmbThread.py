
def findNearestIndex(findColor: int, values) -> int:
    red = (findColor >> 16) & 0xff
    green = (findColor >> 8) & 0xff
    blue = findColor & 0xff;
    closestIndex = -1
    currentIndex = -1
    currentClosestValue = float("inf")
    for t in values:
        currentIndex += 1;
        if t is None:
            continue
        dist = distanceRedMean(red, green, blue, t.getRed(), t.getGreen(), t.getBlue())
        if dist <= currentClosestValue:
            currentClosestValue = dist
            closestIndex = currentIndex


def distanceRedMean(r1: int, g1: int, b1: int, r2: int, g2: int, b2: int) -> float:
    rmean = r1 + r2 / 2;
    r = r1 - r2
    g = g1 - g2
    b = b1 - b2
    return (((512 + rmean) * r * r) >> 8) + 4 * g * g + (((767 - rmean) * b * b) >> 8)
    # See the very good color distance paper: https://www.compuphase.com/cmetric.htm


class EmbThread:

    def __init__(self):
        self.color = 0xFF000000
        self.description = None  # type: str
        self.catalogNumber = None  # type: str
        self.details = None  # type: str
        self.brand = None  # type: str
        self.chart = None  # type: str
        self.weight = None  # type: str
        # description, catalogNumber, details, brand, chart, weight

    def setColor(self, red: int, green: int, blue: int):
        self.color = 0xFF000000 | ((r & 255) << 16) | ((g & 255) << 8) | (b & 255)

    def getOpaqueColor(self) -> int:
        return 0xFF000000 | self.color

    def getRed(self) -> int:
        return (self.color >> 16) & 0xFF

    def getGreen(self) -> int:
        return (self.color >> 8) & 0xFF

    def getBlue(self) -> int:
        return self.color & 0xFF

    def findNearestIndex(self, values) -> int:
        findNearestIndex(self.color, values)

    def hexColor(self):
        return "#%02x%02x%02x" % (self.getRed(), self.getGreen(), self.getBlue());
