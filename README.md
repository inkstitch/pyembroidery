# pyembroidery
Python library for the reading and writing of embroidery files.

It can currently read and write: PES, PEC, DST, EXP, JEF, VP3, with varying degrees of stablity.

Current goals:
* Improve the stablity of these particular formats.
* Improve the API interfacing for the library.
* Add a layer-based stablized middle-format
* Add simple interface for direct file format conversion.

This code is an advancement of converted Embroidermodder/MobileViewer Java code,
Which in turn is a conversion of Embroidermodder/libembroidery C++ code.

pyembroidery's largely intended for eventual use in lexelby/inkstitch but shall be 
entirely reasonable for any python embroidery project.

--

Currently I've centralized much of the data in a PyEmbroidery script.
import pyembroidery.PyEmbroidery as pyemb

pyemb.convert("generated.jef", "conv.dst");

Will read the generated.jef file in JEF format and will export it as conv.dst in DST format.

You write to a pattern, then save the pattern out. 
pyemb.save("myembroidery.dst")

Rather than write the higher level objects you can render the objects from stitches, using some set higher level commands:
These are currently:

* BREAK - Break the stitches. Inserts a trim and jumps to the next stitch in the sequence.
* BREAK_COLOR - Breaks the stitches. Changes to the next color.
* STITCH_FINAL - Stitches the current location, and applies a Break.
* STITCH_FINAL_COLOR - Stitches the current location, and applies a break_color
* FRAME_EJECT(x,y) - breaks the stitches, jumps to the given location, performs a stop, then goes to next stitch accordingly.

These notabily have some overlap and might not be optimal but they are generally helpful.

There's also clearly a need for pattern.add_stitchblock(stitches)
where rather than commands you simply give it a coordinate set, and it'll do the jumping, cutting, trimming, and colorchanges for you.

For now, 
* pattern.add_stitch_absolute(x, y, EmbPattern.STITCH)
* pattern.add_stitch_relative(x, y, EmbPattern.STITCH)
* pattern.add_stitch_absolute(x, y, EmbPattern.BREAK) -- Note, the position doesn't matter for a break command.
* pattern.add_stitch_absolute(x, y, EmbPattern.BREAK_COLOR)

After writing in the higher level stuff to the pattern, call the render()
* pyemb.encode.max_stitch = dstWriter.MAX_STITCH_DISTANCE
* pyemb.encode.max_jump = dstWriter.MAX_JUMP_DISTANCE
* pyemb.encode.tie_on = True
* pyemb.encode.tie_off = True
* pattern = pyemb.render(pattern)

