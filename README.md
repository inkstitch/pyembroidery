# pyembroidery
libembroidery/EmbroideryFormats converted to python

pyembroidery is a embroidery format reader and writer utility. It can read
* DST
* EXP
* JEF

it can write:
* DST
* EXP
* PEC (blank graphics)
* PES (truncated)
* JEF

It's a conversion of Embroidermodder/MobileViewer Java code,
Which in turn is a conversion of Embroidermodder/libembroidery C++ code.

It's largely intended for use in lexelby/inkstitch but is entirely reasonable for any python embroidery project.

The original inkstitch suggestion included VP3 as well.
So that might be needed to round things out.
