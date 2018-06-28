from __future__ import print_function
import pyembroidery.DstWriter as dstWriter
import pyembroidery.EmbPattern as EmbPattern
import pyembroidery.EmbThread as EmbThread
import pyembroidery.PyEmbroidery as pyemb
import math

# Initial test code. pyembroidery

# GENERATES A FRACTAL
pattern = EmbPattern.EmbPattern()

# Proper Testing needs threads.
thread0 = EmbThread.EmbThread()
thread0.brand = "Wilcom";
thread0.description = "Blue"
thread0.chart = "Debug";
thread0.catalog_number = "1"
thread0.details = "Details"
thread0.set_color(0x28, 0x16, 0x6f)

# thread0 = EmbThread.EmbThread()
# thread0.brand = "RandomGoogleBrand"
# thread0.description = "Fairy Orange"
# thread0.chart = "Fairy Floss";
# thread0.catalog_number = "0045"
# thread0.details = "Details"
# thread0.set_color(255,218,185)
pattern.add_thread(thread0)

thread1 = EmbThread.EmbThread()
thread1.brand = "Wilcom";
thread1.description = "Cyan"
thread1.chart = "Debug";
thread1.catalog_number = "2"
thread1.details = "Details"
thread1.set_color(0xff, 0, 0)
# thread1.brand = "RandomGoogleBrand"
# thread1.description = "Fairy Green"
# thread1.chart = "Fairy Floss";
# thread1.catalog_number = "0101"
# thread1.details = "Det check"
# thread1.set_color(185,255,218)
pattern.add_thread(thread1)

import test_fractals
test_fractals.generate(pattern)

# counter.print_counts()

pyemb.encode.max_stitch = dstWriter.MAX_STITCH_DISTANCE
pyemb.encode.max_jump = dstWriter.MAX_JUMP_DISTANCE
pyemb.encode.tie_on = True
pyemb.encode.tie_off = True
pattern = pyemb.render(pattern)

pyemb.write(pattern,"generated.pec")
pyemb.write(pattern,"generated.pes")
pyemb.write(pattern,"generated.exp")
pyemb.write(pattern,"generated.dst")
dstWriter.extended_header = True
pyemb.write(pattern,"generated-eh.dst")
pyemb.write(pattern,"generated.jef")
pyemb.write(pattern,"generated.vp3")

pyemb.convert("generated.jef", "conv.dst");

read_dst = pyemb.read("generated.dst")
for stitchblock in read_dst.get_as_stitchblock():
    block = stitchblock[0]
    thread = stitchblock[1]
    print(thread.hex_color());
    print(len(block))

# vp3Reader.read("Panda.VP3", reader3)
# vp3Reader.read("SP0068.VP3", reader3)
# pesWriter.write(reader3.pattern, "vp3convert.pes")
# printer = print_reader.PrintReader()
# jefReader.read("generated.jef",printer)
