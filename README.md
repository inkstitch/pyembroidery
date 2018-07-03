# pyembroidery

Python library for the reading and writing of embroidery files.

Any suggestions or comments please raise an issue.

pyembroidery is largely intended for eventual use in lexelby/inkstitch. However, it includes a lot of higher level and middle level pattern composition abilities that might not be eventually used there. It duplicates some of the functionalities already present there in order to be entirely reasonable for *any* python embroidery project. You shouldn't have to rewrite the tie_on code yourself if you're converting some vector guilloches to embroidery or wrote a fun cyclocycloid program and want to sew the output, or for some reason sew circuit boards on fabric with electricity conductive thread. That's not my department.

It should be complex enough to go very easily from points to stitches, fine grained enough to let you control everything, and good enough that you shouldn't want to.


Mandate
---
pyembroidery is supposed to be small enough to be finished in short order and big enough to pack a punch.

* The minimum required formats within the mandate are PES, DST, EXP, JEF, VP3.
* It reads and writes all of these.
  * PES was short handed to allow for PES block nulling. If you try to load a PES file in Brother Software it will show up blank.
  * PEC has graphics files. These are simply written to be blank. PES files have PEC blocks. These will show up blank.

* The current mandate for core commands is: STITCH, JUMP, TRIM, STOP, END, COLOR_CHANGE and SEQUIN.
  * SEQUIN is only in DST and it only currently loads, but I'm not really checked what happens after that.

Current goals:
---
No goals currently exist. Mostly done. It needs testings and issues at this point.



How it works:
---
The reader sends a readerobject, namely an EmbPattern object to one of the several embroider readers. This results in producing metadata, threads, stitches with raw commands.

On EmbPattern objects you can iterate stitch blocks .get_as_stitchblocks() or access the raw-stitches.

When a writer is called to save a pattern to disk. It encodes a low level version of the commands in the pattern. So all middle-level commands are implemented with the encoder, into low-level commands. The writer also sets the encoder settings to the correct max_jump and max_stitch. These can be accessed by calling .get_normalized_pattern() on the pattern which returns a new pattern. Saving cannot modify a pattern, so there is a level of isolation between the lossy operation of writing the embroidery and the current pattern in memory.

* File -> Reader -> Pattern
* Pattern -> Encoder -> Writer -> File


Reading:
---

To load a pattern from disk:

* pattern = pyemb.read("myembroidery.exp)

If only a file name is given it detects by the extension what reader it should use.

For the descrete readers, the file may be a FileObject or a the string of the path.

* pattern = pyemb.read_dst(file)
* pattern = pyemb.read_pec(file)
* pattern = pyemb.read_pes(file)
* pattern = pyemb.read_exp(file)
* pattern = pyemb.read_vp3(file)
* pattern = pyemb.read_jef(file)

You can optionally add a pattern to these readers, it will use that object and append the new stitches to the end.

* pattern = pyemb.read_pes(file,pattern)
* pattern = pyemb.read("secondread.dst", pyemb.read("firstread.jef"))

This should cause the pattern to have the stitches from both files.

Writing:
---

To write to a pattern do disk:

* pyemb.write(pattern,"myembroidery.dst")

For the descrete writers, the file may be a FileObject or a string of the path.

* pyemb.write_dst(pattern, file)
* pyemb.write_pec(pattern, file)
* pyemb.write_pes(pattern, file)
* pyemb.write_exp(pattern, file)
* pyemb.write_vp3(pattern, file)
* pyemb.write_jef(pattern, file)
* pyemb.write_svg(pattern, file)

In addition, you can add a dict object to the writer with various settings.
* pyemb.write(pattern, file.dst, { "tie_on": True, "tie_off": true, "translate_x": 40, "max_stitch"=50 }

The encoding parameters currently have recognized values for:
* "translate_x"
* "translate_y"
* "tie_on"
* "tie_off"
* "max_stitch"
* "max_jump"

The max_stitch and max_jump properties are appended by default depending on the format you are writing to. If you overtly set these it will override those values. If you set them low on a format such as .dst with a limited length stitch, you can have it permit overly long stitches to be fed into the reader.

Writing to SVG:
This is largely for testing purposes, it's not a binary writing format. But, it's entirely needed for testing purposes. There is some notable irony in writing an SVG file in a library, whose main genesis is to help another program that *already* writes them. But, without some provably flawless method of exporting the data read, there's no clear way to guarentee a problem is within a reader or a writer.

Conversion:
---

As pyembroidery is a fully fleshed out reader/writer within the mandate, it also does conversion.

* import pyembroidery.PyEmbroidery as pyemb

* pyemb.convert("embroidery.jef", "converted.dst");

This will the embroidery.jef file in JEF format and will export it as converted.dst in DST format.

Internally this stablizes the format:
* Reader -> Pattern -> Pattern.get_stablized_pattern() -> Encoder -> Writer

The stablized pattern clips out the order of the particlar trims, jumps, colorchanges, stops, and turns it into middle-level commands of STITCH, COLOR_BREAK, SEQUENCE_BREAK. 


Composing a pattern:
---

The constants for the stitch types are located in the EmbConstants.py

To compose a pattern you will typically use:

* import pyemboridery.EmbPattern as EmbPattern
* pattern = EmbPattern.EmbPattern()
* pattern.add_stitch_relative(command, dx, dy)
* pattern.add_stitch_absolute(command, x, y)
* pattern.command(command)
* pattern.add_stitchblock(stitchblock)

NOTE: the order here is command, x, y, not x,y command. Python is good with letting you omit values at the end. And the command is *always* needed but the dx,dy can be dropped quite reasonably.

You can:
* Make overt: stitch, jump, trim, color_change, stop, end, and sequin commands
* Use shorthand commands compose a pattern using: STITCH, SEQUENCE_BREAK and COLOR_BREAK, FRAME_EJECT
* Use bulk dump stitchblock
* Mix these different command levels.

StitchBlocks:
---

A stitch block currently has two parts a block and thread.

The block is a list of lists, with each 3 values. x, y, command. iterable set of objects with stitch.command, stitch.x, stitch.y also works for the stitch part of the block.

When you call add_stitchblock(), the thread is needed so that we can know whether the current thread is different than the previous one. Each time it detects a different thread it appends COLOR_BREAK rather than SEQUENCE_BREAK and then tosses the stitches into the pattern. You could always implement your own version of this, depending on your use case.


Middle-Level Commands:
----

The middle-level commands, as they currently stand:
* SEQUENCE_BREAK - Break between stitches. Inserts a trim and jumps to the next stitch in the sequence.
* COLOR_BREAK - Breaks between stitches. Changes to the next color (unless called before anything was stitched)
* FRAME_EJECT(x,y) - Breaks the stitches, jumps to the given location, performs a stop, then goes to next stitch accordingly.
* TRANSLATE(x,y) - Applies an inline translation shift for the encoder. It will treat all future stitches translated from here.
* ENABLE_TIE_ON - Enables Tie_on on the fly.
* ENABLE_TIE_OFF - Enables Tie_off on the fly.
* DISABLE_TIE_ON - Disables Tie_on on the fly.
* DISABLE_TIE_OFF - Disables Tie_off on the fly.

Note: these do not need to have a 1 to 1 conversion to stitches.
They could be anything, if something is needed and within scope of the project, raise an issue.

---

COLOR_BREAK and SEQUENCE_BREAK:

The main two middle-level commands simply serve as dividers for series of stitches.
* pattern.command(COLOR_BREAK)
* (add a bunch of stitches)
* pattern.command(SEQUENCE_BREAK)
* (add a bunch of stitches)
* pattern.command(COLOR_BREAK)
* (add a bunch of stitches)
* pattern.command(SEQUENCE_BREAK)

It will by default ignore any COLOR_BREAK that occurs before any stitches have been put down. So you don't have to worry about the order you put them in. They work expressly as breaks that divide one block of stitches from another, and gives information as to whether this change also requires we use a new color.

You can expressly add any of the core commands to the patterns. These are generalized and try to play nice with other commands. When the patterns are written to disk, they call pattern.get_normalized_pattern() and save the normalized pattern. Saving to any format does not modify the pattern, ever. It writes the modified pattern out. It adds the max_jump and max_stitch to the encoding when it normalizes this to save. So each format can compile to a different set of stitches due to the max_jump etc.

After a load, the pattern will be filled with raw basic stitch data, it's perfectly reasonable call .get_stable_pattern() on this which will make it into a series of stitches, color_breaks, sequence_breaks. Or to iterate through the data with .get_as_stitchblocks() which is a generator that will produce stitch blocks from the raw loaded data. The stablized pattern simply makes a new pattern, iterates through the current pattern by the stitchblocks and feeds that into add_stitch_block(). This results in a pattern without any jumps, trims, etc.

---

This code is based on Embroidermodder/MobileViewer Java code,
Which in turn is based on Embroidermodder/libembroidery C++ code.


