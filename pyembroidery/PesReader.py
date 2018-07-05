from PecReader import read_pec
from EmbThread import EmbThread
from ReadHelper import read_string_8, read_int_8, read_int_32le, read_int_24be, read_int_16le


def read(f, read_object):
    threadlist = []
    pes_string = read_string_8(f, 8)

    if pes_string == "#PEC0001":
        read_pec(f, read_object, threadlist)
        return

    pec_block_position = read_int_32le(f)

    # Ignoring several known PES versions, just abort and read PEC block
    # All versions allow, abort and read PEC block.
    # Metadata started appearing in V4
    # Threads appeared in V5.
    # We quickly abort if there's any complex items in the header.
    # "#PES0100", "#PES0090" "#PES0080" "#PES0070", "#PES0040",
    # "#PES0030", "#PES0022", "#PES0020"
    if pes_string == "#PES0060":
        read_pes_header_version_6(f, read_object, threadlist)
    elif pes_string == "#PES0050":
        read_pes_header_version_5(f, read_object, threadlist)
    elif pes_string == "#PES0055":
        read_pes_header_version_5(f, read_object, threadlist)
    elif pes_string == "#PES0056":
        read_pes_header_version_5(f, read_object, threadlist)
    elif pes_string == "#PES0040":
        read_pes_header_version_4(f, read_object)
    elif pes_string == "#PES0001":
        read_pes_header_version_1(f, read_object)
    else:
        pass  # Header is unrecognised.
    f.seek(pec_block_position, 0)
    read_pec(f, read_object, threadlist)


def read_pes_string(f):
    length = read_int_8(f)
    if length == 0:
        return None
    return read_string_8(f, length)


def read_pes_metadata(f, read_object):
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        read_object.metadata("name", v)
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        read_object.metadata("category", v)
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        read_object.metadata("author", v)
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        read_object.metadata("keywords", v)
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        read_object.metadata("comments", rv)


def read_pes_thread(f, threadlist):
    thread = EmbThread()
    thread.catalog_number = read_pes_string(f)
    thread.color = 0xFF000000 | read_int_24be(f)
    f.seek(5, 1)
    thread.description = read_pes_string(f)
    thread.brand = read_pes_string(f)
    thread.chart = read_pes_string(f)
    threadlist.append(thread)


def read_pes_header_version_1(f, read_object):
    # Nothing I care about.
    pass


def read_pes_header_version_4(f, read_object):
    f.seek(4, 1)
    read_pes_metadata(f, read_object)


def read_pes_header_version_5(f, read_object, threadlist):
    f.seek(4, 1)
    read_pes_metadata(f, read_object)
    f.seek(24, 1)  # this is 36 in version 6 and 24 in version 5
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        read_object.metadata("image", v)
    f.seek(24, 1)
    count_programmable_fills = read_int_16le(f)
    if count_programmable_fills != 0:
        return
    count_motifs = read_int_16le(f)
    if count_motifs != 0:
        return
    count_feather_patterns = read_int_16le(f)
    if count_feather_patterns != 0:
        return
    count_threads = read_int_16le(f)
    for i in range(0, count_threads):
        read_pes_thread(f, threadlist)


def read_pes_header_version_6(f, read_object, threadlist):
    f.seek(4, 1)
    read_pes_metadata(f, read_object)
    f.seek(36, 1)  # this is 36 in version 6 and 24 in version 5
    v = read_pes_string(f)
    if v is not None and len(v) > 0:
        read_object.metadata("image_file", v)
    f.seek(24, 1)
    count_programmable_fills = read_int_16le(f)
    if count_programmable_fills != 0:
        return
    count_motifs = read_int_16le(f)
    if count_motifs != 0:
        return
    count_feather_patterns = read_int_16le(f)
    if count_feather_patterns != 0:
        return
    count_threads = read_int_16le(f)
    for i in range(0, count_threads):
        read_pes_thread(f, threadlist)
