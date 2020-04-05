from .WriteHelper import write_string_utf8


def write(pattern, f, settings=None):
    extents = pattern.extents()
    width = extents[2] - extents[0]
    height = extents[3] - extents[1]
    count_stitches = pattern.count_stitches()
    count_threads = pattern.count_color_changes() + 1
    thread_used = []

    write_string_utf8(f, "Design Details" + "\n")
    write_string_utf8(f, "==============" + "\n\n")

    write_string_utf8(f, "Size (mm): " + str("%.2f" % width) + " x " + str("%.2f" % height) + "\n")
    write_string_utf8(f, "Stitches: " + str(count_stitches) + "\n\n")

    write_string_utf8(f, "Thread Order" + "\n")
    write_string_utf8(f, "============" + "\n\n")

    for i, thread in enumerate(pattern.threadlist):
        write_string_utf8(f, str(i + 1) + " ")
        string = str(thread.description) + " "
        string += str(thread.brand) + " "
        string += str(thread.catalog_number) 
        string += " (" + str(thread.hex_color()) + ")"
        write_string_utf8(f, string + "\n")
        thread_used.append(string)

    write_string_utf8(f, "\n\n")
    write_string_utf8(f, "Thread List" + "\n")
    write_string_utf8(f, "===========" + "\n\n")

    for thread in set(thread_used):
        write_string_utf8(f, thread + "\n")
