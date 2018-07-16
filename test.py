from __future__ import print_function

import test_fractals
from pyembroidery import *


# Initial test code. pyembroidery
pattern2 = EmbPattern()
pattern2.add_command(COLOR_BREAK)
pattern2.add_stitch_absolute(SEW_TO, -100, -100)
pattern2.add_stitch_absolute(SEW_TO, -100, +100)
pattern2.add_stitch_absolute(SEW_TO, +100, +100)
pattern2.add_command(COLOR_BREAK)
pattern2.add_stitch_absolute(SEW_TO, +100, -100)
pattern2.add_stitch_absolute(SEW_TO, -100, -100)
pattern2.add_command(COLOR_BREAK)
pattern2.add_thread({"color": 0xFF0000})
pattern2.fix_color_count()
write(pattern2, "example.csv", {"explicit_trim": False})

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
settings["truncated"] = True
write(pattern, "generatedv1t.pes", settings)
settings["pes version"] = 6
write(pattern, "generatedv6t.pes", settings)

convert("generated.exp", "genconvert.dst", {"stable": False, "encode": False})

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
    for emb_format in supported_formats():
        if emb_format.get('writer', None) is None:
            continue
        results_file = os.path.join("results", file) + \
                       '.' + emb_format["extension"]
        write(pattern, results_file, {
            "deltas": True,
            "scale": 2
            # "tie_on": True,
            # "tie_off": True,
            # "translate": (500, 500)
            # "scale": 2,
            # "rotate": 45
        })
