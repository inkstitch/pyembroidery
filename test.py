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

# thread0 = EmbThread.EmbThread()
# thread0.brand = "PyEmbroidery"
# thread0.description = "Red"
# thread0.chart = "Test Threads";
# thread0.catalog_number = "0099"
# thread0.details = "TestingRed"
# thread0.set_color(255,0,0)
# pattern.add_thread(thread0)
#
# thread1 = EmbThread.EmbThread()
# thread1.brand = "PyEmbroidery"
# thread1.description = "Blue"
# thread1.chart = "Test Threads";
# thread1.catalog_number = "0066"
# thread1.details = "TestingBlue"
# thread1.set_color(0,255,0)
# pattern.add_thread(thread1)
#
# thread2 = EmbThread.EmbThread()
# thread2.brand = "PyEmbroidery"
# thread2.description = "Green"
# thread2.chart = "Test Threads";
# thread2.catalog_number = "0033"
# thread2.details = "TestingGreen"
# thread2.set_color(0,0,255)
# pattern.add_thread(thread2)
#
# thread0 = EmbThread.EmbThread()
# thread0.brand = "Janome"
# thread0.description = "Red"
# thread0.chart = "Test Threads";
# thread0.catalog_number = "225"
# thread0.details = "TestingRed"
# thread0.set_color(255,0,0)
# pattern.add_thread(thread0)
#
# thread2 = EmbThread.EmbThread()
# thread2.brand = "Janome"
# thread2.description = "Meadow Green"
# thread2.chart = "Test Threads";
# thread2.catalog_number = "247"
# thread2.details = "TestingGreen"
# thread2.set_color(0,0,255)
# pattern.add_thread(thread2)
#
# thread1 = EmbThread.EmbThread()
# thread1.brand = "Janome"
# thread1.description = "Blue"
# thread1.chart = "Test Threads";
# thread1.catalog_number = "207"
# thread1.details = "TestingBlue"
# thread1.set_color(0,255,0)
# pattern.add_thread(thread1)
#
# thread1 = EmbThread.EmbThread()
# thread1.brand = "Janome"
# thread1.description = "Peacock Green"
# thread1.chart = "Test Threads";
# thread1.catalog_number = "251"
# thread1.details = "TestingBlue"
# thread1.set_color(0,255,0)
# pattern.add_thread(thread1)
#
#
# import test_fractals
# test_fractals.generate(pattern)
#
# # counter.print_counts()
#
# pyemb.encode.max_stitch = dstWriter.MAX_STITCH_DISTANCE
# pyemb.encode.max_jump = dstWriter.MAX_JUMP_DISTANCE
# pyemb.encode.tie_on = True
# pyemb.encode.tie_off = True
# pattern = pyemb.render(pattern)
#
# pyemb.write(pattern,"generated.pec")
# pyemb.write(pattern,"generated.pes")
# pyemb.write(pattern,"generated.exp")
# pyemb.write(pattern,"generated.dst")
# dstWriter.extended_header = True
# pyemb.write(pattern,"generated-eh.dst")
# pyemb.write(pattern,"generated.jef")
# pyemb.write(pattern,"generated.vp3")
#
#
# pyemb.write_svg(pyemb.read("generated.pec"), "zpec.svg")
# pyemb.write_svg(pyemb.read("generated.pes"), "zpes.svg")
# pyemb.write_svg(pyemb.read("generated.exp"), "zexp.svg")
# pyemb.write_svg(pyemb.read("generated.dst"), "zdst.svg")
# pyemb.write_svg(pyemb.read("generated-eh.dst"), "zdst-eh.svg")
# pyemb.write_svg(pyemb.read("generated.jef"), "zjef.svg")
# pyemb.write_svg(pyemb.read("generated.vp3"), "zvp3.svg")

import os
for file in os.listdir("convert"):
    convert_file = os.path.join("convert", file)
    results_file = os.path.join("results", file) + ".vp3";
    pyemb.convert(convert_file, results_file)