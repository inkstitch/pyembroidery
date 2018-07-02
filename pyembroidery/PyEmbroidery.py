import pyembroidery.EmbPattern as EmbPattern
import pyembroidery.PatternReader as PatternReader
import pyembroidery.WriteEncoder as encode

encode = encode.WriteEncoder()


def render(pattern):
    return encode.process(pattern)


def get_extension_by_filename(filename):
    import os.path
    return os.path.splitext(filename)[1][1:]


def read(filename):
    reader = PatternReader.PatternReader();
    extension = get_extension_by_filename(filename)
    extension = extension.lower()
    try:
        with open(filename, "rb") as f:
            if extension == "dst":
                import pyembroidery.DstReader
                pyembroidery.DstReader.read(f, reader)
            elif extension == "pec":
                import pyembroidery.PecReader
                pyembroidery.PecReader.read(f, reader)
            elif extension == "pes":
                import pyembroidery.PesReader
                pyembroidery.PesReader.read(f, reader)
            elif extension == "exp":
                import pyembroidery.ExpReader
                pyembroidery.ExpReader.read(f, reader)
            elif extension == "vp3":
                import pyembroidery.Vp3Reader
                pyembroidery.Vp3Reader.read(f, reader)
            elif extension == "jef":
                import pyembroidery.JefReader
                pyembroidery.JefReader.read(f, reader)
            f.close()
            return reader.pattern
    except PermissionError:
        pass


def write(pattern, file):
    extension = get_extension_by_filename(file)
    extension = extension.lower()
    with open(file, "wb") as file:
        if extension == "dst":
            import pyembroidery.DstWriter
            pyembroidery.DstWriter.write(pattern, file)
        elif extension == "pec":
            import pyembroidery.PecWriter
            pyembroidery.PecWriter.write(pattern, file)
        elif extension == "pes":
            import pyembroidery.PesWriter
            pyembroidery.PesWriter.write(pattern, file)
        elif extension == "exp":
            import pyembroidery.ExpWriter
            pyembroidery.ExpWriter.write(pattern, file)
        elif extension == "vp3":
            import pyembroidery.Vp3Writer
            pyembroidery.Vp3Writer.write(pattern, file)
        elif extension == "jef":
            import pyembroidery.JefWriter
            pyembroidery.JefWriter.write(pattern, file)
        elif extension == "svg":
            write_svg(pattern, file)
        else:
            pass
        file.close()


def convert(filename_from, filename_to):
    pattern = read(filename_from);
    if pattern == None:
        return
    stablepattern = EmbPattern.EmbPattern();
    for stitchblock in pattern.get_as_stitchblock():
        block = stitchblock[0]
        thread = stitchblock[1]
        stablepattern.add_thread(thread)
        for thread in block:
            stablepattern.add_stitch_absolute(thread[0], thread[1], EmbPattern.STITCH)
        stablepattern.add_stitch_relative(0, 0, EmbPattern.BREAK_COLOR)
    stablepattern = encode.process(stablepattern);
    write(stablepattern, filename_to)


def write_svg(pattern, filename):
    """Writes an svg file of the stitchblocks."""

    NAME_SVG = "svg"
    ATTR_VERSION = "version"
    VALUE_SVG_VERSION = "1.1"
    ATTR_XMLNS = "xmlns"
    VALUE_XMLNS = "http://www.w3.org/2000/svg"
    ATTR_XMLNS_LINK = "xmlns:xlink"
    VALUE_XLINK = "http://www.w3.org/1999/xlink"
    ATTR_XMLNS_EV = "xmlns:ev"
    VALUE_XMLNS_EV = "http://www.w3.org/2001/xml-events"
    ATTR_WIDTH = "width"
    ATTR_HEIGHT = "height"
    ATTR_VIEWBOX = "viewBox"
    NAME_PATH = "path"
    ATTR_DATA = "d"
    ATTR_FILL = "fill"
    ATTR_STROKE = "stroke"
    ATTR_STROKE_WIDTH = "stroke-width"
    VALUE_NONE = "none"

    import xml.etree.cElementTree as et
    root = et.Element(NAME_SVG)
    root.set(ATTR_VERSION, VALUE_SVG_VERSION)
    root.set(ATTR_XMLNS, VALUE_XMLNS)
    root.set(ATTR_XMLNS_LINK, VALUE_XLINK)
    root.set(ATTR_XMLNS_EV, VALUE_XMLNS_EV)
    extends = pattern.extends();
    width = extends[2] - extends[0]
    height = extends[3] - extends[1]
    root.set(ATTR_WIDTH, str(width))
    root.set(ATTR_HEIGHT, str(height))
    viewbox = str(extends[0]) + " " + str(extends[1]) + \
              " " + str(width) + " " + str(height)
    root.set(ATTR_VIEWBOX, viewbox);

    for stitchblock in pattern.get_as_stitchblock():
        block = stitchblock[0]
        thread = stitchblock[1]
        path = et.SubElement(root, NAME_PATH)
        data = "M"
        for stitch in block:
            x = stitch[0]
            y = stitch[1]
            data += " " + str(x) + "," + str(y)
        path.set(ATTR_DATA, data)
        path.set(ATTR_FILL, VALUE_NONE)
        path.set(ATTR_STROKE, thread.hex_color())
        path.set(ATTR_STROKE_WIDTH, "3")
    tree = et.ElementTree(root)
    tree.write(filename)
