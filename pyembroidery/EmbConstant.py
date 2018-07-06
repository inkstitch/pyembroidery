NO_COMMAND = -1
STITCH = 0
JUMP = 1
TRIM = 2
STOP = 3
END = 4
COLOR_CHANGE = 5
SEQUIN = 6

# Different stitch classes.
# If the stitch is long? How do we get there?
SEW_TO = 0xB0
NEEDLE_AT = 0xB1

SEQUENCE_BREAK = 0xE1
COLOR_BREAK = 0xE2
TIE_ON = 0xE4
TIE_OFF = 0xE5
FRAME_EJECT = 0xE9

TRANSLATE = 0xD0
ENABLE_TIE_ON = 0xD1
ENABLE_TIE_OFF = 0xD2
DISABLE_TIE_ON = 0xD3
DISABLE_TIE_OFF = 0xD4
MAX_STITCH_LENGTH = 0xD5
MAX_JUMP_LENGTH = 0xD6
JUMP_THRESHOLD = 0xD8


# Eventually the commands are supposed to be limited to 255 thereby
# allowing additional information like, color change to color in position n
# To be stored in the higher level bits.
COMMAND_MASK = 0xFF
