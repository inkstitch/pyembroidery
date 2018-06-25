# pyembroidery
libembroidery/EmbroideryFormats converted to python

pyembroidery is a embroidery format reader and writer utility. It can read
* DST
* EXP

it can write:
* DST
* EXP

It's a conversion of Embroidermodder/MobileViewer java code,
Which in turn is a conversion of Embroidermodder/Libembroidery C++ code.

It's largely intended for use in lexelby/inkstitch but is entirely reasonable for any python embroidery project.

Hopefully adding the following soon:

* PEC (blank graphics)
* PES (truncated)
* JEF

The original inkstitch suggestion included VP3 as well. So that might be needed to round things out.
