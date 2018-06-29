# pyembroidery

Python library for the reading and writing of embroidery files.

Any suggestions or comments please raise an issue. It should still be a bit before everything solidifies.

pyembroidery is largely intended for eventual use in lexelby/inkstitch. However, it includes a lot of higher level and middle level pattern composition abilities that might not be eventually used there. It duplicates some of the functionalities already present there in order to be entirely reasonable for *any* python embroidery project. You shouldn't have to rewrite the tie_on code yourself if you're converting some vector guilloches to embroidery or wrote a fun cyclocycloid program and want to sew the output, or for some reason sew circuit boards on fabric with electricity conductive thread. That's not my department.

It should be complex enough to go very easily from points to stitches, fine grained enough to let you control everything, and good enough that you shouldn't want to.

The current mandate for formats is: PES, DST, EXP, JEF, VP3

---

pyembroidery read and write: PES, PEC, DST, EXP, JEF, VP3, with varying degrees of stablity.

pyembroidery supports STITCH, JUMP, TRIM, STOP, END, COLOR_CHANGE and SEQUIN. 
(only dsts have sequin, and they currently only read in.)

---

Current goals:
* Improve the stablity of these particular formats.
* Improve the API interfacing for the library.
* Add a layer-based stablized middle-format, for conversion.

---

Conversion:

* import pyembroidery.PyEmbroidery as pyemb
* pyemb.convert("embroidery.jef", "converted.dst");

This will the embroidery.jef file in JEF format and will export it as converted.dst in DST format.

---

Loading:

You load a pattern from disk:

* pattern = pyemb.load("myembroidery.exp)

---

Saving:

You write to a pattern, then save the pattern out:

* pyemb.save(pattern,"myembroidery.dst")

---

Composing a pattern needs to give fine grain control of the embroidery core commands: stitch, jump, trim, color_change, stop, sequin, end
These are what embroidery machines can actually do as a practical matter.

These are augmented with higher level bulk utility commands to render into coherent embroidery files.

The pattern composing therefore must allow the user to:
* Make overt: stitch, jump, trim, color_change, stop, end, and sequin commands
* Use shorthand commands compose a pattern using: STITCH, BREAK and BREAK_COLOR, then encode that into lower level commands.
* Use bulk dump ability, give pattern a list of points and colors, then encode that into lower level commands.
* Mix these different command levels. So write overt stitches/sequins to the pattern, tell it perform a frame_eject, dump a bulk set of points, and encode that.

----

The middle-level commands, as they currently stand:
* BREAK - Break the stitches. Inserts a trim and jumps to the next stitch in the sequence.
* BREAK_COLOR - Breaks the stitches. Changes to the next color.
* STITCH_FINAL - Stitches the current location, and applies a Break.
* STITCH_FINAL_COLOR - Stitches the current location, and applies a break_color
* FRAME_EJECT(x,y) - breaks the stitches, jumps to the given location, performs a stop, then goes to next stitch accordingly.

Note: these do not need to have a 1 to 1 conversion to stitches. They could be anything, if something is needed and within scope of the project raise an issue.

Using the middle-level commands as they currently stand:
* pattern.add_stitch_absolute(x, y, EmbPattern.STITCH)
* pattern.add_stitch_relative(x, y, EmbPattern.STITCH)

Note, for a break commands, the position doesn't matter nor the absolute/relative nature of coord:
* pattern.add_stitch_absolute(x, y, EmbPattern.BREAK)
* pattern.add_stitch_absolute(x, y, EmbPattern.BREAK_COLOR)

After writing middle level commands to the pattern, call the render()
* pyemb.encode.max_stitch = dstWriter.MAX_STITCH_DISTANCE
* pyemb.encode.max_jump = dstWriter.MAX_JUMP_DISTANCE
* pyemb.encode.tie_on = True
* pyemb.encode.tie_off = True
* pattern = pyemb.render(pattern)

---

This code is based on Embroidermodder/MobileViewer Java code,
Which in turn is based on Embroidermodder/libembroidery C++ code.


