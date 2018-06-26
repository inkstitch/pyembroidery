import pyembroidery.EmbThreadJef as JefThread
import pyembroidery.ReadHelper as helper


def read(file, read_object):
    with open(file, "rb") as f:
        jef_threads = JefThread.get_thread_set();
        stitch_offset = helper.read_int_32le(f)
        f.seek(20, 1)
        count_colors = helper.read_int_32le(f)
        count_stitches = helper.read_int_32le(f)
        f.seek(84, 1)
        for i in range(0, count_colors):
            index = abs(helper.read_int_32le(f))
            read_object.add_thread(jef_threads[index % 79])

        f.seek(stitch_offset - 116 - (count_colors * 4), 1)
        for i in range(0, count_stitches + 100):
            b = helper.read_signed(f,2)
            if b[0] & 0xFF is 0x80:
                if b[1] & 1 is not 0:
                    b = helper.read_signed(f, 2)
                    read_object.color_change(0, 0)
                    read_object.move(b[0], -b[1])
                elif b[1] is 0x04 or b[1] is 0x02:  # trim
                    b = helper.read_signed(f, 2)
                    read_object.trim(0, 0)
                    read_object.move(b[0], -b[1])
                elif b[1] is 0x10: #end
                    break
            else:
                read_object.stitch(helper.signed(b[0]),
                                   -helper.signed(b[1]))
        read_object.end(0,0)