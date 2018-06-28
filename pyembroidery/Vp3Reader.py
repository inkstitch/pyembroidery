import pyembroidery.EmbThread as EmbThread
import pyembroidery.ReadHelper as helper


def read_vp3_string_16(stream):
    # Reads the header strings which are 16le numbers of size followed by utf-16 text
    string_length = helper.read_int_16be(stream)
    return helper.read_string_16(stream, string_length)


def read_vp3_string_8(stream):
    # Reads the body strings which are 16be numbers followed by utf-8 text
    string_length = helper.read_int_16be(stream)
    return helper.read_string_8(stream, string_length)

def skip_vp3_string(stream):
    string_length = helper.read_int_16be(stream);
    stream.seek(string_length,1);


def read(f, read_object):
    b = f.read(5)
    # magic code: %vsm%
    f.seek(1, 1) # \x00
    skip_vp3_string(f)
    f.seek(7, 1) # 0,2,0 pos data (4 bytes)
    skip_vp3_string(f)
    f.seek(63, 1) # 4 extends, stitch count, 1, threads, 3, 3, 4
    skip_vp3_string(f)
    f.seek(28, 1)
    skip_vp3_string(f)

    count_colors = helper.read_int_16be(f)
    for i in range(0, count_colors):
        thread = EmbThread.EmbThread()
        f.seek(3, 1) # \x00\x05\x00
        block_end_position = helper.read_int_32be(f) + f.tell();

        start_x = helper.read_int_32be(f)
        if start_x is None:
            break;
        start_y = helper.read_int_32be(f)
        read_object.move_abs(start_x / 100, start_y / -100);

        table_size = helper.read_int_8(f);
        f.seek(1, 1)

        thread.color = helper.read_int_24be(f)
        f.seek((6 * table_size) - 1, 1)
        thread.catalog_number = read_vp3_string_8(f)
        thread.description = read_vp3_string_8(f)
        thread.brand = read_vp3_string_8(f)
        if i != 0:
            read_object.color_change(0,0);
        read_object.add_thread(thread)

        f.seek(11, 1)
        # next_block_seek_distance = helper.read_int_32be(f)
        f.seek(4, 1)
        f.seek(3, 1); # 0A F6 00
        stitch_byte_length = block_end_position - f.tell();
        stitch_bytes = helper.read_signed(f, stitch_byte_length)
        i = 0
        while i < len(stitch_bytes)-1:
            x = stitch_bytes[i]
            y = stitch_bytes[i + 1]
            i += 2;
            if x == 0x80 or x == -127:
                if y == 0x01:
                    x = (stitch_bytes[i] << 24) & stitch_bytes[i + 1] << 16
                    x >>= 16
                    i += 2
                    y = (stitch_bytes[i] << 24) & stitch_bytes[i + 1] << 16
                    y >>= 16
                    i += 2
                    i += 2
                    read_object.trim(x, y)
                if y == 0x02:
                    pass # ends long stitch mode.
            else:
                read_object.stitch(x, y)
