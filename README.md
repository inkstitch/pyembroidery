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
