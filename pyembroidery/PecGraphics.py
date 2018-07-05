blank = [
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0xF0, 0xFF, 0xFF, 0xFF, 0xFF, 0x0F,
    0x08, 0x00, 0x00, 0x00, 0x00, 0x10,
    0x04, 0x00, 0x00, 0x00, 0x00, 0x20,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x02, 0x00, 0x00, 0x00, 0x00, 0x40,
    0x04, 0x00, 0x00, 0x00, 0x00, 0x20,
    0x08, 0x00, 0x00, 0x00, 0x00, 0x10,
    0xF0, 0xFF, 0xFF, 0xFF, 0xFF, 0x0F,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00
]


def get_blank():
    return blank.copy();


def create(width, height):
    width = width / 8;
    return [0x00] * width * height


def draw(points, graphics, stride=6):
    for point in points:
        try:
            try:
                set(graphic,
                    int(point.x),
                    int(point.y),
                    stride)
            except AttributeError:
                set(graphic,
                    int(point[0]),
                    int(point[1]),
                    stride)
        except IndexError:
            pass


def draw_scaled(extends, points, graphic, stride, buffer=5):
    if extends == None:
        draw(points, graphic, stride);
        return
    left = 0
    top = 0
    right = 0
    bottom = 0
    try:
        left = extends.left
        top = extends.top
        right = extends.right
        bottom = extends.bottom
    except AttributeError:
        left = extends[0]
        top = extends[1]
        right = extends[2]
        bottom = extends[3]

    diagram_width = right - left
    diagram_height = bottom - top

    graphic_width = stride * 8
    graphic_height = len(graphic) / stride

    scale_x = (graphic_width - buffer) / diagram_width
    scale_y = (graphic_height - buffer) / diagram_height

    scale = min(scale_x, scale_y)

    cx = (right + left) / 2
    cy = (bottom + top) / 2

    translate_x = -cx
    translate_y = -cy

    translate_x *= scale
    translate_y *= scale

    translate_x += graphic_width / 2
    translate_y += graphic_height / 2

    import math
    for point in points:
        try:
            try:
                set(graphic,
                    math.floor((point.x * scale) + translate_x),
                    math.floor((point.y * scale) + translate_y),
                    stride)
            except AttributeError:
                set(graphic,
                    math.floor((point[0] * scale) + translate_x),
                    math.floor((point[1] * scale) + translate_y),
                    stride)
        except IndexError:
            print("pos: " + str(math.floor((point[0] * scale) + translate_x)),
                  " " + str(math.floor((point[1] * scale) + translate_y)))
            pass


def clear(graphic):
    for b in graphic:
        b = 0;


def set(graphic, x, y, stride=6):
    """expressly sets the bit in the give graphic object"""
    graphic[(y * stride) + int(x / 8)] |= 1 << (x % 8)


def unset(graphic, x, y, stride=6):
    """expressly unsets the bit in the give graphic object"""
    graphic[(y * stride) + int(x / 8)] &= ~(1 << (x % 8))


def get_graphic_as_string(graphic, stride=6, one="#", zero=" "):
    """Prints graphic object in text."""
    mylist = [
        one if (byte >> i) & 1 else zero
        for byte in graphic
        for i in range(0,8)
    ]
    bitstride = 8 * stride;
    bitlength = 8 * len(graphic)
    return '\n'.join(
        ''.join(mylist[m:m + bitstride])
        for m in range(0, bitlength, bitstride))