from __future__ import print_function

import pyembroidery.DstWriter as dstWriter
import pyembroidery.EmbPattern as EmbPattern
import pyembroidery.EmbThread as EmbThread
import pyembroidery.PyEmbroidery as pyemb
import math

# Initial test code. pyembroidery

pattern = EmbPattern.EmbPattern()

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

import test_fractals

test_fractals.generate(pattern)

settings = {
    "tie_on": True,
    "tie_off": True
}

pyemb.write(pattern, "generated.pec", settings)
pyemb.write(pattern, "generated.pes", settings)
pyemb.write(pattern, "generated.exp", settings)
pyemb.write(pattern, "generated.dst", settings)
settings["extended header"] = True
pyemb.write(pattern, "generated-eh.dst", settings)
pyemb.write(pattern, "generated.jef", settings)
pyemb.write(pattern, "generated.vp3", settings)
settings["pes version"] = 1
pyemb.write(pattern, "generatedv1.pes", settings)

# Do not emulate the following pattern
pattern2 = EmbPattern.EmbPattern();
pattern2.command(EmbPattern.STITCH)
pattern2.add_stitch_relative(EmbPattern.TRANSLATE, 500, 0)
pattern2.command(EmbPattern.STITCH)
pattern2.add_stitch_relative(EmbPattern.TRANSLATE, 0, 500)
pattern2.command(EmbPattern.STITCH)
pattern2.add_stitch_relative(EmbPattern.TRANSLATE, -500, 0)
pattern2.command(EmbPattern.STITCH)
pattern2.add_stitch_relative(EmbPattern.TRANSLATE, 0, -500)
pattern2.command(EmbPattern.STITCH)

pyemb.write_dst(pattern2, "test.dst")

import pyembroidery.PecGraphics as pg

import os
for file in os.listdir("convert"):
    convert_file = os.path.join("convert", file)
    pattern = pyemb.read(convert_file)
    if pattern == None:
        continue

    i = 0
    while pattern.get_metadata(i) != None:
        print(pg.get_graphic_as_string(pattern.get_metadata(i)))
        i += 1;

    pattern = pattern.get_stable_pattern()
    for suffix in [".svg", ".pec", ".pes", ".exp", ".dst", ".jef", ".vp3"]:
        results_file = os.path.join("results", file) + suffix;
        pyemb.write(pattern, results_file, {
            "tie_on": True,
            "tie_off": True,
            # "translate_x": 500,
            # "translate_y": 500
        })

#
# read_pes = pyemb.read("results/Panda Freebie.pes.pes")
# i = 0
# while read_pes.get_metadata(i) != None:
#     pg.print_graphic(read_pes.get_metadata(i))
#     print("")
#     print("")
#     i += 1;
