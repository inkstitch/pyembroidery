from .EmbConstant import *
from .WriteHelper import write_string_utf8
from .PecGraphics import get_graphic_as_string

STRIP_SEQUINS = False
FULL_JUMP = False
MAX_JUMP_DISTANCE = 121
MAX_STITCH_DISTANCE = 121


def csv(f, values):
    string = ""
    for v in values:
        if len(string) > 0:
            string += ','
        string += ('\"%s\"' % v)
    write_string_utf8(f, string + "\n")


def write(pattern, f, settings=None):
    deltas = settings is not None and "deltas" in settings

    extends = pattern.extends()
    width = extends[2] - extends[0]
    height = extends[3] - extends[1]

    csv(f, ('#', '[VAR_NAME]', '[VAR_VALUE]'))
    count_stitches = pattern.count_stitches()
    csv(f, ('>', 'STITCH_COUNT:', str(count_stitches)))
    count_threads = pattern.count_color_changes()
    csv(f, ('>', 'THREAD_COUNT:', str(count_threads)))
    csv(f, ('>', 'EXTENTS_LEFT:', str(extends[0])))
    csv(f, ('>', 'EXTENTS_TOP:', str(extends[1])))
    csv(f, ('>', 'EXTENTS_RIGHT:', str(extends[2])))
    csv(f, ('>', 'EXTENTS_BOTTOM:', str(extends[3])))
    csv(f, ('>', 'EXTENTS_WIDTH:', str(width)))
    csv(f, ('>', 'EXTENTS_HEIGHT:', str(height)))
    write_string_utf8(f, "\n")

    if len(pattern.extras) > 0:
        csv(f, (
            '#',
            '[METADATA_NAME]',
            '[METADATA]'
        ))
        for the_key, the_value in pattern.extras.items():
            if isinstance(the_value, tuple):
                the_value = "\n" + get_graphic_as_string(the_value)
            csv(f, (
                '@',
                str(the_key),
                str(the_value)
            ))
        write_string_utf8(f, "\n")

    if len(pattern.threadlist) > 0:
        csv(f, (
            '#',
            '[THREAD_NUMBER]',
            '[HEX_COLOR]',
            '[DESCRIPTION]',
            '[BRAND]',
            '[CATALOG_NUMBER]',
            '[DETAILS]',
            '[WEIGHT]'
        ))
        for i, thread in enumerate(pattern.threadlist):
            csv(f, (
                '$',
                str(i),
                thread.hex_color(),
                thread.description,
                thread.brand,
                thread.catalog_number,
                thread.details,
                thread.weight,
            ))
        write_string_utf8(f, "\n")

    if len(pattern.stitches) > 0:
        if deltas:
            csv(f, (
                '#',
                '[STITCH_INDEX]',
                '[STITCH_TYPE]',
                '[X]',
                '[Y]',
                '[DX]',
                '[DY]'
            ))
        else:
            csv(f, (
                '#',
                '[STITCH_INDEX]',
                '[STITCH_TYPE]',
                '[X]',
                '[Y]'
            ))
        names = get_common_name_dictionary()
        current_x = 0
        current_y = 0
        for i, stitch in enumerate(pattern.stitches):
            try:
                name = names[stitch[2]]
            except IndexError:
                name = "UNKNOWN " + str(stitch[2])
            if deltas:
                csv(f, (
                    '*',
                    str(i),
                    name,
                    str(stitch[0]),
                    str(stitch[1]),
                    str(stitch[0] - current_x),
                    str(stitch[1] - current_y)
                ))
            else:
                csv(f, (
                    '*',
                    str(i),
                    name,
                    str(stitch[0]),
                    str(stitch[1]),
                ))
            current_x = stitch[0]
            current_y = stitch[1]


def get_common_name_dictionary():
    return {
        NO_COMMAND: "NO_COMMAND",
        STITCH: "STITCH",
        JUMP: "JUMP",
        TRIM: "TRIM",
        STOP: "STOP",
        END: "END",
        COLOR_CHANGE: "COLOR_CHANGE",
        SEQUIN_MODE: "SEQUIN_MODE",
        SEQUIN_EJECT: "SEQUIN_EJECT",
        SEW_TO: "SEW_TO",
        NEEDLE_AT: "NEEDLE_AT",
        SEQUENCE_BREAK: "SEQUENCE_BREAK",
        COLOR_BREAK: "COLOR_BREAK",
        TIE_ON: "TIE_ON",
        TIE_OFF: "TIE_OFF",
        FRAME_EJECT: "FRAME_EJECT",
        MATRIX_TRANSLATE: "MATRIX_TRANSLATE",
        MATRIX_SCALE: "MATRIX_SCALE",
        MATRIX_ROTATE: "MATRIX_ROTATE",
        MATRIX_RESET: "MATRIX_RESET",
        OPTION_ENABLE_TIE_ON: "OPTION_ENABLE_TIE_ON",
        OPTION_ENABLE_TIE_OFF: "OPTION_ENABLE_TIE_OFF",
        OPTION_DISABLE_TIE_ON: "OPTION_DISABLE_TIE_ON",
        OPTION_DISABLE_TIE_OFF: "OPTION_DISABLE_TIE_OFF",
        OPTION_MAX_STITCH_LENGTH: "OPTION_MAX_STITCH_LENGTH",
        OPTION_MAX_JUMP_LENGTH: "OPTION_MAX_JUMP_LENGTH",
        CONTINGENCY_NONE: "CONTINGENCY_NONE",
        CONTINGENCY_JUMP_NEEDLE: "CONTINGENCY_JUMP_NEEDLE",
        CONTINGENCY_SEW_TO: "CONTINGENCY_SEW_TO",
    }
