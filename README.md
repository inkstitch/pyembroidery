# pyembroidery
libembroidery/EmbroideryFormats converted to python

pyembroidery is a embroidery format reader and writer utility. It can read
* DST
* EXP
* JEF
* (BROKEN) VP3

it can write:
* DST
* EXP
* PEC (blank graphics)
* PES (truncated)
* JEF
* VP3

It's a conversion of Embroidermodder/MobileViewer Java code,
Which in turn is a conversion of Embroidermodder/libembroidery C++ code.

It's largely intended for use in lexelby/inkstitch but is entirely reasonable for any python embroidery project.
