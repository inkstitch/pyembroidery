from __future__ import print_function
import os

import test_fractals
from pyembroidery import *

#
# from pyembroidery.EmbPattern import EmbPattern
# import pyembroidery.PyEmbroidery as pyemb
# from pyembroidery.EmbConstant import *
# import pyembroidery.PecGraphics as pg


# Initial test code. pyembroidery

# Do not emulate the following pattern
pattern2 = EmbPattern()
pattern2.add_stitch_absolute(STITCH, 0, 0)
pattern2.add_command(TRANSLATE, 500, 0)
pattern2.add_stitch_absolute(STITCH, 0, 0)
pattern2.add_command(TRANSLATE, 0, 500)
pattern2.add_stitch_absolute(STITCH, 0, 0)
pattern2.add_command(TRANSLATE, -500, 0)
pattern2.add_stitch_absolute(STITCH, 0, 0)
pattern2.add_command(TRANSLATE, 0, -500)
pattern2.add_stitch_absolute(STITCH, 0, 0)
pattern2.add_command(COLOR_BREAK)
pattern2.add_command(JUMP_THRESHOLD, 1000)
pattern2.add_stitch_absolute(STITCH, 1000, 1000)
pattern2.add_stitch_absolute(STITCH, 1000, 1200)
pattern2.add_stitch_absolute(STITCH, 1200, 1200)
pattern2.add_stitch_absolute(STITCH, 1200, 1000)
pattern2.add_stitch_absolute(STITCH, 1000, 1000)
write_dst(pattern2, "test.dst", {"tie_on": True})

pattern = EmbPattern()

pattern.add_thread({
    "rgb": 0x0000FF,
    "name": "Blue Test",
    "catalog": "0033",
    "brand": "PyEmbroidery Brand Thread"
})

pattern.add_thread({
    "rgb": 0x00FF00,
    "name": "Green",
    "catalog": "0034",
    "brand": "PyEmbroidery Brand Thread"
})

test_fractals.generate(pattern)

settings = {
    "tie_on": True,
    "tie_off": True
}

write(pattern, "generated.pec", settings)
write(pattern, "generated.pes", settings)
write(pattern, "generated.exp", settings)
write(pattern, "generated.dst", settings)
settings["extended header"] = True
write(pattern, "generated-eh.dst", settings)
write(pattern, "generated.jef", settings)
write(pattern, "generated.vp3", settings)
settings["pes version"] = 1
write(pattern, "generatedv1.pes", settings)
settings["pes version"] = 0x101
write(pattern, "generatedv1t.pes", settings)
settings["pes version"] = 0x106
write(pattern, "generatedv6t.pes", settings)

for file in os.listdir("convert"):
    convert_file = os.path.join("convert", file)
    pattern = read(convert_file)
    if pattern is None:
        continue

    i = 0
    while pattern.get_metadata(i) is not None:
        print(get_graphic_as_string(pattern.get_metadata(i)))
        i += 1

    pattern = pattern.get_stable_pattern()
    for suffix in [".svg", ".pec", ".pes", ".exp", ".dst", ".jef", ".vp3"]:
        results_file = os.path.join("results", file) + suffix
        write(pattern, results_file, {
            "tie_on": True,
            "tie_off": True,
            # "translate_x": 500,
            # "translate_y": 500
        })
