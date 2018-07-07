# pyembroidery

Python library for the reading and writing of embroidery files.
Compatable with Python 2 and 3 Explictly tested with 3.6 and 2.7.

To install:
```bash
pip install pyembroidery
```

Any suggestions or comments please raise an issue.

pyembroidery is largely intended for eventual use in inkscape/inkstitch. However, it includes a lot of higher level and middle level pattern composition abilities that might not be eventually used there. It duplicates some of the functionalities already present there in order to be entirely reasonable for *any* python embroidery project. You shouldn't have to rewrite the tie_on code yourself if you're converting some vector guilloches to embroidery or wrote a fun cyclocycloid program and want to sew the output, or for some reason sew circuit boards on fabric with electricity conductive thread. That's not my department.

It should be complex enough to go very easily from points to stitches, fine grained enough to let you control everything, and good enough that you shouldn't want to.


Mandate
---
pyembroidery must to be small enough to be finished in short order and big enough to pack a punch.

* The minimum required formats within the mandate are PES, DST, EXP, JEF, VP3.
  * It reads and writes all of these.

* The current mandate for core commands is: STITCH, JUMP, TRIM, STOP, END, COLOR_CHANGE and SEQUIN.
  * SEQUIN is only in DST and it only currently loads, but I'm not really checked what happens after that.
  
* The current mandate is required support and function in Python 2.7
  * It is currently compatable with Python 2.7 as well as 3.6

How it works:
---
Readers are sent a fileobject and EmbPattern and parses the file, filling in the metadata, threads, stitches.

EmbPattern objects contain the relevant data. You can iterate stitch blocks .get_as_stitchblocks() or access the raw-stitches, threads, or metadata.

Writers are called to save a pattern to disk. They save raw-stitch data to disk. This data may, however, not be formatted in a way the writer can utilize effectively. For this reason, writers normalize the data with an encoder.

Encoders encode a low level version of the commands in the pattern, not just from low level but also middle-level commands implemented with the encoder. The writer call to the encoder with some format specific values, so each export will reencode that data for the format, without modifying or altering the original data.

The encoder call is made on the EmbPattern with .get_normalized_pattern() on the pattern, this returns a new pattern. Encoding and saving cannot modify a pattern. There is a level of isolation between all lossy operation of writing and converting the pattern.

* Read
  * File -> Reader -> Pattern
* Write
  * Pattern -> Encoder -> Pattern -> Writer -> File
* Convert
  * File -> Reader -> Pattern -> Stablizer -> Pattern -> Encoder -> Pattern -> Writer -> File

Reading:
---

```python
import pyembroidery
```

To load a pattern from disk:

```python
pattern = pyembroidery.read("myembroidery.exp")
```

If only a file name is given it detects by the extension what reader it should use.

For the descrete readers, the file may be a FileObject or a the string of the path.

```python
pattern = pyembroidery.read_dst(file)
pattern = pyembroidery.read_pec(file)
pattern = pyembroidery.read_pes(file)
pattern = pyembroidery.read_exp(file)
pattern = pyembroidery.read_vp3(file)
pattern = pyembroidery.read_jef(file)
```

You can optionally add settings and pattern to these readers, it will use that pattern and append the new stitches to the end.

```python
# append to an existing pattern
pattern = pyembroidery.read_pes(file, None, pattern)

# or even chain together read calls
pattern = pyembroidery.read("secondread.dst", None, pyembroidery.read("firstread.jef"))
```

This will cause the pattern to have the stitches from both files.

Writing:
---

To write to a pattern do disk:

```python
pyembroidery.write(pattern,"myembroidery.dst")
```

For the discrete writers, the file may be a FileObject or a string of the path. It does not need to know the filename to judge an extension.

```python
pyembroidery.write_dst(pattern, file)
pyembroidery.write_pec(pattern, file)
pyembroidery.write_pes(pattern, file)
pyembroidery.write_exp(pattern, file)
pyembroidery.write_vp3(pattern, file)
pyembroidery.write_jef(pattern, file)
pyembroidery.write_svg(pattern, file)
```

In addition, you can add a dict object to the writer, reader, and convert with various settings.

```python
pyembroidery.write(pattern, file.dst, { "tie_on": True, "tie_off": True, "translate": (40, 50) }
```

The parameters currently have recognized values for:
* `max_stitch`
* `max_jump`
* `full_jump`
* `translate`
* `scale`
* `rotate`
* `tie_on`
* `tie_off`
* `encode`
* `long_stitch_contingency`

The max_stitch, max_jump, and full_jump properties are appended by default depending on the format you are writing to. For example, DST files support a maximum stitch length of 12.1mm, and this is set automatically. If you overtly set these, they will override those values. If you override them to a high value on a format such as .dst with limited length stitches, you can have it permit overly long stitches to be fed into the reader, causing a crash. If you disable the encoder "encode" = false. The same thing may occur.

Translate, Scale and Rotate occur in that order. If you want finer grain control over them they can be modified on the fly with middle-level commands.

long_stitch_contingency sets the contingency protocol for when a stitch is longer than the format can encode and how to deal with that event.

Writing to SVG:
This is largely for testing purposes, it's not a binary writing format. But, it's entirely needed for testing purposes. There is some notable irony in writing an SVG file in a library, whose main genesis is to help another program that *already* writes them. But, without some provably flawless method of exporting the data read, there's no clear way to guarentee a problem is within a reader or a writer.

Conversion:
---

As pyembroidery is a fully fleshed out reader/writer within the mandate, it also does conversion.

```python
pyembroidery.convert("embroidery.jef", "converted.dst")
```

This will read the embroidery.jef file in JEF format and will export it as converted.dst in DST format.

Internally this stablizes the format:
* Reader -> Pattern -> Pattern.get_stablized_pattern() -> Encoder -> Writer

The stablized pattern clips out the order of the particlar trims, jumps, colorchanges, stops, and turns it into middle-level commands of STITCH, COLOR_BREAK, SEQUENCE_BREAK.

The stablizer can be disabled by setting "stable" to False.

```python
pyembroidery.convert("embroidery.jef", "converted.dst", {"stable": False})
```

Depending on the formats and files in question this does not have a guarenteed result. It will still use the encoder and should be effective.

You can disable both the stablizer and the encoder:

```python
pyembroidery.convert("embroidery.jef", "converted.dst", {"stable": False, "encode": False})
```


Composing a pattern:
---

The constants for the stitch types are located in the EmbConstants.py

To compose a pattern you will typically use:

```python
import pyembroidery
pattern = pyembroidery.EmbPattern()
pattern.add_stitch_relative(COMMAND, dx, dy)
pattern.add_stitch_absolute(COMMAND, x, y)
pattern.add_command(command)
pattern.add_stitchblock(stitchblock)
```
The relative and absolute markers determine whether the numbers given are relative to the last position or an absolute location. Calling add_command does not update the internal record of position. These are taken as positionless and the x and y are taken as parameters.

NOTE: the order here is `command, x, y`, not `x,y command`. Python is good with letting you omit values at the end. And the command is *always* needed but the dx,dy can be dropped quite reasonably.

For `COMMAND`, you can:
* Use overt low-level commands:
  * `pyembroidery.STITCH`
    * move to position and drop needle once to make a stitch
  * `pyembroidery.JUMP`
    * move to position without dropping needle
  * `pyembroidery.TRIM`
    * trim the thread (for supported machines and file formats)
  * `pyembroidery.COLOR_CHANGE`
  * `pyembroidery.STOP`
    * pause the machine (for applique, thread-change, etc)
  * `pyembroidery.END`
    * end the pattern
  * `pyembroidery.SEQUIN`
    * not fully supported yet
* Use shorthand commands to compose a pattern
  * `pyembroidery.STITCH`
  * `pyembroidery.SEQUENCE_BREAK`
  * `pyembroidery.COLOR_BREAK`
  * `pyembroidery.FRAME_EJECT`
* Use bulk dump stitchblock
* Mix these different command levels.

Shorthand function calls for the above are also available.  These all equate to `pattern.add_stitch_relative` calls using the above constants.  You can omit the `dx` and `dy` parameters if the position should not change (especially useful for trim and color change).

```python
pattern.stitch(dx, dy)
pattern.trim()
pattern.color_change()
```

StitchBlocks:
---
Conceptually a lot of embroidery can be thought of as unbroken blocks of stitches. Given the ubiquity of this, pyembroidery allows several methods for manipulating stitchblocks for reading and writing.

A stitch block currently has two parts a block and thread.

The block is a list of lists, with each 3 values. x, y, command. iterable set of objects with stitch.command, stitch.x, stitch.y also works for adding a stitch block to a pattern. 

When a call is made to add_stitchblock(), the thread object is needed to that we can know whether the current thread is different than the previous one. If a different thread is detected pyembroidery appends COLOR_BREAK rather than SEQUENCE_BREAK and adds the stitches into the pattern. Depending on your use case, you could implement this yourself using singular calls to add_stitch_relative() or add_stitch_absolute()


Middle-Level Commands:
----

The middle-level commands, as they currently stand:
* SEQUENCE_BREAK - Break between stitches. Inserts a trim and jumps to the next stitch in the sequence.
* COLOR_BREAK - Breaks between stitches. Changes to the next color (unless called before anything was stitched)
* FRAME_EJECT(x,y) - Breaks the stitches, jumps to the given location, performs a stop, then goes to next stitch accordingly.
* MATRIX_TRANSLATE(tx,ty) - Applies an inline translation shift for the encoder. It will treat all future stitches translated from here.
* MATRIX_SCALE(sx,sy) - Applies an inline scale shift. It will scale by that factor for future stitches.
* MATRIX_ROTATE(r) - Applies an inline rotateion shift. It will rotate by that factor for future stitches (in degrees).
* MATRIX_RESET - Resets the affine transformation matrix.
* OPTION_ENABLE_TIE_ON - Enables Tie_on on the fly.
* OPTION_ENABLE_TIE_OFF - Enables Tie_off on the fly.
* OPTION_DISABLE_TIE_ON - Disables Tie_on on the fly.
* OPTION_DISABLE_TIE_OFF - Disables Tie_off on the fly.
* OPTION_MAX_STITCH_LENGTH(x) - Sets the max stitch length on the fly.
* OPTION_MAX_JUMP_LENGTH(x) - Sets the max jump length on the fly.
* SEW_TO - STITCH but with forced CONTINGENCY_SEW_TO
* NEEDLE_AT - STITCH but with forced CONTINGENCY_JUMP_NEEDLE
* CONTINGENCY_NONE - Disables long stitch contingency encoding.
* CONTINGENCY_JUMP_NEEDLE - Sets, long stitch contingency to jump the needle to the new position.
* CONTINGENCY_SEW_TO - Sets, long stitch contingency to sew to the new position with interpolated stitches.

Note: these do not need to have a 1 to 1 conversion to stitches. Many have 1 to 0 and trigger changes in states for the encoder, or the matrix being used to filter the locations, or specific higher level commands.

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

The encoder will by default ignore any COLOR_BREAK that occurs before any stitches have been put down. So you don't have to worry about the order you put them in. They work expressly as breaks that divide one block of stitches from another, and gives information as to whether this change also requires we use a new color.

You can expressly add any of the core commands to the patterns. These are generalized and try to play nice with other commands. When the patterns are written to disk, they call pattern.get_normalized_pattern() and save the normalized pattern. Saving to any format does not modify the pattern, ever. It writes the modified pattern out. It adds the max_jump and max_stitch to the encoding when it normalizes this to save. So each format can compile to a different set of stitches due to the max_jump etc.

After a load, the pattern will be filled with raw basic stitch data, it's perfectly reasonable call .get_stable_pattern() on this which will make it into a series of stitches, color_breaks, sequence_breaks. Or to iterate through the data with .get_as_stitchblocks() which is a generator that will produce stitch blocks from the raw loaded data. The stablized pattern simply makes a new pattern, iterates through the current pattern by the stitchblocks and feeds that into add_stitch_block(). This results in a pattern without any jumps, trims, etc.

Stitch Contingency
---
The encoder needs to decide what to do when a stitch is too long. The current modes here are:
* CONTINGENCY_NEEDLE_JUMP (default)
* CONTINGENCY_SEW_TO
* CONTINGENCY_NONE

When a stitch is beyond max_stitch (whether set by the format or by the user) it must deal with this event, however opinions differ as to how what a stitch beyond the maximum should do. If it is your intent that STITCH means SEW_TO this location then setting the stitch contingency to SEW_TO will create a series of stitches until we get to the end location. If you use the command SEW_TO this overtly works like a stitch with CONTINGENCY_SEW_TO. Likewise NEEDLE_AT is the STITCH flavor that jumps to to the end location and then stitches. If you set CONTINGENCY_NONE then no contingency method is used, long stitches are simply fed to the writer as they appear which may throw an error or crash.


Units
---
* The core units are 1/10th mm. This is what 1 refers to within most formats, and internally within pyembroidery itself. You are entirely permitted to use floating point numbers. When writing to a format, fractional values will be lost, but this shall happen in such a way to avoid the propagation of error. Relative stitches from position ( 0.0,  0.31 ) of (+5.4, +5.4), (+5.4, +5,4), (+5.4, +5,4) should encode as changes of 5,6 6,5 5,6. Taking the relative distance in the format as the integer change from the last integer position to the new one, maintaining a position as close to the absolute position as possible.

Core Command Ordering
---
Stitch is taken to mean move_position(x,y), needle_strike. Jump is taken to mean move_position(x,y), block_needle_bar. In those orders.
If a format takes stitch to mean needle_strike, move_position(x,y) in that order. The encoder will may insert an extra jump in to avoid stitching an unwanted element.


---

This code is based on Embroidermodder/MobileViewer Java code,
Which in turn is based on Embroidermodder/libembroidery C++ code.


