import os.path

from .EmbPattern import EmbPattern
import pyembroidery.DstWriter as DstWriter
import pyembroidery.PecWriter as PecWriter
import pyembroidery.PesWriter as PesWriter
import pyembroidery.ExpWriter as ExpWriter
import pyembroidery.Vp3Writer as Vp3Writer
import pyembroidery.JefWriter as JefWriter
import pyembroidery.SvgWriter as SvgWriter
import pyembroidery.CsvWriter as CsvWriter

import pyembroidery.DstReader as DstReader
import pyembroidery.PecReader as PecReader
import pyembroidery.PesReader as PesReader
import pyembroidery.ExpReader as ExpReader
import pyembroidery.Vp3Reader as Vp3Reader
import pyembroidery.JefReader as JefReader

import pyembroidery.XxxReader as XxxReader
import pyembroidery.SewReader as SewReader
import pyembroidery.U01Reader as U01Reader
import pyembroidery.ShvReader as ShvReader
import pyembroidery.A10oReader as A10oReader
import pyembroidery.A100Reader as A100Reader
import pyembroidery.BroReader as BroReader
import pyembroidery.DsbReader as DsbReader
import pyembroidery.DszReader as DszReader
import pyembroidery.EmdReader as EmdReader
import pyembroidery.InbReader as InbReader
import pyembroidery.TbfReader as TbfReader
import pyembroidery.KsmReader as KsmReader
import pyembroidery.TapReader as TapReader
import pyembroidery.StxReader as StxReader
# import pyembroidery.ExyReader as ExyReader
# import pyembroidery.FxyReader as FxyReader
# import pyembroidery.GtReader as GtReader
# import pyembroidery.DatReader as DatReader


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
    yield ({
        "description": "Comma-separated values",
        "extension": "csv",
        "mimetype": "text/csv",
        "category": "debug",
        "writer": CsvWriter,
        "options": {
            "deltas": (True, False)
        },
    })
    yield ({
        "description": "Singer Embroidery Format",
        "extension": "xxx",
        "mimetype": "application/x-xxx",
        "category": "embroidery",
        "reader": XxxReader
    })
    yield ({
        "description": "Janome Embroidery Format",
        "extension": "sew",
        "mimetype": "application/x-sew",
        "category": "embroidery",
        "reader": SewReader
    })
    yield ({
        "description": "Barudan Embroidery Format",
        "extension": "u01",
        "mimetype": "application/x-u01",
        "category": "embroidery",
        "reader": U01Reader
    })
    yield ({
        "description": "Husqvarna Viking Embroidery Format",
        "extension": "shv",
        "mimetype": "application/x-shv",
        "category": "embroidery",
        "reader": ShvReader
    })
    yield ({
        "description": "Toyota Embroidery Format",
        "extension": "10o",
        "mimetype": "application/x-10o",
        "category": "embroidery",
        "reader": A10oReader
    })
    yield ({
        "description": "Toyota Embroidery Format",
        "extension": "100",
        "mimetype": "application/x-100",
        "category": "embroidery",
        "reader": A100Reader
    })
    yield ({
        "description": "Bits & Volts Embroidery Format",
        "extension": "bro",
        "mimetype": "application/x-Bro",
        "category": "embroidery",
        "reader": BroReader
    })
    # yield ({
    #     "description": "Barudan Embroidery Format",
    #     "extension": "dat",
    #     "mimetype": "application/x-dat",
    #     "category": "embroidery",
    #     "stable": False,
    #     "reader": DatReader
    # })
    yield ({
        "description": "Tajima(Barudan) Embroidery Format",
        "extension": "dsb",
        "mimetype": "application/x-dsb",
        "category": "embroidery",
        "reader": DsbReader
    })
    yield ({
        "description": "ZSK USA Embroidery Format",
        "extension": "dsz",
        "mimetype": "application/x-dsz",
        "category": "embroidery",
        "reader": DszReader
    })
    yield ({
        "description": "Elna Embroidery Format",
        "extension": "emd",
        "mimetype": "application/x-emd",
        "category": "embroidery",
        "reader": EmdReader
    })
    # yield ({
    #     "description": "Eltac Embroidery Format",
    #     "extension": "exy", # e??, e01
    #     "mimetype": "application/x-exy",
    #     "category": "embroidery",
    #     "stable": False,
    #     "reader": ExyReader
    # })
    # yield ({
    #     "description": "Fortron Embroidery Format",
    #     "extension": "fxy", # f??, f01
    #     "mimetype": "application/x-fxy",
    #     "category": "embroidery",
    #     "stable": False,
    #     "reader": FxyReader
    # })
    # yield ({
    #     "description": "Gold Thread Embroidery Format",
    #     "extension": "gt",
    #     "mimetype": "application/x-exy",
    #     "category": "embroidery",
    #     "stable": False,
    #     "reader": GtReader
    # })
    yield ({
        "description": "Inbro Embroidery Format",
        "extension": "inb",
        "mimetype": "application/x-inb",
        "category": "embroidery",
        "reader": InbReader
    })
    yield ({
        "description": "Tajima Embroidery Format",
        "extension": "tbf",
        "mimetype": "application/x-tbf",
        "category": "embroidery",
        "reader": TbfReader
    })
    yield ({
        "description": "Pfaff Embroidery Format",
        "extension": "ksm",
        "mimetype": "application/x-ksm",
        "category": "embroidery",
        "reader": KsmReader
    })
    yield ({
        "description": "Happy Embroidery Format",
        "extension": "tap",
        "mimetype": "application/x-tap",
        "category": "embroidery",
        "reader": TapReader
    })
    yield ({
        "description": "Data Stitch Embroidery Format",
        "extension": "stx",
        "mimetype": "application/x-stx",
        "category": "embroidery",
        "reader": StxReader
    })


def convert(filename_from, filename_to, settings=None):
    pattern = read(filename_from, settings)
    if pattern is None:
        return
    if settings is not None:
        stable = settings.get("stable", True)
        if stable:
            pattern = pattern.get_stable_pattern()
    else:
        pattern = pattern.get_stable_pattern()
    write(pattern, filename_to, settings)


def get_extension_by_filename(filename):
    """extracts he extension from a filename"""
    return os.path.splitext(filename)[1][1:]


def read_embroidery(reader, f, settings=None, pattern=None):
    """Reads fileobject or filename with reader."""
    if pattern is None:
        pattern = EmbPattern()
    if isinstance(f, str):
        try:
            with open(f, "rb") as stream:
                reader.read(stream, pattern, settings)
                stream.close()
        except IOError:
            pass
    else:
        reader.read(f, pattern, settings)
    return pattern


def read_dst(f, settings=None, pattern=None):
    """Reads fileobject as DST file"""
    return read_embroidery(DstReader, f, settings, pattern)


def read_pec(f, settings=None, pattern=None):
    """Reads fileobject as PEC file"""
    return read_embroidery(PecReader, f, settings, pattern)


def read_pes(f, settings=None, pattern=None):
    """Reads fileobject as PES file"""
    return read_embroidery(PesReader, f, settings, pattern)


def read_exp(f, settings=None, pattern=None):
    """Reads fileobject as EXP file"""
    return read_embroidery(ExpReader, f, settings, pattern)


def read_vp3(f, settings=None, pattern=None):
    """Reads fileobject as VP3 file"""
    return read_embroidery(Vp3Reader, f, settings, pattern)


def read_jef(f, settings=None, pattern=None):
    """Reads fileobject as JEF file"""
    return read_embroidery(JefReader, f, settings, pattern)


def read(filename, settings=None, pattern=None):
    """Reads file, assuming type by extension"""
    extension = get_extension_by_filename(filename)
    extension = extension.lower()
    for file_type in supported_formats():
        if file_type['extension'] != extension:
            continue
        reader = file_type.get("reader", None)
        return read_embroidery(reader, filename, settings, pattern)
    return None


def write_embroidery(writer, pattern, stream, settings=None):
    if settings is None:
        settings = {}
    else:
        settings = settings.copy()
    if settings.get("encode", True):
        if not ("max_jump" in settings):
            settings["max_jump"] = writer.MAX_JUMP_DISTANCE
        if not ("max_stitch" in settings):
            settings["max_stitch"] = writer.MAX_STITCH_DISTANCE
        if not ("full_jump" in settings):
            settings["full_jump"] = writer.FULL_JUMP
        if not ("strip_sequins" in settings):
            settings["strip_sequins"] = writer.STRIP_SEQUINS
        pattern = pattern.get_normalized_pattern(settings)

    if isinstance(stream, str):
        with open(stream, "wb") as stream:
            writer.write(pattern, stream, settings)
    else:
        writer.write(pattern, stream, settings)


def write_dst(pattern, stream, settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(DstWriter, pattern, stream, settings)


def write_pec(pattern, stream, settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(PecWriter, pattern, stream, settings)


def write_pes(pattern, stream, settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(PesWriter, pattern, stream, settings)


def write_exp(pattern, stream, settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(ExpWriter, pattern, stream, settings)


def write_vp3(pattern, stream, settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(Vp3Writer, pattern, stream, settings)


def write_jef(pattern, stream, settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(JefWriter, pattern, stream, settings)


def write_svg(pattern, stream, settings=None):
    """Writes fileobject as DST file"""
    write_embroidery(SvgWriter, pattern, stream, settings)


def write(pattern, filename, settings=None):
    """Writes file, assuming type by extension"""
    extension = get_extension_by_filename(filename)
    extension = extension.lower()

    for file_type in supported_formats():
        if file_type['extension'] != extension:
            continue
        writer = file_type.get("writer", None)
        if writer is None:
            continue
        write_embroidery(writer, pattern, filename, settings)
