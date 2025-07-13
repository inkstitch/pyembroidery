name = "pystitch"

# items available at the top level (e.g. pystitch.read)
from .EmbConstant import *
from .EmbFunctions import *
from .EmbMatrix import EmbMatrix
from .EmbPattern import EmbPattern
from .EmbThread import EmbThread
from .EmbCompress import compress, expand
import pystitch.GenericWriter as GenericWriter

# items available in a sub-heirarchy (e.g. pystitch.PecGraphics.get_graphic_as_string)
from .PecGraphics import get_graphic_as_string
from .pystitch import *
