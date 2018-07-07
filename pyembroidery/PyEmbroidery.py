import os.path

from .EmbPattern import EmbPattern
import pyembroidery.DstWriter as DstWriter
import pyembroidery.PecWriter as PecWriter
import pyembroidery.PesWriter as PesWriter
import pyembroidery.ExpWriter as ExpWriter
import pyembroidery.Vp3Writer as Vp3Writer
import pyembroidery.JefWriter as JefWriter
import pyembroidery.SvgWriter as SvgWriter
import pyembroidery.DstReader as DstReader
import pyembroidery.PecReader as PecReader
import pyembroidery.PesReader as PesReader
import pyembroidery.ExpReader as ExpReader
import pyembroidery.Vp3Reader as Vp3Reader
import pyembroidery.JefReader as JefReader


def supported_formats():
    """Generates dictionary entries for supported formats. Each entry will
    always have description, extension, mimetype, and category. Reader
    will provide the reader, if one exists, writer will provide the writer,
    if one exists.

    Metadata gives a list of metadata read and/or written by that type.

    Options provides accepted options by the format and their accepted values.
    """
    yield ({
        "description": "Brother Embroidery Format",
        "extension": "pec",
        "mimetype": "application/x-pec",
        "category": "embroidery",
        "reader": PecReader,
        "writer": PecWriter,
        "metadata": ("name")
    })
    yield ({
        "description": "Brother Embroidery Format",
        "extension": "pes",
        "mimetype": "application/x-pes",
        "category": "embroidery",
        "reader": PesReader,
        "writer": PesWriter,
        "options": {
            "pes version": (1, 6),
            "truncated": (True, False)
        },
        "metadata": ("name", "author", "category", "keywords", "comments")
    })
    yield ({
        "description": "Melco Embroidery Format",
        "extension": "exp",
        "mimetype": "application/x-exp",
        "category": "embroidery",
        "reader": ExpReader,
        "writer": ExpWriter,
    })
    yield ({
        "description": "Tajima Embroidery Format",
        "extension": "dst",
        "mimetype": "application/x-dst",
        "category": "embroidery",
        "reader": DstReader,
        "writer": DstWriter,
        "options": {
            "extended headers": (True, False)
        },
        "versions": ("default", "extended headers"),
        "metadata": ("name")
    })
    yield ({
        "description": "Janome Embroidery Format",
        "extension": "jef",
        "mimetype": "application/x-jef",
        "category": "embroidery",
        "reader": JefReader,
        "writer": JefWriter,
    })
    yield ({
        "description": "Pfaff Embroidery Format",
        "extension": "vp3",
        "mimetype": "application/x-vp3",
        "category": "embroidery",
        "reader": Vp3Reader,
        "writer": Vp3Writer,
    })
    yield ({
        "description": "Scalable Vector Graphics",
        "extension": "svg",
        "mimetype": "image/svg+xml",
        "category": "vector",
        "writer": SvgWriter,
    })


def convert(filename_from, filename_to, encode_settings=None):
    pattern = read(filename_from)
    if pattern is None:
        return
    pattern = pattern.get_stable_pattern()
    write(pattern, filename_to, encode_settings)


def get_extension_by_filename(filename):
    """extracts he extension from a filename"""
    return os.path.splitext(filename)[1][1:]


def read_embroidery(reader, f, pattern=None):
    """Reads fileobject or filename with reader."""
    if pattern is None:
        pattern = EmbPattern()
    if isinstance(f, str):
        with open(f, "wb") as stream:
            reader.read(stream, pattern)
    else:
        reader.read(f, pattern)
    return pattern


def read_dst(f, pattern=None):
    """Reads fileobject as DST file"""
    if pattern is None:
        pattern = EmbPattern()
    return read_embroidery(DstReader, f, pattern)


def read_pec(f, pattern=None):
    """Reads fileobject as PEC file"""
    if pattern is None:
        pattern = EmbPattern()
    return read_embroidery(PecReader, f, pattern)


def read_pes(f, pattern=None):
    """Reads fileobject as PES file"""
    if pattern is None:
        pattern = EmbPattern()
    return read_embroidery(PesReader, f, pattern)


def read_exp(f, pattern=None):
    """Reads fileobject as EXP file"""
    if pattern is None:
        pattern = EmbPattern()
    return read_embroidery(ExpReader, f, pattern)


def read_vp3(f, pattern=None):
    """Reads fileobject as VP3 file"""
    if pattern is None:
        pattern = EmbPattern()
    return read_embroidery(Vp3Reader, f, pattern)


def read_jef(f, pattern=None):
    """Reads fileobject as JEF file"""
    if pattern is None:
        pattern = EmbPattern()
    return read_embroidery(JefReader, f, pattern)


def read(filename, pattern=None):
    """Reads file, assuming type by extention"""
    if pattern is None:
        pattern = EmbPattern()
    extension = get_extension_by_filename(filename)
    extension = extension.lower()
    try:
        with open(filename, "rb") as f:
            if extension == "dst":
                return read_dst(f, pattern)
            elif extension == "pec":
                return read_pec(f, pattern)
            elif extension == "pes":
                return read_pes(f, pattern)
            elif extension == "exp":
                return read_exp(f, pattern)
            elif extension == "vp3":
                return read_vp3(f, pattern)
            elif extension == "jef":
                return read_jef(f, pattern)
    except IOError:
        pass


def write_embroidery(writer, pattern, stream, encode_settings=None):
    if encode_settings is None:
        encode_settings = {}
    else:
        encode_settings = encode_settings.copy()
    if not ("max_jump" in encode_settings):
        encode_settings["max_jump"] = writer.MAX_JUMP_DISTANCE
    if not ("max_stitch" in encode_settings):
        encode_settings["max_stitch"] = writer.MAX_STITCH_DISTANCE
    if isinstance(stream, str):
        with open(stream, "wb") as stream:
            normalpattern = pattern.get_normalized_pattern(encode_settings)
            writer.write(normalpattern, stream)
    else:
        normalpattern = pattern.get_normalized_pattern(encode_settings)
        writer.write(normalpattern, stream, encode_settings)


def write_dst(pattern, stream, encode_settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(DstWriter, pattern, stream, encode_settings)


def write_pec(pattern, stream, encode_settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(PecWriter, pattern, stream, encode_settings)


def write_pes(pattern, stream, encode_settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(PesWriter, pattern, stream, encode_settings)


def write_exp(pattern, stream, encode_settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(ExpWriter, pattern, stream, encode_settings)


def write_vp3(pattern, stream, encode_settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(Vp3Writer, pattern, stream, encode_settings)


def write_jef(pattern, stream, encode_settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(JefWriter, pattern, stream, encode_settings)


def write_svg(pattern, stream, encode_settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(SvgWriter, pattern, stream, encode_settings)


def write(pattern, filename, encode_settings=None):
    """Writes file, assuming type by extention"""
    extension = get_extension_by_filename(filename)
    extension = extension.lower()
    with open(filename, "wb") as stream:
        if extension == "dst":
            write_dst(pattern, stream, encode_settings)
        elif extension == "pec":
            write_pec(pattern, stream, encode_settings)
        elif extension == "pes":
            write_pes(pattern, stream, encode_settings)
        elif extension == "exp":
            write_exp(pattern, stream, encode_settings)
        elif extension == "vp3":
            write_vp3(pattern, stream, encode_settings)
        elif extension == "jef":
            write_jef(pattern, stream, encode_settings)
        elif extension == "svg":
            write_svg(pattern, stream, encode_settings)
        else:
            pass
        stream.close()
