import pyembroidery.EmbThread as EmbThread
import pyembroidery.ReadHelper as helper


def read_vp3_string_16(stream):
    # Reads the header strings which are 16le numbers of size followed by utf-16 text
    string_length = helper.read_int_16le(stream)
    return helper.read_string_16(stream, string_length)


def read_vp3_string_8(stream):
    # Reads the body strings which are 16be numbers followed by utf-8 text
    string_length = helper.read_int_16be(stream)
    return helper.read_string_8(stream, string_length)


def read_vp3_hoop(stream):
    # I don't care about the hoop.
    stream.seek(0x41, 1)


def read(f, read_object):
    b = f.read(5)
    # magic code: %vsm%
    f.seek(2, 1)
    software_vender = read_vp3_string_16(f)
    f.seek(8, 1)
    file_comment = read_vp3_string_16(f)
    read_vp3_hoop(f)
    another_comment = read_vp3_string_16(f)
    f.seek(18, 1)  # some other stuff.

    f.seek(7, 1)

    another_vender_string = read_vp3_string_16(f)

    count_colors = helper.read_int_16be(f)
    f.seek(1, 1)
    for i in range(0, count_colors):
        thread = EmbThread.EmbThread()
        f.seek(6, 1)
        start_x = helper.read_int_32be(f)
        if start_x is None:
            break;
        start_y = helper.read_int_32be(f)
        read_object.move_abs(start_x / 100, -start_y / 100);
        table_size = helper.read_int_8(f);
        f.seek(1, 1)
        thread.color = helper.read_int_24be(f)
        f.seek((6 * table_size) - 1, 1)
        thread.catalog_number = read_vp3_string_8(f)
        thread.description = read_vp3_string_8(f)
        thread.brand = read_vp3_string_8(f)
        if i != 0:
            read_object.color_change();
        f.seek(6, 1)
        unknown_thread_data = read_vp3_string_8(f);
        f.seek(1, 1)
        unknown_thread_data2 = read_vp3_string_8(f)
        f.seek(2, 1)  # \xff\xff
        read_object.add_thread(thread)
        bytes_in_color = helper.read_int_32le(f)
        f.seek(3, 1);
        color_bytes = helper.read_signed(f, bytes_in_color)
        i = 0
        while i < len(color_bytes):
            x = color_bytes[i]
            y = color_bytes[i + 1]
            i += 2;
            if x == 0x80 or x == -127:
                if y == 0x01:
                    x = (color_bytes[i] << 24) & color_bytes[i + 1] << 16
                    x >>= 16
                    i += 2
                    y = (color_bytes[i] << 24) & color_bytes[i + 1] << 16
                    y >>= 16
                    i += 2
                    i += 2
                    read_object.trim(x, y);
            else:
                read_object.stitch(x, y)
