import pyembroidery.EmbPattern as EmbPattern
import pyembroidery.PatternReader as PatternReader
from pyembroidery.EmbConstant import *
import math


def convert(filename_from, filename_to, encode_settings=None):
    pattern = read(filename_from)
    if pattern == None:
        return
    pattern = pattern.get_stable_pattern()
    write(pattern, filename_to, encode_settings)


def write(pattern_from, filename_to, encoder_settings=None):
    encoder.write(filename_to, encoder_settings)


def get_extension_by_filename(filename):
    """extracts he extension from a filename"""
    import os.path
    return os.path.splitext(filename)[1][1:]


def read_embroidery(reader, f, pattern=None):
    """Reads fileobject or filename with reader."""
    if pattern == None:
        pattern = EmbPattern.EmbPattern()
    if isinstance(f, str):
        with open(f, "wb") as stream:
            reader.read(f, pattern);
    else:
        reader.read(f, pattern);
    return pattern


def read_dst(f, pattern=None):
    """Reads fileobject as DST file"""
    if pattern == None:
        pattern = EmbPattern.EmbPattern()
    import pyembroidery.DstReader as reader
    return read_embroidery(reader, f, pattern)


def read_pec(f, pattern=None):
    """Reads fileobject as PEC file"""
    if pattern == None:
        pattern = EmbPattern.EmbPattern()
    import pyembroidery.PecReader as reader
    return read_embroidery(reader, f, pattern)


def read_pes(f, pattern=None):
    """Reads fileobject as PES file"""
    if pattern == None:
        pattern = EmbPattern.EmbPattern()
    import pyembroidery.PesReader as reader
    return read_embroidery(reader, f, pattern)


def read_exp(f, pattern=None):
    """Reads fileobject as EXP file"""
    if pattern == None:
        pattern = EmbPattern.EmbPattern()
    import pyembroidery.ExpReader as reader
    return read_embroidery(reader, f, pattern)


def read_vp3(f, pattern=None):
    """Reads fileobject as VP3 file"""
    if pattern == None:
        pattern = EmbPattern.EmbPattern()
    import pyembroidery.Vp3Reader as reader
    return read_embroidery(reader, f, pattern)


def read_jef(f, pattern=None):
    """Reads fileobject as JEF file"""
    if pattern == None:
        pattern = EmbPattern.EmbPattern()
    import pyembroidery.JefReader as reader
    return read_embroidery(reader, f, pattern)


def read(filename, pattern=None):
    """Reads file, assuming type by extention"""
    if pattern == None:
        pattern = EmbPattern.EmbPattern()
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
    except PermissionError:
        pass


def write_embroidery(writer, pattern, stream, encode_settings=None):
    if encode_settings == None:
        encode_settings = {}
    else:
        encode_settings = encode_settings.copy()
    if not ("max_jump" in encode_settings):
        encode_settings["max_jump"] = writer.MAX_JUMP_DISTANCE
    if not ("max_stitch" in encode_settings):
        encode_settings["max_stitch"] = writer.MAX_STITCH_DISTANCE
    if isinstance(stream, str):
        with open(stream, "wb") as stream:
            normalpattern = pattern.get_normalized_pattern(encode_settings);
            writer.write(normalpattern, stream)
    else:
        normalpattern = pattern.get_normalized_pattern(encode_settings);
        writer.write(normalpattern, stream)


def write_dst(pattern, stream, encode_settings=None):
    """Writes fileobject as DST file"""
    import pyembroidery.DstWriter as writer
    write_embroidery(writer, pattern, stream, encode_settings);


def write_pec(pattern, stream, encode_settings=None):
    """Writes fileobject as DST file"""
    import pyembroidery.PecWriter as writer
    write_embroidery(writer, pattern, stream, encode_settings);


def write_pes(pattern, stream, encode_settings=None):
    """Writes fileobject as DST file"""
    import pyembroidery.PesWriter as writer
    write_embroidery(writer, pattern, stream, encode_settings);


def write_exp(pattern, stream, encode_settings=None):
    """Writes fileobject as DST file"""
    import pyembroidery.ExpWriter as writer
    write_embroidery(writer, pattern, stream, encode_settings);


def write_vp3(pattern, stream, encode_settings=None):
    """Writes fileobject as DST file"""
    import pyembroidery.Vp3Writer as writer
    write_embroidery(writer, pattern, stream, encode_settings);


def write_jef(pattern, stream, encode_settings=None):
    """Writes fileobject as DST file"""
    import pyembroidery.JefWriter as writer
    write_embroidery(writer, pattern, stream, encode_settings);


def write_svg(pattern, stream, encode_settings=None):
    """Writes fileobject as DST file"""
    import pyembroidery.SvgWriter as writer
    write_embroidery(writer, pattern, stream, encode_settings);


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
